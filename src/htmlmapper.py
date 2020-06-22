import numpy as np
import sys
import cv2
from edge import EdgeDetector
from classifier import Classifier
from htmlcomponent import HTMLComponent
from Grid import BootstrapGrid

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

class HtmlMapper:
    def __init__(self):
        pass
    
    def Code(self,img,path,static=False):
        components=self.ImageToComponents(img,path,True)
        code="<head>" \
          "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'></head>\n"
        if static:
            for c in components:
                code+=c.Code()
        else:
            grid=BootstrapGrid(components,img)
            code+=grid.CodeGrid()
        return code

    def ImageToComponents(self,img,path,WriteToDisk=True):
        ed=EdgeDetector(True)
        cl=Classifier()
        # kernel_sharpening = np.array([[-1, -1, -1],
        #                               [-1, 9, -1],
        #                               [-1, -1,
        #                                -1]])  # applying the sharpening kernel to the input image & displaying it.
        # img = cv2.filter2D(img, -1, kernel_sharpening)
        # img=cv2.fastNlMeansDenoisingColored(img)
        # cv2.imshow("sharpen",img)
        # cv2.waitKey()
        contours=ed.GetEdgesFromImage(img=img,canny=False)
        edges = cv2.Canny(img.copy(),100, 200,apertureSize=3,L2gradient=False)
        components=[]
        h_parent,w_parent=img.shape[:2]
        attr={'tag':'body'}
        printProgressBar(0, len(contours), prefix = 'Progress:', suffix = 'Complete', length =50)
        parent=HTMLComponent(img,0,0,h_parent,w_parent,attr,0,None)
        for n,cnt in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cnt)
            label=cl.Classify(edges[y:y+h,x:x+w])
            if(WriteToDisk):
                cv2.imwrite(path+label+str(n)+".png",img[y:y+h,x:x+w])
            attr={'tag':label}
            if(label=='input'):
                attr={'tag':label,'type':'text'}
            new_component=HTMLComponent(img[y:y+h,x:x+w],x,y,h,w,attr,1,parent,0)
            components.append(new_component)
            printProgressBar(n + 1, len(contours), prefix ="Found "+attr['tag']+' Progress:', suffix = 'Complete', length = 50)


        ##Load and Predict here in futrue
        
        

        return components
args=sys.argv[1:]
if len(args) < 1:
    sys.exit('Error!No file given!'+ '\n' + 'Arguments: <FILE_NAME>')
filename=args[0]
print("Starting the engine....")
mp=HtmlMapper()
image=cv2.imread("../images/"+filename+".png")
code=mp.Code(img=image,path="../generated/components/",static=True)
f=open("../generated/codes/1.html","w+")
f.write(code)
f.close()

        

