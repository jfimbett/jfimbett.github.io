# save this as app.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <h1>Hello, World!</h1>
    <p>My name is <strong>Flask</strong></p>
"""

from markupsafe import escape
@app.route("/name/<name>")
def hello(name):
    return f"""
    <h1>Hello, {escape(name)}!</h1>
    """