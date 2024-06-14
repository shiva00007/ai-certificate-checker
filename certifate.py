from flask import Flask, render_template, request
import cv2
import os
import tempfile
    
import tensorflow as tf
# Load the trained machine learning model
model = tf.keras.models.load_model('keras_model.h5')

app = Flask(__name__)

@app.route('/')
def home():
    # image_names = os.listdir('E:/Finalcode/templates/images/logo.svg')

    return render_template('index.html')
@app.route('/certi')
def certi():
    # image_names = os.listdir('E:/Finalcode/templates/images/logo.svg')

    return render_template('home.html')

@app.route('/predict', methods=['POST'])

def predict():
    # Get the uploaded certificate image file
    certificate_file = request.files['certificate']

    # Save the certificate image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    certificate_file.save(temp_file.name)
    certificate_file_path = temp_file.name

    # Preprocess the certificate image
    image = cv2.imread(certificate_file_path)

    # Resize the image to a fixed size
    resized_image = cv2.resize(image, (224, 224))

    # Normalize the pixel values to the range [0, 1]
    normalized_image = resized_image / 255.0

    # Expand the dimensions of the image to match the input shape of the model
    expanded_image = tf.expand_dims(normalized_image, axis=0)

    # Use the machine learning model to classify the certificate
    prediction = model.predict(expanded_image)
    print(prediction )
    print(prediction[0])
    print(prediction[0][0])


    # Interpret the model output and display the verification result
    if prediction[0][0] >= 0.5993142:
        result = 'Genuine certificate'
        return render_template('result.html', prediction='Genuine certificate')

    else:
        result = 'Fake certificate'
        return render_template('result.html', prediction='Fake certificate')

    # Remove the temporary file
    # os.unlink(certificate_file_path)

    # return render_template('result.html', prediction=prediction[0][0] )
def preprocess_certificate_image(certificate_file):
    # Read the uploaded image file using OpenCV
    image = cv2.imread(certificate_file)

    # Resize the image to a fixed size
    resized_image = cv2.resize(image, (224, 224))

    # Normalize the pixel values to the range [0, 1]
    normalized_image = resized_image / 255.0

    # Expand the dimensions of the image to match the input shape of the model
    expanded_image = tf.expand_dims(normalized_image, axis=0)

    return expanded_image
if __name__ == '__main__':
    app.run(debug=True)
