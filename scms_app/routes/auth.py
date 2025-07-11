from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from scms_app.models import User
from scms_app import db 

auth_bp = Blueprint('auth', __name__)

# ✅ Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify(msg='Missing JSON data'), 400

    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify(msg='Missing fields'), 400

    hashed = generate_password_hash(password)
    user = User(username=username, password=hashed, role=role)

    db.session.add(user)
    db.session.commit()

    return jsonify(msg='User registered successfully')

# ✅ Combined login route (JSON or HTML form)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            token = create_access_token(identity={'id': user.id, 'role': user.role})
            if request.is_json:
                return jsonify(token=token)
            else:
                return f"✅ Logged in as {username} with role {user.role}"

        error_msg = "❌ Invalid credentials"
        if request.is_json:
            return jsonify(msg=error_msg), 401
        else:
            return error_msg, 401

    return render_template('login.html')
