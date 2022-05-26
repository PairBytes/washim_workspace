from flask import jsonify, request, make_response
import jwt
import datetime


def login():
	auth = request.authorization

	if auth and auth.password == 'password':
		token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, 'SECRET_KEY')
    
		return jsonify({'token' : token})
            

	return make_response('could not verify!', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})