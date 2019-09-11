import json
import pandas as pd
from flask import Flask, jsonify
from flask_cors.extension import CORS
from db.postgresl import PropertyDAO
from model.Property import Property
from flask.globals import request
from simulator import Simulator

#start the rest api application
app = Flask(__name__)
CORS(app) #apply cors for remote connection accept

@app.route('/')
def index():
    data = {}
    data['test'] = {"self": {"href": "/test"}}
    data['get_property'] = {"self": {"href": "/prop/{propid}"}}
    data['testpost'] = {"self": {"href": "/testpost"}}
    data['simulate'] = {"self": {"href": "/simulate"}}
    
    return json.dumps(data);

@app.route('/simulate', methods=['POST'])
def simulate():
    simulator = Simulator()
    req_data = request.get_json()
    data = {'price':[req_data['price']],
        'bedrooms':[req_data['bedrooms']],
        'bath':[req_data['bath']],
        'size_sqft':[req_data['size_sqft']],
        'professionally_managed':[req_data['professionally_managed']],
        'no_pet_allowed':[req_data['no_pet_allowed']],
        'suit_laundry':[req_data['suit_laundry']],
        'park_stall':[req_data['park_stall']], 
        'available_now':[req_data['available_now']], 
        'amenities':[req_data['amenities']], 
        'brand_new':[req_data['brand_new']],
        'loc_vancouver':[req_data['loc_vancouver']], 
        'loc_burnaby':[req_data['loc_burnaby']], 
        'loc_richmond':[req_data['loc_richmond']], 
        'loc_surrey':[req_data['loc_surrey']], 
        'loc_newwest':[req_data['loc_newwest']], 
        'loc_abbotsford':[req_data['loc_abbotsford']], 
        'no_basement':[req_data['no_basement']]
        }
    
    # Create DataFrame
    record = pd.DataFrame(data)
    
    record = simulator.simulate(record)
    
    return record.to_json(orient='index')

@app.route('/test')
def test():
    record = PropertyDAO().getRecord(6842453594)[0]
    property = Property(record[0],record[1],record[2],record[3])
    return property.getJson();

@app.route('/prop/<string:prop_id>')
def getProperty(prop_id):
    try:
        record = PropertyDAO().getRecord(prop_id)[0]
        property = Property(record[0],record[1],record[2],record[3])
        return property.getJson();
    except:
        return 'No record found!'
    


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')