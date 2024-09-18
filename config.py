import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    INSTANCE_NAME = 'Image Hosting'
    SECRET_KEY = 'this-is-example-secret-key-please-change-it'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    UPLOAD_FOLDER = 'uploads/'
    SHORT_LINK_LENGTH = 7
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif', 'tif', 'webp', 'svg', 'ico'}
    MAX_CONTENT_LENGTH_MB = 32
    MAX_CONTENT_LENGTH = 1024 * 1024 * MAX_CONTENT_LENGTH_MB # DO NOT CHANGE THIS LINE !!!
    ENABLE_GALLERY = 1
    GALLERY_IMAGES_PER_PAGE = 10