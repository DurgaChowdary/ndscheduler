import urllib
import requests
import http.client


#Job Name
def jobname(job_id):

    r = requests.get('http://vm-ioed-um-svl4:8888/api/v1/jobs/'+job_id)
    data = r.json()
    job_name = data["name"]
    return job_name


# Call the URL
def callurl(message_text):
    auth = 'Bearer YmI4ZmZjMzMtM2ZmNS00YzkwLThjNDktMTU4ZmQzMzA4N2VhYzE0ODU0M2QtMGMx'
    room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vZWMwMTExYzAtZTYzZi0xMWU2LWI4ZGYtODcxYzNjYmQ0ZDFm'
    r = requests.post('https://api.ciscospark.com/v1/messages', headers={'Authorization': auth },data = {'roomId' : room_id,'text' :message_text})
