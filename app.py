from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# Configure PostgreSQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123%23sajid@localhost:5432/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app, title="Student API", description="A simple Flask API with Swagger UI")

# Define Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Define Namespace
ns = api.namespace('students', description="Student operations")

# Define Request Model for Swagger
student_model = api.model('Student', {
    'name': fields.String(required=True, description="Student Name"),
    'age': fields.Integer(required=True, description="Student Age"),
})

# Routes
@ns.route('/')
class StudentList(Resource):
    @ns.doc("get_students")
    def get(self):
        """Get all students"""
        students = Student.query.all()
        return [{"id": s.id, "name": s.name, "age": s.age} for s in students], 200

    @ns.expect(student_model)
    @ns.doc("add_student")
    def post(self):
        """Add a new student"""
        data = request.get_json()
        new_student = Student(name=data['name'], age=data['age'])
        db.session.add(new_student)
        db.session.commit()
        return {"message": "Student added successfully!"}, 201

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
