 #!/usr/bin/env python3


import cv2
import numpy as np
from keras.models import load_model
from PIL import Image 
from keras.preprocessing import image
import rospy
from std_msgs.msg import String
import tensorflow as tf

image_x, image_y = 64,64

classifier = load_model('../models/other_models/model_epoch_48_98.6_final.h5')

classes = 21
letras = {'0' : 'A', '1' : 'B', '2' : 'C', '3': 'D', '4': 'E', '5':'F', '6':'G', '7': 'G', '8':'I', '9':'L', '10':'M', '11': 'N', '12':'O', '13':'P', '14':'Q', '15':'R', '16':'S', '17':'T', '18':'U', '19':'V','20':'W', '21':'Y'}

letras_de_movimento = [
    'A',
    'B',
    'C',
    'D',
    'L'
]

def predictor():  
    try:        
        test_image = Image.open('../img/img.png').convert('L')
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = classifier.predict(test_image)
        maior, class_index = -1, -1

        for x in range(classes):      
            
            if result[0][x] > maior:
                maior = result[0][x]
                class_index = x

        rec = letras[str(class_index)]
        if( rec in letras_de_movimento ):
            publisher = rospy.Publisher( '/writing', String, queue_size=10 )
            publisher.publish( rec )
            rospy.loginfo( rec )
        #return [result, letras[str(class_index)]]
        return rec
    except rospy.ROSInterruptException:
        pass

  
cam = cv2.VideoCapture(0)

while True:
   ret, frame = cam.read()
   frame = cv2.flip(frame, 1)

   
   imggray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   img = cv2.rectangle(frame, (425,100),(625,300), (0,255,0), thickness=2, lineType=8, shift=0)
   imcrop = img[102:298, 427:623]

   img_name = "../img/img.png"
   save_img = cv2.resize(imggray, (image_x, image_y))
   cv2.imwrite(img_name, save_img)
   img_text = predictor()

   cv2.putText(frame, img_text, (10, 60), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0, 255, 0), thickness=2)

#    cv2.imshow("result", frame)
   cv2.imshow("ROI", imcrop)
   cv2.imshow("FRAME", frame)
  

   if cv2.waitKey(1) == 27:
     break

cam.release()
cv2.destroyAllWindows()


class drone():
    def __init__(move):

        move.session = tf.compact.v1.keras.backend.get_session()

        self.model == tf.keras.Sequential()

    def predict(move, x):
        
        with self.session.graph.as_default():
            tf.compact.v1.keras.backend.set_session(move.session)
            out = move.model.predict(x)
            return out

class roslibras():
    def __init__(move):
        move.wrapped_model = drone()


def main():
            rospy.init_node("ros_tensoflow")
            ri = roslibras()
            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                rate.sleep()

if __name__ == '__main__':
      main()
  
       