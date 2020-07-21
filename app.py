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

	def paginate_questions(request, selection):
	
		page = request.args.get('page', 1, type=int)

		start = (page - 1) * QUESTIONS_PER_PAGE
		end = start + QUESTIONS_PER_PAGE

		questions = [question.format() for question in selection]
		current_questions = questions[start:end]

		return current_questions
		

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