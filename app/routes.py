from flask import render_template, request, redirect, url_for, flash
from app import app

def current_page():
    return {'current_page': request.endpoint}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name + '.html', current_page=page_name)
