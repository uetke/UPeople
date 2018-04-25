from flask import render_template, url_for, redirect

from crm import app, db
from crm.models import Contact, Course
from .forms import NewContactForm, NewCourseForm


@app.route('/')
def index():
    return "Hello World", 200


@app.route('/contacts')
def contacts():
    contacts = Contact.query.all()
    return render_template('contacts.html', contacts=contacts)


@app.route('/new_contact', methods=['GET', 'POST'])
@app.route('/new_contact/', methods=['GET', 'POST'])
def new_contact():
    form = NewContactForm()
    if form.validate_on_submit():
        if form.email is not None:
            contact = Contact.query.filter_by(email=form.email.data).first()
            if contact:
                form.email.errors.append('That e-mail is already registered')
                return render_template('new_contact.html', form=form)
        contact = Contact()
        form.populate_obj(contact)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('contacts'))
    return render_template('new_contact.html', form=form)

@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/new_course', methods=['GET', 'POST'])
def new_course():
    form = NewCourseForm()
    if form.validate_on_submit():
        course = Course()
        form.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('contacts'))
    return render_template('new_contact.html', form=form)