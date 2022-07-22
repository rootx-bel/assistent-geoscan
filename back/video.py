import torch
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms as T
import back.network as network
import torch.nn as nn
from torch.multiprocessing import set_start_method
import subprocess as sp
import argparse
from GPSPhoto import gpsphoto
import os
from PyQt5.QtCore import QThread, pyqtSignal, QSize

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
            self.source = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            self.model.to(self.source)
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

    def get_segmentation(self, img):
        #обработка
        if not self.__debug:
            data = None
            crop = None
            with torch.no_grad():
                self.model.eval()
                img_orig = img.copy()
                img_orig = cv2.resize(img_orig, (1920, 1080))
                img = cv2.resize(img, (self.width, self.height))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                img = self.transform(img).unsqueeze(0)
                img.to(self.source)
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
                if open_cv_image[np.all(open_cv_image == (128, 0, 0), axis=-1)].any():
                    detect = True
                open_cv_image[np.all(open_cv_image == (128, 0, 0), axis=-1)] = self.color
                open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
                open_cv_image = cv2.resize(open_cv_image, (1920, 1080))
                open_cv_image = cv2.addWeighted(img_orig, 0.8, open_cv_image, self.light, 0.0)
                open_cv_image = np.array(open_cv_image)
            crop = np.array(open_cv_image[max*3-100:max2*3+100, min*3-100:min2*3+100])
            crop_orig = np.array(img_orig[max*3-100:max2*3+100, min*3-100:min2*3+100])
            return open_cv_image, detect, crop_orig, crop
        return img, False, img, img

    def set_settings(self, params):
        self.color = params['color']
        self.light = params['brightness']
        self.light = self.light * 0.01

class FileProcessor():
    def __init__(self, load_path, save_path):
        self.name = 0
        self.save_path = save_path
        self.load_path = load_path
        if type(self.load_path) == str:
            self.folder_path = os.path.basename(load_path)
        else:
            self.folder_path = None
        self.subtitles = None

    def save_image(self, image, metadata = None):
        if not os.path.exists(f'{self.save_path}/{self.folder_path}'):
            os.mkdir(f'{self.save_path}/{self.folder_path}')
        path = f'{self.save_path}/{self.folder_path}/{self.name}.jpg'
        cv2.imwrite(path, image)
        self.name += 1
        if metadata is not None:
            self.save_metadata(path, metadata)

    def save_metadata(self, path, data):
        photo = gpsphoto.GPSPhoto(path)
        info = gpsphoto.GPSInfo((data[1], data[0]), alt=int(data[2]))
        photo.modGPSData(info, path)

    def load_subtitles(self):
        out = sp.run(
            ['back/ffmpeg', '-i', self.load_path, '-map', 's:0', '-f', 'webvtt','-'],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            universal_newlines=True
        )
        if out.stdout != '':
            self.subtitles = out.stdout.replace('WEBVTT\n\n', '').split('\n\n')
        else:
            self.subtitles = None

    def get_subtitles(self, frame_number):
        gps = self.subtitles[frame_number].replace(' ', '')
        gps_index = gps.index('GPS') + 3
        end = gps.index(')', gps_index)
        subtitles = [float(coord) for coord in gps[gps_index + 1: end].split(',')]
        return subtitles

class VideoThread(QThread):
    change_pixmap = pyqtSignal(np.ndarray)
    detected = pyqtSignal(bool)
    cropped = pyqtSignal(np.ndarray, np.ndarray)

    scaled_size = QSize()
    frame_processor = FrameProcessor()

    def __init__(self, source, save_path=None, parent=None):
        self.__run = True
        super().__init__(parent)
        self.source = source
        self.frame_count = 0
        self.file_processor = FileProcessor(source, save_path)

    def run(self):
        cap = cv2.VideoCapture(self.source)
        video = False
        frame_number = 0
        if type(self.source) == str and not("rtsp" in self.source) and not("http" in self.source):
            self.frame_count = int(cv2.VideoCapture.get(cap, int(cv2.CAP_PROP_FRAME_COUNT)))
            self.file_processor.load_subtitles()
            video = True

        while self.__run:
            ret, frame = cap.read()
            if ret:
                img, is_detected, crop_orig, crop = self.frame_processor.get_segmentation(frame)
                self.detected.emit(is_detected)
                if is_detected:
                    if video:
                        if self.file_processor.subtitles is not None:
                            self.file_processor.save_image(
                                img,
                                self.file_processor.get_subtitles(frame_number)    
                            )
                        else:
                            self.file_processor.save_image(img)
                    self.cropped.emit(crop_orig, crop)
                self.change_pixmap.emit(img)
            frame_number += 1

    def quit(self):
        self.__run = False
        super().quit()

    def start(self):
        self.__run = True
        super().start()

class VideoWriter():
    def __init__(self, save_path, file_name, fps = 30, frame_size = (640,480)):
        file_name = file_name.replace('.', '_')
        self.save_path = f'{save_path}/{file_name}.avi'
        self.out_stream = cv2.VideoWriter(self.save_path,cv2.VideoWriter_fourcc(*'DIVX'), fps, frame_size)
        self.frame_size = frame_size

    def addFrame(self, frame):
        resized = cv2.resize(frame, self.frame_size)
        self.out_stream.write(resized)

    def save(self):
        self.out_stream.release()

# class VideoReader(QThread):
#     change_pixmap = pyqtSignal(np.ndarray)

#     def __init__(self, source, parent=None):
#         self.__run = True
#         super().__init__(parent)
#         self.source = source

#     def run(self):
#         cap = cv2.VideoCapture(self.source)
#         while self.__run and cap.isOpened():
#             ret, frame = cap.read()
#             if ret:
#                 self.change_pixmap.emit(frame)

#     def quit(self):
#         self.__run = False
#         super().quit()

    def start(self):
        self.__run = True
        super().start()