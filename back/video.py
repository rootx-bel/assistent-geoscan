import torch
import cv2
from torchvision import models
from enum import Enum
import numpy as np
from PIL import Image
from torchvision import transforms as T
import back.network as network
import torch.nn as nn

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

def set_bn_momentum(model, momentum=0.1):
    for m in model.modules():
        if isinstance(m, nn.BatchNorm2d):
            m.momentum = momentum

class FrameProcessor():
    
    cmap = voc_cmap()

    def __init__(self):
        self.model = network.modeling.__dict__["deeplabv3plus_mobilenet"](num_classes=21, output_stride=16)
        set_bn_momentum(self.model.backbone, momentum=0.01)
        checkpoint = torch.load("back/models/model.pth", map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint["model_state"])
        self.model = nn.DataParallel(self.model)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        self.width = 640
        self.height = 480
        self.color = Color.YELLOW
        self.light = 0
        self.transform = T.Compose([
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225]),
            ])

    def get_segmentation(self, img):
        #обработка
        with torch.no_grad():
            self.model.eval()
            img = cv2.resize(img, (self.width, self.height))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = self.transform(img).unsqueeze(0)
            img.to(self.device)
            outputs = self.model(img)
            preds = outputs.max(1)[1].detach().cpu().numpy()
            colorized_preds = self.cmap[preds].astype('uint8')
            colorized_preds = Image.fromarray(colorized_preds[0])
            open_cv_image = np.array(colorized_preds)
        return open_cv_image

    def set_settings(self, params):
        #Настройки; В параметры приходит словарь: color, light
        self.color = Color(params['color'])
        self.light = params['light']
        return 0