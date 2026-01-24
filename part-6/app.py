from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# Main page
@app.route('/')
def index():
    products = Product.query.all()  # For delete dropdown
    return render_template('index.html', products=products)

# Add product
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            quantity=request.form['quantity'],
            price=request.form['price']
        )
        db.session.add(product)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

# Edit product
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = request.form['quantity']
        product.price = request.form['price']
        db.session.commit()
        return redirect('/inventory')
    return render_template('edit.html', product=product)

# Delete product from inventory page
@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/inventory')

# Delete product from main page
@app.route('/delete_from_home', methods=['POST'])
def delete_from_home():
    product_id = request.form.get('product_id')
    if product_id:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
    return redirect('/')

# View inventory
@app.route('/inventory')
def inventory():
    products = Product.query.all()
    total_value = sum(p.quantity * p.price for p in products)
    return render_template('inventory.html', products=products, total_value=total_value)

if __name__ == '__main__':
    app.run(debug=True)