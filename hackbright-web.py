from flask import Flask, request, render_template, flash, redirect, g
import hackbright

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.before_request
def add_to_g():
    g.students = hackbright.get_all_students()
    g.projects = hackbright.get_all_projects()


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def add_student_form():
    """Show form for adding a student."""

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def add_student():
    """Show added student."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(fname, lname, github)

    flash('%s %s Succesfully Added' % (fname, lname))

    return redirect("/student?github="+github)


@app.route("/project")
def project_info():
    """Show all projects and all students who completed them"""

    title = request.args.get('title')
    p_title, description, max_grade = hackbright.get_project_by_title(title)

    grades = hackbright.get_grades_by_title(title)

    dic = {}

    for grade in grades:
        github = grade[0]
        grd = grade[1]
        first, last, github = hackbright.get_student_by_github(github)
        grade = (first, last, grd)
        dic[github] = grade

    print dic

    return render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           grades=dic
                           )

@app.route("/project-add")
def add_project_form():
    """Show form for adding a project."""

    return render_template("project_add.html")


@app.route("/project-add", methods=['POST'])
def add_project():
    """Show added project."""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    flash('%s Succesfully Added' % (title))

    return redirect("/project?title="+title)


@app.route("/")
def homepage():
    """Shows list of all projects and all students"""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("homepage.html",
                           students=students,
                           projects=projects)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
