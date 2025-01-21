#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
# db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
with app.app_context():
    # Add initial data only if the table is empty
    if Venue.query.count() == 0:
      venue1 = Venue(
          name= "The Musical Hop",
          genres= ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
          address= "1015 Folsom Street",
          city= "San Francisco",
          state= "CA",
          phone= "123-123-1234",
          website= "https://www.themusicalhop.com",
          facebook_link= "https://www.facebook.com/TheMusicalHop",
          seeking_talent= True,
          seeking_description= "We are on the lookout for a local artist to play every two weeks. Please call us.",
          image_link= "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        )
      # Venue 2
      venue2 = Venue(
          name="The Dueling Pianos Bar",
          genres=["Classical", "R&B", "Hip-Hop"],
          address="335 Delancey Street",
          city="New York",
          state="NY",
          phone="914-003-1132",
          website="https://www.theduelingpianos.com",
          facebook_link="https://www.facebook.com/theduelingpianos",
          seeking_talent=False,
          image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
      )

      # Venue 3
      venue3 = Venue(
          name="Park Square Live Music & Coffee",
          genres=["Rock n Roll", "Jazz", "Classical", "Folk"],
          address="34 Whiskey Moore Ave",
          city="San Francisco",
          state="CA",
          phone="415-000-1234",
          website="https://www.parksquarelivemusicandcoffee.com",
          facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
          seeking_talent=False,
          image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
      )

      # Add the venues to the session
      db.session.add_all([venue1, venue2, venue3])
      db.session.commit()
    if Artist.query.count() == 0:
      artist1 = Artist(
        name="Guns N Petals",
        genres=["Rock n Roll"],  # Ensure the column supports array types if using Postgres.
        city="San Francisco",
        state="CA",
        phone="326-123-5000",
        website="https://www.gunsnpetalsband.com",
        facebook_link="https://www.facebook.com/GunsNPetals",
        seeking_venue=True,
        seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
        image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        )

      artist2 = Artist(
        name="Matt Quevedo",
        genres=["Jazz"],  # Ensure your database supports array/list types for genres if needed.
        city="New York",
        state="NY",
        phone="300-400-5000",
        facebook_link="https://www.facebook.com/mattquevedo923251523",
        seeking_venue=False,
        image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
        )
      artist3 = Artist(
        name="The Wild Sax Band",
        genres=["Jazz", "Classical"],  # Make sure your database supports array types if needed
        city="San Francisco",
        state="CA",
        phone="432-325-5432",
        seeking_venue=False,
        image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
        )
      db.session.add_all([artist1, artist2, artist3])
      db.session.commit()
    if Show.query.count() == 0:
        show1=Show(
          venue_id= 1,
          artist_id= 2,
          start_time=datetime.strptime( "2025-05-21T21:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        show2=Show(
          venue_id= 1,
          artist_id= 1,
          start_time=datetime.strptime( "2025-06-15T23:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        show3=Show(
          venue_id= 2,
          artist_id= 3,
          start_time=datetime.strptime( "2035-04-01T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        show4=Show(
          venue_id= 2,
          artist_id= 2,
          start_time=datetime.strptime("2035-04-01T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        db.session.add_all([show1, show2, show3,show4])
        db.session.commit()

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
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # Query all venues, grouped by city and state
    venues_query = Venue.query.all()

    # Group venues by city and state
    city_state_mapping = {}
    for venue in venues_query:
        city_state = (venue.city, venue.state)
        if city_state not in city_state_mapping:
            city_state_mapping[city_state] = []
        city_state_mapping[city_state].append({
            "id": venue.id,
            "name": venue.name,
            # Calculate the number of upcoming shows
            "num_upcoming_shows": Show.query.filter(
                Show.venue_id == venue.id,
                Show.start_time >= datetime.now()
            ).count()
        })

    # Convert to the desired structure
    data = [
        {
            "city": city,
            "state": state,
            "venues": venues
        }
        for (city, state), venues in city_state_mapping.items()
    ]

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # Get the search term from the form
    search_term = request.form.get('search_term', '')

    # Perform a case-insensitive search for venues whose name contains the search term
    search_results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

    # Prepare the response data
    response = {
        "count": len(search_results),
        "data": []
    }

    for venue in search_results:
        num_upcoming_shows = Show.query.filter(
            Show.venue_id == venue.id,
            Show.start_time >= datetime.now()
        ).count()

        response["data"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })

    # Render the search results
    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # Query the venue by ID
    venue = Venue.query.get_or_404(venue_id)

    # Get the current time
    now = datetime.now()

    # Query past and upcoming shows for the venue using JOIN
    past_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id,
        Show.start_time < now
    ).all()

    upcoming_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id,
        Show.start_time >= now
    ).all()

    # Prepare past shows data
    past_shows = []
    for show in past_shows_query:
        past_shows.append({
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })

    # Prepare upcoming shows data
    upcoming_shows = []
    for show in upcoming_shows_query:
        upcoming_shows.append({
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })

    # Prepare the venue data
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,  # Assuming genres is a list in the database
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    # Render the venue page
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    if form.validate():
        try:
            # Create a new Venue instance
            new_venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=form.genres.data,  # Assuming genres is a list
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                website=form.website_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data
            )

            # Add the new venue to the database
            db.session.add(new_venue)
            db.session.commit()

            # Flash success message
            flash(f'Venue {new_venue.name} was successfully listed!')
        except Exception as e:
            # Rollback the session in case of an error
            db.session.rollback()
            flash(f'An error occurred. Venue {form.name.data} could not be listed. Error: {str(e)}')
        finally:
            db.session.close()
    else:
        # Handle validation errors
        flash('An error occurred. Please check the form for errors.')

    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        # Query the venue by id
        venue = Venue.query.get(venue_id)
        
        if not venue:
            # Handle case where the venue does not exist
            flash(f'Venue with id {venue_id} does not exist.')
            return jsonify({'success': False}), 404
        
        # Delete the venue
        db.session.delete(venue)
        db.session.commit()
        
        # Flash success message
        flash(f'Venue {venue.name} was successfully deleted!')
        return jsonify({'success': True}), 200
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        flash(f'An error occurred while trying to delete the venue. Error: {str(e)}')
        return jsonify({'success': False}), 500
    finally:
        db.session.close()
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    try:
        # Query all artists from the database
        artists = Artist.query.all()

        # Transform the query results into the desired format
        data = [{"id": artist.id, "name": artist.name} for artist in artists]

        return render_template('pages/artists.html', artists=data)
    except Exception as e:
        flash(f"An error occurred while fetching artists: {str(e)}")
        return render_template('pages/artists.html', artists=[])

@app.route('/artists/search', methods=['POST'])
def search_artists():
    try:
        # Get the search term from the form
        search_term = request.form.get('search_term', '').strip()

        # Query the database for artists matching the search term
        # Use ilike for case-insensitive partial matching
        artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()

        # Prepare the response data
        response = {
            "count": len(artists),
            "data": [
                {
                    "id": artist.id,
                    "name": artist.name,
                    "num_upcoming_shows": len(
                        [
                            show
                            for show in artist.shows
                            if show.start_time > datetime.now()
                        ]
                    ),
                }
                for artist in artists
            ],
        }

        # Render the search results
        return render_template(
            "pages/search_artists.html", results=response, search_term=search_term
        )
    except Exception as e:
        flash(f"An error occurred during the search: {str(e)}")
        return render_template(
            "pages/search_artists.html", results={"count": 0, "data": []}, search_term=""
        )

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:
        # Fetch the artist using the provided artist_id
        artist = Artist.query.get(artist_id)

        if not artist:
            flash(f"Artist with ID {artist_id} does not exist.")
            return render_template('errors/404.html'), 404

        # Prepare the data structure for rendering
        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,  # Now genres is a list of strings
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": [],
            "upcoming_shows": [],
        }

        # Separate past shows using JOIN
        past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
        past_shows = []
        for show in past_shows_query:
            past_shows.append({
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            })
        data["past_shows"] = past_shows

        # Separate upcoming shows using JOIN
        upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
        upcoming_shows = []
        for show in upcoming_shows_query:
            upcoming_shows.append({
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            })
        data["upcoming_shows"] = upcoming_shows

        # Add counts
        data["past_shows_count"] = len(data["past_shows"])
        data["upcoming_shows_count"] = len(data["upcoming_shows"])

        return render_template('pages/show_artist.html', artist=data)

    except Exception as e:
        flash(f"An error occurred while fetching artist data: {str(e)}")
        return render_template('errors/500.html'), 500


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        # Fetch the artist record from the database
        artist = Artist.query.get(artist_id)

        if not artist:
            flash(f"Artist with ID {artist_id} does not exist.")
            return redirect(url_for('artists'))

        # Update artist attributes from form data
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.getlist('genres')  # Assuming genres is a list
        artist.facebook_link = request.form.get('facebook_link')
        artist.website = request.form.get('website_link')
        artist.seeking_venue = request.form.get('seeking_venue') == 'y'
        artist.seeking_description = request.form.get('seeking_description')
        artist.image_link = request.form.get('image_link')

        # Commit changes to the database
        db.session.commit()

        flash(f"Artist {artist.name} was successfully updated!")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred. Artist could not be updated: {str(e)}")
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    # Fetch venue data from the database
    venue = Venue.query.get(venue_id)
    if not venue:
        flash(f"Venue with ID {venue_id} does not exist.")
        return redirect(url_for('index'))

    # Pre-fill the form fields with the venue data
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.website_link.data = venue.website_link
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link

    # Pass the venue data for rendering
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # Retrieve the venue from the database
    venue = Venue.query.get(venue_id)
    
    # If the venue does not exist, flash an error message
    if not venue:
        flash(f"Venue with ID {venue_id} does not exist.")
        return redirect(url_for('venues'))

    # Update the venue record with the form data
    venue.name = request.form['name']
    venue.genres = request.form.getlist('genres')  # Assuming genres is a multi-select field
    venue.address = request.form['address']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.website_link = request.form['website_link']
    venue.facebook_link = request.form['facebook_link']
    venue.seeking_talent = 'seeking_talent' in request.form  # Checkbox or boolean field
    venue.seeking_description = request.form['seeking_description']
    venue.image_link = request.form['image_link']

    # Commit the changes to the database
    try:
        db.session.commit()
        flash(f"Venue '{venue.name}' was successfully updated!")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred. Venue '{venue.name}' could not be updated. Error: {str(e)}")

    # Redirect to the venue's page after successful update
    return redirect(url_for('show_venue', venue_id=venue.id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)  # Use Flask-WTF form class
    
    if form.validate():  # Validate the form
        try:
            # Create a new artist object using the data from the validated form
            artist = Artist(
                name=form.name.data,
                genres=form.genres.data,  # Assuming genres is handled as a list
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                website=form.website_link.data,
                facebook_link=form.facebook_link.data,
                seeking_venue=form.seeking_venue.data,  # Checkbox or boolean field
                seeking_description=form.seeking_description.data,
                image_link=form.image_link.data
            )
            
            db.session.add(artist)
            db.session.commit()
            flash(f'Artist {artist.name} was successfully listed!')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred. Artist {artist.name} could not be listed. Error: {str(e)}')
        finally:
            db.session.close()
    else:
        flash('An error occurred. Please check the form for errors and try again.')

    # Redirect the user to the homepage (or another appropriate page)
    return redirect(url_for('index'))  # Assuming 'index' is the homepage route

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # Query the database for shows with their respective venues and artists
    shows_data = db.session.query(Show, Venue, Artist).join(Venue).join(Artist).all()

    # Prepare data for rendering in the template
    data = [{
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,  # Assuming you have image_link in the Artist model
        "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    } for show, venue, artist in shows_data]

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)  # Use Flask-WTF form class
    if form.validate():  # Validate the form data
        try:
            # Create a new Show object using validated form data
            new_show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data
            )

            # Add and commit the new show to the database
            db.session.add(new_show)
            db.session.commit()

            # Flash success message
            flash('Show was successfully listed!')
        except Exception as e:
            # Rollback and flash an error message in case of any exception
            db.session.rollback()
            flash(f'An error occurred. Show could not be listed. Error: {str(e)}')
    else:
        # If form validation fails, flash an error message
        flash('An error occurred. Please check your input and try again.')

    # Redirect to the appropriate page after submission
    return redirect(url_for('index'))  # Adjust 'index' to your desired redirect route


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
