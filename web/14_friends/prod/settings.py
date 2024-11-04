# Settings for actual deployment: different secret key
import os

DATA_PREFIX = 'data/'
UPLOAD_PREFIX = 'static/'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg',)
FORM_FIELD_NAMES = {
    'name': 'full_name',
    'photos': 'photos',
}
APP_BASE = os.path.dirname(__file__)
SECRET_KEY = b']\x9do\xc5\xf9\xc5\xccZ^:\xc2\xe9\x88\x82\x91#I\xbc|2\x89\xdc\xb9\x11\xab9\xf59&\xd71\xd1'
