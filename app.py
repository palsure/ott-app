#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import sys
from flask import Flask, request, jsonify, abort
from models import setup_db
from flask_cors import CORS
import json
from werkzeug.exceptions import HTTPException
from models import Collection, Category, Season, db
from sqlalchemy import func
from flask_migrate import Migrate
from auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# app setup
#----------------------------------------------------------------------------#


def create_app(test_config=None):

    app = Flask(__name__)
    app.config['DEBUG'] = True
    migrate = Migrate(app, db)
    setup_db(app)
    CORS(app)

    #----------------------------------------------------------------------------#
    # get health of server
    #----------------------------------------------------------------------------#
    @app.route('/')
    def get_health():
        return "Hi! App is up and running!!!"

    #----------------------------------------------------------------------------#
    # helper methods
    #----------------------------------------------------------------------------#
    def get_collection(category_id):
        collections_data = []
        collections = Collection.query.filter(
            Collection.category == str(category_id)).order_by(
            Collection.id).all()
        for collection in collections:
            collections_data.append(get_collection_data(collection))
        return collections_data

    def get_collection_data(collection):
        seasons_data = []
        if len(collection.seasons) > 0:
            for season in collection.seasons:
                seasons_data.append({
                    "season_id": season.id,
                    "name": season.name,
                    "episodes": season.episodes
                })
        return ({
            'id': collection.id,
            'title': collection.title,
            # 'category': collection.category,
            'rating': collection.rating,
            'image_url': collection.image_url,
            'video_url': collection.video_url,
            'seasons': seasons_data
        })

    #----------------------------------------------------------------------------#
    # get collections - supports query parameter 'category'
    #----------------------------------------------------------------------------#
    @app.route("/collections")
    @requires_auth('read:ott')
    def get_collections(jwt):
        # def get_collections():
        try:
            # Allows only GET request
            if request.method != 'GET':
                abort(405)
            # Gets collections based on category parameter
            collections_data = []
            request_category = request.args.get('category', None)
            if request_category is None or request_category.lower() == 'all':
                categories = Category.query.order_by(Category.id).all()
                for category in categories:
                    category_data = get_collection(category.id)
                    if len(category_data) > 0:
                        collections_data.append({
                            category.type: category_data
                        })
            else:
                category = Category.query.filter(func.lower(
                    Category.type) == func.lower(request_category)).first()
                if category is None:
                    print('Category - ' + request_category + " is not valid")
                    abort(400)
                category_data = get_collection(category.id)
                if len(category_data) > 0:
                    collections_data.append({
                        category.type: category_data
                    })
            # Returns error 404 if no collection available
            if len(collections_data) == 0:
                abort(404)
            # returns json response with 200 status
            return jsonify(
                {
                    "success": True,
                    "collections": collections_data
                }
            ), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                print(sys.exc_info())
                # Returns error 422 unprocessable
                abort(422)

    #----------------------------------------------------------------------------#
    # get categories
    #----------------------------------------------------------------------------#
    @app.route("/categories")
    @requires_auth('read:ott')
    def get_categories(jwt):
        # def get_categories():
        try:
            # Allows only GET request
            if request.method != 'GET':
                abort(405)
            # Gets all categories
            categories = Category.query.order_by(Category.id).all()
            # Returns error 404 if no category is available
            if len(categories) == 0:
                abort(404)
            # created dictionary of all categories with short
            categories_data = [category.format() for category in categories]
            # returns json response with 200 status
            return jsonify(
                {
                    "success": True,
                    "categories": categories_data
                }
            ), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                print(sys.exc_info())
                # Returns error 422 unprocessable
                abort(422)

    #----------------------------------------------------------------------------#
    # create categories
    #----------------------------------------------------------------------------#
    @app.route("/categories", methods=['POST'])
    @requires_auth('post:ott')
    def create_category(jwt):
        # def create_category():
        try:
            # Allows only POST request
            if request.method != 'POST':
                abort(405)
            # gets category details from request
            request_json = request.get_json()
            category_type = request_json.get('name', None)
            # Returns error 400 if category type is missing in request
            if (category_type is None):
                abort(400)
            # Get existing categories
            category = Category.query.filter(func.lower(
                Category.type) == func.lower(category_type)).first()
            if category is None:
                # create new category object
                category = Category(
                    type=category_type
                )
                # save new category bject
                category.insert()
            # returns json response with 200 status
            return jsonify(
                {
                    "success": True,
                    "category_id": category.id
                }
            ), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                print(sys.exc_info())
                # Returns error 422 unprocessable
                abort(422)

    #----------------------------------------------------------------------------#
    # create collections for any available category
    #----------------------------------------------------------------------------#
    @app.route("/collections", methods=['POST'])
    @requires_auth('post:ott')
    def create_collection(jwt):
        # def create_collection():
        try:
            # Allows only POST request
            if request.method != 'POST':
                abort(405)
            # gets collection details from request
            request_json = request.get_json()
            collection_title = request_json.get('title', None)
            collection_category = request_json.get('category', None)
            collection_rating = request_json.get('rating', None)
            collection_image_url = request_json.get('image_url', None)
            collection_video_url = request_json.get('video_url', None)
            collection_seasons = request_json.get('seasons', None)
            # Returns error 400 if required fields missing in request
            if (collection_title is None
                or collection_category is None
                or collection_rating is None
                or collection_image_url is None
                    or collection_video_url is None):
                print("Required fields missing in request")
                abort(400)
            # Get existing collection
            collection = Collection.query.filter(func.lower(
                Collection.title) == func.lower(collection_title)).first()
            if collection is not None:
                print("Collection - " + collection_title + " already exists")
                abort(400)
            # create new collection object
            collection = Collection(
                title=collection_title,
                rating=collection_rating,
                category=collection_category,
                image_url=collection_image_url,
                video_url=collection_video_url
            )
            # save new collection bject
            collection.insert()
            # add new season if exists in request
            if (collection_seasons is not None):
                for season in collection_seasons:
                    new_season = Season(
                        name=season['name'],
                        episodes=season['episodes'],
                        collection_id=collection.id
                    )
                    new_season.insert()

            # returns json response with 200 status
            return jsonify(
                {
                    "success": True,
                    "collection": get_collection_data(collection)
                }
            ), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                print(sys.exc_info())
                # Returns error 422 unprocessable
                abort(422)

    #----------------------------------------------------------------------------#
    # update an existing collection
    #----------------------------------------------------------------------------#
    @app.route('/collections/<int:collection_id>', methods=['PATCH'])
    @requires_auth('patch:ott')
    def update_collection(jwt, collection_id):
        # def update_collection(collection_id):
        try:
            # Allows only PATCH request
            if request.method != 'PATCH':
                abort(405)
            # gets collection details from request
            request_json = request.get_json()
            collection_title = request_json.get('title', None)
            collection_category = request_json.get('category', None)
            collection_rating = request_json.get('rating', None)
            collection_image_url = request_json.get('image_url', None)
            collection_video_url = request_json.get('video_url', None)
            collection_seasons = request_json.get('seasons', None)
            # gets collection details from db for collection_id
            collection = Collection.query.filter(
                Collection.id == collection_id).one_or_none()
            # returns 404 error if no collection found for collection_id
            if (collection is None):
                abort(404)
            # update details for collection
            if collection_title:
                collection.title = collection_title
            if collection_category:
                collection.category = collection_category
            if collection_rating:
                collection.rating = collection_rating
            if collection_image_url:
                collection.image_url = collection_image_url
            if collection_video_url:
                collection.video_url = collection_video_url
            collection.update()
            # update season if exists in request
            if (collection_seasons is not None):
                for season in collection_seasons:
                    name = season['name']
                    episodes = season['episodes']
                    existing_season = Season.query.filter(
                        (Season.collection_id == collection_id) & func.lower(
                            Season.name) == func.lower(name)).first()
                    # add new season if not exists
                    if existing_season is None:
                        new_season = Season(
                            name=name,
                            episodes=episodes,
                            collection_id=collection.id
                        )
                        new_season.insert()
                    # update existing season
                    elif name or episodes:
                        if name:
                            existing_season.name = name
                        if episodes:
                            existing_season.episodes = episodes
                        existing_season.update()
            # returns json response with 200 status
            return jsonify(
                {
                    "success": True,
                    "collection": get_collection_data(collection)
                }
            ), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                print(sys.exc_info())
                # Returns error 422 unprocessable
                abort(422)

    #----------------------------------------------------------------------------#
    # delete an existing collection
    #----------------------------------------------------------------------------#
    @app.route('/collections/<int:collection_id>', methods=['DELETE'])
    @requires_auth('delete:ott')
    def delete_collection(jwt, collection_id):
        # def delete_collection(collection_id):
        try:
            # Allows only DELETE request
            if request.method != 'DELETE':
                abort(405)
            # gets frink details from db for collection_id
            collection = Collection.query.filter(
                Collection.id == collection_id).one_or_none()
            # returns 404 error if no collection found for collection_id
            if (collection is None):
                abort(404)
            # delete collection from db
            collection.delete()
            # returns json response with 200 status
            return jsonify(
                {
                    "success": True,
                    "collection_id": collection_id
                }
            ), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                print(sys.exc_info())
                # Returns error 422 unprocessable
                abort(422)

    #----------------------------------------------------------------------------#
    # error handlers
    #----------------------------------------------------------------------------#
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401

    return app


#----------------------------------------------------------------------------#
# create and run app
#----------------------------------------------------------------------------#
app = create_app()

if __name__ == '__main__':
    app.run()
