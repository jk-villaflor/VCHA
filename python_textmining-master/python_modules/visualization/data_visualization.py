from builtins import list

from db.postgresl import PropertyDAO
import matplotlib.pyplot as plt
import pandas as pd  # pip install tables
import seaborn as sns


property_dao = PropertyDAO()

where = ' where bedrooms > 0 and bedrooms < 5 and size_sqft < 5000 and price < 6000 and bath < 5'
properties = property_dao.getDataFrameRecords(where)


print(properties.head())
print(list(properties))

#Bar Charts    
sns.distplot(properties['bedrooms'], bins=10, kde=False)
plt.figure()
sns.distplot(properties['bath'], bins=10, kde=False)
plt.figure()
sns.distplot(properties['size_sqft'], bins=10, kde=False)
plt.figure()
sns.distplot(properties['price'], bins=10, kde=False)
plt.figure()

#BoxPlots
sns.boxplot( y=properties['bedrooms'])
plt.figure()
sns.boxplot( y=properties['bath'])
plt.figure()
sns.boxplot( y=properties['size_sqft'])
plt.figure()
sns.boxplot( y=properties['price'])

#show plots
plt.show()
