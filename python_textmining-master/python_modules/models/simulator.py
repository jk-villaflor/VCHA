import pickle
import pandas as pd
from db.postgresl import PropertyDAO

filename_reg = '../data/reg_model.sav'
filename_grad = '../data/grad_model.sav'
filename_grad_2 = '../data/grad_2_model.sav'
#record = PropertyDAO().getDataFrameRecord(6852790585)

# intialise data of lists.
data = {'price':[2900.0],
        'bedrooms':[2.0],
        'bath':[2.0],
        'size_sqft':[750.0],
        'professionally_managed':[0.0],
        'no_pet_allowed':[1.0],
        'suit_laundry':[1.0],
        'park_stall':[1.0], 
        'available_now':[0.0], 
        'amenities':[0.0], 
        'brand_new':[0.0],
        'loc_vancouver':[1.0], 
        'loc_burnaby':[0.0], 
        'loc_richmond':[0.0], 
        'loc_surrey':[0.0], 
        'loc_newwest':[0.0], 
        'loc_abbotsford':[0.0], 
        'no_basement':[1.0]
        }
 
# Create DataFrame
record = pd.DataFrame(data)
 
# Print the output.
print(record)

try:
    model_reg = pickle.load(open(filename_reg, 'rb'))
    print('Regression model_reg loaded from saved data file')

    model_grad = pickle.load(open(filename_grad, 'rb'))
    print('Regression model_grad loaded from saved data file')

    model_grad_2 = pickle.load(open(filename_grad_2, 'rb'))
    print('Regression model_grad_2 loaded from saved data file')
    
    df = record[['bedrooms', 'bath', 'size_sqft', 'professionally_managed', 'no_pet_allowed', 'suit_laundry', 'park_stall', 'available_now', 'amenities', 'brand_new','loc_vancouver', 'loc_burnaby', 'loc_richmond', 'loc_surrey', 'loc_newwest', 'loc_abbotsford', 'no_basement']]
    predictions_reg = model_reg.predict(df)  # make the predictions_reg by the model_reg
    predictions_grad = model_grad.predict(df)  # make the predictions_grad by the model_grad
    predictions_grad_2 = model_grad_2.predict(df)  # make the predictions_grad_2 by the model_grad
    
    print("Property: ",record.price.tolist())
    print("Prediction Reg: ",predictions_reg.tolist())
    print("Prediction Grad Boosting: ",predictions_grad.tolist())
    print("Prediction Grad Boosting 2: ",predictions_grad_2.tolist())
    
except:
    print('Error loading models found at ',filename_reg)
print('======================================================')