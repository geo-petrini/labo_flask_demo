from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from modules.utils import validate_product, save_product, read_products
from models.conn import db
from models.model import Category, Product
app = Blueprint('frontend', __name__)


@app.route("/")
def home():
    return render_template('base.html')

@app.route('/form')
def product_form():
    categories = Category.query.all()
    data = []
    for category in categories:
        data.append( category.to_dict() )
    return render_template('product_form.html', categories=data)

@app.route('/form', methods=['POST'])
def product_form_submit():
    data = {
        "name" : request.form.get('name', "").strip(),    #short form for name = request.form['name'] if 'name' in request.form else None
        "description" : request.form.get('description', "").strip(),
        "price": request.form.get('price', "").strip(),
        "category": request.form.get('category', "").strip()
    }
    
    errors = validate_product(data)
    data['price'] = float( data['price'] )
    
    
    if errors:
        return render_template('product_form.html', errors=errors, form_data=data)
    
    save_product(data)
    
    return redirect(url_for('frontend.products_list'))

@app.route("/products", methods=["GET"])
def products_list():
    products = read_products()
    return render_template('products_list.html', products=products)


@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    pass

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.execute(stmt).scalar_one_or_none()
    if product:
        db.session.delete(product)
        db.session.commit()
        response = {'message':f'product {id} deleted'}
        return jsonify(response), 204   #no content, no need for an actual response
    else:
        response = {'error':'product not found'}
        return jsonify(response), 404