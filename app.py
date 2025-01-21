from flask import Flask,jsonify,request
import urllib.parse
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

app=Flask(__name__)

DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres.eacwwrbsxlwxqbffhgmm',
    'password': 'G#C@ehQjX68h@XS',
    'host': 'aws-0-us-west-1.pooler.supabase.com',
    'port': '5432'
}
password = urllib.parse.quote_plus(DB_CONFIG['password'])
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{password}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db=SQLAlchemy(app)

#models
class Patient(db.Model):
    __tablename__="patients"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)


#url route to read all patients
@app.route("/patients",methods=["GET"])
def get_patients():
    patients=Patient.query.all()
    patients_list=[]
    for patient in patients:
        patients_list.append({"id":patient.id,"name":patient.name,"age":patient.age})
    return jsonify(patients_list)
#get patient by id 
#query parameters e.g /patients?id=1

#get patient by id  using url parameters (dynamic routes) e.g /patients/1
@app.route("/patients/<int:id>",methods=["GET"])
def get_patient(id):
    patient=Patient.query.get(id)
    return jsonify({"id":patient.id,"name":patient.name,"age":patient.age})

if __name__ == "__main__":
    app.run(debug=True, port=5555)
