from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Save the uploaded file to the 'uploads' directory
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file.save(os.path.join(upload_folder, file.filename))
    return 'File successfully uploaded!'

# Main entry point for the Flask app
if __name__ == '__main__':
    # Set the Flask app to production mode with debug=False and host='0.0.0.0'
    app.run(debug=False, host='0.0.0.0')
