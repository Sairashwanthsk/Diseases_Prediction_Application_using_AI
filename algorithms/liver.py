import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
random_state=42
import joblib

patients=pd.read_csv("./datasets/indian_liver_patient.csv")
patients['Gender']=patients['Gender'].apply(lambda x:1 if x=='Male' else 0)
patients['Dataset'] = patients['Dataset'].apply(lambda x:1 if x==2 else 0)
patients=patients.fillna(0.94)
np.random.shuffle(patients.values)
target=patients["Dataset"]
source=patients.drop(["Dataset"],axis=1)
sm=SMOTE()
sc=StandardScaler()
lr=LogisticRegression()
source=sc.fit_transform(source)
X_train,X_test,y_train,y_test= train_test_split(source,target,test_size=0.01)
X_train, y_train=sm.fit_resample(X_train,y_train)
cv=cross_validate(lr,X_train,y_train,cv=10)
lr.fit(X_train,y_train)
joblib.dump(lr,"./model_liver")