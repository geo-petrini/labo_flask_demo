from flask import Flask, render_template, request
from modules.utils import validate_product, save_product
app = Flask(__name__)


@app.route("/")
def home():
    return "Product Catalog - <a href='/form'>Add Product</a>"

@app.route('/form')
def product_form():
    return render_template('product_form.html')

@app.route('/form', methods=['POST'])
def product_form_submit():
    data = {
        "name" : request.form.get('name', "").strip(),    #short form for name = request.form['name'] if 'name' in request.form else None
        "description" : request.form.get('description', "").strip(),
        "price": request.form.get('price', "").strip(),
        "category": request.form.get('category', "").strip()
    }
    
    errors = validate_product(data)
    
    if errors:
        return render_template('product_form.html', errors=errors, form_data=data)
    
    save_product(data)
    
    #TODO return something to the user or redirect to a page with the list of producs
    #TODO save somewhere
    
    return f'{data}'

if __name__ == "__main__":
    app.run(debug=True)
