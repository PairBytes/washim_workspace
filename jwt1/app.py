from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os 
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY']='thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))
	password = db.Column(db.String(80))
	admin = db.Column(db.Boolean)

class Tod(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text =db.Column(db.String(50))
	complete = db.Column(db.Boolean)
	user_id = db.Column(db.Integer)

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		if not token:
			return jsonify({'message':'Token is Missing'}), 401
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
			create_user = User.query.filter_by(public_id=data['public_id']).first()
		except:
		 	return jsonify({'message':'Token is invalid!'}),401
		 	print('public_id:',public_id)
		return f(create_user, *args, **kwargs)

	return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(create_user):
	if not create_user.admin:
		return jsonify({'message':'cannot perform that funtion!'})
	users = User.query.all()
	output = []
	for user in users:
		user_data = {}
		user_data['public_id'] = user.public_id
		user_data['name'] = user.name
		user_data['password'] = user.password
		user_data['admin'] = user.admin
		output.append(user_data)

	return jsonify({'users':output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(create_user, public_id):
	user = User.query.filter_by(public_id=public_id).first()
	if not user:
		return jsonify({'message':'No user Found!'})
	user_data ={}
	user_data['public_id'] = user.public_id
	user_data['name'] = user.name
	user_data['password'] = user.password
	user_data['admin'] = user.admin
	return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(create_user):
	data = request.get_json()
	hashed_password = generate_password_hash(data['password'], method='sha256')
	new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
	db.session.add(new_user)
	db.session.commit()
	return jsonify({'message':'new user created!'})


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(create_user, public_id):
	user = User.query.filter_by(public_id=public_id).first()
	if not user:
		return jsonify({'message':'No user Found'})
	user.admin = True
	db.session.commit()
	return jsonify({'message':'The User has been promoted'})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(create_user, public_id):
	user = User.query.filter_by(public_id=public_id).first()
	if not user:
		return jsonify({'message':'No user Found'})
	db.session.delete(user)
	db.session.commit()
	return jsonify({'message':'The User has been Deleted!'})

@app.route('/login')
def login():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('could not verify', 401,{'WWW-Authenticate':'Basic realm="Login required"'})

	user = User.query.filter_by(name=auth.username).first()
	if not user:
		return make_response('could not verify',401,{'WWW-Authenticate' : 'Basic realm="Login required"'})
	if check_password_hash(user.password, auth.password):
		token = jwt.encode({'public_id':user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
		return jsonify({'token': token})
	return make_response('could not verify', 401,{'WWW-Authenticate':'Basic realm="Login required"'})




if __name__ == '__main__':
	app.run(debug=True)