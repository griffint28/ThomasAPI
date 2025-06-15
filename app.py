from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Data (using a dictionary for now, but consider a database for real-world apps)
data = {
    "thomas": {
        "experience": [],  # Initialize as empty list
        "education": [],
        "skills": []
    }
}


@app.route('/<string:name>/<string:attribute>', methods=['GET', 'POST'])
def get_info(name, attribute):
    if request.method == 'POST':
        # Get data from the request body
        new_data = request.get_json()

        if not new_data:
            abort(400, description="No data provided in request body.")

        if name not in data:
            data[name] = {}  # Create user's entry if it doesn't exist
        data[name][attribute] = new_data  # Store experience
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
