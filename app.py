from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.template_folder = './templates' 
app.static_folder = './static'


def current_page():
    return {'current_page': request.endpoint}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name + '.html', current_page=page_name)

if __name__ == '__main__':
    app.run()