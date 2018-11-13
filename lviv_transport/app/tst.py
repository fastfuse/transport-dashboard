import csv
import json


with open('stops.txt', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # print(reader.fieldnames)

    data = []

    for row in reader:
        data.append(row)
        # print(row.items())

        # print(row['stop_name'], row['stop_lat'])

    print(len(data))

    # print(json.dumps(data))
