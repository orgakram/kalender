#! python3

import codecs
import datetime
import logging
import json
import pickle

class Event:

    def __init__(self, data_map):
        #still missing the fix for winter time (+01:00)
        stripped_time2 = str(data_map['start']['dateTime']).replace("+02:00", "")
        self.start_time = datetime.datetime.strptime(stripped_time2, '%Y-%m-%dT%H:%M:%S')
        stripped_time3 = str(data_map['end']['dateTime']).replace("+02:00", "")
        self.end_time = datetime.datetime.strptime(stripped_time3, '%Y-%m-%dT%H:%M:%S')
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

