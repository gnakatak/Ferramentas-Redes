from flask import Blueprint, jsonify
from flask import Blueprint, jsonify, request
import backend.ferramentas.metrics.ping as ping_module
import backend.ferramentas.metrics.throughput as tp_module
import backend.ferramentas.firewall.modulo as fw


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/hello')
def hello():
    return jsonify({"message": "Olá do Flask!"})

@api_routes.route("/api/metrics/ping")
def ping_route():
    host = request.args.get("host", "8.8.8.8")
    count = int(request.args.get("count", "3"))
    result = ping_module.ping(host, count)
    return jsonify(result)

@api_routes.route("/api/metrics/throughput")
def throughput_route():
    result = tp_module.medir_throughput()
    return jsonify(result)
