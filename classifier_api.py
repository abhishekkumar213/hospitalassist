import os
from flask import Flask, request
import json
from package.main import main_function
from package.downloading import downloader

app = Flask(__name__)

@app.route('/')
def Welcome():
	#downloader()
	# input_file = 'C:\Users\DivyaS\Desktop\#callforcode\code\\train\input\CV_IP Case_William_B222-tr762.txt'
    #
	# json_data=main_function(input_file)

	with open('data.json') as json_file:
		json_data = json.load(json_file)
	return str(json_data)



port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	downloader()
	input_file = 'C:\Users\DivyaS\Desktop\#callforcode\code\\train\input\CV_IP Case_William_B222-tr762.txt'

	json_data = main_function(input_file)

	with open('data.json', 'w') as outfile:
		json.dump(json_data, outfile)
	app.run(host='0.0.0.0', port=int(port))