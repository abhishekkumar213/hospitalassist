import csv
import re
import nltk
from nltk import sent_tokenize
from Extractor import Rows_A2G, Med, Equip
import json



def fill_a_h(text):
    name, age, Gender, Encounter, Speciality =Rows_A2G(text)
    row=[]
    row.append(name)#A
    #row.append(name)#B
    #row.append(name)#C
    row.append(age)#D
    row.append(Gender)#E
    row.append('MRN')#F
    row.append(Encounter)#G
    row.append(Speciality)#H
    return row


def find_risc_score(asmt):
    asmt = asmt.lower()
    op=re.findall(r'(to\s+(([ci]cu)|((cardiac|intensive|coronary) care unit)))',asmt)
    op1 = re.findall(r'(to\s+ward\s+)', asmt)
    print len(op)
    if len(op) != 0:
        score = 'High'
    elif len(op1) != 0:
        score = 'Medium'
    else:
        score='Low'
    return score

def find_medication(text):
    med = Med(text)
    #med_str='xyz'
    med_str=''
    for item in med:
        med_str = med_str+'\n'+item
    return med_str.strip()

def find_equipment(text):
    eqp = Equip(text)
    #print str(eqp)+'***'
    #eqp='xyz'
    eqp_str = ''
    for item in eqp:
        eqp_str = eqp_str + '\n' + item.strip()
    return eqp_str.strip()

def find_medication_req(plan):
    text = sent_tokenize(plan)
    sent=''
    for item in text:
        op= re.findall(r'(patient to continue same medications)',item.lower())
        if len(op)!=0:
            sent = item
    if sent !='':
        medication = str(find_medication(plan))+'\n'+sent
    else:
        medication = find_medication(plan)
    return str(medication)


def create_csv(sub, ob, asmt, plan, filename,hpi,current_medication,procedures_done,text10,vitals):
    data_list=[]
    row=[]
    asmt = 'The patient was diagnosed to be suffering from Ventricular Ectopy, Peripheral Artery disease, Coronary Artery disease and Ischemic Cardiomyopathy for which she underwent Right Femoral Popliteal Bypass surgery at 10:15am and was moved to Coronary Care Unit at 11:00am in a stable condition. The patient tolerated the procedure well. No complications.'
    plan = 'Patient is under aggressive monitoring and medication therapy in CCU under the supervision of her Cardiologist Dr. Jane. In CCU patient is receiving continued monitoring through Left Ventricular Assist Device for hemodynamic assessment & optimization, Portable Ventilator with Air Compressor, Multi-Parameter Patient Monitor, Perfusor Compact, Biphasic Defibrillator and Blood and Infusion Warmer. Mrs. Elizabeth will be discharged after 2 days, after doing a routine post-surgical ECG and assessing the condition of the patient. Patient is under IV fluids now - Flucloxacillin 75 mg and Gentamicin 50 mg- IV x3, at CCU. Patient to continue same medications but Increase lisinopril to 20 mg daily to improve blood pressure management, add Aspirin 100 mg - IV x2'

    csv_list=[]
    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        #writer.writerow(['Patient First Name', 'Patient Last Name', 'Patient Name Title', 'Patient DEmographics1','Patient DEmographics2','Patient DEmographics3','Encounter','Speciality','Patient Current Condition','Patient condition Risk score','Current Medication','Medication Requirement [Prescribed]','Current Medical Equipment','Medical Equipment Req','Preparedness Instructions for receiving hosp'])
        writer.writerow(['Patient Name', 'Age',
                         'Gender', 'MRN', 'Encounter', 'Speciality','Patient Vitals',
                         'Patient Current Condition', 'Patient condition:Risk score', 'Current Medication',
                         'Medication Requirement [Prescribed]', 'Current Medical Equipment', 'Medical Equipments Required',
                         'Preparedness Instructions for receiving hospital'])
        # csv_list.append(['Patient Name', 'Age',
        #                  'Gender', 'MRN', 'Encounter', 'Speciality','Patient Vitals',
        #                  'Patient Current Condition', 'Patient condition:Risk score', 'Current Medication',
        #                  'Medication Requirement [Prescribed]', 'Current Medical Equipment', 'Medical Equipments Required',
        #                  'Preparedness Instructions for receiving hospital'])

        row = fill_a_h(text10)

        row.append(vitals)
        current_condition = hpi + '\n\n'+asmt
        row.append(current_condition)
        score = find_risc_score(asmt)
        row.append(score)
        current_medication_data = find_medication(current_medication)
        row.append(current_medication_data)
        medication_requirement = find_medication_req(plan)
        row.append(medication_requirement)
        current_medical_equipment = find_equipment(procedures_done)
        row.append(current_medical_equipment)
        medical_equipment_req = find_equipment(plan)
        row.append(medical_equipment_req)
        f=open('eqp.txt','a+')
        f.write(medical_equipment_req)
        f.write(current_medical_equipment)
        f.close()
        preparedness=asmt+'\n\n'+plan+'\n\nMedication required: '+medication_requirement+'\n\nMedical Equipments Required:'+medical_equipment_req
        row.append(preparedness)
        writer.writerow(row)
        csv_list.append(row)

    #json_csv = json.dumps(csv_list)

    return csv_list
#create_csv('sub','ob', 'asmt', 'plan', 'name.csv','hpi','current_medication','procedures_done','text10','vitals')