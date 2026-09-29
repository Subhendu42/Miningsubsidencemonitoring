import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

dataset = pd.read_csv(r"D:\project\SIH\dataset\mine_subsidence_sensor_dataset.csv")
features = ["tilt","displacement","vibration","crack_width"]

data = dataset[features]
cif = IsolationForest(contamination= 0.4,random_state=42)
cif.fit(data)
print("Model Trained Sucessfully....")

data["prediction"] = cif.predict(data)
print("Model is predicting...")

data["status"] = data["prediction"].map({1 : "Normal",
                                         -1:"Abnormal"})
print("Model completed....")
print(data.head(5))


#MAP PLOTING
# sensor = dataset[dataset["sensor_id"] == "N001"]
# plt.plot(sensor["timestamp"],sensor["displacement"])
# plt.xlabel("Time")
# plt.ylabel("Displacement")
# plt.show()

#prediction dataset creation 
data["Tilt_change"] = data["tilt"].diff()
data["vibration_change"] = data["vibration"].diff()
data["crack_width_change"] = data["crack_width"].diff()


#createing csv file 
data.to_csv(
    r"D:\project\SIH\dataset\anomoly.csv",index=False
)
print("Anomoly csv successfully created...")