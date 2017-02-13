import urllib
import requests

def callspark():
    # Call the URL
    auth = 'Bearer YmI4ZmZjMzMtM2ZmNS00YzkwLThjNDktMTU4ZmQzMzA4N2VhYzE0ODU0M2QtMGMx'
    room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vZWMwMTExYzAtZTYzZi0xMWU2LWI4ZGYtODcxYzNjYmQ0ZDFm'
    message_text = 'Hey! Today'
    r = requests.post('https://api.ciscospark.com/v1/messages', headers={'Authorization': auth },data = {'roomId' : room_id,'text' :message_text})
