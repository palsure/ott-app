#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import setup_db, Collection, Category

#----------------------------------------------------------------------------#
# Unit Test Cases
#----------------------------------------------------------------------------#


class OTTApp_Tests(unittest.TestCase):

    load_dotenv()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "ottapp_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #----------------------------------------------------------------------------#
        # Test Data
        #----------------------------------------------------------------------------#
        # get JWT for roles from environment
        self.ott_manager_token = os.getenv('OTT_MANAGER_JWT')
        self.ott_user_token = os.getenv('OTT_USER_JWT')

        self.category_movie = {
            "name": "movies"
        }

        self.collection_movie = {
            "title": "my movie",
            "category": "1",
            "rating": 9,
            "image_url": "test url",
            "video_url": "test video"
        }

        self.collection_movie_update = {
            "title": "my movie update",
            "category": "1",
            "rating": 10,
            "image_url": "test url",
            "video_url": "test video"
        }

        self.collection_show = {
            "title": "my show",
            "category": "2",
            "rating": 8,
            "image_url": "123",
            "video_url": "123",
            "seasons": [
                {
                        "name": "my season",
                        "episodes": 10
                }
            ]
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    #----------------------------------------------------------------------------#
    # Tests
    #----------------------------------------------------------------------------#

    # Create Category Tests
    def test_create_category_success(self):
        response = self.client().post(
            '/categories',
            json=self.category_movie,
            headers={
                "Authorization": "{}".format(
                    self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['category_id'] > 0)

    def test_create_category_invalid_400(self):
        response = self.client().post(
            '/categories',
            json={},
            headers={
                "Authorization": "{}".format(
                    self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['success'], False)

    def test_create_category_auth_error_401(self):
        response = self.client().post(
            '/categories',
            json={})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['success'], False)

    def test_create_category_auth_error_permissions_403(self):
        response = self.client().post(
            '/categories',
            json={},
            headers={
                "Authorization": "{}".format(
                    self.ott_user_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data['success'], False)

    # Get Category Tests
    def test_get_category_success(self):
        response = self.client().get(
            '/categories',
            headers={
                "Authorization": "{}".format(
                    self.ott_user_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['categories'][0]['type'], 'movies')
        self.assertEqual(response_data['categories'][0]['id'], 1)

    def test_get_category_auth_error_401(self):
        response = self.client().get(
            '/categories',
            headers={
                "Authorization": "Bearer invalid"})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['success'], False)

    # Create collections Tests
    def test_create_collection_movie_success(self):
        response = self.client().post(
            '/collections',
            json=self.collection_movie,
            headers={
                "Authorization": "{}".format(
                    self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['collection']['id'] > 0)
        self.assertEqual(
            response_data['collection']['title'],
            self.collection_movie['title'])
        self.assertEqual(
            response_data['collection']['image_url'],
            self.collection_movie['image_url'])
        self.assertEqual(
            response_data['collection']['video_url'],
            self.collection_movie['video_url'])
        self.assertEqual(
            response_data['collection']['rating'],
            self.collection_movie['rating'])

    def test_create_collection_show_success(self):
        # create shows category
        category = Category.query.filter(
            Category.type == "shows").one_or_none()
        if category is None:
            show_category = Category(type="shows")
            show_category.insert()
        response = self.client().post(
            '/collections',
            json=self.collection_show,
            headers={
                "Authorization": "{}".format(
                    self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['collection']['id'] > 0)
        self.assertEqual(
            response_data['collection']['title'],
            self.collection_show['title'])
        self.assertEqual(
            response_data['collection']['image_url'],
            self.collection_show['image_url'])
        self.assertEqual(
            response_data['collection']['video_url'],
            self.collection_show['video_url'])
        self.assertEqual(
            response_data['collection']['rating'],
            self.collection_show['rating'])
        self.assertEqual(
            response_data['collection']['seasons'][0]['name'],
            self.collection_show['seasons'][0]['name'])
        self.assertEqual(
            response_data['collection']['seasons'][0]['episodes'],
            self.collection_show['seasons'][0]['episodes'])

    def test_create_collection_invalid_400(self):
        response = self.client().post(
            '/collections',
            json={},
            headers={
                "Authorization": "{}".format(
                    self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['success'], False)

    def test_create_collection_auth_error_permissions_403(self):
        response = self.client().post(
            '/collections',
            json={},
            headers={
                "Authorization": "{}".format(
                    self.ott_user_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data['success'], False)

    # Get collections Tests
    def test_get_collections_success(self):
        response = self.client().get(
            '/collections',
            headers={
                "Authorization": "{}".format(
                    self.ott_user_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        first_movie_response = response_data['collections'][0]['movies'][0]
        self.assertEqual(
            first_movie_response['title'],
            self.collection_movie['title'])
        self.assertEqual(
            first_movie_response['image_url'],
            self.collection_movie['image_url'])
        self.assertEqual(
            first_movie_response['video_url'],
            self.collection_movie['video_url'])
        self.assertEqual(
            first_movie_response['rating'],
            self.collection_movie['rating'])

    def test_get_movie_collections_success(self):
        response = self.client().get(
            '/collections?category=movies',
            headers={
                "Authorization": "{}".format(
                    self.ott_user_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        first_movie_response = response_data['collections'][0]['movies'][0]
        self.assertEqual(
            first_movie_response['title'],
            self.collection_movie['title'])
        self.assertEqual(
            first_movie_response['image_url'],
            self.collection_movie['image_url'])
        self.assertEqual(
            first_movie_response['video_url'],
            self.collection_movie['video_url'])
        self.assertEqual(
            first_movie_response['rating'],
            self.collection_movie['rating'])
        self.assertEqual(len(response_data['collections']), 1)

    def test_get_collections_auth_error_401(self):
        response = self.client().get(
            '/collections',
            headers={
                "Authorization": ""})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['success'], False)

    # Update collections Tests
    def test_update_collection_success(self):
        collection = Collection.query.filter(
            Collection.category == '1').first()
        response = self.client().patch('/collections/{}'.format(collection.id),
                                       json=self.collection_movie_update,
                                       headers={
            "Authorization":
            "{}".format(self.ott_manager_token)
        })
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['collection']['id'], collection.id)
        self.assertEqual(
            response_data['collection']['title'],
            self.collection_movie_update['title'])
        self.assertEqual(
            response_data['collection']['image_url'],
            self.collection_movie_update['image_url'])
        self.assertEqual(
            response_data['collection']['video_url'],
            self.collection_movie_update['video_url'])
        self.assertEqual(
            response_data['collection']['rating'],
            self.collection_movie_update['rating'])
        collection.delete()

    def test_update_collection_invalid_404(self):
        response = self.client().patch(
            '/collections/0',
            json=self.collection_movie_update,
            headers={
                "Authorization": "{}".format(
                    self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

    def test_update_collection_auth_error_permissions_403(self):
        response = self.client().patch(
            '/collections/0',
            json={},
            headers={
                "Authorization": "{}".format(
                    self.ott_user_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data['success'], False)

    # Delete collections Tests
    def test_delete_collection_success(self):
        collection = Collection.query.filter(
            Collection.category == '2').first()
        response = self.client().delete('/collections/{}'.format(collection.id),
                                        headers={"Authorization": "{}".format(self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_delete_collection_invalid_404(self):
        response = self.client().delete(
            '/collections/0',
            headers={
                "Authorization": "{}".format(
                    self.ott_manager_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

    def test_delete_collection_auth_error_permissions_403(self):
        response = self.client().delete(
            '/collections/0',
            json={},
            headers={
                "Authorization": "{}".format(
                    self.ott_user_token)})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data['success'], False)

#----------------------------------------------------------------------------#
# Make the tests conveniently executable
#----------------------------------------------------------------------------#


if __name__ == "__main__":
    unittest.main()
