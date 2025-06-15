from flask import Flask, jsonify, request, abort

app = Flask(__name__)

data = {
    "thomas": {
        "experience": [],
        "education": [],
        "skills": []
    }
}


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


if __name__ == '__main__':
    app.run(debug=True)
