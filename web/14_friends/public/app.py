import os
from flask import Flask, flash, request, redirect, url_for, render_template, make_response
import re
from PIL import Image, UnidentifiedImageError, ExifTags
from models import *
from settings import *

app = Flask(__name__)
app.config.from_object('settings')

def allowed_file(filename: str):
    return filename.lower().endswith(app.config['ALLOWED_EXTENSIONS'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_hints = {} # only for erronous inputs
        name = request.form.get(app.config['FORM_FIELD_NAMES']['name'])
        # independently validate form fields
        if not name or not re.match('^[A-Za-z ]+$', name):
            form_hints['name_error'] = 'Enter a name! (Letters and white spaces only)'
        if app.config['FORM_FIELD_NAMES']['photos'] not in request.files.keys():
            form_hints['file_error'] = 'Upload a photo!'
        if not form_hints:
            friend = Friend.load(name) or Friend(name=name)
            for file in request.files.getlist('photos'):
                if not allowed_file(file.filename):
                    form_hints['file_error'] = 'Upload a photo! (Accepted: jpeg, png)'
                    break
                write_path = os.path.normpath(
                    os.path.join(app.config['APP_BASE'], app.config['UPLOAD_PREFIX'], file.filename)
                )
                if os.path.exists(write_path):
                    form_hints['file_error'] = f'{file.filename} already exists!'
                    break
                try:
                    with Image.open(file.stream) as img:
                        img.load()
                        exif = {
                            ExifTags.TAGS[k]: v
                            for k, v in img.getexif().items()
                            if k in ExifTags.TAGS
                        }
                except Exception as e:
                    form_hints['file_error'] = 'The uploaded image format is unknown!'
                    break
                else:
                    with open(write_path, 'wb') as target_img:
                        file.stream.seek(0)
                        target_img.write(file.stream.read())
                    photo = Photo(file.filename, exif=exif)
                    friend.photos.append(photo)
            if 'file_error' not in form_hints:
                friend.save()
        if form_hints:
            return make_response(render_template('index.html', form_field_names=app.config['FORM_FIELD_NAMES'], **form_hints), 422)
        else:
            flash('Your images have been successfully uploaded.')
    return render_template('index.html', form_field_names=app.config['FORM_FIELD_NAMES'])

@app.route('/friends/<string:slug>', methods=['GET', 'POST'])
def view_friend(slug: str):
    friend = Friend.load(slug)
    if not friend:
        return make_response('No such friend!', 404)
    person_friends = [Friend.load(slug_name) for slug_name in friend.friends]
    if request.method == 'POST':
        new_friend_name = request.form.get('newFriendName')
        if not new_friend_name:
            flash('Enter a name!')
            return render_template('friend.html', friend=friend, person_friends=person_friends)
        if not re.match('^[A-Za-z ]+$', new_friend_name):
            flash('Invalid name format!')
            return render_template('friend.html', friend=friend, person_friends=person_friends)
        new_friend = Friend.load(new_friend_name)
        if new_friend is None:
            new_friend = Friend(name=new_friend_name)
        friend.friends.add(new_friend.slug)
        new_friend.friends.add(friend.slug)
        friend.save()
        new_friend.save()
    return render_template('friend.html', friend=friend, person_friends=person_friends)
        
