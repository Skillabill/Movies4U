from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import re
import os

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Movies4U'
app.config["MONGO_URI"] = 'mongodb+srv://Mark:<>@myfirstcluster-x7w2o.mongodb.net/Movies4U?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("index.html",
         tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('create.html',
     categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_categories'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edit.html', task=the_task,
                           categories=all_categories)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'title':request.form.get('title'),
        'category_name':request.form.get('category_name'),
        'director': request.form.get('director'),
        'year': request.form.get('year'),
        'actors':request.form.get('actors')
    })
    return redirect(url_for('index'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('collection.html',
                           categories=mongo.db.categories.find())

@app.route('/search')
def search():
    """Provides logic for search bar"""
    orig_query = request.args['query']
    # using regular expression setting option for any case
    query = {'$regex': re.compile('.*{}.*'.format(orig_query)), '$options': 'i'}
    # find instances of the entered word in title, tags or reviews
    results = mongo.db.tasks.find({
        '$or': [
            {'title': query},
            {'director': query},
            {'actors': query},
        ]
    })
    return render_template('search.html', query=orig_query, results=results)

@app.errorhandler(404)
def handle_404(exception):
    return render_template('404.html', exception=exception)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)