##---------------------------------------------------------------------------------------------------------------------------
#  README :- People to People relation - Update Line Manager 	using REST calls                                           
#	                                                                                                                     
#  USAGE :- python2 Axon_UploadBulkData.py input.csv PxP.json 										                                                          |
#	  This Program  will generate the JSON from the CSV :
#                                                     1) login 
#                                                     2) Bulkupload People to People relation                               
#															                                                                                             
#  DEPENDENCY :- Install  'requests' python library									                                                       
#															                                                                                            			
#----------------------------------------------------------------------------------------------------------------------------

#Library
import csv  
import json  
import requests
import sys

DEBUG=1

#Login to Axon
#--------------------------------
def axon_login():
        url="http://axon.localdomain.com:9999/api/login_check"
        payload={"username":"admin@informatica.com","password":"Changeme@123"}
        response=requests.post(url,json=payload)
        if DEBUG==1:  print(" Login =" +  response)
        response_content = json.loads(response.content)
        token = "Bearer " + response_content["token"]


#Bulk Upload
#----------------------------------
def bulk_upload(bulk_upload_json):
        url="http://axon.localdomain.com:9999/bulkupload/v1/relationships"
#       payload2={ "type": "People X People", "objects":  [{ "Manager Lan ID": "2000","Employee Lan ID": "1234","Relationship Type": "Direct report" } ]}
        response=requests.post(url2,json=bulk_uplod_json,headers={"Authorization":token})
        if DEBUG==1:  print ("BulkupLoad Response  = " + response.content)


#Append Records
#---------------------------------
def add_relation(relation):
	update_people["objects"].append(relation)

#Global Variable
#-----------------
token="";
update_people={ "type": "People X People","objects":[]}

#Main Method
#----------------------------------
def main():
	if len(sys.argv) == 3:
	    csvfile = open(sys.argv[1],'rU')
	    jsonfile = open(sys.argv[2], 'w')
	elif len(sys.argv) == 2:
	    csvfile = open(sys.argv[1],'r')
	    jsonfile = open('PxP.json', 'w')
	else:
	    print "Usage - Axon_UploadBulkData.py input.csv PxP.json"
	    sys.exit()

#Bulk Upload Format
#--------------------
#{ "type": "People X People", "stopOnWarning": true, "objects": [ { "LAN ID": "1234", "Manager ID": "2000", "Relationship Type": "Direct Report" } ]}


# Open the CSV  
	reader = csv.DictReader( csvfile, fieldnames = ("LAN ID","Manager ID"),delimiter=',', quotechar='"')  
# Parse the CSV into JSON  

	for row in reader:
		relation ={ }
		for i in row:				
			if(i=="LAN ID"):
				relation["LAN ID"]=row[i]
			if(i == "Manager ID"):
				relation["Manager ID"]=row[i]
		relation["Relationship Type"]="Direct Report"
		add_relation(relation)
	
	if DEBUG==1: print json.dumps(update_people)

	if DEBUG==1: print "JSON parsed!"  
# Save the JSON  
	jsonfile.write(json.dumps(update_people))  
	if DEBUG==1: print "JSON saved!"  

#Call Login and Update Function
	axon_login()
	bulk_upload_json()



if __name__ == "__main__":
    main()



