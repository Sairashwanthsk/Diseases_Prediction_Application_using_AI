import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

data=pd.read_csv("./datasets/indian_liver_patient.csv")
data=data.fillna(method="ffill")
data['Gender'] = data['Gender'].apply(lambda x:1 if x=='Male' else 0)
data['Dataset'] = data['Dataset'].apply(lambda x:1 if x==2 else 0)
data['Total_Bilirubin'] = np.log(data["Total_Bilirubin"])
data['Direct_Bilirubin'] = np.log(data["Direct_Bilirubin"])
data['Alkaline_Phosphotase'] = np.log(data["Alkaline_Phosphotase"])
data['Alamine_Aminotransferase'] = np.log(data["Alamine_Aminotransferase"])
data['Aspartate_Aminotransferase'] = np.log(data["Aspartate_Aminotransferase"])
data['Total_Protiens'] = np.log(data["Total_Protiens"])
data['Albumin'] = np.log(data["Albumin"])
data['Albumin_and_Globulin_Ratio'] = np.log(data["Albumin_and_Globulin_Ratio"])

# X=data[['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin',
#        'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
#        'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin',
#        'Albumin_and_Globulin_Ratio']]
# y=data['Dataset']

# X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=123)
target=data["Dataset"]
data=data.drop(["Dataset"],axis=1)

# print(results)
# print("Accuracy:",results.mean()*100)
sm=SMOTE()
sc=StandardScaler()
data=sc.fit_transform(data)

lr=LogisticRegression()
lr.fit(data,target)

cv_results = cross_validate(lr, data,target, cv=10)
print(cv_results)
# print(cv)
joblib.dump(lr,"./model_liver")



