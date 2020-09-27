import os
import zipfile
from appExtractFeatures import app
from flask import Flask, flash, request, redirect, render_template, url_for, send_file
from werkzeug.utils import secure_filename
import filetype
import time
from extractFeatures import processFiles

def isCSV(str):
    if str[str.rfind('.'):] == '.csv':
        return 1
    return 0

@app.route('/ucs538-assignment5/')
def uploadForm():
    return render_template('uploadExtractFeatures.html')

@app.route('/ucs538-assignment5', methods = ['POST'])
def uploadConvertFile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file sent in post request')
            return redirect(request.url)

        files = request.files.getlist('file')

        if any (file.filename == '' for file in files):
            flash('No file selected')
            return redirect(request.url)

        if all (file and isCSV(file.filename) for file in files):
            outputZipFilePath = os.path.join(app.config['UPLOAD_FOLDER'], 'results+log-'+ str(time.time()) +'.zip')
            outputZipFile = zipfile.ZipFile(outputZipFilePath, 'w', zipfile.ZIP_DEFLATED)
            inputFiles = []

            for file in files:
                filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filePath)
                inputFiles.append(filePath)

            output = processFiles(app.config['UPLOAD_FOLDER'], inputFiles)

            if output[0] == 1:
                flash(output[1])
                return redirect(request.url)

            else:
                for filePath in output[1]:
                    outputZipFile.write(filePath, filePath[filePath.rfind('/'):])

                outputZipFile.close()
                return send_file(outputZipFilePath, as_attachment = True)


        else:
            flash('Only CSV files are allowed')
            return redirect(request.url)

if __name__ == '__main__':
    app.run()
