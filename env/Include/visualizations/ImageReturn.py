import base64

def returnImage ():
    with open("./env/Include/sample/logo.png", "rb") as image:
        return base64.b64encode(image.read())

def returnDate ():
    with open("./env/Include/sample/Part1_Crime_data.csv", "rb") as data:
        return data