#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from datetime import datetime, timezone
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2:///fyyurdb'


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# MOVED TO MODELS.PY

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')



app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()
  artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
  recent = {'venues':venues,
            'artists':artists,
            }
  return render_template('pages/home.html', recent=recent)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  venue1 = Venue(
    name = "The Musical Hop",
    city = "San Francisco",
    state = "CA",
    address = "1015 Folsom Street",
    phone = "123-123-1234",
    image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    website = "https://www.themusicalhop.com",
    facebook_link = "https://www.facebook.com/TheMusicalHop",
    genre = ["JAZZ", "REGGAE", "SWING", "CLASSICAL", "FOLK"],
    seeking_talent = True,
    seeking_talent_desc = "We are on the lookout for a local artist to play every two weeks. Please call us. "
  )

  venue2 = Venue(
    name = "PARK SQUARE LIVE MUSIC & COFFEE",
    city = "San Francisco",
    state = "CA",
    address = "34 Whiskey Moore Ave",
    phone = "415-000-1234",
    image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    website = "https://www.parksquarelivemusicandcoffee.com",
    facebook_link = "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    genre = ["ROCK N ROLL", "JAZZ", "CLASSICAL", "FOLK"],
    seeking_talent = False
  )

  venue3 = Venue(
    name = "THE DUELING PIANOS BAR",
    city = "New York",
    state = "NY",
    address = "335 Delancey Street",
    phone = "914-003-1132",
    image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    website = "https://www.theduelingpianos.com",
    facebook_link = "https://www.facebook.com/theduelingpianos",
    genre = ["CLASSICAL", "R&B", "HIP-HOP"],
    seeking_talent = False
  )

  venues = Venue.query.all()
  locations = Venue.query.distinct(Venue.city).all()

  data = {'venues':venues,
          'locations':locations}

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  venue_search_string = request.form['search_term'].lower()
  venue_search_result = Venue.query.filter((Venue.name.ilike(f'%{venue_search_string}%')) |
                                           (Venue.city.ilike(f'%{venue_search_string}%'))).all()

  response={
    "count": len(venue_search_result),
    "data": venue_search_result
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data = Venue.query.filter_by(id=venue_id).first()

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  if 'seeking_talent' not in request.form:
    seeking_talent = False
  else:
    seeking_talent = True

  venue_to_create=Venue(
    name = request.form['name'],
    city = request.form['city'],
    state = request.form['state'],
    address = request.form['address'],
    phone = request.form['phone'],
    image_link = request.form['image_link'],
    website = request.form['website'],
    facebook_link = request.form['facebook_link'],
    genre = request.form.getlist('genre'),
    seeking_talent = seeking_talent,
    seeking_talent_desc = request.form['seeking_talent_desc']
  )

  try:
    db.session.add(venue_to_create)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  data = Venue.query.filter_by(name=venue_to_create.name).first()
  db.session.close()

  return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/<int:venue_id>/delete', methods=['GET', 'DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  venue_to_delete = Venue.query.filter_by(id=venue_id).first()

  try:
    db.session.delete(venue_to_delete)
    db.session.commit()
    flash('Venue ' + venue_to_delete.name + ' was successfully deleted!')

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue_to_delete.name + ' could not be deleted.')

  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  Artist_search_string = request.form['search_term'].lower()
  Artist_search_result = Artist.query.filter((Artist.name.ilike(f'%{Artist_search_string}%')) |
                                             (Artist.city.ilike(f'%{Artist_search_string}%'))).all()

  response={
    "count": len(Artist_search_result),
    "data": Artist_search_result
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist1=Artist(
    name = "GUNS N PETALS",
    city = "San Francisco",
    state = "CA",
    phone = "326-123-5000",
    image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    website = "https://www.gunsnpetalsband.com",
    facebook_link = "https://www.facebook.com/GunsNPetals",
    genre = ["ROCK N ROLL"],
    seeking_venue = True,
    seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!"
  )

  artist2=Artist(
    name = "Matt Quevedo",
    city = "New York",
    state = "NY",
    phone = "300-400-5000",
    image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    website = "No Website",
    facebook_link = "https://www.facebook.com/mattquevedo923251523",
    genre = ["ROCK N ROLL"],
    seeking_venue = False,
    seeking_description = ""
  )

  artist3=Artist(
    name = "THE WILD SAX BAND",
    city = "San Francisco",
    state = "CA",
    phone = "432-325-5432",
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    website = "No Website",
    facebook_link = "No Facebook Link",
    genre = ["JAZZ", "CLASSICAL"],
    seeking_venue = False,
    seeking_description = ""
  )

  data1={
    "id": 1,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }

  data = Artist.query.filter_by(id=artist_id).first()

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>

  artist = Artist.query.filter_by(id=artist_id).first()
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing

  if 'seeking_venue' not in request.form:
    seeking_venue = False
  else:
    seeking_venue = True

  artist_to_update = Artist.query.filter_by(id=artist_id).first()

  artist_to_update.name = request.form['name']
  artist_to_update.city = request.form['city']
  artist_to_update.state = request.form['state']
  artist_to_update.phone = request.form['phone']
  artist_to_update.image_link = request.form['image_link']
  artist_to_update.website = request.form['website_link']
  artist_to_update.facebook_link = request.form['facebook_link']
  artist_to_update.genre = request.form.getlist('genres')
  artist_to_update.seeking_venue = seeking_venue
  artist_to_update.seeking_description = request.form['seeking_description']

  try:
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>

  venue = Venue.query.filter_by(id=venue_id).first()
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  if 'seeking_talent' not in request.form:
    seeking_talent = False
  else:
    seeking_talent = True

  venue_to_update = Venue.query.filter_by(id=venue_id).first()

  venue_to_update.name = request.form['name']
  venue_to_update.city = request.form['city']
  venue_to_update.state = request.form['state']
  venue_to_update.address = request.form['address']
  venue_to_update.phone = request.form['phone']
  venue_to_update.image_link = request.form['image_link']
  venue_to_update.website = request.form['website']
  venue_to_update.facebook_link = request.form['facebook_link']
  venue_to_update.genre = request.form.getlist('genre')
  venue_to_update.seeking_talent = seeking_talent
  venue_to_update.seeking_talent_desc = request.form['seeking_description']

  print(request.form)

  try:
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  if 'seeking_venue' not in request.form:
    seeking_venue = False
  else:
    seeking_venue = True

  artist_to_create=Artist(
    name = request.form['name'],
    city = request.form['city'],
    state = request.form['state'],
    phone = request.form['phone'],
    image_link = request.form['image_link'],
    website = request.form['website_link'],
    facebook_link = request.form['facebook_link'],
    genre = request.form.getlist('genre'),
    seeking_venue = seeking_venue,
    seeking_description = request.form['seeking_description']
      )

  try:
    db.session.add(artist_to_create)
    db.session.commit()
  except:
    db.session.rollback()

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

  data = Artist.query.filter_by(name=artist_to_create.name).first()
  db.session.close()

  return render_template('pages/show_artist.html', artist=data)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  show1 = Show(
    start_time = "2019-05-21T21:30:00.000Z",
    artist_id = 1,
    venue_id = 1
    )

  show2 = Show(
    start_time = "2019-06-15T23:00:00.000Z",
    artist_id = 2,
    venue_id = 2
  )

  show3 = Show(
    start_time = "2035-04-01T20:00:00.000Z",
    artist_id = 3,
    venue_id = 2
  )

  show4 = Show(
    start_time = "2035-04-08T20:00:00.000Z",
    artist_id = 3,
    venue_id = 2
  )

  show5 = Show(
    start_time = "2035-04-15T20:00:00.000Z",
    artist_id = 3,
    venue_id = 2
  )

  data = Show.query.all()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  print(request.form)

  show_to_create = Show(
    start_time = request.form['start_time'],
    artist_id = request.form['artist_id'],
    venue_id = request.form['venue_id']
       )
  try:
    db.session.add(show_to_create)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

# on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
