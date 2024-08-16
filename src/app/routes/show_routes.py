from flask import render_template, request
from entities.Show import Show
from repositories.ShowRepository import ShowRepository
from app.forms.ShowForm import ShowForm


def register_routes(app, db):

    show_repository = ShowRepository(db.session)

    @app.route("/")
    def all_shows():
        shows = show_repository.get_all()
        return render_template("list_shows.html", shows=shows)

    @app.route("/create_show")
    def create_show():
        form = ShowForm()
        return render_template("edit_show.html", title="Create a new show right now", form=form)
