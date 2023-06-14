from flask import Flask, request, render_template, redirect, send_file, send_from_directory, url_for
from werkzeug.utils import secure_filename
from script import mico_videos
import os

ALLOWED_EXTENSIONS = {'mp4'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

# Define the route to handle the form submission and video processing
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if the request contains the 'video1' and 'video2' files
        if 'video1' not in request.files or 'video2' not in request.files:
            return 'Please select two video files.'

        video1 = request.files['video1']
        video2 = request.files['video2']

        # Check if the file extensions are allowed
        if not allowed_file(video1.filename) or not allowed_file(video2.filename):
            return 'Please upload video files with allowed extensions.'

        # Save the uploaded files to the upload folder
        top_video = secure_filename(video1.filename)
        bot_video = secure_filename(video2.filename)
        video1.save(top_video)
        video2.save(bot_video)

        mirror_top = request.form.get('mirror_top')
        mirror_bot = request.form.get('mirror_bot')
        
        # Process the videos using mico_videos
        mico_videos(bot_video, top_video, mirror_bot, mirror_top)

        # Send the processed video file for download
        return render_template('download.html')
    
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
