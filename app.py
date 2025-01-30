from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from sqlalchemy import text
from routes import *

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pos:Mypos21@192.168.0.131:5432/restservice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели (используем schema='mychat')
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'mychat'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

# Регистрация пользователя
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = bcrypt.hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201

# Вход в систему
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.verify(password, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is blocked"}), 403

    session['user_id'] = user.id
    session['is_admin'] = user.is_admin
    return jsonify({"message": "Logged in"}), 200

# Выход
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return jsonify({"message": "Logged out"}), 200

# Блокировка пользователя (только для админов)
@app.route('/api/block_user', methods=['POST'])
def block_user():
    if not session.get('is_admin'):
        return jsonify({"error": "Forbidden"}), 403

    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = False
    db.session.commit()
    return jsonify({"message": f"User {username} blocked"}), 200

# Сброс пароля (админ или сам пользователь)
@app.route('/api/reset_password', methods=['POST'])
def reset_password():
    username = request.json.get('username')
    new_password = request.json.get('new_password')
    current_user_id = session.get('user_id')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Проверка прав: админ или текущий пользователь
    if not (session.get('is_admin') or user.id == current_user_id):
        return jsonify({"error": "Forbidden"}), 403

    user.password_hash = bcrypt.hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password reset successful"}), 200

#if __name__ == '__main__':
#    with app.app_context():
#        db.create_all()  # Создает таблицы в схеме `mychat`
#    app.run(debug=True, port=5000)

# Пример защищенного эндпоинта

# Объявите ОДИН корректный маршрут для /api/data
@app.route("/api/data", methods=["GET", "POST"])  # Разрешить GET и POST
@login_required  # Добавьте декоратор, если требуется авторизация
def get_data():
    if request.method == "POST":
        return jsonify({"data": "POST request handled"})
    return jsonify({"data": "GET request handled"})