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
        #self.model = models.segmentation.deeplabv3_resnet50(pretrained = True)
        self.color = Color.YELLOW
        self.light = 0
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def get_segmentation(self, img):
        #обработка
        return img

    def set_settings(self, params):
        #Настройки; В параметры приходит словарь: color, light
        self.color = Color(params['color'])
        self.light = params['light']
        return 0