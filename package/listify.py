f = open('eqp.txt','r')
data =f.read()
data = data.split('\n')
lata = list(set(data))
f.close()
import csv
with open('eqp.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for item in lata:
        writer.writerow([item])