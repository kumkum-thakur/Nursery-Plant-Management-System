from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kumkum124@localhost/plant_nursery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    availability = db.Column(db.Boolean, default=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin','viewer'), nullable=False, default='viewer')

# Define the root route ("/") and its handler function
@app.route('/')
def index():
    return render_template("Login.html")

@app.route('/cart.html')
def cart():
    return render_template("cart.html")

@app.route('/About.html')
def about():
    return render_template("About.html")

@app.route('/shop.html')
def shop():
    return render_template("shop.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")
@app.route('/first_page.html')
def index2():
    return render_template("first_page.html")

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    result = [{'id': plant.id, 'name': plant.name, 'description': plant.description, 'price': str(plant.price), 'availability': plant.availability} for plant in plants]
    return jsonify(result)

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'address': 'Plant not found'}), 404
    result = {'id': plant.id, 'name': plant.name, 'description': plant.description, 'price': str(plant.price), 'availability': plant.availability}
    return jsonify(result)

@app.route('/plants', methods=['POST'])
def add_plant():
    data = request.get_json()
    new_plant = Plant(name=data['name'], description=data.get('description'), price=data['price'], availability=data.get('availability', True))
    db.session.add(new_plant)
    db.session.commit()
    return jsonify({'address': 'Plant added successfully'}), 201

@app.route('/plants/<int:id>', methods=['PUT'])
def update_plant(id):
    data = request.get_json()
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'address': 'Plant not found'}), 404
    plant.name = data.get('name', plant.name)
    plant.description = data.get('description', plant.description)
    plant.price = data.get('price', plant.price)
    plant.availability = data.get('availability', plant.availability)
    db.session.commit()
    return jsonify({'address': 'Plant updated successfully'})

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'address': 'Plant not found'}), 404
    db.session.delete(plant)
    db.session.commit()
    return jsonify({'address': 'Plant deleted successfully'})

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, role=data.get('role', 'viewer'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'address': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'address': 'Invalid credentials'}), 401
    return jsonify({'address': 'Login successful', 'role': user.role})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
