#! python3
import logging
import sys
import calendar_retriever
import datetime
import codecs
import pickle
from Conflicts import Conflict
from Event import Event


logging.basicConfig(format = ' %(asctime)s -  %(levelname)s  -  %(message)s')
logger = logging.getLogger('ratzefummel')
logger.setLevel(logging.DEBUG)

def retrieve_data_from_calendar(calendarId, year, month):
    pickled_events_file_name = str(year) + "_" + str(month).rjust(2, '0') + "_pickled_events.pck"

    start_of_duration = datetime.datetime(year, month, 1)
    if month == 12:
        end_month = 1
        end_year = year + 1
    else:
        end_month = month + 1
        end_year = year

    end_of_duration = datetime.datetime(end_year, end_month, 1) - datetime.timedelta(seconds=1)

    events = calendar_retriever.retrieveEvents(calendarId, start_of_duration.isoformat() + 'Z',
                                               end_of_duration.isoformat() + 'Z')
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    with open(pickled_events_file_name, 'wb') as pickle_file:
        pickle.dump(events, pickle_file, protocol=0, fix_imports=True)

    return events

def print_summary(events):
    daily_map = Event.from_list_sorted_by_days(events)
    for day in daily_map:
        print("Am: " + day.strftime("%A") + " " + str(day))
        event_list = daily_map[day]
        for event in event_list:
            print(str(event.start_time) + " bis " + str(
                event.end_time) + " " + event.summary + " Ansprechpartner: " + event.contact)

        conflicts = Conflict.conflicts_of_the_day(event_list)
        if (len(conflicts) == 0):
            print("Es gibt keine Konflikte")
        else:
            print("Es gibt Konflikte:")
            for conflict in conflicts:
                print(conflict.message)
        print("********")


logger.debug("hello ktv")
google_calendarId = "jcodkhd706jr2efm9garroh5ks@group.calendar.google.com"
year = 2018
event_list = []
for monat in range(9, 13):
  events_of_the_month = retrieve_data_from_calendar(google_calendarId, year, monat)
  if (events_of_the_month is None):
      logging.debug("No events scheduled for {0}-{1}".format(year, monat))
  else:
      event_list = event_list + events_of_the_month

print_summary(event_list)