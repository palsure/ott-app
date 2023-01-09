# Udacity FullStack Final Capstone Project 

# OTT App Service

## Summary

This projet is designed to demonstrate the backend service of a simple OTT application. The backend api is designed to work for two types of users: ott user and ott manager. 

OTT users can view collections for categories such as movies, shows, etc. 
1. Display available categories.
2. Display collections - for all categories and by individual category.

OTT managers can create, update, delete and view collections for any category. 
1. Display available categories.
2. Display collections - for all categories and by individual category.
3. Add collections - movies, shows, etc
4. Update collections - movies, shows, etc
5. Delete collections - movies, shows, etc

## Project dependencies

The project depends on the latest version of Python 3.x which we recommend to download and install from their official website and use a virtual environment to install all dependencies.

## PIP dependencies

After having successfully installed Python, navigate to the root folder of the project (the project must be forked to your local machine) and run the following in a command line:

```
pip3 install -r requirements.txt
```

This will install all the required packages to your virtual environment to work with the project.

## Database setup

The `models.py` file contains connection instructions to the Postgres database, which must also be setup and running. Provide a valid username and password, if applicable.

1. Create a database with name `ottapp` using Psql CLI:

`createdb ottapp`

2. Initiate and migrate the database with the following commands in command line:

```
python3 manage.py db init
python3 manage.py db migrate -m "Initial migration"
python3 manage.py db upgrade
```

This will create all necessary tables and relationships to work with the project.

## Data Modelling

The data model of the project is provided in `models.py` file in the root folder. The following schema for the database and helper methods are used for API behaviour:

- There are 3 tables created: Category, Collection and Season.
- The Category table includes the fields category type.
- The Collection table includes the fields title, category, rating, image and video url.
- The season table includes the fields name, episodes.

## Running the local development server

All necessary credential to run the project are provided in the `setup.sh` file. The credentials can be enabled by running the following command:

```
source setup.sh
```

To run the API server on a local development environmental the following commands must be additionally executed:

### On Mac/Linux: export
```
export FLASK_APP=app.py
export FLASK_ENV=development
```

### On Windows: set
```
set FLASK_APP=app.py
set FLASK_ENV=development
```

### API Server

All accessable endpoints of the project are located in the `app.py` file.

Run the following command in the project root folder to start the local development server:

```
flask run --reload
```

## RBAC credentials and roles

Auth0 was set up to manage role-based access control for two users. The API documentation below describes, among others, by which user the endpoints can be accessed. Access credentials and permissions are handled with JWT tockens which must be included in the request header. 

### User and Permissions

Users can access API endpoints that have the following permission requirements:

ott user:
`'read:ott'` - Read categories, collections information

ott manager:
`'read:ott'` - Read categories, collections information
`'post:ott'` - Create categories, collections information
`'patch:ott'` - Update categories, collections information
`'delete:ott'` - Delete categories, collections information

## API Reference
### Getting Started
- Base URL: App can be run locally and can be hosted on a cloud provider. See 'Running the local development server' or 'Render Deployment' section.
Local base url is `http://127.0.0.1:5000/` 
- Authentication: App requires Auth0 authentication. 2 types of users allowed - ott user and ott manager 

### Error Handling
Errors are returned as JSON objects in the following format:

The API will return below error types when requests fail:
- 400: Bad Request
    ```
    {
        "success": False, 
        "error": 400,
        "message": "bad request"
    }
    ```
- 401: Unauthorized
    ```
    {
        "success": False, 
        "error": 401,
        "message": "Authorization header is required/Access denied due to invalid token/Unathorized"
    }
    ```
- 403: Invalid Permission
    ```
    {
        "success": False, 
        "error": 403,
        "message": "Permission is invalid/not allowed"
    }
    ```
- 404: Resource Not Found
    ```
    {
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }
    ```
- 405: Method Not Allowed
    ```
    {
        "success": False, 
        "error": 405,
        "message": "methgod not allowed"
    }
    ```
- 422: Not Processable 
    ```
    {
        "success": False, 
        "error": 422,
        "message": "unable to process the request"
    }
    ```
- 500: Internal Server Error 
    ```
    {
        "success": False, 
        "error": 500,
        "message": "internal server error"
    }
    ```

