import urllib.request, urllib.parse, urllib.error
import http
import json
import time
import ssl
import sys
from postcodeload import getAUpostcodes

baseurl = "https://data.nsw.gov.au/data"
serviceurl = "https://data.nsw.gov.au/data/api/3/action/datastore_search?"
# url like: https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29

#########################################################
# function getUrldata()
#########################################################
"""
Returns the data from the URL GET.

:param arg1: a complete url
:type arg1: string

:return: decode https call result
:rtype: string
"""
def getUrldata(url):
    print('Retrieving', url)
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    fileobj = urllib.request.urlopen(url, context=ctx)
    data = fileobj.read().decode()
    # print('Retrieved', data)
    return data

#########################################################
### function convertData()
#########################################################
"""
Returns the data from the URL GET.

:param arg1: data record array
:type arg1: array

:return: a tuple of 2 list
:rtype: Tuple
"""
def getConvertedData(records):
    recordList = list()
    recordTupList = list()

    for record in records:
        # read each record
        # print(record)
        recordList.append(record)
        # cover it to a duple {postCode, {record}}
        postCode = record['postcode']
        recordTuple = (postCode, record)
        recordTupList.append(recordTuple)
        # print(recordTuple)
    return (recordList, recordTupList)

#########################################################
### function fetchData()
#########################################################
"""
Fill in all data into the provided list.

:param arg1: the URL to start with
:type arg1: String

:param arg2: to record list to be filled in
:type arg1: List of {record}

:param arg3: to record list to be filled in a different way (postcode, {record})
:type arg1: List of (postcode, {record})

:return: (recordList, recordTupList)

"""
def fetchData(url, recordList, recordTupList):
    # read the url
    data = getUrldata(url)
    jsonData = json.loads(data)
    # print(data)

    # total is always the same
    totalCount=jsonData['result']['total']

    # to finish the recursively call
    if (len(recordList) == totalCount):
        print('complete the loop. record count is ', len(recordList))
        return (recordList, recordTupList)
    else:
        # get records
        records = jsonData['result']['records']
        if len(records) > 0 :
            convertedRecords = getConvertedData(records)
            recordList = recordList + convertedRecords[0]
            recordTupList = recordTupList + convertedRecords[1]
            print('the length of records', len(recordTupList))

            # read the next url
            nextUrl = jsonData['result']['_links']['next']
            nextUrl = baseurl + nextUrl
            if nextUrl is not None:
                # recursively read the data
                return fetchData(nextUrl, recordList, recordTupList)



#########################################################
# Main part of the program
#########################################################

def getCovid19Cases():
    resourceId = "21304414-1ff1-4243-a5d2-f52778048b29"
    parms = dict()
    parms["resource_id"] = resourceId
    url = serviceurl + urllib.parse.urlencode(parms)

    # it is the list of dictionary. Each record is a directory
    # totalCount = 0
    recordList = list()
    recordTupList = list()
    result = fetchData(url, recordList, recordTupList)
    # return result
    # recordList = result[0]
    # recordTupList = result[1]

    # totalCount = len(recordTupList)
    # print('Fetch data completed. The total count is ', len(recordTupList))

    return result
