import requests
import json
import time
import csv

bearer = "YOUR_TOKEN_GOES_HERE" #my token
fileName = "people.csv"

def sendSparkGET(url):
    response = requests.get(url,
                           headers={"Accept" : "application/json",
                                    "Content-Type":"application/json",
                                    "Authorization": "Bearer "+bearer})
    return response

counter = 0
url = 'https://webexapis.com/v1/people?max=1000'
items = []
while url != None:
    try:
        result = sendSparkGET(url)
        if result.status_code == 200:
            people = result.json()['items']
            data_file = open(fileName, 'a')
            csv_writer = csv.writer(data_file)
            count = 0
            for pep in people:
                if count == 0:
                    header = pep.keys()
                    csv_writer.writerow(header)
                    count +=1
                csv_writer.writerow(pep.values())
            data_file.close()
            print('Status Code: ' + str(result.status_code))
            print('TrackingId: ' + str(result.headers.get("trackingId")))
            url = result.headers.get("Link")
            if url:
                url, extra = url.split(">;")
                url = url[1:]
            print('Next link: ' + str(url))
            counter += 1
            print('Page: ' + str(counter))
            items += result.json()['items']
        else:
            print('Non-200 response, terminating session. Status Code: '+str(result.status_code))
            break
    except Exception as e:
        print(e)
print(items)
print("Final items length: {0}".format(len(items)))
