import json
import requests
from datetime import datetime

api_token = 'your_api_token'
api_url_base = 'https://api.meetup.com/empugdotorg/'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}

def get_events():

    api_url = '{0}events'.format(api_url_base)

    # response = requests.get(api_url, headers=headers)
    response = requests.get(api_url)

    if response.status_code == 200:
        events = json.loads(response.content.decode('utf-8'))
        for event in events:
            dt = datetime(*[int(item) for item in event['local_date'].split('-')])
            event['day'] = dt.strftime("%d")
            event['month'] = dt.strftime("%b")
            event['excerpt'] = remove_html_tags(event['description'])
        return events
    else:
        return None

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

if __name__ == "__main__":
    # execute only if run as a script
    print(get_events())