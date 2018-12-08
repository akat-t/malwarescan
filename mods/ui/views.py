"""Main views.py file for current application module."""
from flask import Blueprint, render_template, jsonify
from jinja2.exceptions import TemplateNotFound
from libs.decorators import cert_required

# Init Swagger UI Blueprint
mod_ui = Blueprint(
    'mod_ui',
    __name__,
    template_folder='templates',
    url_prefix='/ui',
)


@mod_ui.route('/')
@cert_required
def index():
    try:
        return render_template('ui/index.html')
    except TemplateNotFound:
        return jsonify({"status": "ERROR"}), 404


blueprints = [mod_ui]
