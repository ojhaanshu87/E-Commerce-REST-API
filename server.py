from flask import Flask, request, jsonify
from passlib.hash import pbkdf2_sha256
from mongoengine import connect
from models import Users

#instance of app
app = Flask(__name__)

connect(
    db='test'
)

@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json(force=True)
    username = user_data['username']
    email = user_data['email']

    password = pbkdf2_sha256.hash(user_data['password'])
    user = Users(username=username, email=email, password=password)
    user.save()

    return jsonify({'status': True, 'message': "successfully register"})




if __name__ == "__main__":
	app.run(host = "0.0.0.0", debug = True)