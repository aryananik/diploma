from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Пример данных
patients = [
    {
        "name": "Иван Иванов",
        "appointments": ["Осмотр: 2024-05-21", "Анализ крови: 2024-05-22"],
        "test_results": ["Анализ крови: Норма"],
        "operations": ["Операция на колене: 2024-06-01"],
        "blood_pressure": "120/80",
        "height": "180 см",
        "weight": "75 кг",
        "complaints": "Головная боль"
    }
]

# Главная страница с формой для входа
@app.route('/')
def index():
    return render_template('index.html')

# Обработка входа пользователя
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    user_type = request.form['user_type']
    session['username'] = username
    session['user_type'] = user_type
    if user_type == 'patient':
        patient_data = next((p for p in patients if p["name"] == username), None)
        if not patient_data:
            # Создать нового пациента
            new_patient = {
                "name": username,
                "appointments": [],
                "test_results": [],
                "operations": [],
                "blood_pressure": "",
                "height": "",
                "weight": "",
                "complaints": ""
            }
            patients.append(new_patient)
            return redirect(url_for('edit_patient', username=username))
        return redirect(url_for('patient_dashboard', username=username))
    elif user_type == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    return redirect(url_for('index'))

# Кабинет пациента
@app.route('/patient/<username>')
def patient_dashboard(username):
    patient_data = next((p for p in patients if p["name"] == username), None)
    is_doctor = session.get('user_type') == 'doctor'
    return render_template('patient.html', patient=patient_data, is_doctor=is_doctor)

# Кабинет врача
@app.route('/doctor')
def doctor_dashboard():
    return render_template('doctor.html', patients=patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    if session.get('user_type') != 'doctor':
        return redirect(url_for('index'))

    name = request.form['name']
    new_patient = {
        "name": name,
        "appointments": [],
        "test_results": [],
        "operations": [],
        "blood_pressure": "",
        "height": "",
        "weight": "",
        "complaints": ""
    }
    patients.append(new_patient)
    return redirect(url_for('doctor_dashboard'))


@app.route('/edit_patient/<username>', methods=['GET', 'POST'])
def edit_patient(username):
    patient_data = next((p for p in patients if p["name"] == username), None)
    if request.method == 'POST':
        patient_data['blood_pressure'] = request.form['blood_pressure']
        patient_data['height'] = request.form['height']
        patient_data['weight'] = request.form['weight']
        patient_data['complaints'] = request.form['complaints']
        return redirect(url_for('patient_dashboard', username=username))
    return render_template('edit_patient.html', patient=patient_data)

@app.route('/add_appointment/<username>', methods=['POST'])
def add_appointment(username):
    appointment = request.form['appointment']
    for patient in patients:
        if patient['name'] == username:
            patient['appointments'].append(appointment)
    return redirect(url_for('patient_dashboard', username=username))

@app.route('/add_test_result/<username>', methods=['POST'])
def add_test_result(username):
    test_result = request.form['test_result']
    for patient in patients:
        if patient['name'] == username:
            patient['test_results'].append(test_result)
    return redirect(url_for('patient_dashboard', username=username))

@app.route('/add_operation/<username>', methods=['POST'])
def add_operation(username):
    operation = request.form['operation']
    for patient in patients:
        if patient['name'] == username:
            patient['operations'].append(operation)
    return redirect(url_for('patient_dashboard', username=username))

@app.route('/schedule')
def schedule():
    return render_template('schedule.html', patients=patients)

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
