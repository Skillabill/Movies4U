import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Movies4U'
app.config["MONGO_URI"] = 'mongodb+srv://Mark:<password>@myfirstcluster-x7w2o.mongodb.net/Movies4U?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/create', methods =['POST'])
def create():
    """Creates a review and enters into movie-review collection"""
    return render_template("create.html", title="Create")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)