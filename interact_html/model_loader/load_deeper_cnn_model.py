import tensorflow as tf
from pathlib import Path
from constant import PATH_MODELS
keras = tf.keras
layers = keras.layers

def load_deeper_cnn_model():
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip('horizontal'),
        layers.RandomRotation(  # 随机旋转(-30,30)度
            factor=(-1/24,1/24),
            fill_mode='constant'
        ),
        layers.RandomTranslation(  # 随机平移
            height_factor=(-0.1,0.1),
            width_factor=(-0.1,0.1),
            fill_mode='constant'
        ),
        layers.RandomBrightness(  # 随机亮度变化
            factor=(-0.3,0.3),
            value_range=(0,1)
        ),
    ], name='augmentation')

    # test_augmentation(ds_train, data_augmentation)

    def build_model(inputs_shape=(28,28,1)):
        inputs = layers.Input(shape=inputs_shape, name='img')
        x = data_augmentation(inputs)
        # 卷积块1
        x = layers.Conv2D(128, kernel_size=3, padding='same', activation='relu', name='Conv1')(x)
        x = layers.Conv2D(128, kernel_size=3, padding='same', activation='relu', name='Conv2')(x)
        x = layers.Conv2D(128, kernel_size=3, padding='same', activation='relu', name='Conv3')(x)
        x = layers.MaxPool2D(pool_size=2, strides=2, name='Pool1')(x)
        # 卷积块2
        x = layers.Conv2D(256, kernel_size=3, padding='same', activation='relu', name='Conv4')(x)
        x = layers.Conv2D(256, kernel_size=3, padding='same', activation='relu', name='Conv5')(x)
        x = layers.Conv2D(256, kernel_size=3, padding='same', activation='relu', name='Conv6')(x)
        x = layers.MaxPool2D(pool_size=2, strides=2, name='Pool2')(x)
        x = layers.Flatten(name='Flatten')(x)
        # 全连接1
        x = layers.Dense(1024, activation='relu', name='Dense1')(x)
        x = layers.Dropout(0.5, name='Dropout1')(x)
        # 全连接2
        x = layers.Dense(1024, activation='relu', name='Dense2')(x)
        x = layers.Dropout(0.5, name='Dropout2')(x)
        # 输出
        outputs = layers.Dense(210, activation='softmax', name='Outputs')(x)
        return keras.Model(inputs, outputs)
    model = build_model()

    checkpoint_dirpath = PATH_MODELS.joinpath("deeper_cnn_model/training")
    lastest_cp_path = checkpoint_dirpath.joinpath("cp-0040.ckpt")
    model.load_weights(lastest_cp_path)
    print(f"权重读取地址{lastest_cp_path}")

    return model
