from flask import Blueprint, render_template, request
import os

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_files():
    resume = request.files.get('resume')
    cover_letter = request.files.get('cover_letter')

    if not resume:
        return render_template('index.html', message="Resume is required!")

    # Save uploaded files into the uploads/ folder
    if resume:
        resume.save(os.path.join(UPLOAD_FOLDER, resume.filename))

    if cover_letter:
        cover_letter.save(os.path.join(UPLOAD_FOLDER, cover_letter.filename))

    return render_template('index.html', message="Files uploaded successfully.")
