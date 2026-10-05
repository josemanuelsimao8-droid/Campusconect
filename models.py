from datetime import datetime

from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(50), nullable=False, default="student")
    account_status = db.Column(db.String(20), nullable=False, default="active")

    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    email_verified_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student_profile = db.relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    email_verification_codes = db.relationship(
        "EmailVerificationCode",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    password_reset_tokens = db.relationship(
        "PasswordResetToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class University(db.Model):
    __tablename__ = "universities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    acronym = db.Column(db.String(50), unique=True, nullable=False)

    campuses = db.relationship(
        "Campus",
        back_populates="university",
        cascade="all, delete-orphan",
    )

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="university",
    )


class Campus(db.Model):
    __tablename__ = "campuses"

    id = db.Column(db.Integer, primary_key=True)

    university_id = db.Column(
        db.Integer,
        db.ForeignKey("universities.id"),
        nullable=False,
    )

    name = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(100), nullable=False)

    university = db.relationship("University", back_populates="campuses")

    schools = db.relationship(
        "School",
        back_populates="campus",
        cascade="all, delete-orphan",
    )

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="campus",
    )

    student_profiles = db.relationship(
        "StudentProfile",
        back_populates="campus",
    )


class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)

    campus_id = db.Column(
        db.Integer,
        db.ForeignKey("campuses.id"),
        nullable=False,
    )

    name = db.Column(db.String(255), nullable=False)

    campus = db.relationship("Campus", back_populates="schools")

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="school",
    )


class EducationLevel(db.Model):
    __tablename__ = "education_levels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="education_level",
    )


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    dges_code = db.Column(db.String(30), unique=True, nullable=True)

    course_offerings = db.relationship(
        "CourseOffering",
        back_populates="course",
    )


class CourseOffering(db.Model):
    __tablename__ = "course_offerings"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False,
    )

    university_id = db.Column(
        db.Integer,
        db.ForeignKey("universities.id"),
        nullable=False,
    )

    campus_id = db.Column(
        db.Integer,
        db.ForeignKey("campuses.id"),
        nullable=False,
    )

    school_id = db.Column(
        db.Integer,
        db.ForeignKey("schools.id"),
        nullable=False,
    )

    education_level_id = db.Column(
        db.Integer,
        db.ForeignKey("education_levels.id"),
        nullable=False,
    )

    course = db.relationship("Course", back_populates="course_offerings")
    university = db.relationship("University", back_populates="course_offerings")
    campus = db.relationship("Campus", back_populates="course_offerings")
    school = db.relationship("School", back_populates="course_offerings")
    education_level = db.relationship(
        "EducationLevel",
        back_populates="course_offerings",
    )

    student_profiles = db.relationship(
        "StudentProfile",
        back_populates="course_offering",
    )


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    profile_photo_url = db.Column(db.String(500), nullable=True)

    phone = db.Column(db.String(30), nullable=True)
    location = db.Column(db.String(255), nullable=True)

    campus_id = db.Column(
        db.Integer,
        db.ForeignKey("campuses.id"),
        nullable=True,
    )

    course_offering_id = db.Column(
        db.Integer,
        db.ForeignKey("course_offerings.id"),
        nullable=True,
    )

    academic_year = db.Column(db.Integer, nullable=False)
    student_number = db.Column(db.String(100), nullable=False)
    institutional_email = db.Column(db.String(255), nullable=False)

    verification_status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
    )

    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="student_profile")
    campus = db.relationship("Campus", back_populates="student_profiles")
    course_offering = db.relationship(
        "CourseOffering",
        back_populates="student_profiles",
    )


class EmailVerificationCode(db.Model):
    __tablename__ = "email_verification_codes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="email_verification_codes")


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="password_reset_tokens")
