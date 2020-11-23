
def get_absolute_address():
    return 'http://localhost:9090' #adresse de l'API

def make_address(absolute_address, relative_address):
    if (type(absolute_address) != str) or (type(relative_address) != str):
        return print("Les adresses doivent etre des str")
    return absolute_address + relative_address