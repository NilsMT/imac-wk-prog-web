#import
import model.example

def getAuthors():
    rows = model.example.getAuthors()

    return [r["name"] for r in rows] #liste des noms (un peu tricky j'avoue)
