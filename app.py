import os
from flask import Flask, render_template, redirect, url_for, request
from config import Config
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'Movies4U'
app.config['MONGO_URI'] = 'mongodb+srv://Mark:CTK1rwan@myfirstcluster-x7w2o.mongodb.net/Movies4U?retryWrites=true&w=majority'
app.config.from_object(Config)

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_movie-reviews')
def get_moviereviews():
    return render_template('index.html', moviereviews = mongo.db.movie-reviews.find())

@app.errorhandler(404)
def handle_404(exception):
    return render_template('404.html', exception=exception)

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = False
    app.config['DEBUG'] = False
    app.run(host='127.0.0.1', degug=False)