Author: Zihan Guo

Video Link: https://youtu.be/G8yNr1DOCDE

## Table of Contents:
  1. Project Description
  2. Content Organization
  3. Library and Package 
  4. Assumptions and Conlusions
  

### 1. Project Description

This project aims to effectively infect users when testing a new version of the site. There are several difficulties in solving
this problem. First, we should be cautious that relationships are symmetric and transitive. Therefore, we want to use an undirected 
network repsentation. We chose dictionary to represent undirected graph in solving the first challenge. Second, input data is 
unspecified. However, we only require one piece of information: who is coacing whom. We, therefore, require the dataset to 
have first column name as "id_teacher" and the second column name as "id_student". For every row in our dataset, id_teacher cannot
be empty but id_student can. For example, in our dataset row 11, we have X11 for id_teacher and no student in id_student. In this
case, X11 is teaching himself/herself. The last challenge is when implementing limited infetcion algorithm, we need to decide
the priority of infection. In other words, we need to choose whom we infect first. We solve this challenge by using breadth
first search because we want to avoid the case of one outlier in a group of student. Therefore, we chose to infect by levels from
the start user. 

### 2. Content Organization

There are four files in this folder. The Readme.md file, infection.py file, user_data.csv file and visualization.pdf file. Both 
total infection and limited infection can be found in infection.py file. Notice that I have constructed user_data.csv file myself. 
As a disclaimer, although I have tried my best to cover all edge cases in the program, if you were to construct your own data file, 
make sure to pay sepcial attention to my project description and follow the specification closely. You may also want to read how
I load and process file in the first function of infection.py file. The visualization.pdf file is sketched and is designed to aid 
understanding when running my program. I have also created a Youtube Video to explain this project. The link can be found below: https://youtu.be/G8yNr1DOCDE


### 3. Library and Package

Please use python 2.7 when running my file. For the entire project, I only use one external package "import csv". I have wrote 
the graph representation myself using dictionary and everything was written from scratch. 

### 4. Assumptions and Conclusions

There are several important assumptions for this project. First, we are assuming direction does not matter when representing 
relationships between users. The reason of my assumption is when we infect a pair of users, we don't care who is the coach. 
Second, we are assuming it is possible for a user to teach himself/herself. Therefore, as mentioned in our poject description, we 
included the case when there is only one user in a row. Our last assumption is that we may choose any user to start infection after
filling up a cluster in limited infection algorithm. I will explain this more in details in my video. 





