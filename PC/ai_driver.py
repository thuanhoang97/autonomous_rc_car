#from ANN_Train import Trainer
from ann_train import Trainer
import img_process
from control_car import Controller
import config

import cv2
import numpy as np
import glob

class AiDriver:
        def __init__(self, modelName):
                self.model = Trainer.loadModel(modelName)

        def connectToCar(self, macAddress, port, time_sleep=0.01):
                self.controller = Controller(time_sleep)
                self.controller.connectBluetooth(macAddress, port)
        def runOnDataSet(self):
                imgs, labels = Trainer.loadDataSet("train_data_test")
                num = labels.shape[0]-1
                num_sucess = 0
                for i in range(num):
                        input_data = imgs[i].reshape(1, config.N_NODES_INPUT).astype(np.float32)
                        prediction = self.model.predict(input_data)
                        print("Predict: ", prediction[0])
                        print("Actual: ", labels[i])
                        if(np.array_equal(prediction[0], labels[i])):
                                num_sucess += 1
                                print("True")
                        else:
                                print("False")
                print("Sucess: ", num_sucess, "/", num)

        def runOnImage(self, file_image):
                path = "train_images/original/" + file_image
                controller = Controller(0.075)
                for img in glob.glob(path+"/*.jpg"):
                        input("Enter to go!")
                        image = cv2.imread(img)
                        img_black,img_result = img_process.get_processed_image(image)
                        input_data = img_result.reshape(1, config.N_NODES_INPUT).astype(np.float32)
                        prediction = self.model.predict(input_data)
                        controller.showLabel(prediction[0])
                        cv2.imshow("Video", image)
                        cv2.imshow("Video processed", img_black)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

        def runCar(self):
                self.connectToCar(config.BLUETOOTH_ADDRESS, config.BLUETOOTH_PORT, 0.075)
                print("Start auto run...")
                while True:
                        try:
                                img = img_process.get_image_url(config.URl_IMAGE)
                        except IOError as err:
                                print(err)
                                print("Video err")
                                sys.exit(0)

                        img_bl,img_bl_resized = img_process.get_processed_image(img)
                        input_data = processed_image.reshape(1, config.N_NODES_INPUT).astype(np.float32)
                        prediction = self.momdel.predict(input_data)
                        self.controller.runByLabel(prediction)
                        cv2.imshow("Video", img_bl)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                print("Finished!")
                
                        
                        
if __name__ == "__main__":
        aiDriver = AiDriver("2018y_04m_23d_15h_57m")
##        aiDriver.runOnDataSet()
        aiDriver.runOnImage("2018y_04m_17d_13h_13m")                        
                
        

