from flask import Flask, request, render_template
import os

app = Flask(__name__)

FLAG = os.environ.get('FLAG') or "cuhk24ctf{test-flag}"

malformed_list = ["jp", "ja", "japanese", "japan", "nihongo"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/flag", methods=['POST', "BURP"])
def flag():
    if 'food' not in request.form.keys() or \
        request.form['food'].lower() not in ['choco', 'chocolate']:
        return "Gammamon will give you the flag if you give chocolate."
    
    elif 'amount' not in request.form.keys() or \
        not request.form['amount'].lstrip('-').isdigit() or \
        int(request.form['amount']) < (1 << 64) - 1:
        return "Gammamon wants more chocolate."
    
    elif 'User-Agent' not in request.headers.keys() or \
        request.headers['User-Agent'].lower() != 'hiro':
        return f"Gammamon only trusts people called 'Hiro', but you are {request.headers.get('User-Agent')}."
    
    elif 'Accept-Language' not in request.headers.keys() or \
        (request.headers['Accept-Language'].lower() != 'ja-jp' and request.headers['Accept-Language'].lower() not in malformed_list):
        return f"Hiro only accepts Japanese but you accept language {request.headers.get('Accept-Language')}."
    
    elif 'Accept-Language' not in request.headers.keys() or \
        request.headers['Accept-Language'] != 'ja-JP':
        return "The format of accepting language should follow the \"locale code\" format."
    
    elif request.method != "BURP":
        return "Gammamon can only give you that flag via request method 'BURP'."
    
    else:
        return "Here is your flag: " + FLAG
        
