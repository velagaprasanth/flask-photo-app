from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import base64

app = Flask(__name__)

# Increase the max request size for Heroku (up to 50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    photos = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['POST'])
def upload_file():
    photo_data = request.form.get('photo')

    if not photo_data:
        return redirect(request.url)

    # Remove the image header (base64 metadata)
    photo_data = photo_data.split(",")[1]
    photo_binary = base64.b64decode(photo_data)

    filename = f"photo_{len(os.listdir(UPLOAD_FOLDER)) + 1}.png"
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(photo_path, "wb") as f:
        f.write(photo_binary)

    return redirect(url_for('home'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
