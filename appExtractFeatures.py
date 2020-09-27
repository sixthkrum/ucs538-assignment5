from flask import Flask

app = Flask(__name__, template_folder = "templates")
app.secret_key = "234982374928347"
app.config['UPLOAD_FOLDER'] = '/home/user/apps/ucs538-assignment5/uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
