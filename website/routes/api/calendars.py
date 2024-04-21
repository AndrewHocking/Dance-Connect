from flask import Blueprint, jsonify
from datetime import datetime, timedelta

api_calendar = Blueprint('api_calendar', __name__)

class CalendarEvent:
    def __init__(self, name: str, date: datetime, description: str, picture_url: str):
        self.name = name
        self.date = date
        self.description = description
        self.picture_url = picture_url

class Calendar:
    def __init__(self, year: int):
        self.year = year
        self.events = {}

    def add_event(self, event: CalendarEvent):
        if event.date.year != self.year:
            raise ValueError("Event year does not match calendar year")
        if event.date not in self.events:
            self.events[event.date] = []
        self.events[event.date].append(event)

    def get_events(self, month: int):
        start_date = datetime(self.year, month, 1)
        end_date = datetime(self.year, month + 1, 1) - timedelta(days=1)
        events = []
        for date in self.events.keys():
            if start_date <= date <= end_date:
                events.extend(self.events[date])
        return events


@api_calendar.route('/events-json')
def get_events_json():
    # Create a Calendar instance and add events
    calendar = Calendar(year=2024)
    event1 = CalendarEvent("reSTEP", datetime(2024, 4, 15), 
                           """8:00 PM\n300 Parliament St, Toronto\nreStep is a captivating contemporary dance performance that explores the intricate interplay between movement and memory. 
                           Set against a backdrop of shifting landscapes and dynamic lighting.""", "https://d26oc3sg82pgk3.cloudfront.net/files/media/edit/image/21752/square_thumb%402x.jpg")
    event2 = CalendarEvent("echoes of us", datetime(2024, 4, 20), """7:30 PM\n579 Dundas St East, Toronto\n echoes of us is a mesmerizing dance performance that gracefully weaves the empotional tapestry of shared experiences among three women. Against a backdrop of poignant melodies.""", "https://static.wixstatic.com/media/11062b_1f1763b7452a4880998422d12e4b0c62~mv2.jpg/v1/crop/x_2693,y_0,w_2395,h_2394/fill/w_256,h_256,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/Ballet%20dancers.jpg")
    calendar.add_event(event1)
    calendar.add_event(event2)

    # Serialize events into JSON format
    events_json = []
    for date, events in calendar.events.items():
        for event in events:
            description_with_br = event.description.replace('\n', '<br>')
            events_json.append({
                'title': event.name,
                'start': event.date.strftime('%Y-%m-%d'),
                'description': description_with_br,
                'picture_url': event.picture_url
            })

    return jsonify(events_json)

