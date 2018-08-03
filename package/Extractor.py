
import requests
import string
import re
import datetime
import json
from pprint import pprint
import pandas as pd


###For First A-G Row
def Rows_A2G(message):
    name=''
    age=''
    Gender=''
    for line in message.splitlines():
        #print("Line -->" , line)
        if line.__contains__("Patient Name:"):
            name_list = [x.strip() for x in line.split(':')]
            name = name_list[1]
            print("Name",name)

        elif line.__contains__("Age"):
            age_list = [x.strip() for x in line.split(':')]
            age = age_list[1]
            print("Age", age)

        elif line.__contains__("Gender"):
            Gender_list = [x.strip() for x in line.split(':')]
            Gender = Gender_list[1]
            print("Gender",Gender)
    Encounter = "Inpatient"
    Speciality = "Cardiology"

    return name, age, Gender, Encounter, Speciality



def ACD_med(annotationText):
    time = datetime.datetime.today().strftime('%Y-%m-%d')
    url='https://watsonpow01.rch.stglabs.ibm.com/services/clinical_data_annotator/api/v1/analyze?version='+time+''
    payload = {"annotatorFlows": [{"flow": {"elements": [{"annotator": {"name": "medication"}}],"async": "true"}}],"unstructured": [{"text": annotationText}]}
    ret = requests.post(url,json=payload,verify=False)
    return ret.text

###Call this Method for K&L
def Med(annotationText):
    #print 'acd', annotationText
    text = ACD_med(annotationText)
    data = json.loads(text)
    acd_dict = {}
    # print data
    #data = {u'unstructured': [{u'data': {u'SymptomDiseaseInd': [{u'coveredText': u'open lacerations', u'begin': 15, u'modifiers': [{u'coveredText': u'open', u'type': u'aci.ModifierGroupInd', u'begin': 15, u'end': 19}], u'end': 31, u'symptomDiseaseSurfaceForm': u'lacerations', u'sectionNormalizedName': u'document', u'ccsCode': u'244', u'icd10Code': u'T14.1,T14.8', u'snomedConceptId': u'312608009', u'sectionSurfaceForm': u'document', u'icd9Code': u'879.8', u'symptomDiseaseNormalizedName': u'laceration - injury', u'type': u'aci.SymptomDiseaseInd', u'modality': u'negative', u'cui': u'C0043246', u'dateInMilliseconds': u' '}, {u'coveredText': u'abrasions', u'begin': 35, u'end': 44, u'symptomDiseaseSurfaceForm': u'abrasions', u'sectionNormalizedName': u'document', u'ccsCode': u'244', u'icd10Code': u'T14.8,T14.0', u'snomedConceptId': u'399963005', u'sectionSurfaceForm': u'document', u'icd9Code': u'919.0', u'symptomDiseaseNormalizedName': u'abrasion', u'type': u'aci.SymptomDiseaseInd', u'modality': u'negative', u'cui': u'C1302752', u'dateInMilliseconds': u' '}, {u'coveredText': u'headache', u'begin': 54, u'end': 62, u'symptomDiseaseSurfaceForm': u'headache', u'sectionNormalizedName': u'document', u'ccsCode': u'84', u'icd10Code': u'R51', u'snomedConceptId': u'25064002', u'sectionSurfaceForm': u'document', u'icd9Code': u'784.0', u'symptomDiseaseNormalizedName': u'headache', u'type': u'aci.SymptomDiseaseInd', u'modality': u'positive', u'cui': u'C0018681', u'dateInMilliseconds': u' '}]}}], u'annotatorFlows': [{u'flow': {u'async': True, u'elements': [{u'annotator': {u'name': u'symptom_disease'}}]}}]}
    #print len(data['unstructured'])
    #print data['unstructured'][0], type(data['unstructured'][0])
    for items in data['unstructured']:
        #inp={u'data': {u'SymptomDiseaseInd': [{u'coveredText': u'open lacerations', u'begin': 15, u'modifiers': [{u'coveredText': u'open', u'type': u'aci.ModifierGroupInd', u'begin': 15, u'end': 19}], u'end': 31, u'symptomDiseaseSurfaceForm': u'lacerations', u'sectionNormalizedName': u'document', u'ccsCode': u'244', u'icd10Code': u'T14.1,T14.8', u'snomedConceptId': u'312608009', u'sectionSurfaceForm': u'document', u'icd9Code': u'879.8', u'symptomDiseaseNormalizedName': u'laceration - injury', u'type': u'aci.SymptomDiseaseInd', u'modality': u'negative', u'cui': u'C0043246', u'dateInMilliseconds': u' '}, {u'coveredText': u'abrasions', u'begin': 35, u'end': 44, u'symptomDiseaseSurfaceForm': u'abrasions', u'sectionNormalizedName': u'document', u'ccsCode': u'244', u'icd10Code': u'T14.8,T14.0', u'snomedConceptId': u'399963005', u'sectionSurfaceForm': u'document', u'icd9Code': u'919.0', u'symptomDiseaseNormalizedName': u'abrasion', u'type': u'aci.SymptomDiseaseInd', u'modality': u'negative', u'cui': u'C1302752', u'dateInMilliseconds': u' '}, {u'coveredText': u'headache', u'begin': 54, u'end': 62, u'symptomDiseaseSurfaceForm': u'headache', u'sectionNormalizedName': u'document', u'ccsCode': u'84', u'icd10Code': u'R51', u'snomedConceptId': u'25064002', u'sectionSurfaceForm': u'document', u'icd9Code': u'784.0', u'symptomDiseaseNormalizedName': u'headache', u'type': u'aci.SymptomDiseaseInd', u'modality': u'positive', u'cui': u'C0018681', u'dateInMilliseconds': u' '}]}}
        #print len(inp['data']['SymptomDiseaseInd'])
        inp = items
        if len(inp) ==0:
            continue
        for item in inp['data']['MedicationInd']:

            #print item['coveredText'],item['icd10Code'], item['modality']
            if 'coveredText' in item:

                if ',' in item['coveredText']:
                    item['coveredText'] = item['drugSurfaceForm'].split(',')[0]
                acd_dict[item['coveredText']] = item['coveredText']
    return acd_dict.values()


