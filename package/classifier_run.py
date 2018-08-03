import sys
import os
import pickle
from nltk import sent_tokenize
import csv
import textract
from nltk.corpus import stopwords
import re
import string
from fill_csv import create_csv

#input_file_path = 'test_input'

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def create_dictionary():
    d = {'History of Present Illness': 'History of Present Illness symptoms',
         'HPI': 'History of Present Illness symptoms',
         'HISTORY OF PRESENTING ILLNESS': 'History of Present Illness symptoms',
         'Review Of Symptoms': 'Review Of Symptoms/Systems',
         'Review Of Systems': 'Review Of Symptoms/Systems',
         'Review Of System': 'Review Of Symptoms/Systems',
         'Review Of Symptom': 'Review Of Symptoms/Systems',
         'REVIEW OF SYSTEMS': 'Review Of Symptoms/Systems',
         'ROS': 'Review Of Symptoms/Systems',
         'Symptoms': 'Review Of Symptoms/Systems',
         'PMH': 'Past Medical History',
         'Present Medications': 'Current Medications',
         'Current Prescriptions': 'Current Medications',
         'allergies': 'Medication allergies',
         'SOH': 'Social History',
         'SH': 'Social History',
         'Surgical History': 'Social History',
         'FH': 'Family History',
         'Impression Assessment': 'assessment',
         'Impression': 'assessment',
         'Diagnosis': 'Diagnosis and differential diagnosis',
         'differential diagnosis': 'Diagnosis and differential diagnosis',
         'Diagnosis/differential diagnosis': 'Diagnosis and differential diagnosis',
         'Laboratory Data': 'Diagnosis and differential diagnosis',
         'Diagnostic Data': 'Diagnosis and differential diagnosis',
         'Recommendation Plan': 'Plan',
         'Recommendation': 'Plan',
         'CHD': 'Heart',
         'COPD': 'Heart',
         'Cardiac': 'Heart',
         'Cardiovascular': 'Heart',
         'CV': 'Heart',
         'MUSC': 'Musculoskeletal',
         'CNS': 'Neurologic',
         'Central Nervous system': 'Neurologic',
         'Laboratory': 'Lab',
         'genetourinary': 'G/U',
         'Follow up': 'Follow-up',
         'Followup': 'Follow-up',
         'x-ray': 'X-Rays',
         'xray': 'X-Rays'
         }
    temp_d = {}
    for item in d:
        val = d[item]
        if item.lower() not in d:
            temp_d[item.lower()] = val

    d = merge_two_dicts(d, temp_d)
    return d

def replace_label(label):
    label=label.strip()
    global d
    # if label.lower()=='review of systems':
    #     #if label.lower() in d:
    #     #    print '**'+label
    #     if ('review of systems' in label.lower() ) and (label.lower()!='review of systems'):
    #         print label
    if label.lower() in d:
        return d[label.lower()]
    else:
        return label


def process_text(my_str):
    chars = re.escape(string.punctuation)
    my_str = re.sub(r'^https?:\/\/.*[\r\n]*', '', my_str, flags=re.MULTILINE)
    my_str = re.sub(r'@\w+', '', my_str)  # to remove words starting with@, to remove mentions about people
    my_str = re.sub(r'[' + chars + ']', '', my_str)  # removing special characters
    #my_str = re.sub(r'(?:(?:\d+,?)+(?:\.?\d+)?)', '', my_str)  # remove numbers
    # print text[i]+'----'+my_str
    return my_str


