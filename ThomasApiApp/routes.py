from flask import Blueprint
from ThomasApiApp.handlers.experienceHandler import experience_bp
from ThomasApiApp.handlers.educationHandler import education_bp
from ThomasApiApp.handlers.skillsHandler import skills_bp

bp = Blueprint('main', __name__)

# Register blueprints with URL prefixes
bp.register_blueprint(experience_bp)
bp.register_blueprint(education_bp)
bp.register_blueprint(skills_bp)
