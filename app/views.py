from flask import Blueprint, render_template, request,redirect, url_for, flash
import os

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

@main.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

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

    return redirect(url_for('main.index'))
import json

@main.route('/save_filters', methods=['POST'])
def save_filters():
    title = request.form.get('title')
    location = request.form.get('location')
    keywords = request.form.get('keywords')

    filters = {
        "title": title,
        "location": location,
        "keywords": [kw.strip() for kw in keywords.split(',')] if keywords else []
    }

    # Save to a file (filters.json)
    with open('filters.json', 'w') as f:
        json.dump(filters, f, indent=4)

    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files, filter_message="Filters saved successfully.")

