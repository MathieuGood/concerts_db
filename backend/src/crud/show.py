from typing import List
from models.artist import Artist
from models.concert import Concert
from models.festival import Festival
from models.attendee import Attendee
from models.photo import Photo
from models.show import Show
from models.venue import Venue
from models.video import Video
from schemas.show import ShowCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload


def get(db: Session, show_id: int) -> Show:
    show = (
        db.query(Show)
        .options(
            joinedload(Show.venue).joinedload(Venue.address),
            joinedload(Show.attendees),
            joinedload(Show.festival),
            joinedload(Show.concerts).joinedload(Concert.artist),
            joinedload(Show.concerts).joinedload(Concert.photos),
            joinedload(Show.concerts).joinedload(Concert.videos),
        )
        .filter(Show.id == show_id)
        .first()
    )
    if not show:
        raise HTTPException(
            status_code=404, detail=f"Show with ID {show_id} not found."
        )
    return show


def get_all(db: Session) -> List[Show]:
    shows = (
        db.query(Show)
        .options(
            joinedload(Show.venue).joinedload(Venue.address),
            joinedload(Show.attendees),
            joinedload(Show.festival),
            joinedload(Show.concerts).joinedload(Concert.artist),
            joinedload(Show.concerts).joinedload(Concert.photos),
            joinedload(Show.concerts).joinedload(Concert.videos),
        )
        .all()
    )
    return shows


def create(db: Session, show: ShowCreate) -> Show:
    try:
        venue = db.query(Venue).filter(Venue.id == show.venue_id).first()
        if not venue:
            raise HTTPException(
                status_code=404, detail=f"Venue with ID {show.venue_id} not found."
            )

        festival = db.query(Festival).filter(Festival.id == show.festival_id).first()
        if show.festival_id and not festival:
            raise HTTPException(
                status_code=404,
                detail=f"Festival with ID {show.festival_id} not found.",
            )

        new_show = Show(
            name=show.name,
            event_date=show.event_date,
            comments=show.comments,
            venue_id=show.venue_id,
            festival_id=show.festival_id,
        )
        db.add(new_show)
        db.commit()
        db.refresh(new_show)

        for concert in show.concerts:
            artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
            if not artist:
                raise HTTPException(
                    status_code=404,
                    detail=f"Artist with ID {concert.artist_id} not found.",
                )
            new_concert = Concert(
                comments=concert.comments,
                setlist=concert.setlist,
                show_id=new_show.id,
                artist_id=concert.artist_id,
            )

            db.add(new_concert)
            db.commit()
            db.refresh(new_concert)

            for photo_url in concert.photos:
                new_photo = Photo(path=photo_url, concert_id=new_concert.id)
                db.add(new_photo)

            for video_url in concert.videos:
                new_video = Video(path=video_url, concert_id=new_concert.id)
                db.add(new_video)

        db.commit()
        db.refresh(new_show)

        if show.attendees_ids:
            attendees = (
                db.query(Attendee).filter(Attendee.id.in_(show.attendees_ids)).all()
            )
            new_show.attendees.extend(attendees)
            db.commit()
            db.refresh(new_show)

        # TODO : Find cleaner way to return attendees and concerts with Pydantic Response Model.
        for attendee in new_show.attendees:
            print(attendee)
        for concert in new_show.concerts:
            print(concert.artist)
            print(concert.photos)
            print(concert.videos)

        return new_show

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Show '{new_show.name}' already exists."
        )


def update(db: Session, show_id: int, show: ShowCreate) -> Show:
    try:
        updated_show: Show = db.query(Show).filter(Show.id == show_id).first()
        if updated_show is None:
            raise HTTPException(
                status_code=404, detail=f"Show with ID {show_id} not found."
            )

        updated_show.name = show.name
        updated_show.event_date = show.event_date
        updated_show.comments = show.comments
        updated_show.venue_id = show.venue_id
        updated_show.festival_id = show.festival_id
        updated_show.attendees_id = show.attendees_ids

        updated_show.attendees.clear()
        for attendee_id in show.attendees_ids:
            attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
            if not attendee:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attendee with ID {attendee_id} not found.",
                )
            updated_show.attendees.append(attendee)

        updated_show.concerts.clear()
        updated_concerts = []

        for concert in show.concerts:

            existing_concert = (
                db.query(Concert).filter(Concert.id == concert.id).first()
            )
            print(f"\033[38;5;208mCONCERT ID : {concert.id}\033[0m")
            print(
                f"\033[38;5;208mRESULT OF queried Concert in DB : {existing_concert}\033[0m"
            )

            if existing_concert:
                print("\033[93mCONCERT EXISTS : UPDATE\033[0m")
                existing_concert.show_id = updated_show.id
                existing_concert.comments = concert.comments
                existing_concert.setlist = concert.setlist
                existing_concert.artist_id = concert.artist_id
                existing_concert.artist = (
                    db.query(Artist).filter(Artist.id == concert.artist_id).first()
                )
                update_concert_photos(db, concert, existing_concert)
                update_concert_videos(db, concert, existing_concert)
                updated_concerts.append(existing_concert)
                print("\033[93mEXISTING CONCERT UPDATED\033[0m")
            else:
                print("\033[93mCONCERT DOES NOT EXIST : CREATION\033[0m")
                artist = db.query(Artist).filter(Artist.id == concert.artist_id).first()
                if not artist:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Artist with ID {concert.artist_id} not found.",
                    )
                new_concert = Concert(
                    comments=concert.comments,
                    setlist=concert.setlist,
                    show_id=updated_show.id,
                    artist_id=concert.artist_id,
                    artist=artist,
                )
                update_concert_photos(db, concert, new_concert)
                update_concert_videos(db, concert, new_concert)
                updated_concerts.append(new_concert)

        print(f"\033[93mCOMMITING CONCERTS : {updated_concerts}\033[0m")
        updated_show.concerts.extend(updated_concerts)
        db.commit()
        db.refresh(updated_show)
        return updated_show

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Show '{show.name}' already exists."
        )


def update_concert_photos(
    db: Session, concert_data: Concert, concert_to_update: Concert
):
    concert_to_update.photos.clear()
    if concert_data.photos_ids:
        for photo_id in concert_data.photos_ids:
            print(f"\033[93mPHOTO ID : {photo_id}\033[0m")
            photo = db.query(Photo).filter(Photo.id == photo_id).first()
            if not photo:
                raise HTTPException(
                    status_code=404,
                    detail=f"Photo with ID {photo_id} not found.",
                )
            concert_to_update.photos.append(photo)


def update_concert_videos(
    db: Session, concert_data: Concert, concert_to_update: Concert
):
    concert_to_update.videos.clear()
    if concert_data.videos_ids:
        for video_id in concert_data.videos_ids:
            print(f"\033[93mVIDEO ID : {video_id}\033[0m")
            video = db.query(Video).filter(Video.id == video_id).first()
            if not video:
                raise HTTPException(
                    status_code=404,
                    detail=f"Video with ID {video_id} not found.",
                )
            concert_to_update.videos.append(video)


def delete(db: Session, show_id: int) -> dict:
    deleted_show: Show = db.query(Show).filter(Show.id == show_id).first()
    if not deleted_show:
        return {"message": f"Show #{show_id} does not exist."}
    show_desc = (
        f"{deleted_show.name} at {deleted_show.venue.name} on {deleted_show.event_date}"
    )
    db.delete(deleted_show)
    db.commit()
    return {"message": f"Show #{show_id} '{show_desc}' deleted."}
