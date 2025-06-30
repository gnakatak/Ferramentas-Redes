from flask import Blueprint, jsonify, request
import backend.ferramentas.metrics.ping as ping_module
import backend.ferramentas.metrics.throughput as tp_module
import backend.ferramentas.firewall.modulo as fw

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/hello')
def hello_route():
    return fw.hello()

@api_routes.route('/api/goodbye')
def goodbye():
    return jsonify({"message": "Adeus do backend Flask!"})


@api_routes.route('/api/metrics/ping', methods=['GET'])
def ping_route():
    host = request.args.get('host', '8.8.8.8')
    count = int(request.args.get('count', 4))
    result = ping_module.ping(host, count)
    return jsonify(result)

@api_routes.route('/api/metrics/throughput', methods=['GET'])
def throughput_route():
    result = tp_module.measure_throughput()  # ou outro nome da função
    return jsonify(result)