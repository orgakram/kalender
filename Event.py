#! python3

import codecs
import datetime
import logging
import json
import pickle

class Event:

    def __init__(self, data_map):
        if ('dateTime' in data_map['start']):
            raw_start_time = str(data_map['start']['dateTime']).replace("+02:00", "")
            raw_start_time = raw_start_time.replace("+01:00", "")

            raw_end_time = str(data_map['end']['dateTime']).replace("+02:00", "")
            raw_end_time = raw_end_time.replace("+01:00", "")

        else:
            raw_start_time = data_map['start']['date']+"T02:00:00"
            raw_end_time = data_map['start']['date']+"T20:00:00"

        self.start_time = datetime.datetime.strptime(raw_start_time, '%Y-%m-%dT%H:%M:%S')
        self.end_time = datetime.datetime.strptime(raw_end_time, '%Y-%m-%dT%H:%M:%S')

        self.summary =  data_map['summary']
        self.contact = data_map['creator']['email']
        self.day = self.start_time.date()

    def from_list_sorted_by_days(list_of_events):
         result={}
         for event_map in list_of_events:
             event = Event(event_map)
             list_of_todays_events = result.setdefault(event.day, [])
             list_of_todays_events.append(event)

         return result

