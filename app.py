from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

# Ensure the CSV file exists and has the correct headers
if not os.path.exists('people.csv'):
    with open('people.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'State', 'Salary', 'Grade', 'Room', 'Telnum', 'Picture', 'Keywords']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Load data from CSV
def load_data():
    people = []
    with open('people.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            people.append(row)
    return people

def save_data(people):
    with open('people.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'State', 'Salary', 'Grade', 'Room', 'Telnum', 'Picture', 'Keywords']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for person in people:
            writer.writerow(person)

people = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form.get('name')
    salary = request.form.get('salary')
    results = []

    if name:
        results = [person for person in people if person['Name'].lower() == name.lower()]
    elif salary:
        try:
            salary = float(salary)
            results = [person for person in people if person['Salary'] and person['Salary'].replace('.', '', 1).isdigit() and float(person['Salary']) < salary]
        except ValueError:
            results = []

    return render_template('results.html', results=results)

@app.route('/upload_picture', methods=['POST'])
def upload_picture():
    person_name = request.form.get('person_name')
    picture = request.files.get('picture')

    if person_name and picture:
        filename = f"{person_name.lower().replace(' ', '_')}.jpg"
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        for person in people:
            if person['Name'].lower() == person_name.lower():
                person['Picture'] = filename
                break
        else:
            people.append({
                'Name': person_name,
                'State': '',
                'Salary': '',
                'Grade': '',
                'Room': '',
                'Telnum': '',
                'Picture': filename,
                'Keywords': ''
            })

        save_data(people)

    return redirect(url_for('index'))

@app.route('/remove_person', methods=['POST'])
def remove_person():
    remove_name = request.form.get('remove_name')
    global people
    people = [person for person in people if person['Name'].lower() != remove_name.lower()]
    save_data(people)
    return redirect(url_for('index'))

@app.route('/change_keyword', methods=['POST'])
def change_keyword():
    keyword_name = request.form.get('keyword_name')
    new_keyword = request.form.get('new_keyword')

    for person in people:
        if person['Name'].lower() == keyword_name.lower():
            person['Keywords'] = new_keyword
            break

    save_data(people)
    return redirect(url_for('index'))

@app.route('/change_salary', methods=['POST'])
def change_salary():
    salary_name = request.form.get('salary_name')
    new_salary = request.form.get('new_salary')

    for person in people:
        if person['Name'].lower() == salary_name.lower():
            person['Salary'] = new_salary
            break

    save_data(people)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)