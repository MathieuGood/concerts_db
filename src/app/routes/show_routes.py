from flask import render_template, request
from entities.Show import Show
from repositories.ShowRepository import ShowRepository

def register_routes(app, db):

    @app.route('/')
    def index():
        show_repository = ShowRepository(db.session)
        shows = show_repository.get_all()
        return str(shows)
