from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Olá do backend Flask!"})

if __name__ == '__main__':
    app.run(port=5000)
