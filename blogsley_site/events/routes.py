from flask import render_template, request, current_app, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from flask_babel import _
from blogsley_site.events import bp
from blogsley_site.events.utils import get_events

@bp.route('/')
def index():
    return render_template('events.html', events=get_events())

@bp.route('/calendar')
def calendar():
    return render_template('calendar.html')

@bp.route('/api/events')
def api_events():
    data = [
      {
        "title": "EMPUG Monthly",
        "url": "https://www.meetup.com/empugdotorg/",
        'rrule': {
          'freq': 'monthly',
          'byweekday': [ 'sa' ],
          'bysetpos': [3],
          'dtstart': '2019-04-20T13:00:00',
        },

        # for specifying the end time of each instance
        'duration': '03:00'
      },
      {
        "title": "Christmas",
        "className": "fc-holiday",
        "start": "2019-12-25"
      },
      {
        "title": "Spring",
        "className": "fc-holiday",
        "start": "2019-03-20"
      },
      {
        "title": "Summer",
        "className": "fc-holiday",
        "start": "2019-06-21"
      },
      {
        "title": "Independence Day",
        "className": "fc-holiday",
        "start": "2019-07-04"
      }
    ]

    return jsonify(data)
