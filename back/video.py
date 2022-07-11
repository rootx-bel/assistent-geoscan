import torch
import cv2
from torchvision import models
from enum import Enum
import numpy as np

class Color(Enum):
    RED = 'Красный'
    YELLOW = 'Желтый'
    BLUE = 'Синий'
    WHITE = 'Белый'
    ORANGE = 'Оранжевый'
    GREEN = 'Зеленый'
class FrameProcessor():
    def __init__(self):
        #self.model = torch.load('models/'+'weights.pt')
        self.model = models.segmentation.deeplabv3_resnet50(pretrained = True)
        self.model.eval()
        self.color = Color.YELLOW
        self.light = 0
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    def get_segmentation(self, img):
        #обработка
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (1080, 1920))
        img = img.transpose(2, 0, 1).reshape(1, 3, 1080, 1920)
        with torch.no_grad():
            if self.device == "cuda:0":
                img_mask = self.model(torch.from_numpy(img).type(torch.cuda.FloatTensor)/255)
            else:
                img_mask = self.model(torch.from_numpy(img).type(torch.FloatTensor)/255)
        img_r = img_mask['out'].cpu().detach().numpy()[0][0]
        # if img_r > 0.01:
        #     pass
        return img_r
    def set_settings(self, params):
        #Настройки; В параметры приходит словарь: color, light
        self.color = Color(params['color'])
        self.light = params['light']
        return 0