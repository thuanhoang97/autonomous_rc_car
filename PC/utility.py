import datetime
import os
import config
import time
import math

class Logger:        
    def saveCollectionLog(timeStart, counter):
        print("Saving log to collection text file...")
        with open("log/collection_data.txt","a") as file:
            info = "==============================\n"
            info += "Time start collection: " + timeStart
            ingo += counter.toString()
            file.write(info)
        print("Save log sucessfully!")

    def saveTrainLog(n_train_data, loss, accuracy, time_start):
        print("Saving log to train file...")
        with open("log/training_log.txt","a") as file:
            info = "==============================\n"
            info += "Model config:"
            info += "\n\tNodes input: " + str(config.N_NODES_INPUT)
            info += "\n\tNodes in hidden layer: " + str(config.N_NODES_HL)
            info += "\n\tClasses: " + str(config.N_CLASSES)
            info += "\n\tEpochs: " + str(config.EPOCHS)
            info += "\n\tBatch size: " + str(config.BATCH_SIZE)
            info += "\n\tOptimizer: " + config.OPTIMIZER
            info += "\nTime start train: " + time_start +"\n"
            info += "Number data: " + str(n_train_data) + "\n"
            info += "Loss: " + str(loss) +"\n"
            info += "Accuracy: " + str(accuracy) +"\n"
            file.write(info)
        print("Save log sucessfully!")

    def getCurrentTime():
        return datetime.datetime.now().strftime("%Yy_%mm_%dd_%Hh_%Mm")



class Counter:
    def __init__(self):
        self.n_frame = 0
        self.n_forward = 0
        self.n_left = 0
        self.n_right = 0

    def upForward(self):
        self.n_forward += 1
        self.n_frame +=1
        
    def upLeft(self):
        self.n_left += 1
        self.n_frame +=1
        
    def upRight(self):
        self.n_right += 1
        self.n_frame +=1
    
    def toString(self):
        return  ("\nForward: " + str(self.n_forward) +
                "\nLeft: " + str(self.n_left) +
                "\nRight: " + str(self.n_right) +  
                "\nTotal: " + str(self.n_frame))

    def log(self):
        print(self.toString())

class Timer:
    def __init__(self):
        self.start_time = time.time()

    def getDurationInSecond(self):
        end_time = time.time()
        return math.floor(end_time-self.start_time)

    def getDurationInMinute(self):
        end_time = time.time()
        return math.floor((end_time-self.start_time)/60)
    
