from PIL import Image
import numpy as np
import os
import cv2
import keras
import warnings
warnings.filterwarnings("ignore")
import joblib
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten

data = []
labels= []
parasitized = os.listdir("../malaria_cells_dataset/Parasitized")
for i in parasitized:
    try:
        image = cv2.imread("../malaria_cells_dataset/Parasitized/"+i)
        image_from_array= Image.fromarray(image , "RGB")
        size_image =image_from_array.resize((50,50))
        data.append(np.array(size_image))
        labels.append(0)
        
    except AttributeError as e:
        print("Error: ",e)

Uninfected = os.listdir("../malaria_cells_dataset/Uninfected")
for b in Uninfected:
    try :
        image = cv2.imread("../malaria_cells_dataset/Uninfected/"+b)
        array_image=Image.fromarray(image,"RGB")
        size_image=array_image.resize((50,50))
        resize45= size_image.rotate(15)
        resize75 = size_image.rotate(25)
        data.append(np.array(size_image))
        labels.append(1)
    except AttributeError as e:
        print("Error: ",e)

Cells =np.array(data)
labels =np.array(labels)
print(labels.shape)
print(Cells.shape)

s=np.arange(Cells.shape[0])
np.random.shuffle(s)
len_data = len(Cells)

Cells=Cells[s]
labels =labels[s]

labels =keras.utils.np_utils.to_categorical(labels)

model = Sequential()
model.add(Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(50,50,3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32,kernel_size=2,padding="same",activation ="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dense(2,activation="softmax"))
model.summary()

model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
Cells=Cells/255


model.fit(Cells,labels,batch_size=50,epochs=10,verbose=1)

joblib.dump(model,"model_malaria")