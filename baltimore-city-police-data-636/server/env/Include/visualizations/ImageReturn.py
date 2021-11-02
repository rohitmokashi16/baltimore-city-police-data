import base64

def returnImage ():
    with open("./env/Include/sample/logo.png", "rb") as image:
        return base64.b64encode(image.read())
