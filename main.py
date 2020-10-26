from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    lines = readCsv(True)

    del lines[0]

    return render_template('index.html', headlines=lines)


@app.route('/edit', methods=['POST'])
def updateCSV():
    print('inside edit()')
    data = request.form
    content = data['content']

    row_id = data['id'].split(',')
    posX = int(row_id[0])
    posY = int(row_id[1])

    lines = readCsv(False)

    print(lines[posX][posY])
    print(posX, posY)
    # return None

    lines[posX][posY] = content  # Modifying the cell with updated data

    filename = 'data/dataset.csv'
    writer = csv.writer(open(filename, 'w'))
    writer.writerows(lines)

    del lines[0]

    return 'success'


@app.route('/sort', methods=['GET'])
def sortCSV():
    print("inside sort ()")
    # request.form.decode('UTF-8')
    data = request.form
    # print(request.form)

    sortBy = int(request.args.get('sortBy'))
    print(sortBy)
    lines = readCsv(True)

    # print(lines)
    # lines.sort(key=lambda x: x[sortBy])

    idArr = []
    sortArr = []

    # Check for Timestamp
    if sortBy == 1:
        sortArr, idArr = getDataForSort(lines)
    else:
        for x in lines:
            sortArr.append(x[sortBy])
            idArr.append(x[3])

    sortData(sortArr, idArr)

    sortedArr = []
    for idx in idArr:
        if int(idx) != 0:
            sortedArr.append(lines[int(idx)])
    # print(idArr)
    return render_template('index.html', headlines=sortedArr)


def getDataForSort(lines):
    idArr = []
    sortArr = []
    dateFormat = '%Y-%m-%d %I:%M %p'
    monthDict = {
        "Jan": 1, "Feb": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "Aug": 8, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12
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
            sortArr.append(0.0)  # Making it to view at top of the table
        idArr.append(x[3])
    return sortArr, idArr


def readCsv(idReqd):
    filename = 'data/dataset.csv'

    headlines = csv.reader(open(filename))
    # next(headlines)  # Skipping header
    lines = list(headlines)

    if idReqd:
        for i in range(len(lines)):
            lines[i].append(i)  # Adding Index to uniquely identify

    return lines


def sortData(sortArr, idArr):
    n = len(sortArr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if sortArr[j] > sortArr[j + 1]:
                sortArr[j], sortArr[j + 1] = sortArr[j + 1], sortArr[j]
                idArr[j], idArr[j + 1] = idArr[j + 1], idArr[j]


if __name__ == "__main__":
    app.run(debug=True)
