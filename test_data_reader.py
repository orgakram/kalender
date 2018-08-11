#! python3

import codecs
import datetime
import logging
import json
import pickle
from Lib import ast
from Event import Event
from Conflicts import Conflict

with open('pickled_events.pck', 'rb') as fp:
    events = pickle.load(fp)


daily_map = Event.from_list_sorted_by_days(events)
for day in daily_map:
    print("Am: " + day.strftime("%A") + " " + str(day))
    event_list = daily_map[day]
    for event in event_list:
        print(str(event.start_time) + " bis " + str(event.end_time) + " " +  event.summary + " Ansprechpartner: " + event.contact)

    conflicts = Conflict.conflicts_of_the_day(event_list)
    if (len(conflicts) == 0):
        print("Es gibt keine Konflikte")
    else:
        print("Es gibt Konflikte:")
        for conflict in conflicts:
            print(conflict.message)
    print("********")





if (False):

    event_dict = {}

    for event in events:
        #start = datetime.datetime.fromisoformat(event['start']['dateTime'])
        stripped_time=str(event['start']['dateTime']).replace("+02:00", "")
        start = datetime.datetime.strptime(stripped_time, '%Y-%m-%dT%H:%M:%S')
        print(start.date().strftime("%A"))
        event_date = start.date()
        list_of_todays_events = event_dict.setdefault(event_date, [])
        list_of_todays_events.append(event)

    for day in event_dict:
        print("Am: " + day.strftime("%A") + " " + str(day))
        events = event_dict[day]
        for event in events:
            stripped_time2 = str(event['start']['dateTime']).replace("+02:00", "")
            start_time = datetime.datetime.strptime(stripped_time2, '%Y-%m-%dT%H:%M:%S')
            stripped_time3 = str(event['end']['dateTime']).replace("+02:00", "")
            end_time = datetime.datetime.strptime(stripped_time3, '%Y-%m-%dT%H:%M:%S')
            print(str(start_time.time()) + " bis " + str(end_time.time()) + " " +  event['summary'] + " Ansprechpartner: " + event['creator']['email'])
        print("********")