### Endpoints 
#### GET /categories
- General:
    - Returns available categories list.
- Request Sample: 
    `curl -H "Authorization: Bearer <ACCESS_TOKEN>" {baseUrl}/categories`
- Response Sample JSON:
    ```
   {
    "categories": [
        {
            "id": 1,
            "type": "Movies"
        },
        {
            "id": 2,
            "type": "Shows"
        },
        {
            "id": 3,
            "type": "Others"
        }
    ],
    "success": true
   }
    ```
#### GET /collections
1. without category query parameter
- General:
    - Returns available collections for all categories. Collections will be grouped by category.
- Request Sample: 
    `curl -H "Authorization: Bearer <ACCESS_TOKEN>" {baseUrl}/collections`
    or
    `curl -H "Authorization: Bearer <ACCESS_TOKEN>" {baseUrl}/collections?category=all`
- Response Sample JSON:
    ```
   {
    "collections": [
        {
            "Movies": [
                {
                    "id": 25,
                    "image_url": "123",
                    "rating": 9,
                    "seasons": [],
                    "title": "my movie",
                    "video_url": "123"
                }
            ]
        },
        {
            "Shows": [
                {
                    "id": 26,
                    "image_url": "123",
                    "rating": 6,
                    "seasons": [
                        {
                            "episodes": 10,
                            "name": "my season 1",
                            "season_id": 24
                        },
                        {
                            "episodes": 8,
                            "name": "my season 2",
                            "season_id": 25
                        }
                    ],
                    "title": "my show",
                    "video_url": "123"
                }
            ]
        }
    ],
    "success": true
   }
    ```
2. with category query parameter
- General:
    - Returns available collections for the requested category. 
- Request Sample: 
    `curl -H "Authorization: Bearer <ACCESS_TOKEN>" {baseUrl}/collections?category={categoryName}`
- Response Sample JSON:
    ```
   {
    "collections": [
        {
            "Movies": [
                {
                    "id": 25,
                    "image_url": "123",
                    "rating": 9,
                    "seasons": [],
                    "title": "my movie",
                    "video_url": "123"
                }
            ]
        }
    ],
    "success": true
   }
    ```
#### POST /categories
- General:
    - Add new category or returns category id if already exists.
- Request Sample: 
    `curl -X POST {baseUrl}/categories -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"name": "movies"}'`
- Response Sample JSON:
    ```
   {
    "category_id": 1,
    "success": true
   }
    ```
#### POST /collections
- General:
    - Add new collection for any existing category.
- Request Sample: 
    `curl -X POST {baseUrl}/collections -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"title": "my movie", "category":"1","rating":9, "image_url":"123","video_url":"123"}'`
- Response Sample JSON:
    ```
   {
    "collection": {
        "id": 25,
        "image_url": "123",
        "rating": 9,
        "seasons": [],
        "title": "my movie",
        "video_url": "123"
    },
    "success": true
   }     
    ```
#### PATCH /collections/{collection_id}
- General:
    - Update an collection for an existing collection id.
- Request Sample: 
    `curl -X PATCH {baseUrl}/collections/{collection_id} -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"rating":1}'`
- Response Sample JSON:
    ```
   {
    "collection": {
        "id": 25,
        "image_url": "123",
        "rating": 1,
        "seasons": [],
        "title": "my movie",
        "video_url": "123"
    },
    "success": true
   }    
    ```
#### DELETE /collections/{collection_id}
- General:
    - Delete an collection for an existing collection id.
- Request Sample: 
    `curl -X DELETE {baseUrl}/collections/{collection_id} -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json"`
- Response Sample JSON:
    ```
   {
    "collection_id": 25,
    "success": true
   }    
    ```

## Testing

The testing of all endpoints was implemented with unittest. Each endpoint can be tested with one success test case and one error test case. RBAC feature can also be tested for company user and candidate user.

All test cases are soted in `test_app.py` file in the project rool folder.

Before running the test application, run `source setup.sh`

Then create movieapp_test database using Psql CLI:
`createdb ottapp_test`

Using the command line interface run the test file:

`python3 test_app.py`

A Postman script has also been created for easy testing of these roles. See the json file:
`postman_collection.json`


## Render Deployment

The backend application has been deployed on Render and can be accessed live at
```
https://ott-app-service.onrender.com
```