from flask import Flask, render_template, request
import csv
import json
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    filename = 'data/dataset.csv'

    headlines = csv.reader(open(filename))
    next(headlines)  # Skipping header
    lines = list(headlines)

    for i in range(len(lines)):
        lines[i].append(i)  # Adding Index to uniquely identify

    return render_template('index.html', headlines=lines)


@app.route('/edit', methods=['POST'])
def updateCSV():
    print('inside edit')
    data = request.form
    content = data['content']

    row_id = data['id'].split(',')
    row = int(row_id[0]) + 1
    col = int(row_id[1])

    filename = 'data/dataset.csv'

    headlines = csv.reader(open(filename))
    lines = list(headlines)

    lines[row][col] = content  # Modifying the cell with updated data

    writer = csv.writer(open(filename, 'w'))
    writer.writerows(lines)

    return render_template('index.html', headlines=lines)


@app.route('/sort', methods=['POST'])
def sortCSV():
    print("inside sort ()")
    #request.form.decode('UTF-8')
    data = request.form
    print(request.form)
    content = data['content']
    content = json.loads(content)
    sortBy = int(data['sortBy'])
    lines = list(content)
    print(lines)
    # lines.sort(key=lambda x: x[sortBy])

    idArr = []
    sortArr = []

    # Check for Timestamp
    if sortBy == 1:
        dateFormat = '%Y-%m-%d %I:%M %p'
        monthDict = {
            "Jan": 1,
            "Feb": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }
        for x in lines:
            try:
                temp = x[1].split()
                del temp[2:4]
                temp = temp[::-1]
                # date_string = '2009-11-29 03:17 PM'
                # ['7:51', 'PM', 'ET', 'Fri,', '17', 'July', '2020']
                # print(len(temp))
                temp[1] = monthDict.get(temp[1])
                date_string = temp[0] + '-' + str(temp[1]) + '-' + temp[2] + ' ' + temp[4] + ' ' + temp[3]
                dt_obj = datetime.strptime(date_string, dateFormat)
                sortArr.append(dt_obj.timestamp() * 1000)
            except:
                sortArr.append(0.0)
            idArr.append(x[3])

    else:
        for x in lines:
            sortArr.append(x[sortBy])
            idArr.append(x[3])

    bubbleSort(sortArr, idArr)

    sortedArr = []
    for idx in idArr:
        sortedArr.append(lines[idx])
    #print(idArr)
    return render_template('index.html', headlines=sortedArr)


def bubbleSort(sortArr, idArr):
    n = len(sortArr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if sortArr[j] > sortArr[j + 1]:
                sortArr[j], sortArr[j + 1] = sortArr[j + 1], sortArr[j]
                idArr[j], idArr[j + 1] = idArr[j + 1], idArr[j]


if __name__ == "__main__":
    app.run(debug=True)
