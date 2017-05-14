from flask import Flask, request, jsonify, session
from passlib.hash import pbkdf2_sha256
from mongoengine import connect
from models import Users, Products
import uuid
import json

#instance of app
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

#Connect to mongodb 
connect(
    db='test'
)

#register the user
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

#login user
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

#logout user
@app.route('/logout')
def logout_user():
    session.clear()
    return jsonify({'status': 'username' not in session})

#READ The product by ID for all
@app.route('/searchProductById')
def search_items():
    prod_id =request.args.get('prod_id')
    products = json.loads(Products.objects(product_id=prod_id).to_json())
    if len(products):

        return jsonify({'status': True, 'products':products})
    else:
        return jsonify({'status':False, 'message':'The Item is not available.'})

#READ The product by tile or description or price for all
@app.route('/searchProductByParameters')
def search_items_by_parameters():
    search_filter = {}

    if 'title' in request.args:
        search_filter['title'] = request.args.get('title')

    if 'description' in request.args:
        search_filter['description'] = request.args.get('description')

    if 'price' in request.args:
        search_filter['price'] = request.args.get('price')

    products = json.loads(Products.objects(__raw__=search_filter).to_json())
    if len(products):
        return jsonify({'status': True, 'products':products})
    else:
        return jsonify({'status':False, 'message':'The Item is not available.'})


#CREATE The Product only if Seller or Admin in DataBase
@app.route('/addProduct', methods=['POST'])
def add_product():
    if 'username' not in session:
        return jsonify({'status':False, 'message':'Login Required'})

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
        return jsonify({'status':True, 'message':'Item Added Successfully.'})
    else:
        return jsonify({'status':False, 'message':'Operation not permitted'})


#DELETE The product for Admin or the owner of CREATE product previously, not for other seller and user
#Only Admin or product owner can delete the products
@app.route('/deleteProduct', methods=['DELETE'])
def delete_product():
    if 'username' not in session:
        return jsonify({'status':False, 'message':'Login Required'})

    prod_data = request.get_json(force=True)
    user = Users.objects(user_id=prod_data['user_id']).first()

    if not user.is_admin and not user.is_seller:
        return jsonify({'status':False, 'message': 'Opearation not permitted'})
    elif user.is_admin:
        product = Products.objects(product_id=prod_data['product_id']).first()
        if product :   
            product.delete()
            return jsonify({'status':True, 'message':'Product Deleted'})
        else:
            return jsonify({'status':False, 'message':'No matching product found to delete'})
    elif user.is_seller:
        product = Products.objects(product_id=prod_data['product_id']).first()
        if product :
            if product.seller_id == prod_data['user_id']:
                product.delete()
                return jsonify({'status':True, 'message':'Product Deleted'})
            else:
                return jsonify({'status':False, 'message': 'Not Permitted because you did not add the product'})
        else:
            return jsonify({'status':False, 'message':'No matching product found to delete'})

#UPDATE product only for seller or admin, not for without product seller owner
@app.route('/updateProduct', methods=['POST'])
def update_product():
    if 'username' not in session:
        return jsonify({'status':False, 'message':'Login Required'})

    prod_data = request.get_json(force=True)
    user = Users.objects(user_id=prod_data['user_id']).first()
    if not user.is_admin and not user.is_seller:
        return jsonify({'status':False, 'message': 'Opearation not permitted'})
    elif user.is_admin:
        product = Products.objects(product_id=prod_data['product_id']).first()
        if product:
            product.title = prod_data['title']
            product.description = prod_data['description']
            product.price = prod_data['price']
            product.save()
            return jsonify({'status':True, 'message':'Item updated by Admin'})
        else: 
            return jsonify({'status':False, 'message':'No matching product found to update'})
    elif user.is_seller:
        product = Products.objects(product_id=prod_data['product_id']).first()
        if product:
            if product.seller_id == prod_data['user_id']:
                product.title = prod_data['title']
                product.description = prod_data['description']
                product.price = prod_data['price']
                product.save()
                return jsonify({'status':True, 'message':'Item updated by Seller'})
            else:
                return jsonify({'status':False, 'message': 'Not Permitted because you did not add the product'})
        else:
            return jsonify({'status':False, 'message':'No matching product found to Update'})

if __name__ == "__main__":
    app.run(host ="0.0.0.0", debug = True)