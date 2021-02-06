import requests
import json
import pandas as pd

def parseLinkHeader(headers):
    links = {}
    if "link" in headers:
        linkHeaders = headers["link"].split(", ")
        for linkHeader in linkHeaders:
            (url, rel) = linkHeader.split("; ")
            url = url[1:-1]
            rel = rel[5:-1]
            links[rel] = url
    return links

def getTotalPages(headers):
    return int(headers['total_page'])


def get_issues(owner, repo, state='open'):
    s = requests.session()
    s.keep_alive = False
    s.auth = ('', '')
    type = 'issues'
    access_token = '4e0e0f9ce494043609a20f163f7b4934'
    request_url = f'https://gitee.com/api/v5/repos/{owner}/{repo}/{type}?access_token={access_token}&state={state}&sort=created&direction=desc&page=1&per_page=20'
    response = s.get(request_url)
    pages = getTotalPages(response.headers)
    data = pd.DataFrame()
    for page in range(1, pages):
        request_url = f'https://gitee.com/api/v5/repos/{owner}/{repo}/issues?access_token={access_token}&state={state}&sort=created&direction=desc&page={page}&per_page=20'
        response = s.get(request_url)
        contents = json.loads(response.text)
        for content in contents:
            data = data.append([{
                'id': content['id'],
                'number': content['number'],
                'state': content['state'],
                'userId': content['user']['id'],
                'userlogin': content['user']['login'],
                'username': content['user']['name'],
                'labels': content['labels'],
                'createTimestamp': content['created_at'],
                'updateTimestamp': content['updated_at'],
                'finishTimestamp': content['finished_at'],
                'type': content['issue_type']
            }], ignore_index=True)
        print(len(data))
    print(data.head(5))
    print('ok， now begin to write')
    data.to_csv(f"data/{owner}-{repo}-{type}.csv", encoding='utf8')

def get_contributors(owner, repo):
    s = requests.session()
    s.keep_alive = False
    s.auth = ('', '')
    access_token = '4e0e0f9ce494043609a20f163f7b4934'
    type = 'contributors'
    request_url = f"https://gitee.com/api/v5/repos/{owner}/{repo}/contributors?access_token={access_token}"
    response = s.get(request_url)
    jsonOfRepo = []
    jsonOfRepo.extend(json.loads(response.text))
    print('ok， now begin to write')
    pd.DataFrame(jsonOfRepo).to_csv(f"data/{owner}-{repo}-{type}.csv", encoding='utf8')

if __name__ == '__main__':
    owner = 'mindspore'
    repo = 'mindspore'
    get_issues(owner, repo)
    get_contributors(owner, repo)
 