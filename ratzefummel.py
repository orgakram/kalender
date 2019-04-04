#! python3

import calendar_retriever
import datetime
import logging
import codecs
import pickle

logging.basicConfig(format = ' %(asctime)s -  %(levelname)s  -  %(message)s')
logger = logging.getLogger('ratzefummel')
logger.setLevel(logging.DEBUG)

logger.debug("hello ktv")

now_time = datetime.datetime.utcnow()
sometimeJuly = now_time - datetime.timedelta(days=30)
now = sometimeJuly.isoformat() + 'Z' # 'Z' indicates UTC time

start_of_month = datetime.datetime(2018, 7, 1)
end_of_month = datetime.datetime(2018, 8,1) - datetime.timedelta(seconds=1)

#events = calendargoogle.retrieveEvents("jcodkhd706jr2efm9garroh5ks@group.calendar.google.com", now, None)
events = calendar_retriever.retrieveEvents("jcodkhd706jr2efm9garroh5ks@group.calendar.google.com", start_of_month.isoformat() + 'Z', end_of_month.isoformat() + 'Z')
if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])

with open('pickled_events.pck', 'wb') as pickle_file:
  pickle.dump(events, pickle_file, protocol=0, fix_imports=True)

print(events)

