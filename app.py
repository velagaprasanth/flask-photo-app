from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import base64

app = Flask(__name__)

# Folder where uploaded photos will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB limit



# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    photos = os.listdir(UPLOAD_FOLDER)  # List files in uploads/
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['POST'])
def upload_file():
    photo_data = request.form.get('photo')

    if not photo_data:
        return redirect(request.url)

    # Convert Base64 image to binary
    photo_data = photo_data.replace('data:image/png;base64,', '')
    photo_binary = base64.b64decode(photo_data)

    filename = f"photo_{len(os.listdir(UPLOAD_FOLDER)) + 1}.png"
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(photo_path, "wb") as f:
        f.write(photo_binary)

    return redirect(url_for('home'))

# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
