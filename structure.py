import requests
import json
import pymongo
from dateutil.parser import parse as dateParser
MONGO_URL = "mongodb://127.0.0.1:27017"
db = pymongo.MongoClient(MONGO_URL, connect=False, maxPoolSize=200).mindspore
owner = 'mindspore'
repo = 'mindspore'
access_token = '2644cbdbc6cabb9438509e89c627c34a'

def get_text(url: str):
    s = requests.session()
    s.keep_alive = False
    s.auth = ('', '')
    response = s.get(url + f'?access_token={access_token}')
    contents = json.loads(response.text)
    return contents


class PR:
    def __init__(self, pr: dict):
        self.number = pr['number']
        self.id = pr['id']
        self.state = pr['state']
        self.issue = []
        self.commits = []
        self.comments = []
        self.create_time = pr['created_at']
        self.update_time = pr['updated_at']
        self.issue_url = pr['issue_url']
        self.commits_url = pr['commits_url']
        self.comments_url = pr['comments_url']
        self.get_commits()

    def get_commits(self):
        '''获得pr中commit信息'''
        contents = get_text(self.commits_url)
        for content in contents:
#             sha = content['sha']
            self.commits.append(Commit(content))
        return self.commits

# TODO: 评论以及Issue信息
    # def get_comments(self):
    #     contents = get_text(self.comments_url)
    #     for content in contents:
    #         pass


class Commit:
#     def __init__(self, sha):
#         commit = db.all_commits.find_one({"sha": sha})
#         if commit is None:
#             commit_url = f"https://gitee.com/api/v5/repos/{owner}/{repo}/commits/{sha}"
#             commit = get_text(commit_url)
        
#         # print(commit)
#         self.sha = commit['sha']
#         self.author_login = commit['author']['login']
#         self.url = commit['url']
#         self.comments_url = commit['comments_url']
#         self.additions = commit['stats']['additions']
#         self.deletions = commit['stats']['deletions']
#         self.files = []
#         self.timestamp = dateParser(commit['commit']['author']['date'])
#         self.parents = []  # array of commit
#         for parent in commit['parents']:
#             self.parents.append(parent['sha'])
    def __init__(self, commit):
#         commit = db.all_commits.find_one({"sha": sha})
#         if commit is None:
#             commit_url = f"https://gitee.com/api/v5/repos/{owner}/{repo}/commits/{sha}"
#             commit = get_text(commit_url)
        
#         print(commit)
        self.sha = commit['sha']
        self.author_login = commit['author']['login']
        self.url = commit['url']
        self.comments_url = commit['comments_url']
#         self.additions = commit['stats']['additions']
#         self.deletions = commit['stats']['deletions']
        self.files = []
        self.timestamp = dateParser(commit['commit']['author']['date'])
        self.parents = []  # array of commit
        if not isinstance(commit['parents'], list):
            commit['parents'] = [commit['parents']]
        for parent in commit['parents']:
            self.parents.append(parent['sha'])
            
    def get_diff(self):
        content = get_text(self.url)
        for file in content['files']:
            self.files.append(file)
# TODO: patch信息提取（diff)


class Issue:
    def __init__(self):
        self.number = ""


class Comment:
    def __init__(self):
        pass
