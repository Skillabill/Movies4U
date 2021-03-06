from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    all_tasks = mongo.db.tasks.find()
    return render_template('index.html', tasks=all_tasks)


@app.route('/add_task')
def add_task():
    return render_template('create.html',
                           task=mongo.db.tasks.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find({'_id': ObjectId(task_id)})
    return render_template('edit.html', task=the_task)


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    task = mongo.db.tasks
    task.update({'_id': ObjectId(task_id)},
                 {
                     'title': request.form.get('title'),
                     'actors': request.form.get('actors'),
                     'director': request.form.get('director'),
                     'description': request.form.get('description'),
                     'review': request.form.get('review'),
                     'running_time': request.form.get('running_time')
                 })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/search')
def search():
    orig_query = request.args['query']
    return render_template('search.html', query=orig_query, results=mongo.db.tasks.find({'title': {'$regex': orig_query }}))


@app.route('/review/<review_id>')
def review(review_id):
    print(review_id)
    """Shows full review and increments view"""
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
