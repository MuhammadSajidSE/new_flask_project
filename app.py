from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configure PostgreSQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://neondb_owner:npg_Od7nk1yFtgWE@'
    'ep-summer-meadow-a8dvj3fd-pooler.eastus2.azure.neon.tech/neondb?sslmode=require'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app, title="Student API", description="A simple Flask API with Swagger UI")

# Define Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Create Database Tables (only if they don't exist)
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

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
        try:
            students = Student.query.all()
            return [{"id": s.id, "name": s.name, "age": s.age} for s in students], 200
        except Exception as e:
            return {"message": f"Error fetching students: {str(e)}"}, 500

    @ns.expect(student_model)
    @ns.doc("add_student")
    def post(self):
        """Add a new student"""
        data = request.get_json()
        try:
            new_student = Student(name=data['name'], age=data['age'])
            db.session.add(new_student)
            db.session.commit()
            return {"message": "Student added successfully!"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error adding student: {str(e)}"}, 500

# Health Check Route
@app.route('/health')
def health_check():
    return {"status": "UP"}, 200

# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
