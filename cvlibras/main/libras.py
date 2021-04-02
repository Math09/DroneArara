 #!/usr/bin/env python3
import cv2
import numpy as np
from keras.models import load_model
from PIL import Image 
from keras.preprocessing import image

image_x, image_y = 64,64

classifier = load_model('../models/other_models/model_epoch_61_98%_leakyRelu.h5')

classes = 4
letras = {'0' : 'A', '1' : 'B', '2' : 'C', '3' : 'L'}


def predictor():         
      test_image = Image.open('../img/img.png').convert('L')
      test_image = image.img_to_array(test_image)
      test_image = np.expand_dims(test_image, axis = 0)
      result = classifier.predict(test_image)
      maior, class_index = -1, -1

      for x in range(classes):      
         
         if result[0][x] > maior:
            maior = result[0][x]
            class_index = x
      
      #return [result, letras[str(class_index)]]
      return letras[str(class_index)]
       
    
cam = cv2.VideoCapture(0)

while True:
   ret, frame = cam.read()
   frame = cv2.flip(frame, 1)

   imggray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   img_name = "../img/img.png"
   save_img = cv2.resize(imggray, (image_x, image_y))
   cv2.imwrite(img_name, save_img)
   img_text = predictor()

   cv2.putText(frame, img_text, (10, 60), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0, 255, 0), thickness=2)
   cv2.imshow("result", frame)
      
   if cv2.waitKey(1) == 27:
     break

cam.release()
cv2.destroyAllWindows()
