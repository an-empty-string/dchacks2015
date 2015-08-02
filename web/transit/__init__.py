from flask import Flask
app = Flask("transit")

from . import routes
