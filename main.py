from flask import Flask
from routes import mod
from models import User, db


app = Flask(__name__)
app.register_blueprint(mod)


if __name__ == '__main__':
  db.create_tables([User])
  app.run("0.0.0.0", port=5701, debug=True)