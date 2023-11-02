import numpy as np
import tensorflow as tf
from pathlib import Path
from utils import test_augmentation
from constant import target_labels, PATH_DATASET

keras = tf.keras
layers = keras.layers
BATCH_SIZE = 48

ds_train, ds_val = tf.keras.utils.image_dataset_from_directory(
    directory=PATH_DATASET,
    class_names=target_labels,
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    image_size=(28,28),
    subset='both',
    seed=42
)

def convert_data(x, y):
    x = x / 255.
    y = tf.one_hot(y, depth=210)
    return x, y

ds_train = ds_train.map(convert_data, num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)
ds_val = ds_val.map(convert_data, num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)

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
model.summary()
keras.utils.plot_model(model, to_file="model.png", show_shapes=True)

model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-4), loss=keras.losses.CategoricalCrossentropy(from_logits=False),
              metrics=[keras.metrics.TopKCategoricalAccuracy(1, name="Top1"), keras.metrics.TopKCategoricalAccuracy(5, name="Top5")])

import datetime
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

checkpoint_dirpath = Path.cwd().joinpath("training")
lastest_cp_path = tf.train.latest_checkpoint(checkpoint_dirpath)
checkpoint_path = "training/cp-{epoch:04d}"+".ckpt"
# model.load_weights(lastest_cp_path)
# print(f"Load weight from {lastest_cp_path}")


cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, 
    verbose=1, 
    save_weights_only=True)

model.fit(ds_train, epochs=100, validation_data=ds_val, callbacks=[tensorboard_callback, cp_callback])