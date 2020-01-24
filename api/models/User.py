from api.models.base import db


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role {!r}>".format(self.name)


class User(db.Model):
    """User model for storing login credentials
    """

    __table_name__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User {!r}>".format(self.username)
