# run.py
from app import app

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

if __name__ == '__main__':
    app.run()
