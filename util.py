
def find(fn, list):
    for elem in list:
        if fn(elem):
            return elem