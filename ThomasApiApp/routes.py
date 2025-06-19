from flask import Blueprint, jsonify, request, abort
from ThomasApiApp.auth import requires_auth
from ThomasApiApp.utils import validate_experience

bp = Blueprint('main', __name__)  # Use blueprint

data = {  # You might move this to a separate data module later
    "thomas": {
        "experience": [],
        "education": [],
        "skills": []
    }
}


@bp.route('/<string:name>/<string:attribute>', methods=['GET', 'POST'])  # apply blueprint
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

