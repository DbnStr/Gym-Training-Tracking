from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
import constants
from database.models.customer import Customer
from flask_login import *

from database.models.training import Training

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(id):
    data = db.get_by_unique_int('Customer', 'customerId', int(id))
    if data is None:
        return None
    else:
        return Customer(*data)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_get():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('get_trainings', customer_id=current_user.id))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    customer = Customer(*db.get_consumer_by_email(email))

    if not customer or (customer.password != password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login_get'))

    login_user(customer)
    return redirect(url_for('get_trainings', customer_id=customer.id))

@app.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    phoneNumber = request.form.get('phoneNumber')
    password = request.form.get('password')

    if not phoneNumber.isnumeric() or len(phoneNumber) != constants.PHONE_NUMBER_SIZE:
        flash('Wrong phone number', 'error')
        return redirect(url_for('signup_get'))

    if db.user_exists(email, phoneNumber):
        flash('User with this email or phone number already exists', 'notification')
        return redirect(url_for('signup_get'))

    db.insert('customer', {
        'email': email,
        'phoneNumber': phoneNumber,
        'password': password
    })
    return render_template('login.html')

@app.route('/customers/<int:customer_id>/trainings', methods=['GET'])
@login_required
def get_trainings(customer_id):
    trainings_data = db.get_all_trainings(customer_id)
    trainings = []
    for i in range(len(trainings_data)):
        training = Training(*trainings_data[i])
        trainings.append(training)
    print(trainings_data)
    return render_template('trainings.html', trainings=trainings)

@app.route('/customers/<int:customer_id>/trainings/<int:training_id>/exercises', methods=['GET'])
@login_required
def get_exercises(customer_id, training_id):
    return False

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

#В этом эндпоинте происходит следующее (в зависимости от query параметров):
#  1. Публикация прихода в зал клиента (начало тренировки) (POST)
#  2. Добавление силового упражнения тренажёром (POST)
#  3. Добавление бегового упражнения тренажёром (POST)
@app.route('/customers/<int:customer_id>/trainings', methods=['POST'])
def post_training(customer_id):
    queries = request.args.to_dict()
    if queries.get('addExercise'):
        exerciseType = queries['exerciseType']
        request_data = request.get_json()
        trainingId = db.get_last_training(customer_id)
        if exerciseType == 'running':
            return add_running_exercise(request_data, trainingId)
        if exerciseType == 'strength':
            return add_strength_exercise(request_data, trainingId)
    else:
        return customer_came(customer_id)

#Беговой тренажёр добавляет новую тренировку пользователя
def add_running_exercise(data, training_id):
    if db.insert('running_exercise', {
        'datetimeOfStart': data['datetimeOfStart'],
        'datetimeOfFinish': data['datetimeOfFinish'],
        'distance': data['distance'],
        'time': data['time'],
        'averageSpeed': data['averageSpeed'],
        'averagePulse': data['averagePulse'],
        'minPulse': data['minPulse'],
        'maxPulse': data['maxPulse'],
        'runningExerciseTypeId': data['runningExerciseTypeId'],
        'trainerId': data['trainerId'],
        'trainingId': training_id
    }):
        return "running exercise added successfully"
    else:
        return "running exercise cannot be added"

#Силовой тренажёр добавляет новую тренировку пользователя
def add_strength_exercise(data, training_id):
    strengthExerciseId = db.insert_strengthExercise({
        'datetimeOfStart': data['datetimeOfStart'],
        'datetimeOfFinish': data['datetimeOfFinish'],
        'strengthExerciseTypeId': data['strengthExerciseTypeId'],
        'trainerId': data['trainerId'],
        'trainingId': training_id
    })[0]
    if strengthExerciseId:
        flag = False
        for approach in data['approaches']:
            flag = flag & db.insert('approach', {
                'datetimeOfStart': approach['datetimeOfStart'],
                'datetimeOfFinish': approach['datetimeOfFinish'],
                'weight': approach['weight'],
                'repetition': approach['repetition'],
                'strengthExerciseId': strengthExerciseId
            })
        if flag:
            return "strength exercise added successfully"
        else: return "strength exercise cannot be added"
    else:
        return "strength exercise cannot be added"

#Турникет на входе фиксирует приход клиента
def customer_came(customer_id):
    request_data = request.get_json()
    datetime_of_start = request_data['datetimeOfStart']
    status = db.insert('training', {
        'datetimeOfStart': datetime_of_start,
        'customerId': customer_id
    })
    if status:
        return "training added successfully"
    else:
        return "training cannot be added"

#Клиент выходит из спортзала, тренировка окончена
@app.route('/customers/<int:customerId>/trainings', methods=['PATCH'])
def complete_training(customer_id):
    queries = request.args.to_dict()
    if queries.get('lastTraining'):
        request_data = request.get_json()
        datetime_of_finish = request_data['datetimeOfFinish']
        trainingId = db.get_last_training(customer_id)
        if db.complete_training(trainingId, datetime_of_finish):
            return "training completed successfully"
    return "training cannot be completed"

#весы добавили данные о взвешивании клиента
@app.route('/customers/<int:customerId>/weighings', methods=['POST'])
def add_weighing(customer_id):
    request_data = request.get_json()
    if db.insert('weighing', {
        'weight': request_data['weight'],
        'musclePercentage': request_data['musclePercentage'],
        'fatPercentage': request_data['fatPercentage'],
        'datetimeOfWeighing': request_data['datetimeOfWeighing'],
        'customerId': customer_id}):
        return "weighing added successfully"
    return "weighing cannot be added"
