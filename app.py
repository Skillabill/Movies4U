from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import CreateReviewForm, EditReviewForm, ConfirmDelete
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId
import re
import math
import os

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Movies4U'
app.config["MONGO_URI"] = 'mongodb+srv://Mark:<password>@myfirstcluster-x7w2o.mongodb.net/Movies4U?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    """Home page"""
    return render_template("index.html", title="Home")

@app.route('/create')
def create():
    """Creates a review and enters into movie-review collection"""
    return render_template("create.html", title="Create")

@app.route('/collection')
def collection():
    """Brings you to the Movie Review Collection"""
    return render_template("collection.html", title="Collection")

# Search for a recipe

@app.route('/search', methods=['POST'])
def search():
  query = request.form.get('query')
  search_collection = mongo.db.collection.find({'$text': {'$search': query}})
  return render_template('collection.html', search_collection=search_collection, query=query)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)