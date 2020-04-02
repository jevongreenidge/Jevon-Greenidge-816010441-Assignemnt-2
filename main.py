import json
from flask import Flask, request, render_template
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from flask_cors import CORS




from models import db, User, Pokemon, Box

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7)
  CORS(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here '''
def authenticate(uname, password):
  #search for the specified user
  user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  if user and user.check_password(password):
    return user

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

''' End JWT Setup '''


@app.route('/')
def index():
  pokemon = Pokemon.query.limit(50).all()
  return render_template('index.html', pokemon=pokemon)

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

@app.route('/signup', methods=['POST'])
def signup():
  userdata = request.get_json() # get userdata
  newuser = User(username=userdata['username'], email=userdata['email']) # create user object
  newuser.set_password(userdata['password']) # set password
  try:
    db.session.add(newuser)
    db.session.commit() # save user
  except IntegrityError: # attempted to insert a duplicate user
    db.session.rollback()
    return 'username or email already exists' # error message
  return 'user created' # success

@app.route('/mypokemon', methods=['POST'])
@jwt_required()
def create_my_pokemon():
  data = request.get_json()
  rec = Box(pid=data["pid"], name=data["name"], id=current_identity.id)
  db.session.add(rec)
  db.session.commit()
  return data["name"]+" captured", 201 # return data and set the status code

@app.route('/pokemon', methods=['GET'])
def get_pokemon():
  pokemon = Pokemon.query.all()
  pokemon = [poke.toDict() for poke in pokemon] # list comprehension which converts my_pokemon objects to dictionaries
  return json.dumps(pokemon)

@app.route('/mypokemon', methods=['GET'])
@jwt_required()
def get_my_pokemons():
  queryset = Box.query.filter_by(id=current_identity.id).all()
  if queryset == None:
    return 'Invalid id or unauthorized'
  if len(queryset) == 0:
    return 'No Pokemon captured!'
  pokemon = [poke.toDict() for poke in queryset]
  return json.dumps(pokemon)

@app.route('/mypokemon/<num>', methods=['GET'])
@jwt_required()
def get_my_pokemon(num):
  num = int(num)
  queryset = Box.query.filter_by(id=current_identity.id).all()
  if queryset == None:
    return 'Invalid id or unauthorized'
  if len(queryset) == 0:
    return 'No Pokemon captured!'
  if num > len(queryset):
    return 'Invalid num specified'
  return json.dumps(queryset[num-1].toDict())

@app.route('/mypokemon/<num>', methods=['PUT'])
@jwt_required()
def update_my_pokemon(num):
  num = int(num)
  queryset = Box.query.filter_by(id=current_identity.id).all()
  if queryset == None:
    return 'Invalid id or unauthorized'
  if len(queryset) == 0:
    return 'No Pokemon captured!'
  if num > len(queryset):
    return 'Invalid num specified'
  my_pokemon = queryset[num - 1]
  data = request.get_json()
  if 'name' in data:
    my_pokemon.name = data['name']
  db.session.add(my_pokemon)
  db.session.commit()
  return 'Updated', 201

@app.route('/mypokemon/<num>', methods=['DELETE'])
@jwt_required()
def delete_my_pokemon(num):
  num = int(num)
  queryset = Box.query.filter_by(id=current_identity.id).all()
  if queryset == None:
    return 'Invalid id or unauthorized'
  if len(queryset) == 0:
    return 'No Pokemon captured!'
  if num > len(queryset):
    return 'Invalid num specified'
  my_pokemon = queryset[num - 1]
  db.session.delete(my_pokemon) # delete the object
  db.session.commit()
  return 'Deleted', 204

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)