from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
   todoList = Todo.query.all() 
   return render_template("index.html", todoList = todoList)

@app.route('/add', methods=["POST"])
def addTodo():
   title = request.form.get("title")   
   todo = Todo(title= title, is_complete=False)
   db.session.add(todo)
   db.session.commit()
   return redirect(url_for("index"))
   
@app.route('/complete/<string:id>')
def complete(id):
   todo = Todo.query.filter_by(id = id).first()
   todo.is_complete = not todo.is_complete
   db.session.commit()
   return redirect(url_for("index"))

@app.route('/delete/<string:id>')
def delete(id):
   todo = Todo.query.filter_by(id=id).first()
   db.session.delete(todo)
   db.session.commit()
   return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    is_complete = db.Column(db.Boolean)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)