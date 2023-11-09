"""
@author: Roshni
"""

import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
#import testTotal as hi
import demoClient
import emailPython2

UPLOAD_FOLDER = 'C:\Users\sonal\.spyder\Internship\Attendance New\UploadedPhotos\Front'
UPLOAD_FOLDER1 = 'C:\Users\sonal\.spyder\Internship\Attendance New\UploadedPhotos\Back'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.secret_key = '4546545'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def index1():
    return render_template("index.html")

@app.route("/sheets")
def index():
        file1 = open("Subjects/SY_ODD.txt","r").read()
        file2 = open("Subjects/SY_EVEN.txt","r").read()
        file3 = open("Subjects/TY_ODD.txt","r").read()
        file4 = open("Subjects/TY_EVEN.txt","r").read()
        file5 = open("Subjects/LY_ODD.txt","r").read()
        file6 = open("Subjects/LY_EVEN.txt","r").read()
        sy_odd=file1.split('\n')
        sy_even=file2.split('\n')
        ty_odd=file3.split('\n')
        ty_even=file4.split('\n')
        ly_odd=file5.split('\n')
        ly_even=file6.split('\n')
        return render_template("update.html",sy_odd=sy_odd,sy_even=sy_even,ty_odd=ty_odd,ty_even=ty_even,ly_odd=ly_odd,ly_even=ly_even)

@app.route("/defaulters")
def index2():
    return render_template("defaulters.html")
    
@app.route("/sendmail", methods=['POST'])
def func():
    if 'Generate Excel' in request.form["action"]:
            files1=[]
            files2=[]
            sem=request.form["sem"]
            yr=request.form["year"]
            div=request.form["division"]
            monyr=request.form["m&y"]
            subj=request.form["subj"]
            
            sheetname = yr+"-"+div
            sub = int(subj)
            mon = monyr[5:]
            year = monyr[:4]
            month = int(mon)
            print month
            
            if sem == "ODD":
                month = month-7
            else:
                month = month-1

            print month
            
            if request.method == 'POST':
                # check if the post request has the file part
                        if 'file1' not in request.files:
                                #flash('No file part')
                                return redirect("/")
                        if 'file2' not in request.files:
                                #flash('No file part')
                                return redirect("/")
                        

                        for f in request.files.getlist("file1"):
                                if f.filename == '':
                                        flash('No selected Front image')
                                        return redirect("/")
                                else:
                                        i=0
                                        #files1=[]
                                        #or f in request.files.getlist("file1"):
                                        if allowed_file(f.filename):
                                                        filename = secure_filename(f.filename)
                                                        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                                        files1.append(url_for('uploaded_file', filename=filename))
                                print(files1);        
                                        

                        for f1 in request.files.getlist("file2"):
                                if f1.filename == '':
                                        flash('No selected Back image')
                                        return redirect("/")
                                else:
                                        i=0
                                        #files1=[]
                                        #for f1 in request.files.getlist("file2"):
                                        if allowed_file(f1.filename):
                                                        filename1 = secure_filename(f1.filename)
                                                        f1.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename1))
                                                        files2.append(url_for('uploaded_file1', filename=filename1))
                                print(files2);        
                    
            done1 = demoClient.fillColumn(sheetname,sub,month,year,sem,files1,files2)
            print "here"
            print done1
            file1 = open("Subjects/SY_ODD.txt","r").read()
            file2 = open("Subjects/SY_EVEN.txt","r").read()
            file3 = open("Subjects/TY_ODD.txt","r").read()
            file4 = open("Subjects/TY_EVEN.txt","r").read()
            file5 = open("Subjects/LY_ODD.txt","r").read()
            file6 = open("Subjects/LY_EVEN.txt","r").read()
            sy_odd=file1.split('\n')
            sy_even=file2.split('\n')
            ty_odd=file3.split('\n')
            ty_even=file4.split('\n')
            ly_odd=file5.split('\n')
            ly_even=file6.split('\n')
            return render_template("update.html", pop=done1,sy_odd=sy_odd,sy_even=sy_even,ty_odd=ty_odd,ty_even=ty_even,ly_odd=ly_odd,ly_even=ly_even, sheet=sheetname)
            #return render_template("mail.html", semval=sem, yr1=yr, div1=div,subj1=subj, monyr1=monyr, files=files1, bfiles=files2)
            
    elif 'Send Mail' in request.form["action"]:
        print("inside elif")
        sem=request.form["sem"]
        yr=request.form["year"]
        div=request.form["division"]
        monyr=request.form["m&y"]
        print sem
            
        sheetname = yr+"-"+div
        
        mon = monyr[5:]
        year = monyr[:4]
        month = int(mon)
        print month
            
        if sem == "ODD":
            month = month-7
        else:
            month = month-1

        print month
        sent1=emailPython2.emailFunction(sem,month,sheetname,year)
        return render_template("defaulters.html",pop=sent1 )
    else:
        print("inside else")
        return render_template("update.html")
    

@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<filename>')
def uploaded_file1(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER1'], filename)    
    
if __name__ == "__main__":
    app.run(debug=True)
