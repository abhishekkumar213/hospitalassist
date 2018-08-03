import os
from package.classifier_run import main1

def main_function(input_file):
    # for items in os.listdir('files'):
    #     print items
    classifier = 'C:\Users\DivyaS\Desktop\#callforcode\code\classifier\seha_classifier_40files.pickle'
    output = input_file.split('.txt')[0]+'.csv'
    data_sentence, json_csv=main1(input_file, classifier,output)
    return json_csv

if __name__ == '__main__':
    input_file = 'C:\Users\DivyaS\Desktop\#callforcode\code\\train\input\CV_IP Case_William_B222-tr762.txt'
    jsonv=main_function(input_file)
