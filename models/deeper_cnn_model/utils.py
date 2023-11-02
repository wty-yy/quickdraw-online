import numpy as np
import matplotlib.pyplot as plt
from constant import eng_to_chn, target_labels, PATH_AUG

plt.rcParams['font.family'] = ['serif', 'SimSun']
plt.rcParams['font.size'] = 25

def test_augmentation(ds, data_augmentation):
    def sample_data_augmentation(idx, x, y):
        def img_plot(ax, img):
            ax.imshow(img, cmap='gray')
            ax.axis('off')

        fig, axs = plt.subplots(5,5,figsize=(15,15))
        for i in range(5):
            for j in range(5):
                if i == 0 and j == 0:
                    img_plot(axs[0,0], x)
                else: img_plot(axs[i,j], data_augmentation(x))
        label = target_labels[np.argmax(y)]
        fig.suptitle(f"{label} {eng_to_chn[label]}")
        fig.tight_layout()
        plt.savefig(PATH_AUG.joinpath(f"{idx:02}.png"), dpi=100)
        plt.close()

    X, y = next(iter(ds))

    for i in range(32):
        sample_data_augmentation(i, X[i], y[i])