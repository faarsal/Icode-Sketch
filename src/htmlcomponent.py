import numpy as np
import cv2
import copy
from operator import itemgetter
from PIL import Image
from collections import Counter


class HTMLComponent:
    def __init__(self, img, x, y, h, w, attributes,id,parent=None, text=0):
        self.value = ""
        self.img = img
        self.id=str(attributes['tag'])+str(id)
        # noinspection PyDictCreation
        self.styles = {}
        self.attributes = attributes
        self.classes = []
        self.parent = parent
        if(type(self.img)!=int):
            w = img.shape[1]
            h = img.shape[0]
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.setBSclass()
        self.bgcolor = (255, 255, 255)
        self.color = (0, 0, 0)
        # self.cnt = cnt
        self.path = ""
        self.sub = []  # sub elements
        self.innerHTML = self.get_inner_html()
        self.assignAbsPosition()
        #self.setDominantColor()
        #self.SetBorderColor()
        self.SetupGrid()
        


    def setImage(self, img):
        self.img = img
    def setBSclass(self):
        self.attributes['class']=""
        if(self.attributes['tag']=='button'):
            self.attributes['class']='btn btn-primary'
        if (self.attributes['tag'] == 'input'):
            self.attributes['class'] = 'form-control'
        if(self.attributes['tag']=='img'):
            self.attributes['class'] = 'img-fluid'
        # if(self.attributes['tag']=='ul'):
        #     self.attributes['class'] = 'list-group'
        
        # if(self.attributes['tag'] not in ["section","div","body"] ):
        #     self.attributes['class'] +=" w-100"
    def SetBorderColor(self):
        colors=[]
        if(type(self.img)==int):
            return None
        w = self.img.shape[1]
        for i in range(w):
            colors.append(self.img[0][i])
        sum=np.array([0,0,0])
        for i in range(len(colors)):
            sum=np.add(colors[i],sum)
        color=sum/len(colors)
        if 255-color[0] >10 or 255-color[1]>10 or 255-color[2]>10:
            color[0]-=40
            color[1]-=40
            color[2]-=40
        self.styles['border-color']='rgb('+str(int(color[2]))+','+str(int(color[1]))+','+str(int(color[0]))+')'
        return color
    def CalcualteBlocks(self):
        self.block_size=1
        self.col_size = int(self.w / self.parent.blockwidth)
    def SetupGrid(self):
        #block size is 50x50
        self.block_size=1
        self.grid=[]
        self.rows=int(self.h/self.block_size)+2
        self.cols=12
        self.blockwidth=int(self.w/12)
       

        if(self.parent!=None):
            self.col_size = int(self.w / self.parent.blockwidth)
        else:
            self.col_size=12
        
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                self.grid[i].append(0)
    
    def CheckEmptyRow(self,i):
        if(i<self.rows):
            for j in self.grid[i]:
                if(type(j)!=int or j!=1):
                    return False;
        return True; 
    def CheckEmptyRowZero(self,i):
        if(i<self.rows):
            for j in self.grid[i]:
                if(type(j)!=int or j!=0):
                    return False;
        return True; 
    def PopulateGrid(self):
        index=len(self.sub)-1
        # if(self.attributes['tag']=='section'):
        #     self.rows=len(self.sub)
        #     self.block_size=self.h/self.rows
        print("Populting grid of element:",self.attributes['tag'],"rows",self.rows,self.cols)
        while index>=0:
            element=self.sub[index]
            index-=1
            self.printGrid()
            i=int(element.y/self.block_size)
            if i>0:
                i-=1
            j=int(element.x/self.blockwidth)
            if j>=12:
                j=11
            org_i=i
            org_j=j
            print(element.attributes['tag'],"tries to be at",i,j)
            while(self.CheckEmptyRow(i)):
                i-=1
                if(i<0):
                    break
            if(i<0):
                i=org_i
            print(i,j)
            while(self.grid[i][j]==-1):
                    j-=1
                    if(j<0):
                        j=org_j
                        break
                    print(i,j)
            if(self.grid[i][j]==0):
                print(element.attributes['tag'],"placed at",i,j)
                self.grid[i][j]=element
                temp=i
                while temp<element.h/self.block_size:
                    temp+=1
                    if(self.CheckEmptyRowZero(temp)):
                        self.grid[int(temp)]=[1]*12
                #print(self.grid)
            
            elif(self.grid[i][j]!=1):
                    if(self.attributes['tag']=='section'):
                        ##the one with greater height wins
                        if element.h>self.grid[i][j].h:
                            self.grid[i][j]=element

                    elif(self.grid[i][j].attributes['tag']=='section'):
                        print(element.attributes['tag'],"added as a child with",self.grid[i][j].attributes['tag'], "at",i,j)
                        height_composite=self.grid[i][j].h+element.h+(element.y-self.grid[i][j].y)
                        width_composite=max(element.w,self.grid[i][j].w)
                        new_section=HTMLComponent(1,j*self.blockwidth,(i)*self.block_size,height_composite,width_composite,{"tag": "section"},-1,self,0)
                        for e1 in self.grid[i][j].sub:
                            e1.parent=new_section
                            e1.CalcualteBlocks()
                            new_section.sub.append(e1)
                        element.parent=new_section
                        element.x -= j * self.blockwidth#-element.x
                        element.y -= i * self.block_size#-element.
                        element.CalcualteBlocks()
                        new_section.sub.append(element)
                        self.grid[i][j]=new_section
                    #make a  composite element
                    else:
                        print(element.attributes['tag'],"made composite with",self.grid[i][j].attributes['tag'], "at",i,j)
                        height_composite=self.grid[i][j].h+element.h+(element.y-self.grid[i][j].y)
                        width_composite=max(element.w,self.grid[i][j].w)
                        composite_element=HTMLComponent(1,j*self.blockwidth,(i+1)*self.block_size,height_composite,width_composite,{"tag": "section"},-1,self,0)
                        self.grid[i][j].x-=j*self.blockwidth#-self.grid[i][j].x
                        self.grid[i][j].y-=i*self.block_size#self.grid[i][j].y
                        element.x -= j * self.blockwidth#-element.x
                        element.y -= i * self.block_size#-element.
                        self.grid[i][j].parent=composite_element;
                        element.parent=composite_element;
                        element.CalcualteBlocks()
                        self.grid[i][j].CalcualteBlocks()
                        composite_element.sub.append((self.grid[i][j]))
                        composite_element.sub.append((element))
                        composite_element.innerHTML="I'm Composite-deep copy"
                        self.grid[i][j]=(composite_element)
            else:
                print(element.attributes['tag'], "was not placed anywhere",i,j)
                #self.grid[self.rows-1][j]=element
            if element.col_size > 1:
                for k in range(1,element.col_size):
                    if j+k<12:
                        if(self.grid[i][j+k]!=0):
                            break
                        self.grid[i][j+k]=-1
    def printGrid(self):
        for i in range(self.rows):
            for j in range(12):
                if(type(self.grid[i][j])!=int):
                    print(self.grid[i][j].attributes['tag'],end=" ")
                else:
                    print(self.grid[i][j],end=" ")
            print("")
            
    def CodeGrid(self):
        code=self.StartTag()
        css=self.getCSSCode()
        for i in range(self.rows):
            code+="<div class='row'>\n"
            for j in range(self.cols):
                if(self.grid[i][j]==0):
                    code += "<div class='col-sm-1'></div>\n"
                    continue
                if(self.grid[i][j]==1 or self.grid[i][j]==-1):
                    continue
                code+="<div class='col-sm-"+str(self.grid[i][j].col_size)+"'>\n"
                c1,css1=self.grid[i][j].CodeGrid()
                code+=c1
                css+=css1
                code+="</div>"
            code+="</div>"
        if(len(self.sub)==0):
            code+=self.innerHTML
        code+=self.CloseTag();
        return code,css;

    def assignAbsPosition(self):
        self.styles['left'] = str(self.x) + "px"
        self.styles['top'] = str(self.y) + "px"
        self.styles['width'] = str(self.w) + "px"
        self.styles['height'] = str(self.h) + "px"
        self.styles['display'] = "block"
        self.styles['position'] = "absolute"
        self.styles['text-align'] = "center"

    def getStyle(self):
        return self.styles

    def get_inner_html(self, ocr=0):
        if(self.attributes['tag']=='button'):
            return 'Button'
        s = "a"*int(self.w/10)
        if ocr == 0:
            return self.getRandomText(len(s))
        elif ocr == 1:
            return s
        else:
            return "{" + self.attributes['tag'] + "}"

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y

    def getRandomText(self, n):
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pretium mauris enim, at congue lacus " \
               "accumsan at. Integer vel suscipit neque. Integer eu dolor in mi consequat tincidunt sed non augue. " \
               "Nullam condimentum mi tempus leo maximus, vel bibendum odio tempor. Nunc convallis dignissim ex, " \
               "a aliquam orci commodo non. Integer lacinia fringilla est ut mollis. Aenean dignissim metus eget " \
               "augue pulvinar, ac vulputate nisl mattis. Ut non elementum dolor. Aliquam dictum finibus gravida. " \
               "Quisque elementum mauris felis, ac facilisis enim porta ac.";
        while n > len(text):
            text *= 2
        return text[0:n]

    def AddSubElement(self, e):
        self.sub.append(e)

    def getSubElements(self):
        return self.sub

    def getImage(self):
        return self.img

    def getCoordinates(self):
        return self.x, self.y

    def getAttributes(self):
        return self.x, self.y, self.w, self.h

    def setPath(self, p):
        self.path = p

    def getColors(self):
        return (self.bgcolor[2], self.bgcolor[1], self.bgcolor[0]), (self.color[2], self.color[1], self.color[0]);

    def setDominantColor(self):
        # You may need to convert the color.
        if type(self.img)==int:
            return
        my_img = np.array(self.img, dtype=np.uint8)
        my_img = cv2.cvtColor(my_img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(my_img)
        # For reversing the operation:
        # im_np = np.asarray(im_pil)
        my_colours = pil_image.getcolors(100000)
        if my_colours:
            self.styles['background-color'] = "rgb" + str(max(my_colours, key=itemgetter(0))[1])
            self.bgcolor = max(my_colours, key=itemgetter(0))[1];
            my_colours.remove(max(my_colours, key=itemgetter(0)))
            if my_colours:
                self.styles['color'] = "rgb" + str(max(my_colours, key=itemgetter(0))[1])
                self.color = max(my_colours, key=itemgetter(0))[1];
            else:
                self.styles['color'] = "white"
        else:
            self.styles['background-color'] = "white"

        return

    def set_shape(self, approx):
        if len(approx) <= 5:
            # self.styles['shape'] = "rectangle"
            self.styles['border-radius'] = str(len(approx) * 0) + "px"
        else:
            # self.styles['shape'] = "round"
            self.styles['border-radius'] = str(len(approx) * 3) + "px"
        return


    def StartTag(self):
        code = "<"
        for key, value in self.attributes.items():
            if key == "tag":
                code += value + " "
            else:
                code += key + "='" + value + "' "

        code+=" id='"+str(self.id)
        # for key, value in self.styles.items():
        #     code += key + ": " + str(value) + ";"
        return code + "'>\n";

    def CloseTag(self):
        if self.attributes['tag'] != "input" and self.attributes['tag'] != "img":
            return "</" + self.attributes['tag'] + ">\n"
        else:
            return "\n"
    def getCSSCode(self):
        code="#"+str(self.id)+"{\n"
        for key, value in self.styles.items():
            code += key + ": " + value + ";"+"\n"
        code+="}\n"
        return code
    def Code(self):
        #      self.styles[]
        code = "<" + \
               self.attributes['tag'] + \
               " id='"+str(self.id)+"'style='"
        for key, value in self.styles.items():
            code += key + ": " + value + ";"
        code=code[:len(code)-1]
        code+="'class='"+self.attributes['class']
        if self.attributes['tag'] != "input" and self.attributes['tag'] != "img":
            code += "'>" + self.innerHTML + "</" + self.attributes['tag'] + ">\n"
        elif self.attributes['tag'] == 'img':
            code += "' src='./images/default_image.png'>"
        else:
            code += "'>"
        return code
