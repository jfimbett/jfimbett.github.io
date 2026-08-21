# save this as app.py
from flask import Flask, request
from markupsafe import escape
app = Flask(__name__)


@app.route("/say_hello")
def say_hello():
    name1 =  request.args.get('name1')
    name2 =  request.args.get('name2')
    return f"""
    <h1> Hello to: </h1>
    <ul>
        <li> {escape(name1)} </li>
        <li> {escape(name2)} </li>
    </ul>
"""

# /say_hello?name1=ThomasAndrieu&name2=GhalyaHassani