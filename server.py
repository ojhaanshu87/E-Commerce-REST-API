from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.serving import run_simple
from passlib.hash import pbkdf2_sha256
from mongoengine import connect
from models import Users, Products
import json
import uuid

#Connect to mongodb 
connect(
    db='test'
)


class Webapp(object):
    def __init__(self):
        self.url_map = Map([
                Rule('/register', endpoint='register_user'),
                Rule('/login', endpoint='login_user'),
                Rule('/logout', endpoint='logout_user'),
                Rule('/addProduct', endpoint='add_product'),
                Rule('/searchProductById', endpoint='search_items'),
                Rule('/searchProductByParameters', endpoint='search_items_by_parameters'),
                Rule('/updateProduct', endpoint='update_product'),
                Rule ('/deleteProduct', endpoint='delete_product')
            ])

        self.session_store = FilesystemSessionStore()


    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    #register the user
    def register_user(self, request):
        if request.method == "POST":
            user_data = json.loads(request.data)
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

            return Response(json.dumps({'status': True, 'message': "successfully register"}))

    #login user
    def login_user(self, request):
        if request.method == "POST":
            credentials = json.loads(request.data)
            sid = request.cookies.get('session_id')
            try:
                if credentials['username'] and credentials['password']:
                    valid_credentials = pbkdf2_sha256.verify(credentials['password'],
                                                             Users.objects(username=credentials['username']).first().password)
                else:
                    valid_credentials = False
            except:
                valid_credentials = False
            if valid_credentials:
                if sid is None:
                    request.session = self.session_store.new()
                else:
                    request.session = self.session_store.get(sid)
                request.session['username'] = credentials['username']
                if request.session.should_save:
                    self.session_store.save(request.session)

            response = Response(json.dumps({'status': valid_credentials}))
            response.set_cookie('session_id', request.session.sid)
            return response

    #logout user
    def logout_user(self, request):
        sid = request.cookies.get('session_id')
        if request.method == "GET" and sid is not None:
            request.session = self.session_store.get(sid)
            if 'username' in request.session:
                del request.session['username']

            if request.session.should_save:
                self.session_store.save(request.session)
            return Response(json.dumps({'status': 'username' not in request.session}))

    #CREATE The Product only if Seller or Admin in DataBase
    def add_product(self, request):
        if request.method == "POST":
            sid = request.cookies.get('session_id')

            if sid is None or 'username' not in self.session_store.get(sid):
                return Response(json.dumps({'status':False, 'message':'Login Required'}))

            prod_data = json.loads(request.data)

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
                return Response(json.dumps({'status':True, 'message':'Item Added Successfully.'}))
            else:
                return Response(json.dumps({'status':False, 'message':'Operation not permitted'}))

    #READ The product by ID for all
    def search_items(self, request):
        if request.method == "GET":
            prod_id =request.args.get('prod_id')
            products = json.loads(Products.objects(product_id=prod_id).to_json())
            if len(products):

                return Response(json.dumps({'status': True, 'products':products}))
            else:
                return Response(json.dumps({'status':False, 'message':'The Item is not available.'}))

    #READ The product by tile or description or price for all
    def search_items_by_parameters(self, request):
        if request.method == "GET":

            search_filter = {}

            if 'title' in request.args:
                search_filter['title'] = request.args.get('title')

            if 'description' in request.args:
                search_filter['description'] = request.args.get('description')

            if 'price' in request.args:
                search_filter['price'] = request.args.get('price')

            products = json.loads(Products.objects(__raw__=search_filter).to_json())
            if len(products):
                return Response(json.dumps({'status': True, 'products':products}))
            else:
                return Response(json.dumps({'status':False, 'message':'The Item is not available.'}))

    #UPDATE product only for seller or admin, not for without product seller owner
    def update_product(self, request):
        if request.method == "POST":
            sid = request.cookies.get('session_id')
            if sid is None or 'username' not in self.session_store.get(sid):
                return Response(json.dumps({'status':False, 'message':'Login Required'}))

            prod_data = json.loads(request.data)
            user = Users.objects(user_id=prod_data['user_id']).first()
            if not user.is_admin and not user.is_seller:
                return Response(json.dumps({'status':False, 'message': 'Opearation not permitted'}))
            elif user.is_admin:
                product = Products.objects(product_id=prod_data['product_id']).first()
                if product:
                    product.title = prod_data['title']
                    product.description = prod_data['description']
                    product.price = prod_data['price']
                    product.save()
                    return Response(json.dumps({'status':True, 'message':'Item updated by Admin'}))
                else: 
                    return Response(json.dumps({'status':False, 'message':'No matching product found to update'}))
            elif user.is_seller:
                product = Products.objects(product_id=prod_data['product_id']).first()
                if product:
                    if product.seller_id == prod_data['user_id']:
                        product.title = prod_data['title']
                        product.description = prod_data['description']
                        product.price = prod_data['price']
                        product.save()
                        return Response(json.dumps({'status':True, 'message':'Item updated by Seller'}))
                    else:
                        return Response(json.dumps({'status':False, 'message': 'Not Permitted because you did not add the product'}))
                else:
                    return Response(json.dumps({'status':False, 'message':'No matching product found to Update'}))

    #DELETE The product for Admin or the owner of CREATE product previously, not for other seller and user
    #Only Admin or product owner can delete the products
    def delete_product(self, request):
        if request.method == "DELETE":
            sid = request.cookies.get('session_id')
            if sid is None or 'username' not in self.session_store.get(sid):
                return Response(json.dumps({'status':False, 'message':'Login Required'}))

            prod_data = json.loads(request.data)
            user = Users.objects(user_id=prod_data['user_id']).first()

            if not user.is_admin and not user.is_seller:
                return Response(json.dumps({'status':False, 'message': 'Opearation not permitted'}))
            elif user.is_admin:
                product = Products.objects(product_id=prod_data['product_id']).first()
                if product :   
                    product.delete()
                    return Response(json.dumps({'status':True, 'message':'Product Deleted'}))
                else:
                    return Response(json.dumps({'status':False, 'message':'No matching product found to delete'}))
            elif user.is_seller:
                product = Products.objects(product_id=prod_data['product_id']).first()
                if product :
                    if product.seller_id == prod_data['user_id']:
                        product.delete()
                        return Response(json.dumps({'status':True, 'message':'Product Deleted'}))
                    else:
                        return Response(json.dumps({'status':False, 'message': 'Not Permitted because you did not add the product'}))
                else:
                    return Response(json.dumps({'status':False, 'message':'No matching product found to delete'}))

def create_app():
    app = Webapp()
    return app

if __name__ == "__main__":
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
