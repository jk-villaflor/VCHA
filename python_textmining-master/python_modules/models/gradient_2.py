import numpy as np
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import pickle

from db.postgresl import PropertyDAO
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

# #############################################################################
# Load data
filename = '../data/grad_2_model.sav'

dataset = PropertyDAO().getDataFrameRecords(' where bedrooms > 0 and bedrooms < 5 and size_sqft < 5000 and price < 6000 and bath < 5');
print('Dataset Acquired: (',dataset.id.count(),')')

# define the data/predictors as the pre-set feature names  
# old dataset 
#df = dataset[['bedrooms', 'bath', 'size_sqft', 'professionally_managed', 'no_pet_allowed', 'suit_laundry', 'park_stall', 'available_now', 'amenities', 'brand_new']]

# new dataset
df = dataset[['bedrooms', 'bath', 'size_sqft', 'professionally_managed', 'no_pet_allowed', 'suit_laundry', 'park_stall', 'available_now', 'amenities', 'brand_new','loc_vancouver', 'loc_burnaby', 'loc_richmond', 'loc_surrey', 'loc_newwest', 'loc_abbotsford', 'no_basement']]


# Put the target (housing value -- MEDV) in another DataFrame
target = dataset[['price']]

X = df
y = target["price"]
y_train = y.values
X_train = X
y_test = y.values
X_test = X


# #############################################################################
# Fit regression model
print('======================================================')
try:
    model = pickle.load(open(filename, 'rb'))
    print('Gradient Boosting model loaded from saved data file')
except:
    print('Calculating Gradient Boosting')
    params = {'n_estimators': 700, 'max_depth': 20, 'min_samples_split': 5,
              'learning_rate': 0.01, 'loss': 'ls'}
    model = ensemble.GradientBoostingRegressor(**params)
    
    model.fit(X_train, y_train)
    pickle.dump(model, open(filename, 'wb'))
    print('Gradient Boosting Model exported to: ', filename)

print('======================================================')

pred = model.predict(X_test)

mean = statistics.mean(y_test.flatten())
print('Mean: ', mean)
mse = mean_squared_error(y_test, pred)
print("MSE: %.4f" % mse)
rmse = np.round(np.sqrt(mse),2)
print('Root Mean Squared Error:', rmse)
perf = 1 - (rmse/mean)
perf = perf * 100
print('Performance ', perf, '%')

# #############################################################################
# Plot
test = pd.DataFrame({"prediction": pred, "observed": y})
lowess = sm.nonparametric.lowess
z = lowess(pred.flatten(), y)
test.plot(figsize = [14,8],
          x ="prediction", y = "observed", kind = "scatter", color = 'darkred')
plt.title("Extreme Gradient Boosting: Prediction Vs Test Data", fontsize = 18, color = "darkgreen")
plt.xlabel("Predicted Power Output", fontsize = 18) 
plt.ylabel("Observed Power Output", fontsize = 18)
plt.plot(z[:,0], z[:,1], color = "blue", lw= 3)
plt.show()
