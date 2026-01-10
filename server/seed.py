from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Hero, Power, HeroPower

fake = Faker()

with app.app_context():

    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()

    heroes = []
    for i in range(10):
        hero = Hero(name = fake.name(),super_name = fake.first_name())
        heroes.append(hero)

    db.session.add_all(heroes)

    powers = []
    for i in range(10):
        power = Power(name = fake.word(), description = fake.sentence())
        powers.append(power)

    db.session.add_all(powers)
    
    db.session.commit()

    hero_powers = []
    strengths = ['Strong', 'Weak', 'Average']
    for i in range(20):
        hero_power = HeroPower(
            strength = rc(strengths),
            hero_id = rc(heroes).id,
            power_id = rc(powers).id
        )
        hero_powers.append(hero_power)
    db.session.add_all(hero_powers)
    db.session.commit()


