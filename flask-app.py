from os import chdir
from os.path import dirname

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# DEMO STUFF

@app.route('/')
def view_hello():
    return 'Hello World!'

@app.route('/demo-1')
def view_demo_1():
    return render_template('demo-1.html', name='Justin')

@app.route('/demo-2/<name>')
def view_demo_2(name):
    return render_template('demo-1.html', name=name)

@app.route('/demo-3')
def view_demo_3():
    names = ['Alice', 'Bob', 'Charlie']
    return render_template('demo-3.html', salutation='Roll call', names=names)

# STUDENT DIRECTORY APP

class Student:
    def __init__(self, first_name, last_name, username, majors, advisor):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.majors = majors
        self.advisor = advisor
    def __repr__(self):
        return 'Student(' + self.username + ')'
    def __str__(self):
        return 'Student(' + self.username + ')'
    def __hash__(self):
        return self.username
    def __eq__(self, other):
        return self.username == other.username


def get_data():
    students = []
    with open('students.csv') as fd:
        for line in fd.read().splitlines():
            name, username, majors, advisor = line.split('\t')
            last_name, first_name = name.split(', ')
            students.append(Student(first_name, last_name, username, majors, advisor))
    return sorted(students, key=(lambda s: s.username))

@app.route('/directory')
def view_directory():
    # call the list from get_data directory
    master_list = get_data()
    # put list of all students into directory template
    return render_template('directory.html', students=master_list)

@app.route('/directory/<username>')
def view_student(username):
    # use list of students
    master_list = get_data()
    current_student = None
    # for every number from zero to the length of the master list...
    for i in range(0, len(master_list)):
        # if the property username of the student at that index is the username
        if master_list[i].username == username:
            # current student is student at that position in the master list
            current_student = master_list[i]
            break
    # if not first or last student...
    if i != 0 and i != (len(master_list)-1):
        # make the previous student the student at the previous index
        prev_student = master_list[i - 1]
        # make the next student at the next index
        next_student = master_list[i + 1]
    elif i == 0:
        # make the previous student the last student on the master list
        prev_student = master_list[(len(master_list))-1]
        # and the next student the same as normal
        next_student = master_list[i + 1]
    # if it's at the last student...
    elif i == (len(master_list)-1):
        # previous student same as normal
        prev_student = master_list[i - 1]
        # but make the next student the first student on the list
        next_student = master_list[0]
    # return template with information defined
    return render_template('student.html', student=current_student, prev_student=prev_student, next_student=next_student)

# DON'T TOUCH THE CODE BELOW THIS LINE

@app.route('/css/<file>')
def view_css(file):
    return send_from_directory('css', file)

if __name__ == '__main__':
    chdir(dirname(__file__))
    app.run(debug=True)
