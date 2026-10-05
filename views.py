from flask import Blueprint, render_template, request, jsonify

from database import db
from models import CourseOffering, University, Campus


views = Blueprint('views', __name__)


@views.route('/')
def homepage():
    return render_template('homepage.html')


@views.route('/login')
def login():
    return render_template('login.html')


@views.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_notice = None

    universities = (
        University.query
        .order_by(University.name.asc())
        .all()
    )

    if request.method == 'POST':
        signup_notice = 'O cadastro está sendo processado.'

    return render_template(
        'signup.html',
        signup_notice=signup_notice,
        universities=universities
    )


@views.route('/api/universities/<int:university_id>/campuses')
def university_campuses(university_id):

    campuses = (
        Campus.query
        .filter_by(university_id=university_id)
        .order_by(Campus.name.asc())
        .all()
    )

    return jsonify([
        {
            'id': campus.id,
            'name': campus.name,
            'district': campus.district
        }
        for campus in campuses
    ])

@views.route('/api/campuses/<int:campus_id>/courses')
def campus_courses(campus_id):

    offerings = (
        CourseOffering.query
        .filter_by(campus_id=campus_id)
        .all()
    )

    return jsonify([
        {
            'id': offering.id,
            'name': offering.course.name,
            'education_level': offering.education_level.name
        }
        for offering in offerings
    ])