# Author: Zihan Guo
# File: Neural Network Using Backpropagation Algorithm with 1 Hidden Layer
# Dataset: Education Dataset - Predicting Final Score using Midterm and 
#          Homework Grades 
# Last Modified Date: November 1, 2016 

import csv 
import sys 
import numpy 

class Neural_network():

    def data_generator(self, file):
        data = [] 
        with open(file, 'rb') as csvfile: 
            lines = csv.reader(csvfile)
            for row in lines:
                data += [row] 
        return data[1:]

    def file_cleaner(self, train_data):
        for row in xrange(len(train_data)):
            for col in xrange(len(train_data[0])):
                elem = train_data[row][col] 
                train_data[row][col] = float(elem) / 100
        return train_data

    def input_output(self, data, train_data = True): 
        input_x = [] 
        input_y = [] 
        if not train_data:
            for row in data:
                input_x += [row] 
            return input_x  
        for row in data:
            input_x += [row[:-1]]
            input_y += [[row[-1]]]
        return (input_x, input_y)

    def sigmoid(self, x, derivative):
        if derivative:
            return x * (1 - x)
        return 1 / (1 + numpy.exp(-x))

    def weight_initialization(self, input_x, input_y, h_layer = 50):
        col_x = len(input_x[0])
        # we want our weight to have mean 0 to achieve optimal result
        numpy.random.seed(1)
        weight_layer0 = 2 * numpy.random.random((col_x, h_layer)) - 1
        weight_layer1 = 2 * numpy.random.random((h_layer, 1)) - 1
        return weight_layer0, weight_layer1 

    def get_dim(self, matrix):
        # useful for debugging
        print (len(matrix), len(matrix[0]))
        return

    def main(self, loops = 10000, step = 0.001):
        
        train_file = sys.argv[1]
        test_file = sys.argv[2] 

        train_data = self.data_generator(train_file)
        test_data = self.data_generator(test_file)

        cleaned_data_test = self.file_cleaner(test_data) 
        cleaned_data_train= self.file_cleaner(train_data)

        (input_x, input_y) = self.input_output(cleaned_data_train)
        input_x_test = self.input_output(cleaned_data_test, train_data = False)
        (w0, w1) = self.weight_initialization(input_x, input_y) 

        for index in xrange(loops):
            hidden_layer = self.sigmoid(numpy.dot(input_x, w0), 0)
            output_layer = self.sigmoid(numpy.dot(hidden_layer, w1), 0)
            output_error = input_y - output_layer
            
            delta_k = self.sigmoid(output_layer, 1) * output_error 
            hidden_error = delta_k.dot(w1.T)
            delta_h = self.sigmoid(hidden_layer, 1) * hidden_error     

            w1 += step * (hidden_layer.T).dot(delta_k)
            w0 += step * (numpy.array(input_x).T).dot(delta_h)
            print str(numpy.sum(output_error ** 2))

        print "TRAINING COMPLETED! NOW PREDICTING."
        hidden_layer = self.sigmoid(numpy.dot(input_x_test, w0), 0) 
        output_layer = self.sigmoid(numpy.dot(hidden_layer, w1), 0) 
        
        for prediction in output_layer:
            print prediction[0] * 100

x = Neural_network()
x.main()
