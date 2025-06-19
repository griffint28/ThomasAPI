from functools import wraps
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

#TODO:Replace Auth with JWT
users = {
    "user1": "password123"
}

data = {
    "thomas": {
        "experience": [],
        "education": [],
        "skills": []
    }
}

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST':
            auth = request.authorization
            if not auth or not authenticate(auth.username, auth.password):
                abort(401)
        return f(*args, **kwargs)

    return decorated

def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    return False

def validate_experience(experience_data):
    if not isinstance(experience_data, list):
        return False

    for entry in experience_data:
        if not isinstance(entry, dict):
            return False

        required_keys = ["title", "company", "years"]
        if not all(key in entry for key in required_keys):
            return False

        if not isinstance(entry["title"], str) or not isinstance(entry["company"], str) or not isinstance(
                entry["years"], str):
            return False
    return True


@app.route('/<string:name>/<string:attribute>', methods=['GET', 'POST'])
@requires_auth
def get_info(name, attribute):
    if request.method == 'POST':

        new_data = request.get_json()

        if not new_data:
            abort(400, description="No data provided in request body.")

        if attribute == "experience":
            if not validate_experience(new_data):
                abort(400, description="Invalid experience data format.")

        if name not in data:
            data[name] = {}
        data[name][attribute] = new_data
        return jsonify({"message": "Information added successfully"}), 201

    elif request.method == 'GET':

        if not name in data:
            abort(404, description=f"User '{name}' not found.")

        if not attribute in data[name]:
            abort(404, description=f"Attribute '{attribute}' not found for '{name}'.")

        return jsonify(data[name][attribute])


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify(error=str(error)), 401

if __name__ == '__main__':
    app.run(debug=True)
