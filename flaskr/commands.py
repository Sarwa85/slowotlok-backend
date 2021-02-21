import click
from flask import Blueprint
from flask.cli import with_appcontext

commands_bp = Blueprint('commands', __name__)


@with_appcontext
@click.command('init-model')
def init_model():
    """Clear the existing data and create new tables."""
    # db.create_all()
    click.echo('Initialized the database.')