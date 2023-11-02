import numpy as np
from model_loader.load_cnn_model import *
from model_loader.load_deeper_cnn_model import *
from constant import target_labels, eng_to_chn
import matplotlib.pyplot as plt

# 利用高斯金字塔将img图像从500x500下采样到28x28像素
def image_reshape_pyramid(img, x=28, y=28):
    def image_sample_half(img, times):
        if times == 0: return img
        shape = img.shape
        img = layers.Resizing(shape[0]//2, shape[1]//2)(img)
        return image_sample_half(img, times-1)

    power = min(int(np.log2(img.shape[0] / x)), int(np.log2(img.shape[1] / y)))
    img = image_sample_half(img, power)
    img = layers.Resizing(28, 28)(img)
    img = np.log(img + 1)
    img = img / np.max(img)
    return img

class Model:
    def __init__(self, name):
        if name == 'cnn':
            self.model = load_cnn_model()
        elif name == 'deeper_cnn':
            self.model = load_deeper_cnn_model()
    def predict_table(self, x):
        x = np.expand_dims(x, axis=-1)
        x = image_reshape_pyramid(x)
        x = np.expand_dims(x, axis=0)
        # plt.imshow(x[0])
        # plt.savefig("fig.png")
        # plt.close()
        pred = self.model.predict(x, verbose=0)[0]
        top5_idxs = np.argsort(pred)[::-1][:5]
        top5_labels = target_labels[top5_idxs]
        top5_table = []
        for rk, (label, pred) in enumerate(zip(top5_labels, pred[top5_idxs])):
            top5_table.append((rk+1, label+' '+eng_to_chn[label], str(np.round(pred*100,2))+"%"))
        return top5_table