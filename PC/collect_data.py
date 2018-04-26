import img_process
import control_car
from utility import Counter
from utility import Logger
import model_config

import cv2
import numpy as np
import time
import os
import sys
import pygame

class Collector:
    def __init__(self):
        self.controller = None
        self.url = ""

        self.time = logger.getCurrentTime()
        self.imgOriDirect = "train_data/original/" + time
        self.imgProDirect = "train_data/processed/" + time
        os.makedirs(imgOriDirect)
        os.makedirs(imgProDirect)
        
        self.labels = = self.get_labels_present()
        self.image_arr = np.zeros((1, config.N_NODES_INPUT), 'float')
        self.label_arr = np.zeros((1, config.N_CLASSES), 'float')
        
        counter = Counter()

    def connectToCar(self, macAddress, port, time_sleep=0.01):
        self.controller = new Controller(time_sleep)
        self.controller.connectBluetooth(macAddress, port)
    
    def get_labels_present(self):
        labels = {
            "UP":[1,0,0],
            "LEFT":[0,1,0],
            "RIGHT":[0,0,1]
            }
        return labels

    def startCollectData():
        pygame.init()
        pygame.display.set_mode((100, 100))

        print("Collecting data....")
        while True:
            try:
                img = img_process.get_image_url(config.URl_IMAGE)
            except IOError as err:
                print(err)
                print("Video err")
                self.saveToFile()
                sys.exit(0)
                
            img_bl,img_bl_resized = img_process.get_processed_image(img)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    try:
                        if event.key == pygame.K_UP:
                            self.saveTrainData(img, img_bl_resized, "UP")
                            self.controller.forward()
                            self.counter.upForward()
                        elif event.key == pygame.K_LEFT:
                            self.saveTrainData(img, img_bl_resized, "LEFT")
                            self.controller.turnLeft()
                            self.counter.upLeft()
                        elif event.key == pygame.K_RIGHT:
                            self.saveTrainData(img, img_bl_resized, "RIGHT")
                            self.controller.turnRight()
                            self.counter.upRight()
                        elif event.key == pygame.K_SPACE:
                            self.counter.log()
                    except:
                        print("Bluetooth connection error!")
                        self.saveToFile()
                        sys.exit(0)
                        
            cv2.imshow("Video", img)
            cv2.imshow("Video black", img_bl)
            cv2.imshow("Video result", img_bl_resized)
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        self.saveToFile()
        pygame.display.quit()
        print("Finishing collection data!")


    def saveTrainData(self, original_image, processed_image, key_name):
        self.saveTrainInput(processed_image, key_name)
        self.saveTrainImage(original_image, processed_image)

    def saveTrainInput(self, processed_image, key_name):
        image_arr = processed_image.reshape(1, img_process.SIZE_1D).astype(np.float32)
        self.image_arr = np.vstack((self.image_arr, image_arr))
        self.label_arr = np.vstack((self.label_arr, self.labels[key_name]))

    def saveTrainImage(self, original_image, processed_image):
        cv2.imwrite((imgOriDirect+"/img{:>05}.jpg").format(self.counter.n_frame), original_image)
        cv2.imwrite((imgProDirect+"/img{:>05}.jpg").format(self.counter.n_frame), processed_image)

    def saveToFile(self):
        self.saveCollectedData()
        Logger.saveCollectionLog(self.time, self.counter)

    def saveCollectedData(self):
        print("Saving data to numpy file...")
        self.image_arr = self.image_arr[1:,:]
        self.label_arr = self.label_arr[1:,:]
        dicrectory = "train_data/" + self.time + ".npz" 
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            np.savez(directory, train_imgs = self.image_arr, train_labels = self.label_arr)
        except IOError as e:
            print(e)
            return
        print("Save sucessfully!")

       

if __name__ == "__main__":
    collector = Collector()
    collector.connectToCar(config.BLUETOOTH_ADDRESS, config.BLUETOOTH_PORT,0.075)
    collector.startCollectData()
    
