import numpy as np
import psutil
import os
#import keras
from tensorflow.python.keras.utils.data_utils import Sequence
       
class Data_Generator_3D(Sequence):

    def __init__(self, feature_files, label_files, batch_size, dim=(249, 374,45), n_channels=1,
                 n_classes=3):
        self.files = [file for file in zip(feature_files,label_files)]
        self.x, self.y = feature_files, label_files
        self.batch_size = batch_size
        self.on_epoch_end()
    def __len__(self):
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_index1 = idx * self.batch_size
        batch_index2 = (idx + 1) * self.batch_size
        
        batch_Paths_X = self.x[batch_index1:batch_index2]
        batch_Paths_y = self.y[batch_index1:batch_index2]
        batch_x, batch_y = self.Three_D_Data_Generator(batch_Paths_X,batch_Paths_y)

        return np.array(batch_x), np.array(batch_y)
   
    def on_epoch_end(self):
        'Shuffles after each epoch'
        np.random.shuffle(self.files) 
        print("Shuffle")
        self.x = []
        self.y = []
        
        for features, label in self.files:
            self.x.append(features)
            self.y.append(label)
    
    def Get_Input(self,filename):
        img = np.load(filename)
        img = np.divide(img,255)
        return img

    def Get_Output(self,filename):    
        labels = np.genfromtxt(filename, delimiter = ',')
        return np.int_(labels)
    
    def getFilePath(self,filename):
        slashcount=0
        output_path =""
        for i, c in enumerate(reversed(filename)):
            if(c =='\\'or c =='/'):
                slashcount+=1
                
            if(slashcount== 0):
                output_path =filename[-(i+1):-4]
        
        return output_path
       
    def Three_D_Data_Generator(self,feature_files,label_files):
        BatchX = []
        BatchY = []
        
        for i,feature in enumerate(feature_files):
            if(self.getFilePath(label_files[i]) !=self.getFilePath(feature)):
                print(self.getFilePath(label_files[i]))
                print(self.getFilePath(feature))
        
        for file in feature_files:
            BatchX.append(self.Get_Input(file))
        for file in label_files:
            BatchY.append(self.Get_Output(file))
        BatchX = np.array(BatchX)
        BatchY = np.array(BatchY)
        
        
        #print(BatchX.shape)
        
        #like return but for data generators
        return (np.array(BatchX),BatchY)
    
def Predict_Data_Generator(feature_files,index):
    print(feature_files[index])
    img =np.load(feature_files[index])
    return np.expand_dims(img, axis = 0)
        
## User Guide:
#   when fitiing to data, use model.fit_generator()
#   files is a list of filepaths for all saved data
#   LabelDict should be a dictionary where the labels are the folder names and the data is in the form [0,0,0,0,0]
#   BatchSize is an integer