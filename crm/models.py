from hashlib import md5
from datetime import datetime

from crm import db


courses = db.Table('courses',
                   db.Column('course_id', db.Integer, db.ForeignKey('course.id'), nullable=False),
                   db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), nullable=False))

supervisors = db.Table('supervisors',
                       db.Column('supervisor_id', db.Integer, db.ForeignKey('contact.id'), nullable=False),
                       db.Column('employee_id', db.Integer, db.ForeignKey('contact.id'), nullable=False))

class Contact(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))  # Dr. Mr. Prof., etc.
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(256), unique=True)
    added = db.Column(db.DateTime, default=datetime.utcnow)
    last_contacted = db.Column(db.DateTime, nullable=True)
    phone = db.Column(db.String(20))
    notes = db.Column(db.Text)
    address = db.Column(db.String(512))
    workplace_id = db.Column(db.Integer, db.ForeignKey('work_place.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('work_group.id'))

    employees = db.relationship('Contact',
                                secondary=supervisors,
                                primaryjoin=(supervisors.c.employee_id == id),
                                secondaryjoin=(supervisors.c.supervisor_id == id),
                                backref='supervisor')

    courses = db.relationship('Course',
                              secondary=courses,
                              backref='contacts')

    @property
    def gravatar(self):
        code = md5(self.author_email.encode('ascii')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s=60'.format(code)

    def register_course(self, course):
        if not course in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def add_supervisor(self, supervisor):
        if self not in supervisor.employees:
            supervisor.employees.append(self)
        else:
            print("It is already your supervisor")

    def __repr__(self):
        if self.first_name:
            return '<Contact {}.{}>'.format(self.id, self.first_name)
        else:
            return '<Contact {}>'.format(self.id)


class WorkGroup(db.Model):
    __tablename__ = 'work_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    members = db.relationship('Contact', backref='group', lazy=True)
    work_place_id = db.Column(db.Integer, db.ForeignKey('work_place.id'))

    def __repr__(self):
        if self.name:
            return '<WorkGroup {}.{}>'.format(self.id, self.name)
        return '<WorkGroup {}>'.format(self.id)

    def __str__(self):
        if self.name:
            return 'Group {}'.format(self.name)
        return 'Group {}'.format(self.id)


class WorkPlace(db.Model):
    __tablename__ = 'work_place'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(512))
    groups = db.relationship('WorkGroup', backref='work_place', lazy='dynamic')
    country = db.Column(db.String(128))
    state = db.Column(db.String(128))
    city = db.Column(db.String(128))


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    # participants = db.relationship('Contact', secondary=courses, backref='courses')

    @property
    def from_to(self):
        start = self.start_date.strftime('%Y-%m-%d')
        end = self.end_date.strftime('%Y-%m-%d')
        return start + ' - ' + end