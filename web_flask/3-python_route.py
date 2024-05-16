#!/usr/bin/python3
""" Module that starts a flask app"""
from flask import Flask


app = Flask(__name__)
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Function to print hello hbnb"""
    return 'Hello HBNB!'

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Function to print hbnb"""
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Function to print c is fun"""
    return 'C %s' % text.replace('_', ' ')

@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """ Function to print python is cool"""
    return f'Python {text.replace("_", " ")}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
