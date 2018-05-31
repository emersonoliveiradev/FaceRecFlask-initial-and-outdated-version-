import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')


SQLALCHEMY_TRACK_MODIFICATIONS = True

#key for encript informations of formularies
SECRET_KEY = 'chavequalquer'
#ver pra q serve
#SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#SQLALCHEMY_TRACK_MODIFICATIONS = False

