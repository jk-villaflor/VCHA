import xgboost as xgb
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pickle
import statistics

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from db.postgresl import PropertyDAO

filename = '../data/grad_model.sav'

dataset = PropertyDAO().getDataFrameRecords(' where bedrooms > 0 and bedrooms < 5 and size_sqft < 5000 and price < 6000 and bath < 5');
print('Dataset Acquired: (',dataset.id.count(),')')

#Create training and test datasets

# old dataset
#X = dataset[['bedrooms','bath','size_sqft','professionally_managed', 'no_pet_allowed', 'suit_laundry', 'park_stall', 'available_now', 'amenities', 'brand_new']]

# new dataset
X = dataset[['bedrooms', 'bath', 'size_sqft', 'professionally_managed', 'no_pet_allowed', 'suit_laundry', 'park_stall', 'available_now', 'amenities', 'brand_new','loc_vancouver', 'loc_burnaby', 'loc_richmond', 'loc_surrey', 'loc_newwest', 'loc_abbotsford', 'no_basement']]
y = dataset['price'].values
y = y.reshape(-1, 1)


X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.2, random_state=42)

#Convert the training and testing sets into DMatrixes
DM_train = xgb.DMatrix(data = X, 
                       label = y)  
DM_test =  xgb.DMatrix(data = X,
                       label = y)


gbm_param_grid = {
     'colsample_bytree': np.linspace(0.5, 0.9, 5),
     'n_estimators':[100, 200],
     'max_depth': [10, 15, 20, 25]
}

#Instantiate the regressor
gbm = xgb.XGBRegressor()

#Perform grid search
try:
    grid_model = pickle.load(open(filename, 'rb'))
    print('Gradient Boosting model XGBRegressor loaded from saved data file')
except:
    print('Calculating Gradient Boosting XGBRegressor')
    
    grid_model = GridSearchCV(estimator = gbm, param_grid = gbm_param_grid, scoring = 'neg_mean_squared_error', cv = 5, verbose = 1)
    grid_model.fit(X, y)
    print("Best parameters found: ",grid_model.best_params_)
    print("Lowest RMSE found: ", np.sqrt(np.abs(grid_model.best_score_)))

    pickle.dump(grid_model, open(filename, 'wb'))
    print('Gradient Boosting XGBRegressor Model exported to: ', filename)
print('======================================================')


#Predict using the test data
pred = grid_model.predict(X)
print("Root mean square error for test dataset: {}".format(np.round(np.sqrt(mean_squared_error(y, pred)), 2)))
mean = statistics.mean(y.flatten())
print('Mean: ', mean)
rmse = np.round(np.sqrt(mean_squared_error(y, pred)),2)
print('Root Mean Squared Error:', rmse)
perf = 1 - (rmse/mean)
perf = perf * 100
print('Performance ', perf, '%')

#test
test = pd.DataFrame({"prediction": pred, "observed": y.flatten()})
lowess = sm.nonparametric.lowess
z = lowess(pred.flatten(), y.flatten())
test.plot(figsize = [14,8],
          x ="prediction", y = "observed", kind = "scatter", color = 'darkred')
plt.title("Extreme Gradient Boosting: Prediction Vs Test Data", fontsize = 18, color = "darkgreen")
plt.xlabel("Predicted Power Output", fontsize = 18) 
plt.ylabel("Observed Power Output", fontsize = 18)
plt.plot(z[:,0], z[:,1], color = "blue", lw= 3)
plt.show()