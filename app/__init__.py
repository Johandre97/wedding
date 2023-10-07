# app/__init__.py
from flask import Flask
import os


app = Flask(__name__)
app.template_folder = '../templates' 
app.static_folder = '../static'

from app import routes