class BootstrapGrid:
    def __init__(self,components,img):
        self.sub=components
        self.h,self.w=img.shape[:2]
        self.SetupGrid()
        self.PopulateGrid()
        
    def CodeGrid(self):
        code=""
        for i in range(self.rows):
            if self.CheckEmptyRowZero(i):
                continue
            code+="<div class='row'>\n"
            for j in range(self.cols):
                if(self.grid[i][j]==0):
                    code += "<div class='col-sm-1'></div>\n"
                    continue
                if(self.grid[i][j]==1 or self.grid[i][j]==-1):
                    continue
                code+="<div class='col-sm-"+str(self.grid[i][j].col_size)+"'>\n"
                c1=self.grid[i][j].Code()
                code+=c1
                #css+=css1
                code+="</div>"
            code+="</div>"
        # if(len(self.sub)==0):
        #     code+=self
        # code+=self.CloseTag();
        return code;
    def SetupGrid(self):
        self.block_size=50
        self.grid=[]
        self.rows=int(self.h/self.block_size)
        self.cols=12
        self.blockwidth=int(self.w/11)
        
        self.col_size = int(12)
        
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
        while index>=0:
            element=self.sub[index]
            index-=1
            #self.printGrid()
            i=int(element.y/self.block_size)
            j=int(element.x/self.blockwidth)
            org_i=i
            org_j=j
            print(element.attributes['tag'],"tries to be at",i,j)
            # while(self.CheckEmptyRow(i)):
            #     i-=1
            #     if(i<0):
            #         break
            # if(i<0):
            #     i=org_i
            print(i,j)
            # while(self.grid[i][j]==-1):
            #         j-=1
            #         if(j<0):
            #             j=org_j
            #             break
            #         print(i,j)
            if(self.grid[i][j]==0):
                print(element.attributes['tag'],"placed at",i,j)
                self.grid[i][j]=element
                temp=i
                while temp<element.h/self.block_size:
                    temp+=1
                    # if(self.CheckEmptyRowZero(temp)):
                    #     self.grid[int(temp)]=[1]*12
                #print(self.grid)
            
            # elif(self.grid[i][j]!=1):
            #         # if(self.attributes['tag']=='section'):
            #         #     ##the one with greater height wins
            #         #     if element.h>self.grid[i][j].h:
            #         #         self.grid[i][j]=element

            #         if(self.grid[i][j].attributes['tag']=='section'):
            #             print(element.attributes['tag'],"added as a child with",self.grid[i][j].attributes['tag'], "at",i,j)
            #             height_composite=self.grid[i][j].h+element.h+(element.y-self.grid[i][j].y)
            #             width_composite=max(element.w,self.grid[i][j].w)
            #             new_section=HTMLComponent(1,j*self.blockwidth,(i)*self.block_size,height_composite,width_composite,{"tag": "section"},-1,self,0)
            #             for e1 in self.grid[i][j].sub:
            #                 e1.parent=new_section
            #                 e1.CalcualteBlocks()
            #                 new_section.sub.append(e1)
            #             element.parent=new_section
            #             element.x -= j * self.blockwidth#-element.x
            #             element.y -= i * self.block_size#-element.
            #             element.CalcualteBlocks()
            #             new_section.sub.append(element)
            #             self.grid[i][j]=new_section
            #         #make a  composite element
            #         else:
            #             print(element.attributes['tag'],"made composite with",self.grid[i][j].attributes['tag'], "at",i,j)
            #             height_composite=self.grid[i][j].h+element.h+(element.y-self.grid[i][j].y)
            #             width_composite=max(element.w,self.grid[i][j].w)
            #             composite_element=HTMLComponent(1,j*self.blockwidth,(i+1)*self.block_size,height_composite,width_composite,{"tag": "section"},-1,self,0)
            #             self.grid[i][j].x-=j*self.blockwidth#-self.grid[i][j].x
            #             self.grid[i][j].y-=i*self.block_size#self.grid[i][j].y
            #             element.x -= j * self.blockwidth#-element.x
            #             element.y -= i * self.block_size#-element.
            #             self.grid[i][j].parent=composite_element;
            #             element.parent=composite_element;
            #             element.CalcualteBlocks()
            #             self.grid[i][j].CalcualteBlocks()
            #             composite_element.sub.append((self.grid[i][j]))
            #             composite_element.sub.append((element))
            #             composite_element.innerHTML="I'm Composite-deep copy"
            #             self.grid[i][j]=(composite_element)
            else:
                print(element.attributes['tag'], "was not placed anywhere",i,j)
                #self.grid[self.rows-1][j]=element
            if element.w/self.blockwidth > 1:
                for k in range(1,int(element.w/self.blockwidth)):
                    if j+k<12:
                        # if(self.grid[i][j+k]!=0):
                        #     break
                        self.grid[i][j+k]=-1
    