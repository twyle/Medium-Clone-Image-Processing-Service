from ..extensions.extensions import db, ma
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User(db.Model):
    """A user."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.Text, nullable=False)
    date_registered = db.Column(db.DateTime(), default=datetime.utcnow)
    active: bool = db.Column(db.Boolean(), nullable=False, default=False)
    profile_pic: str = db.Column(db.String(100), nullable=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "email",
            "date_registered",
            "active",
            "profile_pic"
        )


user_schema = UserSchema()
