from flask import render_template, request, flash
from entities.Show import Show
from repositories.ShowRepository import ShowRepository
from repositories.VenueRepository import VenueRepository
from repositories.ConcertRepository import ConcertRepository
from repositories.FestivalRepository import FestivalRepository
from app.forms.ShowForm import ShowForm


def register_routes(app, db):

    show_repository = ShowRepository(db.session)
    concert_repository = ConcertRepository(db.session)
    venue_repository = VenueRepository(db.session)
    festival_repository = FestivalRepository(db.session)

    @app.route("/")
    def all_shows():
        shows = show_repository.get_all()
        return render_template("list_shows.html", shows=shows)

    @app.route("/show/")
    def new_show():
        concerts = concert_repository.get_all()
        venue_choices = [
            f"{venue.name}, {venue.address.city}, {venue.address.country}"
            for venue in venue_repository.get_all()
        ]
        festival_choices = [festival.name for festival in festival_repository.get_all()]

        show_form = ShowForm(venues=venue_choices, festivals=festival_choices)
        new_show = Show()
        return render_template(
            "edit_show.html",
            title="Create a new show right now",
            show_form=show_form,
            show=Show(),
        )

    @app.route("/show/<int:show_id>")
    def edit_show(show_id):
        concerts = concert_repository.get_all()
        show = show_repository.get_by_id(show_id)
        venue_choices = [
            f"{venue.name}, {venue.address.city}, {venue.address.country}"
            for venue in venue_repository.get_all()
        ]
        festival_choices = [festival.name for festival in festival_repository.get_all()]

        show_form = ShowForm(venues=venue_choices, festivals=festival_choices)

        # Populating the form with the show data
        show_form.name.data = show.name
        show_form.event_date.data = show.event_date
        show_form.venue.data = f"{show.venue.name}, {show.venue.address.city}, {show.venue.address.country}"
        show_form.comments.data = show.comments

        return render_template(
            "edit_show.html",
            title="Create a new show right now",
            show=show,
            show_form=show_form,
        )

    @app.route("/show/<int:show_id>", methods=["POST"])
    def update_show(show_id):
        pass

    def render_show_template(form, title):
        return render_template(
            "edit_show.html",
            title=title,
            form=form,
            show=Show(),
        )
