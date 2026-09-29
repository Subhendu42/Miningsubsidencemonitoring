import pandas as pd

df = pd.read_csv(r"D:\project\SIH\dataset\anomoly.csv")

def normalize(safe,critical,value):
    if(safe == critical):
        return 0.0
    score = ((value - safe)/(critical - safe))*100
    score = max(0,min(100,score))
    return score


limits = {
    "displacement" : {
        "safe" : 0.0,
        "critical" : 10.0
    },
    "tilt" : {
            "safe" : 0.0,
            "critical" : 10.0
        },
        "crack" : {
                "safe" : 0.0,
                "critical" : 10
            },
            "vibration" : {
                    "safe" : 0.0,
                    "critical" : 10.0
                },
                "future_displacement" : {
                        "safe" : 0.0,
                        "critical" : 10.0
                    },
}

def anomaly(prediction):
    if (prediction == 1):
        anomaly_score = 0
        return anomaly_score
    elif (prediction == -1):
        anomaly_score = 1
        return anomaly_score

for index,row in df.iterrows():


    displacement = row["displacement"]
    tilt = row["tilt"]
    vibration = row["vibration"]
    crack = row["crack_width"]
    future_displacement = row["Future displacement"]
    prediction = row["prediction"]




    displacement_score = normalize(limits["displacement"]["safe"],limits["displacement"]["critical"],displacement)
    tilt_score = normalize(limits["tilt"]["safe"],limits["tilt"]["critical"],tilt)
    vibration_score = normalize(limits["vibration"]["safe"],limits["vibration"]["critical"],vibration)
    crack_score = normalize(limits["crack"]["safe"],limits["crack"]["critical"],crack)
    anomaly_score = anomaly(prediction)
    future_displacement_score = normalize(limits["future_displacement"]["safe"],limits["future_displacement"]["critical"],future_displacement)



    risk_percentage = (displacement_score*0.20 + tilt_score*0.15+vibration_score*0.15+crack_score*0.20+future_displacement_score*0.20+anomaly_score*100*0.10 )
    risk_percentage = max(0,min(100,risk_percentage))
    print("Risk-Percentage = ",risk_percentage)


    if risk_percentage <= 30:
        risk_level = "low"
    elif risk_percentage<= 60:
        risk_level = "medium"
    elif risk_percentage <= 80:
        risk_level = "high"
    elif risk_percentage >80:
        risk_level = "critical"

    df.loc[index,"risk_percentage"] = round(risk_percentage,2)
    df.loc[index,"risk_level"] = risk_level
df.insert(0,"Sl.No",range(1,len(df)+1))
df.to_csv(r"D:\project\SIH\dataset\risk_result.csv",index=False)