def sentence_tokenization(text):
    text1 = text.replace("?", "-questionmark-")
    text1 = re.sub('\n\d+\s?\.\s+', '\n', text1)
    text_list = sent_tokenize(text1)

    main_list = []
    for j in range(len(text_list)):
        split_l = re.split(r"\n", text_list[j])
        for item in split_l:
            item = re.sub(r'\s+|\t+', ' ', item)
            # item = re.sub(r'      ', ' ', item)
            item = item.replace("questionmark", "?")
            #main_list.append(item)
            newitem = re.split(r":", item)
            newitem[0] = replace_label(newitem[0])
            if len(newitem) == 2:
                sent=newitem[0]+': '+newitem[1]
                sent = process_text(sent)
                main_list.append(sent)
            else:
                sent=item
                sent = process_text(sent)
                main_list.append(sent)
            main_list = filter(None, main_list)
    '''# print main
    var = ''
    temp = ''
    for i in range(0, len(main)):
        if main[i].lower() in string_lst:
            # print main[i]
            # key_val_list.append([var,temp])
            var = main[i]
        elif var != '' and main[i].strip() != '' and len(main[i].strip()) >= 3:
            temp = main[i]
            key_val_list.append([var, temp])'''
    return main_list


def process_min(text):
    '''function to remove special character and stopwords from the text'''
    new_text = []
    for i in range(len(text)):
        my_str = text[i].lower()
        my_str = my_str.strip()
        chars = re.escape(string.punctuation)
        my_str = re.sub(r'^https?:\/\/.*[\r\n]*', '', my_str, flags=re.MULTILINE)
        my_str = re.sub(r'@\w+', '', my_str)  # to remove words starting with@, to remove mentions about people
        my_str = re.sub(r'[' + chars + ']', ' ', my_str)  # removing special characters
        #my_str = re.sub(r'(?:(?:\d+,?)+(?:\.?\d+)?)', '', my_str)  # remove numbers
        new_text.append(my_str)
    return new_text





def write_csv_soap(filename, key_val_list):
    sub = ['subjective', 'History of Present Illness symptoms', 'Review Of Symptoms/Systems',
           'Past Medical History', 'Current Medications', 'Medication allergies',
           'Social History', 'Family History', 'medications', 'greetings']
    assessment = ['assessment', 'Diagnosis and differential diagnosis']
    objective = ['objective', 'Physical Examination', 'Skin', 'HEENT', 'Heart', 'Lungs', 'Abdomen', 'Musculoskeletal',
                 'Neurologic', 'G/I', 'procedures Done', 'Emergency Care']
    #plan = ['plan', 'Laboratory', 'Lab', 'X-Rays', 'Patient Education', 'Other', 'Follow-up']
    plan = ['plan', 'Lab', 'X-Rays', 'Follow-up', 'ECG', 'Radiology']

    sub = [i.lower() for i in sub]
    assessment = [i.lower() for i in assessment]
    objective = [i.lower() for i in objective]
    plan = [i.lower() for i in plan]
    sub = process_min(sub)
    objective = process_min(objective)
    assessment = process_min(assessment)
    plan = process_min(plan)

    soap_category = []
    for item in key_val_list:
        content = item[0].encode("utf-8")
        topic = item[1].strip()
        if content in ['', '    ']:
            soap_category.append('NIL')
        elif topic.lower() in sub:
            soap_category.append('subjective')
        elif topic.lower() in objective:
            soap_category.append('objective')
        elif topic.lower() in assessment:
            soap_category.append('assessment')
        elif topic.lower() in plan:
            soap_category.append('plan')
        else:
            soap_category.append('NIL')


    csv_list=[]

    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['content', 'subtopic', 'topic'])
        for i in range(len(key_val_list)):
            content = key_val_list[i][0].encode("utf-8")
            topic = key_val_list[i][1].strip()
            if content in ['', '    ']:
                continue
            else:
                writer.writerow([content, topic, soap_category[i]])
                csv_list.append([content, topic, soap_category[i]])
    return csv_list

