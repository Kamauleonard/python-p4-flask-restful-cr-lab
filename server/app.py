from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Plant.query.all()]
        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        return response

    def post(self):
        data = request.get_json()
        new_record = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        response = make_response(
            jsonify(response_dict),
            201,
        )
        return response

api.add_resource(Plants, '/plants')  # Endpoint for listing and creating plants

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant is None:
            abort(404, message="Plant not found")
        
        response_dict = plant.to_dict()
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

api.add_resource(PlantByID, '/plants/<int:id>')  # Endpoint for retrieving a specific plant by ID

if __name__ == '__main__':
    app.run(port=5555, debug=True)
