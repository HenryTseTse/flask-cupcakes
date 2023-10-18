"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"
app.app_context().push()

connect_db(app)


@app.route("/")
#@cross_origin()
def root():
    """Homepage"""
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return Cupcakes
    Respond in JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = [cupcake.seralize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add Cupcake
    Respond in JSON {cupcake: {id, flavor, size, rating, image}}."""

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

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """"Return Specific Cupcake
    Respond in JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.seralize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update Cupcake
    in JSON {cupcake: {id, flavor, size, rating, image}}"""

    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.seralize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Remove Cupcake
    Respond in JSON {message: "Deleted"}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")