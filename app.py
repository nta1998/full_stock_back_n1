import json
from flask import Flask,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.sqlite3'

db = SQLAlchemy(app)

class Persons(db.Model):
    id = db.Column('person_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    favorite_color = db.Column(db.String(100))
    def __init__(self, name, email, phone_number, favorite_color):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.favorite_color = favorite_color


@app.route("/add/", methods=['GET','POST'])
@app.route("/add/<id>",methods=['DELETE','PUT'])
def crod_p(id=-1):
    if request.method == 'POST':
       request_data = request.get_json()
       name = request_data['name']
       email = request_data['email']
       phone_number = request_data['phone_number']
       favorite_color = request_data['favorite_color']
       newperson = Persons(name,email,phone_number,favorite_color)
       db.session.add(newperson)
       db.session.commit()
       return []
    if request.method == 'GET':
        respons=[]
        for person in Persons.query.all():
            respons.append({'id':person.id,'name': person.name ,'email': person.email, 'phone_number': person.phone_number, 'favorite_color': person.favorite_color})
        return (json.dumps(respons))
    if request.method == 'PUT':
        the_put_person=Persons.query.get(id)
        request_data = request.get_json()
        the_put_person.name= request_data['name']
        the_put_person.email = request_data['email']
        the_put_person.phone_number = request_data['phone_number']
        the_put_person.favorite_color = request_data['favorite_color']
        db.session.commit()
        return{}
    if request.method == 'DELETE':
        the_put_person=Persons.query.get(id)
        db.session.delete(the_put_person)
        db.session.commit()



if __name__ == ('__main__'):
    with app.app_context():
        db.create_all()
    app.run(debug=True)
