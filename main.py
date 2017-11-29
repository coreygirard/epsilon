from flask import Flask, request, redirect, render_template, Markup, session
from pprint import pprint
import hashlib
import json
import time
import random
import os



app = Flask(__name__)

@app.route('/')
def home():
    return 'hey there'

if __name__ == '__main__':
    app.run(debug=True)
