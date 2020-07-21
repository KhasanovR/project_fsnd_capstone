from flask import (
	Flask, 
	request, 
	abort, 
	jsonify
	)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import (
	AuthError, 
	requires_auth
	)
from models import (
	setup_db, 
	db_drop_and_create_all,
	Actor, 
	Movie, 
	Performance
	)
from config import pagination

ROWS_PER_PAGE = pagination['example']


def create_app(test_config=None):

	app = Flask(__name__)
	setup_db(app)
	db_drop_and_create_all()

	CORS(app)

	@app.after_request
	def after_request(response):

		response.headers.add(
			'Access-Control-Allow-Headers', 
			'Content-Type,Authorization,true'
			)
		response.headers.add(
			'Access-Control-Allow-Methods', 
			'GET,PATCH,POST,DELETE,OPTIONS'
			)

		return response

	def paginate_results(request, selection):
	
		page = request.args.get('page', 1, type=int)

		start = (page - 1) * ROWS_PER_PAGE
		end = start + ROWS_PER_PAGE

		selections = [sel.format() for sel in selection]

		return selections[start:end]


	# ---------------------------------------------------------------------------- #
  	# API Endpoints																   #
  	# ---------------------------------------------------------------------------- #
	

	# ---------------------------------------------------------------------------- #
	# Endpoint /actors GET 														   #
	# ---------------------------------------------------------------------------- #


	@app.route('/actors', methods=['GET'])
	@requires_auth('read:actors')
	def get_actors(payload):

		selection = Actor.query.all()
		actors_paginated = paginate_results(request, selection)

		if len(actors_paginated) == 0:
			abort(404, {'message': 'no actors found in database.'})

		return jsonify({
			'success': True,
			'actors': actors_paginated
			})


	# ---------------------------------------------------------------------------- #
	# Endpoint /actors POST		 												   #
	# ---------------------------------------------------------------------------- #

	
	@app.route('/actors', methods=['POST'])
	@requires_auth('create:actors')
	def insert_actors(payload):

		body = request.get_json()

		if not body:
			abort(400, {'message': 'request does not contain a valid JSON body.'})

	    
	    name = body.get('name', None)
	    age = body.get('age', None)

	    
	    gender = body.get('gender', 'Other')

	    
	    if not name:
	      abort(422, {'message': 'no name provided.'})

	    if not age:
	      abort(422, {'message': 'no age provided.'})

	    
	    new_actor = (Actor(
	          name = name, 
	          age = age,
	          gender = gender
	          ))
	    
	    new_actor.insert()

	    return jsonify({
	      'success': True,
	      'created': new_actor.id
	    })


	# ---------------------------------------------------------------------------- #
	# Error Handlers                                                               #
	# ---------------------------------------------------------------------------- #
	

	@app.errorhandler(400)
	def bad_request(error):
	    try:
	        msg = error['description']
	    except TypeError:
	        msg = "resource not found"

	    return jsonify({
	        "success": False,
	        "error": 400,
	        "message": msg
	    }), 400


	@app.errorhandler(404)
	def resource_not_found(error):
	    try:
	        msg = error['description']
	    except TypeError:
	        msg = "resource not found"

	    return jsonify({
	        "success": False,
	        "error": 404,
	        "message": msg
	    }), 404


	@app.errorhandler(422)
	def unprocessable(error):
	    try:
	        msg = error['description']
	    except TypeError:
	        msg = "unprocessable"

	    return jsonify({
	        "success": False,
	        "error": 422,
	        "message": msg
	    }), 422


	@app.errorhandler(500)
	def internal_server_error(error):
		try:
			msg = error['description']
		except TypeError:
			msg = "internal server error"

		return jsonify({
            "success": False,
            "error": 500,
            "message": msg
            }), 500


	@app.errorhandler(AuthError)
	def authentification_failed(auth_error):
	    try:
	        msg = auth_error.error['description']
	    except TypeError:
	        msg = "authentification fails"

	    return jsonify({
	        "success": False,
	        "error": auth_error.status_code,
	        "message": msg
	    }), 401


	return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)