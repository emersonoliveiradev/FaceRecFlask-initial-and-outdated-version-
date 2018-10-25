#from app import app
from app import manager

if __name__== "__main__":
    manager.run()
    #if not Manager
    #app.run()

# Apos executado aqui, ele cria uma "variavel global" app,
# depois procura o __init__ dentro a pasta app