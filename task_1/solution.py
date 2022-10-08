import csv

res_dict = {}

with open('data.csv', encoding='utf-8') as f:
    csv_reader = csv.reader(f, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        country = res_dict.update({
            row[0]: {
                'people': res_dict.get(row[0], {'people': []})['people'] + [row[1]],
                'count': res_dict.get(row[0], {'count': 0})['count'] + 1
            }
        })

print(res_dict)
