import img_process
from utility import Timer
from utility import Logger
import config

import cv2
import glob
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, Flatten
from keras.models import model_from_json
from keras import optimizers
import os
import time




class Trainer:    
    def __init__(self):
        self.loss = 0.0
        self.accuracy = 0.0
        self.time_start = Logger.getCurrentTime()
        self.x_train = 0
        self.x_test = 0
        self.y_train = 0
        self.y_test = 0

    def loadDataSet(directory):
        print("Loading data...")
        timer = Timer()
        
        train_data = glob.glob(directory + '/*.npz')
        image_arr = np.zeros((1, config.N_NODES_INPUT ), 'float')
        label_arr = np.zeros((1, config.N_CLASSES), 'float')

        if not train_data:
            print("No training data in directory!")
            sys.exit()

        for file in train_data:
            print("Loading file: ", os.path.basename(file))
            with np.load(file) as data:
                train_imgs = data["train_imgs"]
                train_labels = data["train_labels"]
                print("\tTrain images: ", train_imgs.shape[0])
                print("\tTrain labels: ", train_labels.shape[0])
            image_arr = np.vstack((image_arr, train_imgs))
            label_arr = np.vstack((label_arr, train_labels))

        image_arr = image_arr[:-3,:]            
        print("\n\nTotal train images:", image_arr.shape)
        print("Total train labels:", label_arr.shape)
        print("Load data sucessfully in ", timer.getDurationInSecond(), " seconds.")
        return image_arr, label_arr


    def train(self, X, Y):
##        X, Y = Trainer.loadDataSet("train_data")
        self.x_train, self.x_test, self.y_train, self.y_test =  train_test_split(X, Y, test_size=0.2)
        print("Start tranning...")
        timer = Timer()

        model = self.getModel()
        model.compile(loss='categorical_crossentropy',
                      optimizer = config.OPTIMIZER,
                      metrics=['accuracy'])

        model.fit(self.x_train, self.y_train,
          nb_epoch = config.EPOCHS,
          batch_size = config.BATCH_SIZE)
        
        print("Trainning sucessfully in ", timer.getDurationInMinute(), " minutes.")

        self.evaluate(model)
        self.saveModel(model)
        Logger.saveTrainLog(self.x_train.shape[0], self.loss, self.accuracy, self.time_start)

    def getModel(self):
        model = Sequential()
        model.add(Dense(config.N_NODES_HL,input_dim=config.N_NODES_INPUT, init='uniform'))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(Dense(config.N_CLASSES, init='uniform')) 
        model.add(Activation('softmax'))
        return model
        
    def evaluate(self, model):
        print ('Evaluating model...')
        timer = Timer()
        
        score = model.evaluate(self.x_test, self.y_test, batch_size = config.BATCH_SIZE)
        self.loss = score[0]
        self.accuracy = score[1]

        print("Loss: ", self.loss)
        print ("Accuracy: ", self.accuracy)
        print("Evaluate sucessfully in ",timer.getDurationInSecond(), " seconds")
        
    def saveModel(self, model):
        print("Saving model....")
        # Save model as h5
        model.save_weights('ann_model/params_{}.h5'.format(self.time_start))
        
        # Save parameters to json file
        json_string = model.to_json()
        with open('ann_model/model_{}.json'.format(self.time_start), 'w') as json_file:
            json_file.write(json_string)

        print("Save model successfully!")

    def loadModel(file_name):
        model_file = "ann_model/model_" + file_name + ".json"
        params_file = "ann_model/params_" + file_name + ".h5"
        #load model
        json_file = open(model_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        #load weights
        loaded_model.load_weights(params_file)

        return loaded_model



if __name__ == '__main__':
    X, Y = Trainer.loadDataSet("train_data")
    for i in range(75):
        config.N_NODES_HL -=1
        trainer = Trainer()
        trainer.train(X , Y)
        
