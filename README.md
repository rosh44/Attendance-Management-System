# Automated Attendance System using Image Processing

## Team Members
- Rushabh Bid
- Tanmay Dhaundiyal
- Roshni Soni

## Overview
This system automates the attendance and defaulter management process through scanned attendance sheets using image processing, storing data in an Excel sheet, and automatically emailing defaulters about their attendance.

## Report Summary
The project was undertaken at K. J. Somaiya College of Engineering, Mumbai, under the guidance of Ms. Suchitra Patil (suchitrapatil@somaiya.edu).

### Modules
1. **Attendance Counting**: Adds attendance from scanned sheets into an Excel file.
2. **Email to Defaulters**: Sends emails to students with low attendance.
3. **User Interface**: A Flask application with forms for updating attendance and sending defaulter emails.

### Tools Used
- Python 2
- OpenCV
- Flask
- SMTP

### Key Learnings
- Image processing techniques.
- Writing in Excel using Python
- Excel manipulation through Python.

## Prerequisites
- Python 2

## Running the System
Navigate to the main folder (`Attendance New`) in the command prompt and execute:
python2 FlaskTry.py

The system runs on localhost, presenting two forms:
1. **Update Attendance**: Upload scanned attendance sheets (batch processing available) and fill the form to update attendance.
2. **Check Defaulters**: This form triggers emails to students who are defaulters based on the filled-in criteria.

## Sheet Dimensions and Guidelines
To ensure high accuracy, the attendance sheet must be printed with specific dimensions (provided in `Attendance Sheet_dimensions.xls`) and teachers should mark absence with an 'A'. Example sheets can be found in the `Final Scanned Images` folder.



