import pickle
import statistics

from sklearn import datasets  # # imports datasets from scikit-learn
from sklearn import metrics

from db.postgresl import PropertyDAO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


print('Regression model Init')
dataset = PropertyDAO().getDataFrameRecords(' where bedrooms > 0 and bedrooms < 5 and size_sqft < 5000 and price < 6000 and bath < 5');
print('Dataset Acquired: (',dataset.id.count(),')')
print(dataset.head())
print(list(dataset))

# old dataset
# define the data/predictors as the pre-set feature names  
#df = dataset[['bedrooms', 'bath', 'size_sqft', 'professionally_managed', 'no_pet_allowed', 'suit_laundry', 'park_stall', 'available_now', 'amenities', 'brand_new']]

# new dataset
# define the data/predictors as the pre-set feature names  
df = dataset[['bedrooms', 'bath', 'size_sqft', 'professionally_managed', 'no_pet_allowed', 'suit_laundry', 'park_stall', 'available_now', 'amenities', 'brand_new','loc_vancouver', 'loc_burnaby', 'loc_richmond', 'loc_surrey', 'loc_newwest', 'loc_abbotsford', 'no_basement']]

# Put the target (housing value -- MEDV) in another DataFrame
target = dataset[['price']]

X = df
y = target["price"]

# Note the difference in argument order
filename = '../data/reg_model.sav'
print('======================================================')
try:
    model = pickle.load(open(filename, 'rb'))
    print('Regression model loaded from saved data file')
except:
    print('Calculating regression model')
    model = sm.OLS(y, X).fit()
    pickle.dump(model, open(filename, 'wb'))
    print('Regression Model exported to: ', filename)
print('======================================================')

predictions = model.predict(X)  # make the predictions by the model

dataset['prediction'] = predictions;

dataset.to_csv('../data/result.csv')

# Print out the statistics
print(model.summary())
print(model.conf_int())
print('Mean: ', statistics.mean(y))
print('Mean Absolute Error:', metrics.mean_absolute_error(y, predictions))  
print('Mean Squared Error:', metrics.mean_squared_error(y, predictions))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, predictions)))
perf = 1 - (np.sqrt(metrics.mean_squared_error(y, predictions)) / statistics.mean(y))
perf = perf * 100
print('Performance ', perf, '%')


