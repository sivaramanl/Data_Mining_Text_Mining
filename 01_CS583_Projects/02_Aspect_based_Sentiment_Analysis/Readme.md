Aspect Based Sentiment Analysis
---------------------

Authors: 
<ul>
  <li>
      Lakshmi Divya Jillellamudi Kamala<br>https://github.com/lakshmidivyajk
  </li>
  <li>
      Sivaraman Lakshmipathy<br>https://github.com/sivaramanl
  </li>
</ul>
<hr>

<b>Pre requisites</b>
1. The source code for Aspect Based Sentiment Analysis has been developed using the 'Python' programming language.
2. Please ensure that Python 3.6.5 is available in your environment before executing the program.
-------------------

<b>Setup</b>
1. Extract the contents of the compressed file. There will be four files and a folder.
a) absa_classifiers.py - contains the classifier implementation.
b) absa_utils.py - contains the data pre-processing and feature engineering methods.
c) absa_train.py - contains the source code for training the model on the given dataset.
d) absa_predict.py - contains the source code for predicting the values on the given dataset.
e) opinion-lexicon-English - folder containing the positive and negative lexicon required to build the model.
2. Please execute the absa_train.py file to train the model. The input dataset file name can be provided as an argument in the command line.
> python absa_train.py data-1_train.csv
If the performance measure is required to be printed, please use "--performance" as the second command line argument.
> python absa_train.py data-1_train.csv --performance
On execution, two files will be generated.
a) tf_vect.sav - model to convert the text to tf-idf notation.
b) absa_train.sav - the trained model
Please ensure that the two files are available when trying to predict the output for the test dataset.
3. Please execute the absa_predict.py file to predict the output for the test dataset. The test dataset file name can be provided as an argument in the command line.
> python absa_predict.py Data-1_test.csv
The output will be recorded in a file named "absa_predictions.txt" in the following format.
review_id;;predicted_class
