# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://webshop_user:yourpassword@db/webshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80, collation='utf8mb4_unicode_ci'), nullable=False)
    description = db.Column(db.String(200, collation='utf8mb4_unicode_ci'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80, collation='utf8mb4_unicode_ci'), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

@app.route('/')
def index():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    category_id = request.form.get('category')
    new_product = Product(name=name, description=description, price=price, category_id=category_id)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = request.form.get('price')
        product.category_id = request.form.get('category')
        db.session.commit()
        return redirect(url_for('index'))
    categories = Category.query.all()
    return render_template('update.html', product=product, categories=categories)

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form.get('name')
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('categories'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
