from flask import render_template
from myapp import app


@app.route('/')
def homepage():
    handlers = [
        ('search airport', '/search'),
        ('show popular', '/api/v1.0/stats'),
    ]
    return render_template('home.html', handlers=handlers)
