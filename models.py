from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance
db = SQLAlchemy()

# Definition of the Department table
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255), nullable=False)

    # __repr__ method for more readable representation in the console
    def __repr__(self):
        return f"<Department {self.department}>"

# Definition of the Job table
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=False)

    # __repr__ method for more readable representation in the console
    def __repr__(self):
        return f"<Job {self.job}>"

# Definition of the Employee table
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)

    # Relationships with Department and Job
    job = db.relationship('Job', backref=db.backref('employees', lazy=True))
    department = db.relationship('Department', backref=db.backref('employees', lazy=True))

    # __repr__ method for more readable representation in the console
    def __repr__(self):
        return f"<Employee {self.name}>"
