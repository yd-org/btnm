import base64

def base64encode(stren):
    stren = base64.encodebytes(bytes(stren,'utf-8'))
    stren = stren.decode('utf-8')
    return stren

def base64decode(strde):
    strde = base64.decodebytes(bytes(strde, 'utf-8'))
    strde = strde.decode('utf-8')
    return strde