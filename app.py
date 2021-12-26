from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pymysql

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/db' #db docker
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@172.17.0.23/db' #db k8s
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    name = db.Column(db.String(100))
    instructor = db.Column(db.String(100))

    def __init__(self, id, date, name, instructor):
        self.id = id
        self.date = date
        self.name = name
        self.instructor = instructor

class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'name', 'instructor')

# init shcema
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


# add a course
@app.route('/course', methods=['POST'])
def add_product():
    global new_course
    id = request.json['id']
    date = request.json['date']
    name = request.json['name']
    instructor = request.json['instructor']

    new_course = Course(id, date, name, instructor)

    db.session.add(new_course)
    db.session.commit()

    return course_schema.jsonify(new_course)

# edit a course by id
@app.route('/course/<id>', methods=['PUT'])
def update_product(id):
    course = Course.query.get(id)

    date = request.json['date']
    name = request.json['name']
    instructor = request.json['instructor']

    course.date = date
    course.name = name
    course.instructor = instructor

    db.session.commit()

    return course_schema.jsonify(course)

# get all courses sorted by date
@app.route('/course', methods=['GET'])
def get_products():
    all_products = Course.query.order_by(Course.date).all() 
    result = courses_schema.dump(all_products)
    return jsonify(result)

# get single course by id
@app.route('/course/<id>', methods=['GET'])
def get_product(id):
    product = Course.query.get(id)
    return course_schema.jsonify(product)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')