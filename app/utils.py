from datetime import datetime
# Found on : https://pytutorial.com/python-datetime-to-string-guide/
def getCurrentTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")