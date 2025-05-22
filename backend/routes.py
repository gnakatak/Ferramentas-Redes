from flask import Blueprint, jsonify
import backend.ferramentas.firewall.modulo as fw

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/hello')
def hello_route():
    return fw.hello()

@api_routes.route('/api/goodbye')
def goodbye():
    return jsonify({"message": "Adeus do backend Flask!"})
