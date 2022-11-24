from flask import Flask

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.route("/")
def home():
    return {"Hello": app.config["MESSAGE"]}

if __name__ == "__main__":
    app.run()