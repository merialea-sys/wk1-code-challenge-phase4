from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Hero Power API</h1>'

@app.route('/heroes')
def get_heroes():
    heroes = []
    for hero in Hero.query.all():
        heroes_dict = hero.to_dict()
        heroes.append(heroes_dict)
    response = make_response(heroes, 200)
    return response

@app.route('/heroes/<int:id>')
def get_hero_by_id(id):
    hero = Hero.query.filter_by(id=id).first()
    if hero:
        response = make_response(hero.to_dict(), 200)
    else:
        response = make_response({"error": "Hero not found"}, 404)
    return response

@app.route('/powers')
def get_powers():
    powers = []
    for power in Power.query.all():
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name
        }
        powers.append(power_dict)
    response = make_response(powers, 200)
    return response

@app.route('/powers/<int:id>')
def get_power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    power_dict = {
        "description": power.description,
        "id": power.id,
        "name": power.name
    }
    if power:
        response = make_response(power_dict, 200)
    else:
        response = make_response({"error": "Power not found"}, 404)
    return response

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return make_response({"error": "Power not found"}, 404)

    data = request.get_json()
    if "description" not in data:
        return make_response({"error": "Description is required"}, 400)

    power.description = data["description"]
    db.session.commit()

    response = make_response({
        "description": power.description,
        "id": power.id,
        "name": power.name
    }, 200)
    return response

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        new_hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(new_hero_power)
        db.session.commit()

        response = make_response(new_hero_power.to_dict(), 201)
    except Exception as e:
        response = make_response({"error": ["validation errors"]}, 400)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)