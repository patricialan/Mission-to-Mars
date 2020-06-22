from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    mars_list = mongo.db.mars_list.find()
    return render_template('index.html', mars=mars, mars_list=mars_list)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)

    mars_list = mongo.db.mars_list
    mars_data_list = scraping.hemis_data()
    mars_list.update_many({}, mars_data_list, upsert=True)

    return "Scraping Successful!"

if __name__ == "__main__":
   app.run()
