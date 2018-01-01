from app import dbm

#Create class for table
class User(db.Model):
    #Create table
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)


    #Set required / initialize an user
    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self. email = email

    #Return informations about User
    def __repr__(self):
        return "<User %r>" % self.username


class Faces(db.Model):
    __tablename__ = "faces"
    id = db.Column(db.Integer, primary_key=True)
    face_image = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.Foreignkey('users.id'))

    #Create relashionship between FACE and USER
    user = db.relashionship('User', foreign_keys=user_id)

    def __init__(self, face_image, user_id):
        self.face_image = face_image
        self.user_id = user_id

    def __repr__(self):
        return "<Post %r>" % self.id
