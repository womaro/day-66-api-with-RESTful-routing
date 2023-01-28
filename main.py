from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import randint

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def list_cafes(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def get_random_cafe():
    with app.app_context():
        no_of_rows = db.session.query(Cafe).count()
        random_id = randint(1, no_of_rows + 1)
        random_cafe = db.session.query(Cafe).filter(Cafe.id == random_id).scalar()
        output = {"cafe": {
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
            "has_socket": random_cafe.has_sockets,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "id": random_cafe.id,
            "img_url": random_cafe.img_url,
            "location": random_cafe.location,
            "map_url": random_cafe.map_url,
            "name": random_cafe.name,
            "seats": random_cafe.seats
        }}
    return jsonify(output)


@app.route("/all", methods=["GET"])
def get_all_cafes():
    cafe_list = []
    with app.app_context():
        all_cafes = db.session.query(Cafe).all()
    for cafe in all_cafes:
        cafe_list.append(cafe.list_cafes())
    output = {"cafes": cafe_list}
    return jsonify(output)


@app.route("/search", methods=["GET"])
def get_caffe_by_loc():
    cafe_list = []
    area = request.args.get("loc")
    with app.app_context():
        area_caffe = db.session.query(Cafe).filter(Cafe.location == area).all()
    if len(area_caffe) == 0:
        output = {
            "error": {
                "Not Found": f"Sorry, we don´t have cafe at {area} location."
            }
        }
    else:
        for cafe in area_caffe:
            cafe_list.append(cafe.list_cafes())
        output = {"cafes": cafe_list}
    return jsonify(output)


@app.route("/add", methods=["GET"])
def add_cafe():
    name = request.args.get("name")
    map_url = request.args.get("map_url")
    img_url = request.args.get("img_url")
    location = request.args.get("location")
    seats = request.args.get("seats")
    has_toilet = request.args.get("has_toilet")
    has_wifi = request.args.get("has_wifi")
    has_sockets = request.args.get("has_sockets")
    can_take_calls = request.args.get("can_take_calls")
    coffee_price = request.args.get("coffee_price")

    new_cafe = Cafe(
        name=name,
        map_url=map_url,
        img_url=img_url,
        location=location,
        seats=seats,
        has_toilet=eval(has_toilet),
        has_wifi=eval(has_wifi),
        has_sockets=eval(has_sockets),
        can_take_calls=eval(can_take_calls),
        coffee_price=coffee_price
    )
    with app.app_context():
        db.session.add(new_cafe)
        db.session.commit()

    response = {
        "response": {
            "success": "Succesfully added the new cafe."
        }
    }
    return jsonify(response)


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
