from sqlalchemy import Engine, create_engine, MetaData, insert, text
from entities.Base import Base
from entities.User import User
from sqlalchemy.orm import Session

from mockup_data.characters import characters

def delete_all_users(session: Session):
    session.execute(text("DELETE FROM user_account"))
    session.commit()


def main():
    # engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    engine: Engine = create_engine(
        "sqlite+pysqlite:///database/concerts_db.sqlite", echo=True
    )
    metadata_obj = MetaData()
    session = Session(engine)

    # Base.metadata.create_all(engine)

    # delete_all_users(session)

    # for character in characters:
    #     session.add(character)
    # session.flush()
    # session.commit()


    # Edit the first record of the user_account table
    # first_user = session.query(User).first()
    # if first_user:
    #     first_user.fullname = "New Name"
    #     session.commit()

    # eric = session.get(User, 1)
    # print(eric.fullname)

    all_users = session.query(User).all()
    print(f"Type of all_users: {type(all_users)}")
    for user in all_users:
        print(user)
        print(f"Type of user: {type(user)}")


if __name__ == "__main__":
    main()
