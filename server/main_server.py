from flask import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from database import db_session
from database.tables import *


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def hello():
    return "Hello World!"


def convert_to_json(inf_type, queue):
    inf = {}
    session = db_session.create_session()
    if inf_type == 'user':
        for elem in queue:
            s = {'id': elem.id,
                 'name': elem.name,
                 'surname': elem.surname,
                 'patronymic': elem.patronymic,
                 'is_admin': elem.is_admin}
            s = json.dumps(s)
            inf = {elem.id: s}
    else:
        for elem in queue:
            s = {'id': elem.id,
                 'task_type': elem.task_type,
                 'user_id': elem.user_id,
                 'is_finished': elem.is_finished,
                 'inf': elem.inf}
            s = json.dumps(s)
            inf = {elem.id: s}
    return json.dumps(inf)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        login = request.values.get('login')
        password = request.values.get('password')
        try:
            session = db_session.create_session()
            user = session.query(User).filter(User.email == login).first()
            # user.check_password(password) #когда добавится регистрация с хешированием пароля
            user_inf = {'id': user.id,
                        'name': user.name,
                        'surname': user.surname,
                        'patronymic': user.patronymic,
                        'is_admin': user.is_admin
                        }
            if password == user.password:
                response = {'status': 'success',
                            'user': json.dumps(user_inf)}
            else:
                print(1)
                response = {'status': 'password fail',
                            'user': None}
            return jsonify(response)
        except:
            response = {'status': 'login fail',
                        'user': None}
            return jsonify(response)


@app.route('/task_interacting_with_db',  methods=['GET', 'POST'])
def task_interacting_with_db():
    if request.method == 'POST':
        try:
            session = db_session.create_session()
            task = Task(
                task_type=request.values.get('task_type'),
                user_id=request.values.get('user'),
                is_finished=False,
                inf=request.values.get('inf')
            )
            session.add(task)
            session.commit()
            session.close()
            return 'success'
        except Exception:
            return 'error'
    if request.method == 'GET':
        pass


if __name__ == "__main__":
    db_session.global_init()
    app.run(host='localhost', port=4567)
