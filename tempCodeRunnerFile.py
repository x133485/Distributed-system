import http.client
import json

conn = http.client.HTTPConnection("localhost", 8080)
conn.request("GET", "/")

response = conn.getresponse()
response = conn.getresponse()

data = response.read()

courses = json.loads(data)

for course in courses:
    print(course)

conn.close()