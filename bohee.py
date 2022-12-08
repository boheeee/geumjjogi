import cv2
import numpy as np 
import pytesseract 
from PIL import Image

class Recognition:
    def ExtractNumber(self):
        Number='16.png'
        img=cv2. imread (Number, cv2. IMREAD_COLOR ) 
        img=cv2.resize(img, None, fx=1.1, fy = 1.1) 
        copy_img=img.copy() 
        img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2. GaussianBlur (img2, (3,3), 0)
        canny= cv2.Canny(blur, 100,200) 
        cv2.imshow('canny.png', canny)
        contours,hierarchy = cv2. findContours(canny, cv2.RETR_TREE, cv2. CHAIN_APPROX_SIMPLE)
        box1=[] 
        f_count = 0
        selected = 0
        plate_width=0
        
        for i in range(len(contours)):
            cnt = contours [i]
            area = cv2.contourArea(cnt)
            x,y,w, h = cv2.boundingRect (cnt)
            rect_area=w*h 
            aspect_ratio = float (w)/h # ratio - width/height
            
            if (aspect_ratio>=0.2)and(aspect_ratio<=1.0)and(rect_area>=100)and(rect_area<=400):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0, 255,0) , 1) 
                box1.append(cv2.boundingRect(cnt))

        for i in range(len(box1)): ##Buble Sort on python
            for j in range(len (box1)-(i+1)):
                if box1[j][0]>box1[j+1][0]:
                    temp=box1[j]
                    box1[j] =box1[j+1] 
                    box1[j+1]=temp
                    
        #to find number plate measuring length between rectangles
        for m in range(len(box1)):
            count=0
            for n in range(m+1,(len(box1) -1)):       
                delta_x=abs(box1[n+1][0]-box1[m][0])
                if delta_x > 150:
                    break
                delta_y =abs(box1 [n+1][1]-box1[m][1])
                if delta_x ==0:
                    delta_x=1
                if delta_y ==0:
                    delta_y=1
                gradient =float (delta_y) /float (delta_x)
                if gradient < 0.25:
                    count=count+1
#measure number plate size 
            if count > f_count:
                select = m
                f_count = count;
                plate_width=delta_x
                
        cv2.imshow('snake.png', img)
        
        number_plate=copy_img[box1[select][1]-10:box1[select][3]+box1[select][1]+20,box1[select][0]-10:140+box1[select][0]]
        resize_plate=cv2.resize(number_plate, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR) 
        plate_gray=cv2.cvtColor(resize_plate, cv2.COLOR_BGR2GRAY)
        ret, th_plate = cv2.threshold(plate_gray, 120, 255, cv2. THRESH_BINARY)
        
        kernel = np.ones((3,3),np.uint8)
        er_plate = cv2.erode (th_plate, kernel, iterations=1)
        er_plate = cv2.dilate(er_plate, kernel, iterations=1)
        
        er_invplate = er_plate
        cv2.imrite('er_plate.png',er_invplate)
        cv2.imshow ('er_plate.png' ,er_invplate)
        result = pytesseract.image_to_string(Image.open('er_plate.png'), lang='kor')
        li = list(result)
        
        for number in range(len(li)):
            if number > 7:
                li[number] = ' '
                continue
            if li[number].isalpha():
                continue
            if li[number].isdigit():
                continue
            else:
                li[number] = ' '
        result = ''.join(li)
        return (result.replace(" ",""))
    
recogtest = Recognition()
result = recogtest.ExtractNumber()
    
print(result)