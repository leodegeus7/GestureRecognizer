from keras.models import model_from_json
import coremltools
import os
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model, model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D


model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(54, 54, 1)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(4))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model_json = model.to_json()
with open("saved_model.json", "w") as json_file:
    json_file.write(model_json)

OUTPUT_FOLDER = os.getcwd()

with open(os.path.join(os.getcwd(),"saved_model.json"), 'r') as f:
    loaded_model_json = f.read()

    keras_model = model_from_json(loaded_model_json)
    keras_model.load_weights(os.path.join(os.getcwd(),"hand_model.hdf5"))

    # convert model to Core ML
    coreml_model = coremltools.converters.keras.convert(keras_model, input_names='input', output_names='output')

    # set general model metadata
    coreml_model.author = 'Leonardo de Geus'
    coreml_model.license = 'BSD'
    coreml_model.short_description = 'Gesture recognizer'

    # set model input information
    coreml_model.input_description['input'] = 'Images'

    # set model output information
    coreml_model.output_description['output'] = 'Gesture'

    f_name, f_ext = os.path.splitext("saved_model.json")
    coreml_model.save(os.path.join(OUTPUT_FOLDER, f_name + "mlmodel"))