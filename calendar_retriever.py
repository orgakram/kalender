#! python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import logging
import datetime


logger = logging.getLogger('calendargoogle')
logger.setLevel(logging.DEBUG)


def retrieveEvents(calendar_id, timeMin, timeMax):
    #see https://developers.google.com/calendar/quickstart/python for the kickstart of this


    creds = getCredentials()
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    currentCalendar = service.calendars().get(calendarId=calendar_id).execute()
    logger.debug("connected to calendar " + currentCalendar["summary"])

    # Call the Calendar API
    logger.debug("""Getting maximum of 100 events in the time between {0} and {1}""".format(timeMin, timeMax))
    events_result = service.events().list(calendarId=calendar_id, timeMin=timeMin, timeMax=timeMax,
                                          maxResults=100, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def getCredentials():
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    return creds