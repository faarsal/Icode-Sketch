import cv2
import numpy as np
class EdgeDetector:
    def __init__(self,speak=False):
        self.speak=speak
    def GetEdgesFromImage(self,img,otsu=True,canny=True):
        if self.speak:
            print("Detecting html components...")
        border_size=1
        img=cv2.copyMakeBorder(img,border_size,border_size,border_size,border_size,cv2.BORDER_CONSTANT,value=[255,255,255])
        org=img.copy()
        b1=[]
        b2=[]
        if otsu:
            img,b1=self.ApplyOtso(img,False)
        if canny:
            b2=self.ApplyCanny(img)
        boxes=self.nms(b2,b1,0.5)
        self.BoxContours(org,boxes)
        return boxes

    def ApplyCanny(self,img):
        #img=cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_CONSTANT)
        height_img, width_img = img.shape[:2]
        edges = cv2.Canny(img.copy(), 100, 200,apertureSize=3,L2gradient=False)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        new_contours=[]
        for cnt, h1 in zip(contours, hierarchy[0]):
                    x, y, w, h = cv2.boundingRect(cnt)
                    if((h>20 or w>20) and (h<height_img-10 or w<width_img-10)):
                        new_contours.append(cnt)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.imwrite("generated/canny.png", img)
        return new_contours

    def ApplyOtso(self,img,remove=False):
        height_img, width_img = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 10))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        new_contours=[]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if((h>20 or w>20) and (h<height_img-10 or w<width_img-10)):
                new_contours.append(cnt)
                cv2.rectangle(img, (x+2, y), (x + w-3, y + h), (0, 255, 199), 1)
                if remove:
                    img[y:y+h,x:x+w]=255
        cv2.imwrite("generated/otso.png", img)
        return img,new_contours


    def nms(self,otso_boxes,canny_boxes,threshold):
        boxes=[]
        for c in otso_boxes:
                x,y,w,h=cv2.boundingRect(c)
                boxes.append( (x,y,x+w,y+h))
        for c in canny_boxes:
                x,y,w,h=cv2.boundingRect(c)
                boxes.append( (x,y,x+w,y+h))
        threshold=float(threshold)
        boxes=np.array(boxes)
        # if there are no boxes, return an empty list
        if len(boxes) == 0:
            return []
        # initialize the list of picked indexes
        pick = []
        # grab the coordinates of the bounding boxes
        x1 = boxes[:,0]
        y1 = boxes[:,1]
        x2 = boxes[:,2]
        y2 = boxes[:,3]
        # compute the area of the bounding boxes and sort the bounding
        # boxes by the bottom-right y-coordinate of the bounding box
        area = (x2 - x1 + 1) * (y2 - y1 + 1)

        idxs = np.argsort(y2)
            # keep looping while some indexes still remain in the indexes
        # list
        while len(idxs) > 0:
            # grab the last index in the indexes list, add the index
            # value to the list of picked indexes, then initialize
            # the suppression list (i.e. indexes that will be deleted)
            # using the last index
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)
            suppress = [last]
            # loop over all indexes in the indexes list
            for pos in range(0, last):
                # grab the current index
                j = idxs[pos]
                # find the largest (x, y) coordinates for the start of
                # the bounding box and the smallest (x, y) coordinates
                # for the end of the bounding box
                xx1 = max(x1[i], x1[j])
                yy1 = max(y1[i], y1[j])
                xx2 = min(x2[i], x2[j])
                yy2 = min(y2[i], y2[j])
                # compute the width and height of the bounding box
                w = max(0, xx2 - xx1 + 1)
                h = max(0, yy2 - yy1 + 1)
                # compute the ratio of overlap between the computed
                # bounding box and the bounding box in the area list
                overlap = float(w * h) / area[j]
                # if there is sufficient overlap, suppress the
                # current bounding box
                overlap=float(overlap)
                if overlap > threshold:
                    suppress.append(pos)
            # delete all indexes from the index list that are in the
            # suppression list
            idxs = np.delete(idxs, suppress)
        # return only the bounding boxes that were picked
        
        p= boxes[pick]
        y1 = p[:,1]
        x1=p[:,0]
        idxx=np.lexsort((-1*x1,-1*y1))
        p=p[idxx]
        res=[]
        for i in p:
            x1,y1,x2,y2=i
            u_c=np.array([[[x1,y1]], [[x2,y1]], [[x2,y2]], [[x1,y2]]])
            res.append(u_c)
        return res        


    def BoxContours(self,img,contours):
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 1)
            # cv2.imshow("s",img[y:y+h,x:x+w])
            # cv2.waitKey()
        cv2.imwrite("labelled.png", img)



# image=cv2.imread("sample1.jpg")
# e=EdgeDetector()
# boxes=e.GetEdgesFromImage(image)
# e.BoxContours(image,boxes)


