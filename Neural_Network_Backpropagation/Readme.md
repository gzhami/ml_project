Author: Zihan Guo

This respository contains files for my class project. Under no circumstances, should anyone use my code without consent. After downloading all the files, using the following command: 

      python NN_education.py education_train.csv education_dev.csv

on temrinal would allow the program to run automatically. You will observe how the sum of squared errors decreases as the learner learns and builds the neural network model. The purpose of this program is on learning and understanding how backpropagation works. From experiements, we observe, when hidden layer has 50 nodes, 0.001 learning rate and 10,000 iterations, the program is capable to reduce the sum of squared error to 0.0443465171558. 

In addition, we also tested our model on more difficult dataset such as music ranking prediction. In the end, our model is able to reduce the sum of squared error to 6.93947568195 for predicting if a music piece is able to hit top 100 for that year. 


