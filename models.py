#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#----------------------------------------------------------------------------#
# Super Class for Models
#----------------------------------------------------------------------------#


class Operations:
    def __init__(self) -> None:
        pass

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

"""
Collection
"""


class Collection(db.Model, Operations):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    image_url = Column(String(300))
    video_url = Column(String(300))
    rating = Column(Integer)
    category = Column(String(20))
    seasons = db.relationship(
        'Season',
        backref='collections',
        lazy='joined',
        cascade='all, delete')

    def __init__(self, title, image_url, video_url, rating, category):
        Operations.__init__(self)
        self.title = title
        self.image_url = image_url
        self.video_url = video_url
        self.rating = rating
        self.category = category

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'rating': self.rating,
            'category': self.category,
            'seasons': self.seasons
        }


"""
Season
"""


class Season(db.Model, Operations):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    episodes = Column(Integer)
    collection_id = Column(
        Integer,
        ForeignKey('collections.id'),
        nullable=True)

    def __init__(self, name, episodes, collection_id):
        Operations.__init__(self)
        self.name = name
        self.episodes = episodes
        self.collection_id = collection_id

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'episodes': self.episodes,
            'collection_id': self.collection_id
        }


"""
Category
"""


class Category(db.Model, Operations):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        Operations.__init__(self)
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
