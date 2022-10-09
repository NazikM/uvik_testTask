import csv


def get_res(filename='data.csv'):
    res_dict = {}
    with open(filename, encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            country = res_dict.get(row[0], {'people': [], 'count': 0})
            res_dict.update({
                row[0]: {
                    'people': country['people'] + [row[1]],
                    'count': country['count'] + 1
                }
            })
    return res_dict


print(get_res())
