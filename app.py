import os
from flask import Flask, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, ToDo, User

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR,'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

Migrate(app, db)
CORS(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/todos/user/<username>', methods=['GET'])
def index(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error':'User does not exist'}),404

    todos = list(map(lambda todo: todo.serialize(), user.todos))
    return jsonify(todos)

@app.route('/todos/user/<username>', methods=['POST'])
def create(username):
    request_body = request.json
    if request_body != []:
        return jsonify({'error':'Request body must be an empty array'}),400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error':'User already exists'}),422

    user = User()
    user.username = username

    db.session.add(user)
    db.session.commit()
    
    todo = ToDo()
    todo.label = 'sample task'
    todo.done = False
    todo.user_id = user.id

    db.session.add(todo)
    db.session.commit()

    return jsonify({'result':'ok'}),201

@app.route('/todos/user/<username>', methods=['PUT'])
def update(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error':'User does not exist'}),404

    request_body = request.json
    if type(request_body)  != list or len(request_body) == 0:
        return jsonify({'error':'The request body must be an array with at least one task'}),400
    
    for task in user.todos:
        task.query.delete()

    for task in request_body:
        todo = ToDo()
        todo.label = task['label']
        todo.done = task['done']
        todo.user_id = user.id
        db.session.add(todo)

    db.session.commit()
    
    return jsonify({"result": "A list with " + str(len(user.todos)) + " todos was succesfully saved"})

@app.route('/todos/user/<username>', methods=['DELETE'])
def delete(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error':'User does not exist'}),404
    
    for task in user.todos:
        task.query.delete()

    user.query.delete()

    db.session.commit()

    return jsonify({'result':'User successfully deleted'})

if __name__ == "__main__":
    manager.run()
