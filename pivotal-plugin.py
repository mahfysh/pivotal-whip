# Python

import requests
import json
from datetime import datetime, timedelta
import dateutil.parser

PROJECTS = ['1980391',  # random
            '1856655']  # appunite general

# TODO update to slack channel


def check_stories(project_id, token):

    url_filter = '?filter=state:started'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'X-TrackerToken': token}
    project_url = "https://www.pivotaltracker.com/services/v5/projects/" + project_id + "/stories/"
    url = project_url + url_filter
    print("Checking", project_id, project_url)

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Project " + project_id + " error, not connected.")
        exit(400)

    response = json.loads(r.content)
    for i in response:

        d = dateutil.parser.parse(i['updated_at'])
        updated = d.strftime('%d/%m/%Y')
        outdated = datetime.today() - timedelta(days=3)
        outdated = outdated.strftime('%d/%m/%Y')
        date_created = datetime.strptime(updated, '%d/%m/%Y')
        today = datetime.strptime(outdated, '%d/%m/%Y')

        if date_created <= today:
            print(i['url'], "is too old")
            url = project_url + str(i['id']) + '/comments'
            # r = requests.post(url, headers={'X-TrackerToken': TOKEN}, data={"text": "This is outdated @miloszcisowski"})
            # if r.status_code != 200:
            #     print('fuck')

        else:
            print(i['id'], "is ok")

    print("\n")


def main():

    new_token = input('Input Pivotal API token: ')
    for project in PROJECTS:
        check_stories(project, new_token)


if __name__ == '__main__':
    main()
