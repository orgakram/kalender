#! python3

import datetime

class Conflict:

    BUFFER_BETWEEN_EVENTS = 3

    def __init__(self, msg):
        self.message = msg

    def check_for_conflict(event, other_event):
        #check if other events start already during my time or too early after my event finished
        other_start = other_event.start_time
        if (other_start > event.start_time) and (other_start < event.end_time):
            return Conflict("Der Termin '" + other_event.summary + "' fängt schon während des Termins '" + event.summary + "' an.")
        if (other_start < (event.end_time + datetime.timedelta(hours=Conflict.BUFFER_BETWEEN_EVENTS))) and (other_start > event.end_time):
            return Conflict("Der Termin '" + other_event.summary + "' fängt sehr schnell nach Termin '" + event.summary + "' an.")
        return None

    def conflicts_of_the_day(events_of_the_day):
        existing_conflicts = []
        for event in events_of_the_day:
            other_events = events_of_the_day.copy()
            other_events.remove(event)
            for other_event in other_events:
                conflict = Conflict.check_for_conflict(event, other_event)
                if (conflict is not None):
                    existing_conflicts.append(conflict)
        return existing_conflicts