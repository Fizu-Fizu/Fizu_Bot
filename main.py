import os
from flask import Flask

app = Flask(__name__)
@app.route("/receive_event", methods=["POST"])
def receive_event():
    
    return {"status": "ok"}
