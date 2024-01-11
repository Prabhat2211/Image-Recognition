# Image-Recognition
* This is an image classification web app that can also be deployed to Google Cloud.
  * There are 2 ways the input is given:
    * Image upload
    * web cam capture every 10 sec
  * The results are displayed differently for both the input channels:
    * When an image is uploaded a different page opens showing the output
    * For web cam capture the result is displayed on the capture image itself.
  * The output contains
    * If a human is detected
       * If human is zomato delivery boy: (human_detected, zomato_delivery_boy)
       * If human is not zomato_delivery_boy: (human_detected, others)
    * If no human is detected: 'no human detected'

* The repo consists of 4 main parts:
  ## Data Preparation(image_downloader.ipynb) :
     - The data was downloaded from google.com by using a custom function.
     - The custom function takes an input of search and no. of images.
     - Output is images downloaded in our local machine at specified path
     - Ref: https://www.geeksforgeeks.org/download-google-image-using-python-and-selenium/
     - Issue: Max images downlaoded in one run is 300
  ## Model Training:
     - 2 different models were trainind as binary classifiers.
        * image_rec.h5
        * image_rec_zomato.h5
     - Both the models were trained using same algorithm (img_rec_person.ipynb, img_rec_zomato.ipynb)
     - CNN was used to train the model as baseline model, with 4 CNN blocks and finally 3.45 million parameters
     - Dropout was used as regularizor in the network.
     - VGG16 with 14 million parameter was also used for comparison. 
     - Ref: https://keras.io/examples/vision/image_classification_from_scratch/, https://sourestdeeds.github.io/pdf/Deep%20Learning%20with%20Python.pdf
  ## Model Evaluation:
  |Model|Training_acc|Test_acc|
  |-----|------------|--------|
  |CNN-custom|82%|70%|
  |VGG16|89%|75%|
  ## Model Deployment:
     - CNN-custom was deployed for simplicity as VGG16 only showed marginal improvement.
     - The model was deployed using Flask app on GCP.
     - deployment evidence on local
  <img width="1440" alt="Screenshot 2024-01-11 at 1 35 46 PM" src="https://github.com/Prabhat2211/Image-Recognition/assets/56192290/0927134b-8a65-4ca6-893b-f5d523e37150">
     -deployment evidence on GCP

     - Ref: https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service, https://www.cloudskillsboost.google/focuses/3339?parent=catalog
     - Issue: The web-cam service didn't work on GCP using opencv library.
