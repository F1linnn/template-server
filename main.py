from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import logging
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')
app.config['LOG_FILE'] = os.environ.get('LOG_FILE', 'access.log')

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', backref=db.backref('items', lazy=True))

@app.route('/index.html')
def index():

    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add.html', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category_id = request.form['category_id']
        item = Item(name=name, description=description, price=price, category_id=category_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        categories = Category.query.all()
        return render_template('add.html', categories=categories)

@app.route('/edit.html/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get(id)

    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.category_id = request.form['category_id']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        categories = Category.query.all()
    return render_template('edit.html', item=item, categories=categories)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

logging.basicConfig(filename=app.config['LOG_FILE'], level=logging.INFO)
app.run()
