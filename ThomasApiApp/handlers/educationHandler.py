from flask import Blueprint, jsonify, request, abort
from ThomasApiApp.auth import requires_auth
from ThomasApiApp.dummy_data import data

education_bp = Blueprint('education', __name__)

@education_bp.route('/<string:name>/education', methods=['GET', 'POST'])
@requires_auth
def manage_education(name):
    if request.method == 'POST':
        new_data = request.get_json()

        if not new_data:
            abort(400, description="No data provided in request body.")

        if name not in data:
            data[name] = {}

        data[name]["education"] = new_data
        return jsonify({"message": "Information added successfully"}), 201

    elif request.method == 'GET':
        if name not in data:
            abort(404, description=f"User '{name}' not found.")

        if "education" not in data[name]:
            abort(404, description=f"Attribute 'education' not found for '{name}'.")

        return jsonify(data[name]["education"])
