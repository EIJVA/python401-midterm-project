from authlib.jose import jwt
import requests
from requests import Response
from datetime import date, datetime


class Zoomify:

    def __init__(self, API_KEY, API_SECRET, JWT):
        # Init instance variables such as api_key, api_secret, api base url, jwt token expiration, jwt algo
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.JWT = JWT
        self.base_url = "https://api.zoom.us/v2"
        self.reports_url = f"{self.base_url}/report/meetings"
        self.users_url = f"{self.base_url}/report/users"


    def get_meeting_reports(self, email):
        url = f"{self.users_url}/{email}/meetings"        
        now = datetime.now()
        # Here we will had to add an option of how far back we go checking meetings
        query_params = {
                "from": "2018-09-13",
                "to": str(now.strftime("%Y-%m-%d")),
                "page_size": 30,
            }
        r = (requests.get(url, headers={"Authorization": f"Bearer {self.JWT}"},
        params=query_params)).json()
        
        meetings = r['meetings'][::-1] 
        self.format_meetings(meetings)
        
        # Allow user to select the meeting to display information
        user_selection = int(input('Type which meeting you would like to select: '))
        return meetings[user_selection]['uuid']


    def format_meetings(self, meetings):
        #
        #{'uuid': 'jxhNkUJ8SLunKbmGJG68Xw==', 'id': 6118089019, 'host_id': 'ZS6Hi-buTWmYhnyK75HtWQ', 'type': 4,
        #  'topic': "Isaiah Burkes's Personal Meeting Room", 'user_name': 'Isaiah Burkes', 'user_email': 'idkburkes@gmail.com',
        #  'start_time': '2022-02-19T22:25:30Z', 'end_time': '2022-02-19T22:26:38Z', 'duration': 2, 'total_minutes': 3, 'participants_count': 3, 'source': 'Zoom'} 
        #
        counter = 0
        for meeting in meetings:
            res = f" [{counter}] - Topic Name: {meeting['topic']} -  Start Time: {meeting['start_time']}"
            counter += 1
            print(res)

        # return res

        
        
    # Here is where we use the Zoom API do get all the participants of an ongoing zoom meeting
    def get_meeting_participants(self, uuid):
        url = f"{self.reports_url}/{uuid}/participants"
        query_params = {
            "page_size": 30
        }
        r = (requests.get(url, headers={"Authorization": f"Bearer {self.JWT}"}, 
        params=query_params)).json()

        participants = []
        [participants.append(p["name"]) for p in r["participants"] if p["name"] not in participants]
        
        # print("\n Attendees \n ---------")
        # for name in participants: 
        #     print(f'{name}')
        
        return participants

