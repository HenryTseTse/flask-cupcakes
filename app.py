"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"
app.app_context().push()

connect_db(app)

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return Cupcakes
    in JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = [cupcake.seralize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("api/cupcake", methods=["POST"])
def create_cupcake():
    """Add Cupcake
    in JSON {cupcake: {id, flavor, size, rating, image}}."""

    data = request.json

    cupcake = Cupcake(
        flavor = data['flavor'],
        size =  data['size'],
        rating = data['rating'],
        image = data['image'] or None,
    )

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.seralize()), 201)

@app.route("/api/cupcakes/<int:cupcake_id")
def get_cupcake(cupcake_id):
    """"Return Specific Cupcake
    in JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.seralize())