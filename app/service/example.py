#import
import model.example

def getAuthors():
    rows = model.example.getAuthors()
    return [row["name"] for row in rows] #liste des noms


