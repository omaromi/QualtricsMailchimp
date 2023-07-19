import requests
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from decouple import config

directory_id = config("qdir_id")
qualtrics_api_key = config("qkey")
survey_id = config("qsurvey_id")
mailist_id = config("qlist_id")
mailchimpkey = config("mckey")
mclist_id = config("mclist_id")

def create_qualtrics_contact(student):
    # create a contact in Qualtrics directory, it gets auto added to OMN testing list due to a rule/automation in Qualtrics itself.
    url = f"https://yul1.qualtrics.com/API/v3/directories/{directory_id}/contacts"

    payload = student
    payload = {
        "firstName": student['firstName'],
        "lastName": student['lastName'],
        "email": student['email'],
        "extRef": "mujtaba",
        "unsubscribed": False
    }

    headers = {
    "Content-Type": "application/json",
    "X-API-TOKEN": qualtrics_api_key
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

    return "Contact created in Qualtrics"

def generate_survey_link():
    # generate survey link by providing a survey ID and the specific mailing list
    url = "https://yul1.qualtrics.com/API/v3/distributions"

    payload = {
    "surveyId": survey_id,
    "linkType": "Individual",
    "description": "omn's first distrib",
    "action": "CreateDistribution",
    "expirationDate": "2023-09-13T06:00:00Z",
    "mailingListId": mailist_id
    }

    headers = {
    "Content-Type": "application/json",
    "X-API-TOKEN": qualtrics_api_key
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    distrib_id = response.json()['result']['id']

    # use the distribution id to retrieve the actual personalized link

    url3 = f"https://co1.qualtrics.com/API/v3/distributions/{distrib_id}/links?surveyId={survey_id}"
    response3 = requests.request("GET",url3,headers=headers)
    seekrlink = response3.json()['result']['elements'][0]['link']

    return seekrlink

def add_mailchimp_contact(student):
    mc = Client()
    mc.set_config({
        "api_key":mailchimpkey,
        "server":"us15"
    })

    link = generate_survey_link()

    try:
        add_member = mc.lists.add_list_member(mclist_id,{
            "email_address":student['email'],
            "status":"subscribed",
            "merge_fields" : {
                "firstName": student['firstName'],
                "lastName": student['lastName'],
                "SEEKRLINK":link,
            }
        })
        print(add_member['id'])
    except ApiClientError as error:
        print(f"Error: {error.text}")

    try:
        add_tag = mc.lists.update_list_member_tags(mclist_id, add_member['id'], {"tags": [{"name":"Created Account","status": "active"}]})
        print(add_tag)
    except ApiClientError as error:
        print("Error: {}".format(error.text))

    return "mailchimp contact added and tagged as created account active"


def add_surveycomplete_tag(student):
    mc = Client()
    mc.set_config({
        "api_key":mailchimpkey,
        "server":"us15"
    })

    try:
        add_tag = mc.lists.update_list_member_tags(mclist_id, student['email'], {"tags": [{"name":"Completed Survey","status": "active"}]})
        print(add_tag)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
    
    return "survey complete tag added"