import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from PIL import Image
from torch.autograd import Variable
import cv2
class Classifier:
    def __init__(self):
        self.classes=['button', 'img', 'p', 'input']
        self.test_transforms = transforms.Compose([transforms.Resize((224,224)),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406], # PyTorch recommends these but in this
                                                                [0.229, 0.224, 0.225])
                                        ])
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model=models.alexnet(pretrained=True)
        self.model.classifier = nn.Sequential(nn.Linear(9216, 1024),
                                 nn.ReLU(),
                                 nn.Dropout(0.2),
                                 nn.Linear(1024, 512),
                                  nn.Linear(512, 4),
                                 nn.LogSoftmax(dim=1))
        self.model.load_state_dict(torch.load("../model/Sketch.sav"))
        self.model.eval()
        
    def Classify(self,img):
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        #im_pil= self.test_transforms(im_pil)
        index=self.Predict(im_pil)
        return self.classes[index]
    def Predict(self,img):
        image_tensor = self.test_transforms(img).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input = Variable(image_tensor)
        input = input.to(self.device)
        output = self.model(input)
        #print(output.data.cpu().numpy())
        index = output.data.cpu().numpy().argmax()
        return index