from flask import Blueprint, jsonify, request, abort
from ThomasApiApp.auth import requires_auth
from ThomasApiApp.dummy_data import data

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/<string:name>/skills', methods=['GET', 'POST'])
@requires_auth
def manage_skills(name):
    if request.method == 'POST':
        new_data = request.get_json()

        if not new_data:
            abort(400, description="No data provided in request body.")

        if name not in data:
            data[name] = {}
        data[name]["skills"] = new_data
        return jsonify({"message": "Information added successfully"}), 201

    elif request.method == 'GET':

        if name not in data:
            abort(404, description=f"User '{name}' not found.")

        if "skills" not in data[name]:
            abort(404, description=f"Attribute 'skills' not found for '{name}'.")

        return jsonify(data[name]["skills"])
