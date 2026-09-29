import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error


data = pd.read_csv(r"D:\project\SIH\dataset\anomoly.csv")
data = data.dropna()


features = ["tilt","vibration","displacement","crack_width","Tilt_change","vibration_change","prediction","crack_width_change"]
x = data[features]
y = data["Future displacement"]

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=58)
print("Model traning in process...")

rf = RandomForestRegressor(random_state=30,n_jobs=-1,n_estimators=200,max_depth= 8)
rf.fit(x_train,y_train)
print("Model sucessfully trained...")

Accuracy = rf.score(x_test,y_test)
print("Accuracy of the model = ",Accuracy*100)

y_pred = rf.predict(x_test)
print("Prediction = ",y_pred)
mae = mean_absolute_error(y_test,y_pred)
mse = mean_squared_error(y_test,y_pred)
r2 = r2_score(y_test,y_pred)

# model_performance
print("Mean_absolute_error = ",mae)
print("Mean_squared_error = ",mse)
print("R2_score = ",r2)

