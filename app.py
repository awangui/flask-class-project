from flask import Flask,jsonify,request
import urllib.parse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
migrate=Migrate(app,db)#Initialize migrate object

#models
class Student(db.Model):
    __tablename__="students"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    parents=db.relationship("Parent",backref="student",lazy=True,cascade="all, delete-orphan")#cascade="all, delete-orphan" means when a student is deleted, all the parents will also be deleted

    def single_student(self):
        return {"id":self.id,"name":self.name,"age":self.age,"email":self.email}


#url route to read all students
@app.route("/students",methods=["GET"])
def get_students():
    students=Student.query.all()
    studentList=[]
    for student in students:
      student_dic={
        "id":student.id,
        "name":student.name,
        "age":student.age
      }
    print(student.parents)
    parents=student.parents
    parents_list=[]
    for parent in parents:
        parent_dic={
            "id":parent.id,
            "name":parent.name,
                "email":parent.email
        }
        parents_list.append(parent_dic)
    student_dic["parents"]=parents_list 
    studentList.append(student_dic)

    return jsonify(studentList)

    

#get student by id  using url parameters (dynamic routes) e.g /students/1
@app.route("/students/<int:id>",methods=["GET"])
def get_student_by_id(id):
    student=Student.query.get(id)
    if student:
        return jsonify({"id":student.id,"name":student.name,"age":student.age})
    else:
        return jsonify({"message":"student not found"}),404
    

#get student by id using query parameters e.g /students?id=1
@app.route("/students/find",methods=["GET"])
def get_student_by_id_query():
    query_params=request.args
    id = query_params.get("id")
    student = Student.query.get(id)
    if student:
        return jsonify({"id": student.id, "name": student.name, "age": student.age, "email": student.email})
    else:
        return jsonify({"message": "student not found"}), 404

@app.route("/students",methods=["POST"])
def add_student():
    data=request.get_json()
    name=data.get("name")
    age=data.get("age")
    email=data.get("email")
    
    if not name or not age:
        return jsonify({"error":"name and age are required"}),400
    
    if not isinstance(age,int):
        return jsonify({"error":"age must be an integer"}),400
    
    if not isinstance(name,str):
        return jsonify({"error":"name must be a string"}),400
    
    if len(name)<4:
        return jsonify({"error":"name must be at least 4 characters"}),400
    
    if not email:
        return jsonify({"error":"email is required"}),400
    if len(email)<5:
        return jsonify({"error":"email must be at least 5 characters"}),400
    
    if '@' not in email:
        return jsonify({"error":"email is invalid"}),400
    
    student_by_email=Student.query.filter_by(email=email).first()
    
    if student_by_email:
        return jsonify({"error":"email already exists"}),400
    student=Student(name=name,age=age,email=email)
    db.session.add(student)
    db.session.commit()
    return jsonify({"message":"student added successfully"}),201


class Parent(db.Model):
    # def __init__(self,name,age,email):
    #     self.name=name
    #     self.age=age
    #     self.email=email
    
    
    __tablename__="parents"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id", ondelete="CASCADE"),nullable=False)#ondelete="CASCADE" means when a student is deleted, the parent will also be deleted
    
    #if on delete is set to null e.g ondelete="SET NULL" then the student_id will be set to null when the student is deleted
    def to_dict(self):
        return {"id":self.id,"name":self.name,"email":self.email,"student_id":self.student_id}
@app.route("/parents",methods=["POST"])
def add_parent():
    data=request.get_json()
    name=data.get("name")
    email=data.get("email")
    student_id=data.get("student_id")
    
    if not isinstance(name,str):
        return jsonify({"error":"name must be a string"}),400
    
    if len(name)<4:
        return jsonify({"error":"name must be at least 4 characters"}),400
    
    if not email:
        return jsonify({"error":"email is required"}),400
    if len(email)<5:
        return jsonify({"error":"email must be at least 5 characters"}),400
    
    if '@' not in email:
        return jsonify({"error":"email is invalid"}),400
    
    student=Student.query.get(student_id)
    if not student:
        return jsonify({"error":"student not found"}),404
    
    parent=Parent(name=name,email=email,student_id=student_id)
    db.session.add(parent)
    db.session.commit()
    return jsonify(parent.to_dict()),201

if __name__ == "__main__":
    app.run(debug=True, port=5555)