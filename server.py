from flask import Flask, request, jsonify, session
from passlib.hash import pbkdf2_sha256
from mongoengine import connect
from models import Users, Products
import uuid
import json

#instance of app
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
connect(
    db='test'
)

@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json(force=True)
    username = user_data['username']
    email = user_data['email']
    is_admin = False
    is_seller = False
    password = pbkdf2_sha256.hash(user_data['password'])
    user_id = str(uuid.uuid4())
    if 'is_admin' in user_data:
        is_admin = user_data['is_admin']
    if 'is_seller' in user_data:
        is_seller = user_data['is_seller']
    user = Users(username=username, email=email, user_id=user_id, password=password, is_admin=is_admin, is_seller=is_seller)
    user.save()

    return jsonify({'status': True, 'message': "successfully register"})

@app.route('/login', methods=['POST'])
def login_user():
    credentials = request.get_json(force=True)
    try:
        if credentials['username'] and credentials['password']:
            valid_credentials = pbkdf2_sha256.verify(credentials['password'],
                                                     Users.objects(username=credentials['username']).first().password)
        else:
            valid_credentials = False
    except:
        valid_credentials = False

    if valid_credentials:
        session['username'] = credentials['username']

    return jsonify({'status': valid_credentials})

@app.route('/logout')
def logout_user():
    session.clear()
    return jsonify({'status': 'username' not in session})

@app.route('/searchProduct')
def search_items():
    prod_id =request.args.get('prod_id')
    products = json.loads(Products.objects(product_id=prod_id).to_json())
    return jsonify({'status': True, 'products':products})

@app.route('/addProduct', methods=['POST'])
def add_product():
    prod_data = request.get_json(force=True)

    user = Users.objects(user_id=prod_data['user_id']).first()

    if user.is_admin or user.is_seller:
        #allow to add product
        product_id = str(uuid.uuid4())
        title = prod_data['title']
        description = prod_data['description']
        price = prod_data['price']
        seller_id =prod_data['user_id']
        product = Products(product_id=product_id, title=title, description=description, price=price,
         seller_id=seller_id)
        product.save()
        return jsonify({'status':True})
    else:
        return jsonify({'status':False, 'message':'Operation not permitted'})

@app.route('/deleteProduct', methods=['DELETE'])
#Only Admin or product owner can delete the products
def delete_product():
    prod_data = request.get_json(force=True)
    user = Users.objects(user_id=prod_data['user_id']).first()
    if not user.is_admin and not user.is_seller:
        return jsonify({'status':False, 'message': 'Opearation not permitted'})
    elif user.is_admin:
        product = Products.objects(product_id=prod_data['product_id']).first()
        product.delete()
        return jsonify({'status':True})
    elif user.is_seller:
        product = Products.objects(product_id=prod_data['product_id']).first()
        if product.seller_id == prod_data['user_id']:
            product.delete()
            return jsonify({'status':True})
        else:
            return jsonify({'status':False, 'message': 'Not Permitted because you did not add the product'})

@app.route('/updateProduct', methods=['POST'])
def update_product():
    prod_data = request.get_json(force=True)
    title = prod_data['title']
    description = prod_data['description']
    price = prod_data['price']
    user = Users.objects(user_id=prod_data['user_id']).first()
    if not user.is_admin and not user.is_seller:
        return jsonify({'status':False, 'message': 'Opearation not permitted'})
    elif user.is_admin:
        product = Products.objects(product_id=prod_data['product_id']).first()
        product.title = title
        product.description = description
        product.price = price
        product.save()
        return jsonify({'status':True})
    elif user.is_seller:
        product = Products.objects(product_id=prod_data['product_id']).first()
        if product.seller_id == prod_data['user_id']:
            product.title = title
            product.description = description
            product.price = price
            product.save()
            return jsonify({'status':True})
        else:
            return jsonify({'status':False, 'message': 'Not Permitted because you did not add the product'})

if __name__ == "__main__":
	app.run(host = "0.0.0.0", debug = True)