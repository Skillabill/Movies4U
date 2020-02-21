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
    all_tasks=mongo.db.tasks.find()
    print(all_tasks)
    return render_template('index.html', tasks=all_tasks)


@app.route('/add_task')
def add_task():
    return render_template('create.html',
     task=mongo.db.tasks.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find({'_id': ObjectId(task_id)})
    return render_template('edit.html', task=the_task)

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'title':request.form.get('title'),
        'actors':request.form.get('actors'),
        'director': request.form.get('director'),
        'description': request.form.get('description'),
        'review':request.form.get('review'),
        'running_time' : request.form.get('running_time')
    })
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


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

@app.route('/review/<review_id>')
def review(review_id):
    print(review_id)
    """Shows full recipe and increments view"""
    mongo.db.tasks.find_one_and_update(
        {'_id': ObjectId(review_id)},
        {'$inc': {'views': 1}}
    )
    tasks_db = mongo.db.tasks.find_one_or_404({'_id': ObjectId(review_id)})
    return render_template('review.html', review=tasks_db)

@app.errorhandler(404)
def handle_404(exception):
    return render_template('404.html', exception=exception)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)