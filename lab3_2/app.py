from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def repr(self):
        return f'<User {self.name}>'

@app.before_request
def create_tables():
    db.create_all()
    add_test_data()

def add_test_data():
    # Проверим, если в таблице нет пользователей, добавим тестовых
    if User.query.count() == 0:
        test_users = [
            User(name='Alice', email='alice@example.com'),
            User(name='Bob', email='bob@example.com'),
            User(name='Charlie', email='charlie@example.com')
        ]
        db.session.add_all(test_users)
        db.session.commit()
        print("Test data added to the database.")

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

if __name__ == '__main__':
    app.run(debug=True)