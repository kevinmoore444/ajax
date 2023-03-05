from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = "dec_sasquatch"


# Setting the database as equal to the name of the model in SQL.