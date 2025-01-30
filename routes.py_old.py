from flask import Flask, session, jsonify, request,render_template
from functools import wraps
from models import User, db  # Импортируйте ваши модели и экземпляр db

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Обязательно!

if __name__ == "__main__":
    app.run(debug=True)
# Маршрут для главной страницы
@app.route("/")
def index():
    return render_template("login.html")  # Или chat.html

# Маршрут для входа (POST)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Сохраняем ID пользователя в сессии
    session["user_id"] = user.id
    return jsonify({"message": "Logged in"})





# Декоратор
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# Публичный эндпоинт
@app.route("/login", methods=["POST"])
def login():
    # Проверка логина/пароля
    session["user_id"] = 123  # Пример
    return jsonify({"status": "success"})



# Выход
@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    return jsonify({"status": "logged_out"})
# регистрация
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)  # Хешируем пароль
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201
# Пример защищенного эндпоинта

@app.route("/api/data", methods=["post"])
def get_data():
    # Проверка авторизации
    #if "user_id" not in session:
    #   return jsonify({"error": "Unauthorized"}), 401
    # Логика получения данных
    return jsonify({"data": "test1"})

@app.route("/data", methods=["GET"])
def get_data():
    # Проверка авторизации
    #if "user_id" not in session:
    #   return jsonify({"error": "Unauthorized"}), 401
    # Логика получения данных
    return jsonify({"data": "test2"})