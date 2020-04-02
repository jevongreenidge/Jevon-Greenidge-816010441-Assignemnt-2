from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Box(db.Model):
  bid = db.Column('bid', db.Integer, primary_key=True)
  id = db.Column('id', db.Integer, db.ForeignKey('user.id'))
  pid = db.Column('pid', db.Integer, db.ForeignKey('pokemon.pid'))
  name = db.Column(db.String(50))
  pokemon = db.relationship('Pokemon')

  def toDict(self):
    return{
      'name': self.name,
      'stats': self.pokemon.toDict()
    }

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  # box = db.relationship('Pokemon', backref=db.backref('trainer', lazy='dynamic'))

  def toDict(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "password": self.password
    }
  
  #hashes the password parameter and stores it in the object
  def set_password(self, password):
      """Create hashed password."""
      self.password = generate_password_hash(password, method='sha256')
  
  #Returns true if the parameter is equal to the object’s password property
  def check_password(self, password):
      """Check hashed password."""
      return check_password_hash(self.password, password)
  
  #To String method
  def __repr__(self):
      return '<User {}>'.format(self.username)  

class Pokemon(db.Model):
  pid = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  attack = db.Column(db.Integer, nullable=False)
  defense = db.Column(db.Integer, nullable=False)
  hp = db.Column(db.Integer, nullable=False)
  height = db.Column(db.Float) 
  sp_attack = db.Column(db.Integer, nullable=False)
  sp_defense = db.Column(db.Integer, nullable=False)
  speed = db.Column(db.Integer, nullable=False)
  type1 = db.Column(db.String(255), nullable=False)
  type2 = db.Column(db.String(255))
  weight = db.Column(db.Float)

  def toDict(self):
   return {
     'pid': self.pid,
     'name': self.name,
     'attack': self.attack,
     'defense': self.defense,
     'hp': self.hp,
     'height': self.height,
     'sp_attack': self.sp_attack,
     'sp_defense': self.sp_defense,
     'speed': self.speed,
     'type1': self.type1,
     'type2': self.type2,
     'weight': self.weight
   }
