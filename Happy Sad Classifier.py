

# Below is code to a happy or sad dataset which contains 80 images, 40 happy and 40 sad. 



import tensorflow as tf
import os
import zipfile
from os import path, getcwd, chdir


path = f"{getcwd()}/../tmp2/happy-or-sad.zip"

zip_ref = zipfile.ZipFile(path, 'r')
zip_ref.extractall("/tmp/h-or-s")
zip_ref.close()



def train_happy_sad_model():
   
    DESIRED_ACCURACY = 0.999

    class myCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self,epoch,logs={}):
            if(logs.get('acc')>0.999):
                print("\nReached 99.9% accuracy so cancelling training")
                self.model.stop_training=True
        
         
            

    callbacks = myCallback()
    
    # This Code Block should Define and Compile the Model. Please assume the images are 150 X 150 in your implementation.
    model = tf.keras.models.Sequential([
        
        tf.keras.layers.Conv2D(16,(3,3),activation='relu',input_shape=(150,150,3)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(150,150,3)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(64,(3,3),activation='relu',input_shape=(150,150,3)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512,activation='relu'),
        tf.keras.layers.Dense(1,activation='sigmoid')

    ])

    from tensorflow.keras.optimizers import RMSprop

    model.compile(loss='binary_crossentropy',optimizer=RMSprop(lr=0.001),metrics=['accuracy'])
        

    # This code block should create an instance of an ImageDataGenerator called train_datagen 
    # And a train_generator by calling train_datagen.flow_from_directory

    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    train_datagen = ImageDataGenerator(rescale=1./255)

    # Please use a target_size of 150 X 150.
    train_generator = train_datagen.flow_from_directory("/tmp/h-or-s",
                                                        target_size=(150,150),
                                                        batch_size=10,
                                                        class_mode='binary'
                    )
    
    # This code block should call model.fit_generator and train for
    # a number of epochs.
    # model fitting
    history = model.fit_generator(
          train_generator,
          steps_per_epoch=8,
          epochs=15,callbacks=[callbacks]
          
    )
    # model fitting
    return history.history['acc'][-1]



train_happy_sad_model()


