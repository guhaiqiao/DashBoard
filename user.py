import pymongo
import structure
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import shelve
from dateutil.parser import parse as dateParser
MONGO_URL = "mongodb://127.0.0.1:27017"
db = pymongo.MongoClient(MONGO_URL, connect=False, maxPoolSize=200).mindspore


class ContributionType:
    def __init__(self):
        self.code = False
        self.issue = False
        self.pr = False

    def __str__(self):
        return f"code contribution: {self.code}\nissue contribution: {self.issue}\npr contribution: {self.pr}"


class User:
    def __init__(self, login):
        self.username = ''
        self.login = login
        self.contribution_type = ContributionType()
        self.PR = []
        self.commits = []
        self.updateTimestamp = None
    
    def update_info(self):
        get_pr()
        get_commit_frequency()
        self.updateTimestamp = dateParser(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
        
        
    def get_contribution_type(self):
        # try:
        if len(list(db.commits.find({"author.login": self.login}))) != 0:
            self.contribution_type.code = True
        if len(list(db.issues.find({"user.login": self.login}))) != 0:
            self.contribution_type.issue = True
        if len(list(db.pulls.find({"user.login": self.login}))) != 0:
            self.contribution_type.pr = True
        # except

    def get_pr(self):
        if self.updateTimestamp is not None:
            prs = list(db.all_pulls.find({"user.login": self.login, "created_at": {'$gt': str(self.updateTimestamp)}}, sort=[
                                            ("created_at", pymongo.DESCENDING)]))
        else:
            prs = list(db.all_pulls.find({"user.login": self.login, "created_at": {'$gt': str(self.updateTimestamp)}}, sort=[
                                            ("created_at", pymongo.DESCENDING)]))
            print(len(prs))
            for pr in prs:
                self.PR.append(structure.PR(pr))
            print('writing to cache...')
            with shelve.open('cache/user') as db:
                db[self.login] = self
            
    def get_commit_frequency(self):
        print('calculating freq...')
        for pr in self.PR:
            for commit in pr.commits:
                self.commits.append(commit)
        if len(self.commits) == 0:
            return
        else:
            self.commits = sorted(self.commits, key=lambda commit: commit.timestamp)
            start = self.commits[0].timestamp
            time = []
            for commit in self.commits:
                time.append((commit.timestamp - start).months)
            df = pd.DataFrame({"Month":time})
            print(f"Total\t    {len(df)}")
            print(pd.value_counts(df['Month'], sort=False))
        
    @staticmethod
    def get_all_contributor():
        contributors = set()
        for pr in list(db.all_pulls.find()):
            contributors.add(pr['user']['login'])
        name=['contributors']
        data = pd.DataFrame(columns=name,data=contributors)
        data.to_csv('data/contributor.csv',encoding='utf8')
        return contributors


if __name__ == '__main__':
    user = User("jachua")
    user.get_contribution_type()
    print(user.contribution_type)
    user.update_info()
    # User.get_all_contributor()
