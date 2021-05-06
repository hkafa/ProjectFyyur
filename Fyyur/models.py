from app import db
from datetime import datetime

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    genre = db.Column(db.ARRAY(db.String(100)))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_talent_desc = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True))

    def __repr__(self):
        return f'<{self.id}-{self.name}-{self.city}>'

    @property
    def upcoming_shows(self):
        return Show.query.filter((datetime.now() < Show.start_time), (Show.venue_id == self.id)).all()

    @property
    def upcoming_shows_count(self):
        return len(Show.query.filter((datetime.now() < Show.start_time), (Show.venue_id == self.id)).all())

    @property
    def past_shows(self):
        return Show.query.filter((datetime.now() > Show.start_time), (Show.venue_id == self.id)).all()

    @property
    def past_shows_count(self):
        return len(Show.query.filter((datetime.now() > Show.start_time), (Show.venue_id == self.id)).all())

# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    genre = db.Column(db.ARRAY(db.String(100)))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<{self.id}-{self.name}>'

    @property
    def upcoming_shows(self):
        return Show.query.filter((datetime.now() < Show.start_time), (Show.artist_id == self.id)).all()

    @property
    def upcoming_shows_count(self):
        return len(Show.query.filter((datetime.now() < Show.start_time), (Show.artist_id == self.id)).all())

    @property
    def past_shows(self):
        return Show.query.filter((datetime.now() > Show.start_time), (Show.artist_id == self.id)).all()

    @property
    def past_shows_count(self):
        return len(Show.query.filter((datetime.now() > Show.start_time), (Show.artist_id == self.id)).all())

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)


# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.