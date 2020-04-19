import csv
from collections import OrderedDict

def getAUpostcodes():
    result = list()
    with open("australian_postcodes.csv") as fhand:
        reader  = csv.DictReader(fhand, delimiter=',')
        for row in reader:
            # (4570, {'locality': 'GLANMIRE', 'state': 'QLD', 'long': '152.616943','lat': '-26.153831'})
            selectedColumns = dict((k, row[k]) for k in ('locality', 'state', 'long', 'lat'))
            result.append((int(row["postcode"]), selectedColumns))


        # get rid of the duplication records with the same postcode. By default, use the first row
        result = OrderedDict(result).items()
        return result


 # (4570, {'id': '13040', 'postcode': '4570', 'locality': 'GILLDORA', 'state': 'QLD', 'long': '152.616943', 'lat': '-26.153831', 'dc': 'GYMPIE DC', 'type': 'Delivery Area', 'status': 'Updated 6-Feb-2020', 'sa3': '31905', 'sa3name': 'Maryborough', 'sa4': '319', 'sa4name': 'Wide Bay'}),
 # (4570, {'id': '13041', 'postcode': '4570', 'locality': 'GLANMIRE', 'state': 'QLD', 'long': '152.616943', 'lat': '-26.153831', 'dc': 'GYMPIE DC', 'type': 'Delivery Area', 'status': 'Updated 6-Feb-2020', 'sa3': '31905', 'sa3name': 'Maryborough', 'sa4': '319', 'sa4name': 'Wide Bay'}
