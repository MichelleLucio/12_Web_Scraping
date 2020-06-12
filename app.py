
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import ML_scrape_mars1

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scrape_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    mars_data = mongo.db.mars_scrape_data.find_one()
    print(mars_data)
    # Return template and data
    return render_template("index.html", mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
    # Run the scrape function
    mars_data = ML_scrape_mars1.scrape_all()
    mongo.db.mars_scrape_data.update({}, mars_data, upsert=True)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
