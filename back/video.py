import torch
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms as T
import back.network as network
import torch.nn as nn
from torch.multiprocessing import Pool, Process, set_start_method
import subprocess as sp
import pysrt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', help='Debug mode')
args = parser.parse_args()

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
        global args
        self.__debug = args.debug
        if not self.__debug:
            set_start_method('spawn')
            self.model = network.modeling.__dict__["deeplabv3plus_mobilenet"](num_classes=21, output_stride=16)
            set_bn_momentum(self.model.backbone, momentum=0.01)
            checkpoint = torch.load("back/models/model.pth", map_location=torch.device('cpu'))
            self.model.load_state_dict(checkpoint["model_state"])
            self.model = nn.DataParallel(self.model)
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
            self.transform = T.Compose([
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225]),
            ])
        self.width = 640
        self.height = 480
        self.color = (255, 0, 0)
        self.light = 100 * 0.01
        self.subs = None
        self.numframe = 0

    def get_segmentation(self, img, video = False):
        #обработка
        if not self.__debug:
            print('debug')
            data = None
            crop = None
            with torch.no_grad():
                self.model.eval()
                img_orig = img.copy()
                img_orig = cv2.resize(img_orig, (1920, 1080))
                img = cv2.resize(img, (self.width, self.height))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                img = self.transform(img).unsqueeze(0)
                img.to(self.device)
                outputs = self.model(img)
                preds = outputs.max(1)[1].detach().cpu().numpy()
                colorized_preds = self.cmap[preds].astype('uint8')
                colorized_preds = Image.fromarray(colorized_preds[0])
                open_cv_image = np.array(colorized_preds)
                open_cv_image = cv2.resize(open_cv_image, (self.width, self.height))
                detect = False
                gr = open_cv_image.copy()
                gr[np.all(gr == (128, 0, 0), axis=-1)] = (255,255,255)
                gray =cv2.cvtColor(gr, cv2.COLOR_BGR2GRAY)
                ret,binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
                contours,hierarchy = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)         
                rects = []
                for i in contours:
                    x,y,w,h = cv2.boundingRect(i)
                    rects.append([x, y, w, h])
                min, max, min2, max2 = 20000, 20000, 0, 0
                for r in rects:
                    if r[0] < min:
                        min = r[0]
                    if r[1] < max:
                        max = r[1]
                    if r[0] + r[2] > min2:
                        min2 = r[0] + r[2]
                    if r[1] + r[3] > max2:
                        max2 = r[1] + r[3]
                #cv2.rectangle(open_cv_image,(min,max),(min2,max2),(0,255,0),2)
                if open_cv_image[np.all(open_cv_image == (128, 0, 0), axis=-1)].any():
                    detect = True
                open_cv_image[np.all(open_cv_image == (128, 0, 0), axis=-1)] = self.color
                open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
                open_cv_image = cv2.resize(open_cv_image, (1920, 1080))
                open_cv_image = cv2.addWeighted(img_orig, 0.8, open_cv_image, self.light, 0.0)
                open_cv_image = np.array(open_cv_image)
            if video:
                gps = self.subs[self.numframe].replace(' ', '')
                gps_index = gps.index('GPS') + 3
                end = gps.index(')', gps_index)
                data = [float(coord) for coord in gps[gps_index + 1: end].split(',')]
                self.numframe += 1
            crop = np.array(open_cv_image[max*3-100:max2*3+100, min*3-100:min2*3+100])
            crop_orig = np.array(img_orig[max*3-100:max2*3+100, min*3-100:min2*3+100])
            return open_cv_image, detect, data, crop_orig, crop
        return img, False, [], None, None

    def process_subtitles(self, path):
        if not self.__debug:
            out = sp.run(['back/ffmpeg','-i', path, '-map', 's:0', '-f','webvtt','-'], stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
            self.subs = out.stdout.replace('WEBVTT\n\n', '').split('\n\n')

    def set_settings(self, params):
        #Настройки; В параметры приходит словарь: color, light
        self.color = params['color']
        self.light = params['brightness']
        self.light = self.light * 0.01
