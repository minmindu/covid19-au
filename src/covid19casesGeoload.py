from postcodeload import *
from covid19casesload import getCovid19Cases
import codecs


## part 1 - load the json file.
# it is the list of duple. Each record is a directory
totalCount = 0
recordList = list()
recordTupList = list()

cases = getCovid19Cases()
recordList = cases[0]
recordTupList = cases[1]
totalCount = len(recordTupList)
print('Fetch data completed. The total count is: ', len(recordTupList))

# each record:
# (2024, {'_id': 777, 'notification_date': '2020-03-22T00:00:00', 'postcode': 2024, 'lhd_2010_code': 'X720', 'lhd_2010_name': 'South Eastern Sydney', 'lga_code19': 18050, 'lga_name19': 'Waverley (A)'})
# (2026, {'_id': 778, 'notification_date': '2020-03-22T00:00:00', 'postcode': 2026, 'lhd_2010_code': 'X720', 'lhd_2010_name': 'South Eastern Sydney', 'lga_code19': 18050, 'lga_name19': 'Waverley (A)'})



## part 2 - load post code record.
# it is the list of duple. Each record is a directory
# (4570, {'locality': 'GLANMIRE', 'state': 'QLD', 'long': '152.616943','lat': '-26.153831'})
postcodes = getAUpostcodes()
print('Load postcode completed. The total count is: ', len(postcodes))


## part 3 - combine the 2 list together to get the (lang, long) for each causes
for caseTuple in recordTupList:
    for postcodeTuple in postcodes:
        if caseTuple[0] == postcodeTuple[0]:
            # combine the post code goe info to the case record
            caseTuple[1].update(postcodeTuple[1])
            break
            # get the other inform for this post code

# print (recordTupList)

## part 4 -- print the where.js file in the requried format

fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in recordTupList:
    data = row[1]

    if 'lat' in data and 'long' in data and 'locality' in data:
        lat = data['lat']
        lng = data['long']
        if lat == 0 or lng == 0 : continue
    else:
        continue

    where = data['locality']

    try :
        print(where, lat, lng)

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")
