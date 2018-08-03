import os
from flask import Flask, request

app = Flask(__name__)

def read():
	f = open('file1.txt','r')
	data = f.read().split(',')
	users=[]
	if len(data) <=1:
		if len(data) == 1:
			if len(data[0])>1:
				item = data[0].split(':')
				if len(item) == 2:
					d = {"name": item[0].strip(), "age": item[1].strip()}
					users.append(d)
	for item in data:
		item = item.split(':')
		d= {"name":item[0].strip(), "age":item[1].strip()}
		users.append(d)
	f.close()
	return users
def write(users):
	f = open('file1.txt', 'w')
	s=''
	for item in users:
		key = item["name"]
		val = item["age"]
		s=s+key+':'+val+','
	s=s.strip(',')
	f.write(s)
	f.close()



@app.route('/')
def Welcome():
	return 'Welcome user, I am Divya S'

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)



@app.route('/getrecord/<name>')
def get(name):
	users=read()
	for item in users:
		if item["name"] == name:
			return 'The record is '+str(item)

	return 'item not present'



@app.route('/rest/<name>',methods = ['GET', 'DELETE'])
def curd(name):
	users = read()
	if request.method == 'GET':
			for item in users:
				if item["name"] == name:
					return 'The record is '+str(item)
			return 'item not present' +str(users)
	if request.method == 'DELETE':
			temp=''
			for item in users:
				if item["name"] == name:
					temp = item
			if temp == '':
				return 'item not present'
			else:
				users.remove(temp)
				write(users)
				return 'record deleted: '+name

@app.route('/rest/<name>/<age>',methods = ['POST', 'PUT'])
def post_put(name, age):
	if request.method == 'POST':
			users = read()
			for item in users:
				if item["name"] == name:
					return 'The record is already present '+str(item)
			users.append({"name":name,"age":age})
			write(users)
			return 'record added '+str(users)
	if request.method == 'PUT':
			users=read()
			temp=''
			for item in users:
				if item["name"] == name:
					temp = item
			if temp == '':
				return 'item not present'
			else:
				users.remove(temp)
				users.append({"name":name,"age":age})
				write(users)
				return 'record updated: '+name

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))