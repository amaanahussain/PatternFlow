import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.regularizers import l2

LEAKY_RELU_ALPHA = 0.01
DROPOUT = 0.35
L2_WEIGHT_DECAY = 0.0005
CONV_PROPERTIES = dict(
    kernel_regularizer=l2(L2_WEIGHT_DECAY),
    bias_regularizer=l2(L2_WEIGHT_DECAY),
    padding="same")


def improved_unet(width, height, channels):
    input = keras.Input(shape=(width, height, channels))

    x1 = keras.layers.Conv2D(16, (3, 3), **CONV_PROPERTIES, input_shape=(width, height, channels))(input)
    x2 = keras.layers.BatchNormalization()(x1)
    x3 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x2)
    x4 = context_module(x3, 16)
    x5 = keras.layers.Add()([x3, x4])

    x6 = keras.layers.Conv2D(32, (3, 3), **CONV_PROPERTIES, strides=2)(x5)
    x7 = keras.layers.BatchNormalization()(x6)
    x8 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x7)
    x9 = context_module(x8, 32)
    x10 = keras.layers.Add()([x8, x9])

    x11 = keras.layers.Conv2D(64, (3, 3), **CONV_PROPERTIES, strides=2)(x10)
    x12 = keras.layers.BatchNormalization()(x11)
    x13 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x12)
    x14 = context_module(x13, 64)
    x15 = keras.layers.Add()([x13, x14])

    x16 = keras.layers.Conv2D(128, (3, 3), **CONV_PROPERTIES, strides=2)(x15)
    x17 = keras.layers.BatchNormalization()(x16)
    x18 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x17)
    x19 = context_module(x18, 128)
    x20 = keras.layers.Add()([x18, x19])

    x21 = keras.layers.Conv2D(256, (3, 3), **CONV_PROPERTIES, strides=2)(x20)
    x22 = keras.layers.BatchNormalization()(x21)
    x23 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x22)
    x24 = context_module(x23, 256)
    x25 = keras.layers.Add()([x23, x24])
    x26 = upsampling_module(x25, 128)

    x27 = keras.layers.Concatenate()([x20, x26])
    x28 = localisation_module(x27, 128)
    x29 = upsampling_module(x28, 64)

    x30 = keras.layers.Concatenate()([x15, x29])
    x31 = localisation_module(x30, 64)
    x32 = upsampling_module(x31, 32)

    x33 = keras.layers.Concatenate()([x10, x32])
    x34 = localisation_module(x33, 32)
    x35 = upsampling_module(x34, 16)

    x36 = keras.layers.Concatenate()([x5, x35])
    x37 = keras.layers.Conv2D(32, (3, 3), **CONV_PROPERTIES)(x36)
    x38 = keras.layers.BatchNormalization()(x37)
    x39 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x38)

    u1 = upsampling_module(x31, 32)
    s1 = keras.layers.Add()([u1, x34])
    u2 = upsampling_module(s1, 32)
    s2 = keras.layers.Add()([u2, x39])

    output = keras.layers.Conv2D(1, (1, 1), activation="sigmoid", **CONV_PROPERTIES)(s2)
    u_net = keras.Model(inputs=[input], outputs=[output])
    return u_net


def context_module(input, out_filter):
    x1 = keras.layers.Conv2D(out_filter, (3, 3), **CONV_PROPERTIES)(input)
    x2 = keras.layers.BatchNormalization()(x1)
    x3 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x2)
    x4 = keras.layers.Dropout(DROPOUT)(x3)
    x5 = keras.layers.Conv2D(out_filter, (3, 3), **CONV_PROPERTIES)(x4)
    x6 = keras.layers.BatchNormalization()(x5)
    x7 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x6)
    return x7


def upsampling_module(input, out_filter):
    x1 = keras.layers.UpSampling2D(size=(2, 2))(input)
    x2 = keras.layers.Conv2D(out_filter, (3, 3), **CONV_PROPERTIES)(x1)
    x3 = keras.layers.BatchNormalization()(x2)
    x4 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x3)
    return x4


def localisation_module(input, out_filter):
    x1 = keras.layers.Conv2D(out_filter, (3, 3), **CONV_PROPERTIES)(input)
    x2 = keras.layers.BatchNormalization()(x1)
    x3 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x2)
    x4 = keras.layers.Conv2D(out_filter, (1, 1), **CONV_PROPERTIES)(x3)
    x5 = keras.layers.BatchNormalization()(x4)
    x6 = keras.layers.LeakyReLU(alpha=LEAKY_RELU_ALPHA)(x5)
    return x6


if __name__ == "__main__":
    print("Please run 'test_driver.py, not 'layers_model.py'.'")
    exit(1)
