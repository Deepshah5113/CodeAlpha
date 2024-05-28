from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, long_url):
        self.long_url = long_url
        self.short_code = self.generate_short_code()

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for i in range(5))
        return short_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    new_url = URL(long_url)
    db.session.add(new_url)
    db.session.commit()
    short_url = f'{request.url_root}{new_url.short_code}'
    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.long_url)
    else:
        return 'Shortened URL not found', 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
