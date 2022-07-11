import torch
import cv2
from torchvision import models
from enum import Enum
import numpy as np
from PIL import Image

class Color(Enum):
    RED = 'Красный'
    YELLOW = 'Желтый'
    BLUE = 'Синий'
    WHITE = 'Белый'
    ORANGE = 'Оранжевый'
    GREEN = 'Зеленый'

def voc_cmap(N=256, normalized=False):
    def bitget(byteval, idx):
        return ((byteval & (1 << idx)) != 0)

    dtype = 'float32' if normalized else 'uint8'
    cmap = np.zeros((N, 3), dtype=dtype)
    for i in range(N):
        r = g = b = 0
        c = i
        for j in range(8):
            r = r | (bitget(c, 0) << 7-j)
            g = g | (bitget(c, 1) << 7-j)
            b = b | (bitget(c, 2) << 7-j)
            c = c >> 3

        cmap[i] = np.array([r, g, b])

    cmap = cmap/255 if normalized else cmap
    return cmap

class FrameProcessor():
    
    cmap = voc_cmap()

    def __init__(self):
        self.model.load_state_dict(torch.load("/models/model.pth"))['model_state']
        self.color = Color.YELLOW
        self.light = 0
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.eval()
        self.width = 640
        self.height = 480

    def get_segmentation(self, img):
        #обработка
        img = cv2.resize(img, (self.width, self.height))
        outputs = self.model(img)
        preds = outputs.max(1)[1].detach().cpu().numpy()
        colorized_preds = self.cmap[preds].astype('uint8')
        colorized_preds = Image.fromarray(colorized_preds[0])
        return img

    def set_settings(self, params):
        #Настройки; В параметры приходит словарь: color, light
        self.color = Color(params['color'])
        self.light = params['light']
        return 0