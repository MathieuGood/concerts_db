from sqlalchemy import (
    Engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)

metadata_obj = MetaData()


def create_user_table(metadata_obj: MetaData = metadata_obj) -> Table:
    return Table(
        "user",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )


def create_address_table(metadata_obj: MetaData = metadata_obj) -> Table:
    return Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )


def run_table_queries(engine: Engine, metadata_obj: MetaData = metadata_obj):
    user_table = create_user_table(metadata_obj)
    address_table = create_address_table(metadata_obj)
    metadata_obj.create_all(engine)