def ACD_equip(annotationText):
    time = datetime.datetime.today().strftime('%Y-%m-%d')
    url = 'https://watsonpow01.rch.stglabs.ibm.com/services/clinical_data_annotator/api/v1/analyze?version=' + time + ''
    payload = {"annotatorFlows": [{"flow": {"elements": [{"annotator": {"name": "concept_detection"}}], "async": "true"}}],
               "unstructured": [{"text": annotationText}]}
    ret = requests.post(url, json=payload, verify=False)
    return ret.text


###Call this function for M&N row
def Equip(annotationText):
    # print 'acd', annotationText
    equipments_list = pd.read_csv(r"C:\Users\DivyaS\Desktop\#callforcode\code\Equipments.csv")
    #equip1 = equipments_list['Equipment_list'].values.tolist()
    equip1 = []
    my_list = equipments_list["Equipment_list"].tolist()
    for line in annotationText.splitlines():
        for value in my_list:
            #print("Value",value)
            if value in line:
                #print("Line22",value)
                equip1.append(value)
    #word_list_text = string.split(annotationText)
    #print("word_list_text",word_list_text)
    #words_found = {}
    #words_found = list(set(word_list_text) & set(my_list))
    #print("Words found",words_found)

    #print("my_list",my_list)
    text = ACD_equip(annotationText)
    data = json.loads(text)
    acd_dict = {}

    for items in data['unstructured']:
        inp = items
        for item in inp['data']['concepts']:
            if "type" in item:
                if item['type'] == 'umls.MedicalDevice':
                    #print item#['umls.MedicalDevice']
                    if ',' in item['coveredText']:
                        item['coveredText'] = item['umls.MedicalDevice'].split(',')[0]
                    acd_dict[item['coveredText']] = item['coveredText']
    equip2 = acd_dict.values()
    ans = []
    ans = set(equip1) & set(equip2)
    ans = set(equip1).union(set(equip2))
    return ans

if __name__=='__main__':
    #f = open(r"C:\Users\AbhishekKumar\Desktop\Health_Insurance\CallForCode\Med.txt", "r")
    #message = f.read()
    #f.close()
    #Rows_A2G(message)
    #ACD_text = ACD(message)
    #print(ACD_text)
    #dict = Equip(message)
    #print("dict",dict.values())
    #data = json.load(ACD)
    text ='With the help of a Wholey wire a 4French 4curve Judkins right coronary artery catheter was advanced into the ascending aorta The wire was removed the catheter was flushed The catheter was engaged in the left main Injections were performed at the left main in different views'
    print Equip(text)
