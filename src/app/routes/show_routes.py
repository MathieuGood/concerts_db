from flask import render_template, request
from entities.Show import Show
from repositories.ShowRepository import ShowRepository


def register_routes(app, db):

    show_repository = ShowRepository(db.session)

    @app.route("/")
    def all_shows():
        shows = show_repository.get_all()
        return render_template("list_shows.html", shows=shows)
