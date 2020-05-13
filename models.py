from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class ToDo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'done': self.done
        }

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    todos = db.relationship('ToDo')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'todos': self.todos
        }
