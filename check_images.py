#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# TODO: 0. Fill in your information in the programming header below
# PROGRAMMER:Hiral Raval
# DATE CREATED:16/5/2018
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print 
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # TODO: 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()
    
   
    
    # TODO: 2. Define get_input_args() function to create & retrieve command
    # line arguments
    in_arg = get_input_args()
    #print("command line arguments :\n    dir = ",in_arg.dir,"\n    arch = ",in_arg.arch,"\n     dogfile = ",in_arg.dogfile)    
    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    answers_dic = get_pet_labels(in_arg.dir)
    host_dict = in_arg.dir
    arch_model = in_arg.arch
# #     print(answers_dic)
#     print(host_dict)
#     print(arch_model)
    
    #temporary code to pair 10 values key pairs & make sures there r 40 pairs,
    #one for each  file pet_images/
    
#     print("\n answers_dic has",len(answers_dic),"key-value pairs.\n below are 10 of them:")
    
#     prnt = 0
#     for key in answers_dic:
#        if prnt < 10 :
#          print("%2d key : %-30s label: %-26s " % (prnt+1, key, answers_dic[key]))
#          prnt += 1
             

    # TODO: 4. Define classify_images() function to create the classifier 
    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    results = dict()
    results = classify_images(host_dict,answers_dic,arch_model)

    #temp code for check classifier function working properly or not
    print("\n    MATCH:")
    n_match = 0
    n_notmatch =0
    for key in results :
        if results[key][2] == 1:
            n_match += 1
            print("Real : %-26s   classifier: %-30s " % (results[key][0],results[key][1]))
     
    print("\n   NOT A MATCH:")
  
    for key in results :
        if results[key][2] == 0:
            n_notmatch += 1
            print("Real : %-26s   classifier: %-30s " % (results[key][0],results[key][1]))
    print("\n # Total images", n_match+n_notmatch , "# matches:",n_match  ,"#NOt match:", n_notmatch)
            
    
    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog()

    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats()

    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results()

    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    sleep(65)
    end_time = time()

    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    
    print("\n** Total Elapsed Runtime:", tot_time)
    print("\nTotal Elapsed Runtime:", str( int( (tot_time / 3600) ) ) + ":" +
          str( int(  ( (tot_time % 3600) / 60 )  ) ) + ":" + 
          str( int(  ( (tot_time % 3600) % 60 ) ) ) )



# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and 
    
    
    s the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    # creates parse
    
    parser = argparse.ArgumentParser()
# create 3 command line argument
    parser.add_argument('--dir', type = str, default = 'pet_images/', 
                    help = 'path to the folder of images') 

    parser.add_argument('--arch', type = str, default = 'vgg', 
                    help = 'chosen model')
    parser.add_argument('--dogfile', type = str, default = 'dognames.txt', 
                    help = 'text file having dognames')

#return parsed argument collection
    return parser.parse_args()
    
    


def get_pet_labels(image_dir):
    
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
   #create list of file in directory
    in_files = listdir(image_dir)
    
    #processes each of the files to create dictionary where key is the file name
    #and value is picture label(below)
    
    #creates empty dictionary for the labels
    petlabels_dic = dict()
    
    #processes through each file in the dictionary ,extracting  only 
    #words of the file that contains pet image label
    
    for idx in range (0, len(in_files), 1):
        #skips the file if starts with .(like .DS_store of MAC OSX) bcz
        #it is not a pet image file (it requires to write for MAC not for windows)
        
        if in_files[idx][0] != "." :
            
            #uses split to extract words of file names in to list image_name
            image_name = in_files[idx].split("_")
            
            #creates tamporary label variable to hold pet label name extracted
            pet_label = ""
            
            #processes each of the character string(words) split by "_" in the
            #list image_name by processing each word  - only adding to the pet_label
            #if word is all letters - then process by putting blanks between 
            # these words and putting them in all lower case letters
            
            for word in image_name:
                
                #only add to pet_label if word is all letters add blank at end
                if word.isalpha():
                    pet_label += word.lower() + " "
            #strip of trailling whitespaces
            pet_label = pet_label.strip()
            
           #if filename doesn't already exist in dictionary add it and it's 
           #pet_label -otherwise print an error message bcz indicates duplicate files(filenames)
            
            if in_files[idx] not in petlabels_dic:
                petlabels_dic[in_files[idx]] = pet_label
                
            else:
                print("warning: Duplicate files available in dictionary",in_files[idx])
                
    #return dictionary of labels
    return(petlabels_dic)
    
    


def classify_images(images_dir,petlabels_dic,model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
   
    results = dict()

#process all files in petlabel_dic we are using for loop

    for key in petlabels_dic:
    #  model_lable runs clssifier function to classify images
    #input :path+filename and model,Retuns:model_label as classifier label
        # model = 'vgg'
#         print(images_dir + key)
#         print(model)
        model_label = classifier(images_dir + key,model)
    
    #processes result so that they can be comapared with pet image labels
    #lower case and sripting is required
        model_label = model_label.lower()
        model_label = model_label.strip()
    
    
   #defines truth as per pet image label and tryes to find using find()
   #string function to find within classifier label(model_label)
        truth = petlabels_dic[key]
        found = model_label.find(truth)
    
    #if found 0 or > than make sure true answer wasn't found within
    #another word and thus not rally foundif truelly found than add to result dict
    # and set match type =1 or otherwise 0
        if found >= 0:
            if ( (found == 0) and (len(truth) == len(model_label))  
                or
                ( (  ( found == 0) or (model_label[found - 1] ==" ")) and  
                ( (found + len(truth) == len(model_label) )or
                model_label [found + len(truth) : found + len(truth) + 1]
                    in  (","," ") ) 
                    )
                ):
                #if label is not found within label
                if key  not in results:
                    results[key] = [truth,model_label,1]
                    
                 #found a word/term not a label 
                else:
                     if key  not in results:
                        results[key] = [truth,model_label,0]
     #if not found a set result dic with match 0
            else:
                if key  not in results:
                     results[key] = [truth,model_label,0]

    return(results)
            
        
    


def adjust_results4_isadog():
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """           
    pass


def calculates_results_stats():
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    pass


def print_results():
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    pass

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()
