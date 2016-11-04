
# Last Modified Date: 09/18/12:18AM
# Objective: Write file to partA.txt

# rawToInstance take a raw data string and convert into tidy data
# tidy data has the form of: attr_0 attr_0_value ... attr_n attr_n_value  

from sys import argv


def rawToInstance(s):
    splitted_string = s.split()
    tidy_data = []
    for i in range(len(splitted_string)):
        if i % 2 == 1:
            tidy_data += [splitted_string[i]]
    return tidy_data

# getInstance uses rawToInstance to generate a 2D list with all the tidy data
def getInstances(input_file):
    file_object = open(input_file)
    instances = []
    for line in file_object:
        instances += [rawToInstance(line)]
    return instances

# return hypotheses and the last hypothesis from training data in a 2d list 
def getHypotheses(instances):
    result = []
    attributes_length = len(instances[0]) - 1
    h = ["null"] * attributes_length

    # main algorithm
    for index in range(len(instances)):
        instance = instances[index]
        if instance[-1] == "high":
            for i in range(len(instance) - 1):
                if h[i] != instance[i] and h[i] == "null":
                    h[i] = instance[i]
                elif h[i] != instance[i]:
                    h[i] = "?"
        if (index + 1) % 30 == 0: 
            # we use list(h) to avoid list aliasing 
            result = result + [ list(h) ]
    return (result, result[-1])

# write file to store hypothesis in "partA4.txt"
def write_file(result):
    f_to_write = open("partA4.txt", 'w')
    for line in result:
        string_line = "\t".join(line)
        f_to_write.write(string_line + '\n')
    f_to_write.close()

# test if the attributes of the instance satisfies the h0 
def attrEqual(h0, instance):
    for i in range(len(h0)):
        if h0[i] != instance[i] and h0[i] != "?":
            return False
    return True

# return the classificationRate of the given file 
def getMissClassificationRate(h0):
        instances = getInstances("9Cat-Dev.labeled")
        miss_count = 0
        # set total_instances as a float number 
        total_instances = len(instances) + 0.0
        for instance in instances:
            if (instance[-1] == 'high' and not(attrEqual(h0, instance)) or
                instance[-1] == 'low'  and attrEqual(h0, instance)):
                miss_count += 1
        return (miss_count / total_instances)

# main file contains answer for PartA from question 1 to 6 
def main():
    code, input_file = argv
    # question 1: size of input space
    input_space = 2 ** 9 
    print(input_space)

    # question 2: number of decimal digits in |C|
    concept_space = 2 ** input_space
    num_digits = len(str(concept_space)) 
    print(num_digits)

    # question 3: |H| Hypothesis Space
    hypothesis_space = 3 ** 9 + 1
    print(hypothesis_space)

    # question 4: find-S Algorithm
    # h0 is the last hypothesis we have obtained 
    result, h0 = getHypotheses(getInstances("9Cat-Train.labeled"))
    write_file(result)
    
    # question 5: find misclassification rate 
    print(getMissClassificationRate(h0)) 

    # question 6: classification 
    instances = getInstances(input_file)
    for i in xrange(len(instances)):
        if attrEqual(h0, instances[i]): 
            print("high")
        else: 
            print("low")
    
main()





