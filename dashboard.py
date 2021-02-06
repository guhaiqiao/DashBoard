import data_util
import os
import pandas as pd

def get_contributors(owner, repo):
    type = 'contributors'
    path = f'data/{owner}-{repo}-{type}.csv'
    if not os.path.exists(path): 
        data_util.get_contributors(owner, repo)
    data = pd.read_csv(path)
    contributors = [x[2] for x in data.values]
    return contributors

def get_contributor_issue_open_number(owner, repo, contributor):
    data = pd.read_csv(f'data/{owner}-{repo}-issues.csv')
    count = [x[5] == contributor for x in data.values].count(True)
    return count

def get_all_contributors_issue_open_number(owner, repo):
    data = pd.DataFrame()
    for contributor in get_contributors(owner, repo):
        data = data.append([{'contributor': contributor, 'issues': get_contributor_issue_open_number(owner, repo, contributor)}], ignore_index=True)
    data.to_csv('data/issue_open_number.csv')

if __name__ == '__main__':
    owner = 'mindspore'
    repo = 'mindspore'
    get_all_contributors_issue_open_number(owner, repo)