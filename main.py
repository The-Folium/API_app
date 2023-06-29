from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# опис елементу БД (ORM)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


# створення початкової БД
with app.app_context():
    db.create_all()

# імплементація API
# отримати список користувачів
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'name': user.name, 'email': user.email} for user in users]
    return jsonify(result), 200

# додати користувача
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# видалити користувача
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    name = request.json['name']
    user = User.query.filter_by(name=name).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 204
    else:
        return jsonify({'message': 'User not found'}), 404

# додати колонку до таблиці (міграція)
@app.route('/add_field', methods=['POST'])
def add_field():
    field_name = request.json['field_name']
    field_type = request.json['field_type']
    db.session.execute(text(f'ALTER TABLE user ADD COLUMN "{field_name}" {field_type}'))
    db.session.commit()
    return jsonify({'message': 'Field added successfully'}), 200

# створити тестове наповнення БД
@app.route('/create_test_db', methods=['POST'])
def create_test_db():
    test_users = [
        {'name': 'John Doe', 'email': 'john@example.com'},
        {'name': 'Jane Smith', 'email': 'jane@example.com'},
        {'name': 'David Johnson', 'email': 'david@example.com'},
        {'name': 'Michael Brown', 'email': 'michael@example.com'},
        {'name': 'Emily Davis', 'email': 'emily@example.com'},
        {'name': 'Daniel Wilson', 'email': 'daniel@example.com'},
        {'name': 'Sophia Anderson', 'email': 'sophia@example.com'},
        {'name': 'Oliver Martinez', 'email': 'oliver@example.com'},
        {'name': 'Ava Thomas', 'email': 'ava@example.com'},
        {'name': 'William Clark', 'email': 'william@example.com'},
    ]

    for user_data in test_users:
        new_user = User(name=user_data['name'], email=user_data['email'])
        db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Test database created successfully'}), 200


if __name__ == '__main__':
    app.run()