def extract_section(csv_l):
    #print csv_l
    sub=''
    ob=''
    asmt=''
    plan=''
    hpi =''
    cm=''
    proc_done=''
    vitals=''
    for item in csv_l:
        if item[2] == 'subjective':
            sub = sub+' '+item[0]
            if item[1] == 'history of present illness symptoms':
                if item[0].endswith(('.','?')):
                    hpi = hpi+' '+item[0]
                else:
                    hpi = hpi+' '+item[0]+'.'
            elif item[1] == 'current medications':
                cm = cm+' '+item[0]

        elif item[2] == 'objective':
            ob= ob+ ' '+item[0]
            if item[1] == 'procedures done':
                proc_done = proc_done+' '+item[0]
            elif item[1] == 'physical examination':
                vitals = vitals+' '+item[0]

        elif item[2] == 'assessment':
            asmt = asmt+ ' '+item[0]
        elif item[2] == 'plan':
            plan = plan + ' '+item[0]


    return sub, ob, asmt, plan,hpi,cm,proc_done,vitals



def main_classifier(input_file,clf2,output,data1):

    global d
    d=create_dictionary()
    # input_f = open(input_file, 'r')
    # data1 = input_f.read()
    data1 = unicode(data1, "utf-8", errors="ignore")#uncomment for normal files, comment for utf16 files
    #data1 = data1.decode('utf-16').encode('utf-8')#comment for normal files, uncomment for utf16 files

    data1 = data1.encode('ascii', 'ignore').decode('ascii')
    # data=unicode(data, "utf-8", errors="ignore")
    #input_f.close()
    text10 = ' '.join(sent_tokenize(data1)[:10])
    data1 = sentence_tokenization(data1)[7:]#comment for files without headers#uncomment for files with initial 7 fields as data like mrn and all
    for i in range(len(data1)):
        data1[i] = data1[i].strip()
    sentence = clf2.predict(data1)
    # pr = clf2.predict_proba(data)
    data_sentence_list = []
    for i in range(len(data1)):
        data_sentence_list.append([data1[i], sentence[i]])
    #csv_l = write_csv_soap('C:\Users\DivyaS\Desktop\#callforcode\code\classifier\output\classifier_output1.csv', data_sentence_list)
    csv_l = write_csv_soap(output, data_sentence_list)
    csv_path = 'op '+output.split('\\')[-1]
    sub, ob, asmt, plan,hpi,cm,proc_done,vitals =extract_section(csv_l)
    json_csv=create_csv(sub, ob, asmt, plan,csv_path,hpi,cm,proc_done,text10,vitals)
    return csv_l, json_csv

def main1(input_file, classifier,output):
    csv_l=[]
    csv_l.append(['Patient Name', 'Age',
                         'Gender', 'MRN', 'Encounter', 'Speciality','Patient Vitals',
                         'Patient Current Condition', 'Patient condition:Risk score', 'Current Medication',
                         'Medication Requirement [Prescribed]', 'Current Medical Equipment', 'Medical Equipments Required',
                         'Preparedness Instructions for receiving hospital'])
    with open(classifier, 'rb') as s:
        clf2 = pickle.load(s)
    for item in os.listdir('package/files'):
        print item
        f =open('package\\files\\'+item,'r')
        data = f.read()
        print data
        data_sentence, csv_list = main_classifier(input_file,clf2, output,data)
        csv_l.append(csv_list[0])

    with open('consolidated.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for item in csv_l:
            writer.writerow(item)
    return data_sentence, csv_l


if __name__ == '__main__':
    #input_path = 'C:\Users\DivyaS\Desktop\MEDICAL_CODING\Data shared by Prakash\test_input\\'
    input_file = 'C:\Users\DivyaS\Desktop\#callforcode\code\\train\input\CV_IP Case_William_B222-tr762.txt'
    #classifier = 'pickle_files/classifier_full_dataset_with_occ_code/classifier.pickle'
    classifier = 'C:\Users\DivyaS\Desktop\#callforcode\code\classifier\seha_classifier_40files.pickle'
    output = input_file.split('.txt')[0]+'.csv'
    print output
    data_sentence, json_csv =main1(input_file, classifier,output)