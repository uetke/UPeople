from crm import app, db
from crm.models import Contact, Course, WorkGroup, WorkPlace


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Contact': Contact,
        'Course': Course,
        'WorkGroup': WorkGroup,
        'WorkPlace': WorkPlace,
    }