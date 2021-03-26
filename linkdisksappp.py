from flask import Flask,make_response,request,jsonify
import flask
from flask_mongoengine import MongoEngine

from api_constraints import mongodb_password


from werkzeug.security import generate_password_hash,check_password_hash

import jwt
import datetime
import json

from functools import wraps

import os

import userModel

app = Flask(__name__)

database_name = "LinkDisksApi"

DB_URI = "mongodb+srv://bhupendrakumarlal:{}@cluster0.2fmhs.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_password,database_name)


app.config['SECRET_KEY'] = 'USERTOKEN'

app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()

db.init_app(app)







def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token',None)

        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']


        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401    

        

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user = userModel.users.objects(email=data['user']).first()

            return f(current_user.to_json(), *args, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({'message' : 'Token is invalid!'}), 401

        

    return decorated








@app.route('/linkApi/user1',methods=['GET','POST'])
@token_required
def get_all_users(current_user):


    if current_user['admin'] == False:
        return jsonify({'message','Cannot perform that function'})
           

    elif current_user['admin'] == True:
         if request.method == "GET":
            user=[]
            for u in userModel.users.objects:
                user.append(u)
            return make_response(jsonify(user),200)

         elif request.method == "POST":
             pass   
        

    








@app.route('/linkApi/getOneuser',methods=['GET','POST','PUT'])
@token_required
def get_one_users(current_user):

    if request.method == "GET":
        user  = userModel.users.objects(user_id=current_user['user_id'])
        
        if user:
            return make_response(jsonify(user),200)

    elif request.method == "POST":
        pass     
    elif request.method == "PUT":
        pass   






@app.route('/linkApi/create_user', methods=['POST','GET'])
def create_user():

    if request.method == "POST":
        data = request.get_json()
        hash_pass_code=generate_password_hash(data['pass_code'],method="sha256")

        book1=users(user_id=data['user_id'],size=data['size'],email=data['email'],pass_code=hash_pass_code,admin=False)
        book1.save()
        return make_response("success! new user created",201)
    elif request.method == "GET":
        pass









@app.route('/linkApi/login',methods=['GET', 'POST'])
def login_user(): 
 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  user = userModel.users.objects(email=auth.username).first()
  data =user.to_json()
     
  if check_password_hash(data['pass_code'], auth.password):

      token = jwt.encode({
          'user':request.authorization.username,
          'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30),

      },app.config['SECRET_KEY']) 

      return ({
         'token':token.encode().decode('UTF-8')
      })

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})









@app.route('/linkApi/upload_image', methods=['GET', 'POST'])
def upload_image():

    imagefile = flask.request.files['image']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print("\nReceived image File name : " + imagefile.filename)
    imagefile.save(filename)
    return "Image Uploaded Successfully"





if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)


#{"user_id":"saurav","size":"512KB","email":"sauravsrivastava121@gmail.com","pass_code":"1234"}
