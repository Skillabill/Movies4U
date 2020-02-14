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
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)