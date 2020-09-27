#python3
import sys
import csv
import os
import time

def processFiles(savePath, inputFiles):
    recordIndex = 0
    fileIndex = 0
    delimiter = ','
    recordList = []
    errorList = []
    classMap = {'+': 1, '-': 0}

    for file in inputFiles:
        fileIndex += 1
        f = open(file, 'r')
        csvFile = csv.reader(f, delimiter = delimiter)
        fields = next(csvFile)

        if len(fields) != 2:
            outputString = "file no." + str(fileIndex) + " does not have only 2 columns " + len(fields)
            return [1, outputString]

        for row in csvFile:
            if not row[0].isalpha() or not row[1] in ['+', '-']:
                errorEntry = []
                errorEntry.append(file)
                errorEntry.append(row[0])
                errorEntry.append(row[1])
                errorList.append(errorEntry)

            else:
                recordIndex += 1
                record = []
                record.append(recordIndex)
                record.append(row[0].count('N'))
                record.append(row[0].count('H'))
                record.append(row[0].count('Q'))
                record.append(row[0].count('G'))
                record.append(row[0].count('D'))
                record.append(row[0].count('T'))
                record.append(classMap[row[1]])
                recordList.append(record)

    outputFiles = []

    resultFields = ['SN', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'Class']
    resultFilePath = os.path.join(savePath, 'result-' + str(time.time()) + '.csv')
    resultFile = open(resultFilePath, 'w')
    csvResult = csv.writer(resultFile, delimiter = delimiter)
    csvResult.writerow(resultFields)
    csvResult.writerows(recordList)
    outputFiles.append(resultFilePath)

    logFields = ['FileName', 'Sequence', 'Class']
    logFilePath = os.path.join(savePath, 'log-' + str(time.time()) + '.csv')
    logFile = open(logFilePath, 'w')
    csvLog = csv.writer(logFile, delimiter = delimiter)
    csvLog.writerow(logFields)
    csvLog.writerows(errorList)
    outputFiles.append(logFilePath)

    return [0, outputFiles]
