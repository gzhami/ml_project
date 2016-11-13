# File: total_infection.py
# Author: Zihan Guo
# Date: November 12, 2016

import csv

class infection:


    def __init__(self, file_name):
        self.file_name = file_name
        self.infected = set([])
        self.users = set([]) 
        self.user_data = dict()


    def load_file(self, file_name): 
        with open(file_name, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                teacher = row[0]
                student = row[1] 
                if teacher == "id_teacher":
                    continue
                self.users.add(teacher)
                if student is "":
                    self.user_data[teacher] = set()
                else:
                    self.users.add(student) 
                    if teacher not in self.user_data: 
                        self.user_data[teacher] = set([student])
                    if student not in self.user_data:
                        self.user_data[student] = set([teacher])
                    if student in self.user_data and teacher in self.user_data:
                        students = self.user_data[teacher] 
                        students.add(student)
                        teachers = self.user_data[student]
                        teachers.add(teacher)
                        self.user_data[teacher] = students
                        self.user_data[student] = teachers


    def total_infect(self, start_user):
        # infect all connected users with start_user
        self.infected = set()
        to_be_infected = [start_user]
        while to_be_infected:
            current = to_be_infected.pop(0) 
            if current not in self.infected:
                self.infected.add(current)
                print "Infecting ...", str(current)
                to_be_infected.extend(self.user_data[current] - self.infected) 


    def limit_infect(self, start_user, limit):
        # infect exactly the number of users specificed by limit
        self.infected = set()
        to_be_infected = [start_user]
        while len(self.infected) != int(limit):
            if len(to_be_infected) == 0:
                start_user = list(self.users - self.infected)[0]
                to_be_infected = [start_user]
            while to_be_infected:
                current = to_be_infected.pop(0) 
                if current not in self.infected:
                    self.infected.add(current)
                    print "Infecting ... ", str(current)
                    if len(self.infected) == int(limit):
                        break
                    to_be_infected.extend(self.user_data[current] - self.infected) 


    def printer(self, jobs):
        if len(jobs) == 0:
                print "No Infected Users"
        for i in jobs:
            print i,
        print ""


    def main(self):
        quit = False
        while not quit: 

            print "Welcome to Infection Simulation: "
            print "Here are our users             : ", 
            self.load_file(self.file_name)
            self.printer(self.users)
            print "Here are infected users        : ",
            self.printer(self.infected)

            algorithm = raw_input("Select algorithm to infect (1: Total, 2: Limited): ")
            while not(algorithm == "1" or algorithm == "2"):
                print "Sorry we only have two algorithms to select"
                algorithm = raw_input("Select algorithm to infect (1: Total, 2: Limited): ")

            start_user = raw_input("Enter the 1st user to infect: ")
            if algorithm == "2":
                limit = raw_input("How many would you like to infect: ") 
                while int(limit) > len(self.user_data) or int(limit) <= 0:
                    print "Invalid Input Limit"
                    limit = raw_input("Choose Limit between 1 and " + 
                                     str(len(self.user_data)) + " : ")

            while start_user not in self.users:
                print "Please use an existing user: "
                start_user = raw_input("Enter the 1st user to infect: ")
                if algorithm == "2":
                    limit = raw_input("How many would you like to infect: ")

            if algorithm == "1":
                self.total_infect(start_user)
            elif algorithm == "2":
                self.limit_infect(start_user, limit) 

            print "We have infected               : ", 
            self.printer(self.infected)
            exit = raw_input("Press Q to quit and any other keys to continue: ")
            
            if exit == "Q" or exit == "q":
                quit = True
            self.infected = set()


run = infection("user_data.csv")
run.main()





    
