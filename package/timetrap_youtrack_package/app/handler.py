import datetime
import sys

from python3_youtrack_api.client import Connection
from sqlalchemy import and_

from .application import app
from .models import Entry


def get_epochtime_ms(time):
    return round(int(time.strftime("%s")) * 1000)


def get_timings():
    if app.args.since:
        if app.args.till:
            end = datetime.datetime.strptime(app.args.till, "%Y-%m-%d").date()
        else:
            end = datetime.datetime.date(datetime.datetime.today())
        start = datetime.datetime.strptime(app.args.since, "%Y-%m-%d").date()
    elif app.args.days:
        delta = datetime.timedelta(days=app.args.days)
        today = datetime.datetime.date(datetime.datetime.today())
        start = today - delta
        end = today
    elif app.args.previous_day:
        delta = datetime.timedelta(days=1)
        today = datetime.datetime.date(datetime.datetime.today())
        start = today - delta
        end = today
    else:
        sys.stderr.write("Too few args, add one of 'since', 'days', 'previous_day'")
        sys.exit(0)

    return start, end


def get_queryset(start, end):
    filters = [
        Entry.start > start,
        Entry.end < end
    ]

    sheet = app.configuration.get('time_sheet')
    if sheet:
        filters.append(Entry.sheet == sheet)

    entries = app.db_part.session.query(Entry).filter(and_(*filters)).all()
    return entries


def _check_mapping(mappings, note):
    for m in mappings:
        if m in note:
            return True
    return False


def handle():
    start, end = get_timings()
    entries = get_queryset(start, end)
    url = app.configuration.get('track_auth', {}).get('url')
    login = app.configuration.get('track_auth', {}).get('login')
    passwd = app.configuration.get('track_auth', {}).get('password')
    yt = Connection(url, auth=(login, passwd))

    time = 0
    mappings = app.configuration.get('tasks_name_masks', [])
    names = []
    for i in entries:
        try:

            if _check_mapping(mappings, i.note):
                names.append(i.note)
                sys.stdout.write(i.note)

                minutes = (i.end - i.start).seconds / 60
                time = time + minutes

                yt.add_time_entry(i.note, get_epochtime_ms(i.start.date()), minutes)
            else:
                sys.stderr.write('==== Error ====')
                sys.stderr.write('Entry doesn\'t compares with mappings you provided!')
                sys.stderr.write('mappings', mappings)
                sys.stderr.write(i.id)
                sys.stderr.write(i.note)
                sys.stderr.write(i.start)
                sys.stderr.write(i.end)

        except Exception as e:
            print(e)

    if app.args.verbose:
        print('minutes', time)
        print('hours', time / 60)

        print('names', names)
        print('handling.....')
