# This script will delete all existing discovery jobs from DNA Center
# this can be useful if many jobs have built up over time and need to be cleaned up

# BASE_URL variable needs to be updated with the IP address of your DNAC appliance, or in the case of a cluster, the DNAC VIP

# developed using Python 3.6.8 


import requests
from requests.auth import HTTPBasicAuth

# Disable SSL warnings
import urllib3
urllib3.disable_warnings()

# Variables
BASE_URL = 'https://xxx.xxx.xxx.xxx'
AUTH_URL = '/dna/system/api/v1/auth/token'

def get_token():
    print('\n\nEnter DNA Center Credentials')
    user = input("USERNAME: ").strip()
    passwd = input("PASSWORD: ").strip()
    response = requests.post(
       BASE_URL + AUTH_URL,
       auth=HTTPBasicAuth(username=user, password=passwd),
       headers={'content-type': 'application/json'},
       verify=False,
    )
    data = response.json()
    if response:
        return data['Token']
    else:
        sys.exit('Unable to connect to ' + BASE_URL + ' using supplied credentials')

def delete_discovery_jobs(token):

    try:
        response = requests.delete(
           BASE_URL + '/dna/intent/api/v1/discovery',
           headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'},
           verify=False,
        )
    except requests.exceptions.RequestException as e:
        return e
        
    return response

def main():

    #get DNAC authorization token to be used with all API calls
    token = get_token()
    
    delete_jobs = input('\nDo you want to delete all existing discovery jobs? (y/n)')
    inputvalid = (delete_jobs.lower() == 'y' or delete_jobs.lower() == 'n')
    while inputvalid != True:
        delete_jobs = input('Do you want to delete devices prior to redicovery? (y/n)')
        inputvalid = (delete_jobs.lower() == 'y' or delete_jobs.lower() == 'n')
    if delete_jobs.lower() == 'y':
        result = delete_discovery_jobs(token)
        # print(result)
        print('\nAll discovery jobs completed')
    else:
        print('\nProgram aborted!')
        
    
    
if __name__ == "__main__":
    main()
