from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Налаштування секретного ключа для JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Замініть на свій секретний ключ
jwt = JWTManager(app)

# Простий словник для імітації бази даних
USERS = {
    "admin": "password",
    "user1": "12345"
}

# Login endpoint для генерації JWT токена
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in USERS and USERS[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# Logout endpoint
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"User {current_user} logged out successfully"}), 200

# Захищений endpoint
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200

# Примр публічного endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"msg": "Welcome to the Flask JWT Example API!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
