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
    # db_drop_and_create_all,
    Actor,
    Movie,
    Performance
)
from config import PAGINATION

ROWS_PER_PAGE = int(PAGINATION)


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # db_drop_and_create_all()

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
        
        start = (int(page) - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        objects_formatted = [object_name.format() for object_name in selection]
        
        return objects_formatted[start:end]

    # ---------------------------------------------------------------------------- #
    # API Endpoints																   #
    # ---------------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------- #
    # Endpoint /actors GET 														   #
    # ---------------------------------------------------------------------------- #

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "access_token": request.args.get("access_token")
            })
    
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

        new_actor = Actor(
            name=name,
            age=age,
            gender=gender
        )

        new_actor.insert()

        return jsonify({
            'success': True,
            'created': new_actor.id
        })

    # ---------------------------------------------------------------------------- #
    # Endpoint /actors PATCH	 												   #
    # ---------------------------------------------------------------------------- #

    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actors(payload, actor_id):

        body = request.get_json()

        if not actor_id:
            abort(400, {'message': 'please append an actor id to the request url.'})

        if not body:
            abort(400, {'message': 'request does not contain a valid JSON body.'})

        actor_to_update = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor_to_update:
            abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})

        name = body.get('name', actor_to_update.name)
        age = body.get('age', actor_to_update.age)
        gender = body.get('gender', actor_to_update.gender)

        actor_to_update.name = name
        actor_to_update.age = age
        actor_to_update.gender = gender

        actor_to_update.update()

        return jsonify({
            'success': True,
            'updated': actor_to_update.id,
            'actor': [actor_to_update.format()]
        })

    # ---------------------------------------------------------------------------- #
    # Endpoint /actors DELETE	 												   #
    # ---------------------------------------------------------------------------- #

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):

        if not actor_id:
            abort(400, {'message': 'please append an actor id to the request url.'})

        actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor_to_delete:
            abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})

        actor_to_delete.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    # ---------------------------------------------------------------------------- #
    # Endpoint /movies GET		 												   #
    # ---------------------------------------------------------------------------- #

    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movies(payload):

        selection = Movie.query.all()
        movies_paginated = paginate_results(request, selection)

        if len(movies_paginated) == 0:
            abort(404, {'message': 'no movies found in database.'})

        return jsonify({
            'success': True,
            'movies': movies_paginated
        })

    # ---------------------------------------------------------------------------- #
    # Endpoint /movies POST		 												   #
    # ---------------------------------------------------------------------------- #

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def insert_movies(payload):

        body = request.get_json()

        if not body:
            abort(400, {'message': 'request does not contain a valid JSON body.'})

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not title:
            abort(422, {'message': 'no title provided.'})

        if not release_date:
            abort(422, {'message': 'no "release_date" provided.'})

        new_movie = Movie(
            title=title,
            release_date=release_date
        )

        new_movie.insert()

        return jsonify({
            'success': True,
            'created': new_movie.id
        })

    # ---------------------------------------------------------------------------- #
    # Endpoint /movies PATCH		 											   #
    # ---------------------------------------------------------------------------- #

    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movies(payload, movie_id):

        body = request.get_json()

        if not movie_id:
            abort(400, {'message': 'please append an movie id to the request url.'})

        if not body:
            abort(400, {'message': 'request does not contain a valid JSON body.'})

        movie_to_update = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie_to_update:
            abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})

        title = body.get('title', movie_to_update.title)
        release_date = body.get('release_date', movie_to_update.release_date)

        movie_to_update.title = title
        movie_to_update.release_date = release_date

        movie_to_update.update()

        return jsonify({
            'success': True,
            'edited': movie_to_update.id,
            'movie': [movie_to_update.format()]
        })

    # ---------------------------------------------------------------------------- #
    # Endpoint /movies DELETE		 											   #
    # ---------------------------------------------------------------------------- #

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):

        if not movie_id:
            abort(400, {'message': 'please append an movie id to the request url.'})

        movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie_to_delete:
            abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})

        movie_to_delete.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
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


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
