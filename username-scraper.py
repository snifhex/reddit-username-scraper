import os
import csv
import praw
import json
import pandas as pd

usernameList = []
stats = {}


def auth():
    with open('credentials.json', 'r') as json_obj:
        credentials = json_obj.read()
    credentials = json.loads(credentials)
    print(credentials)
    username = credentials['username']
    password = credentials['password']
    client = credentials['client_id']
    secret = credentials['client_secret']
    agent = credentials['user_agent']
    reddit = praw.Reddit(username=username, password=password,
                         client_id=client, client_secret=secret, user_agent=agent)
    return reddit


def usernameDf():
    userDf = pd.read_csv('usernames.csv')
    return userDf


def writer():
    if os.path.isfile('usernames.csv'):
        with open('usernames.csv', 'a') as doc:
            writer = csv.writer(doc)
            for username in usernameList:
                writer.writerow((username,))
    else:
        with open('usernames.csv', 'w') as doc:
            writer = csv.writer(doc)
            writer.writerow(('username',))
            for username in usernameList:
                writer.writerow((username,))


def statWriter():
    if os.path.isfile('stat.csv'):
        with open('stat.csv', 'a') as doc:
            writer = csv.writer(doc)
            for key, values in stats.items():
                writer.writerow((key, values))
    else:
        with open('stat.csv', 'w') as doc:
            writer = csv.writer(doc)
            for key, values in stats.items():
                writer.writerow(('pages', 'usernames'))


def getUsernames(reddit, df):
    page = 0
    for submission in reddit.front.hot():
        page += 1
        count = 0
        if submission.author not in usernameList:
            if submission.author not in df.iloc[:, 0].values:
                usernameList.append(submission.author)
        for comment in submission.comments:
            try:
                if comment.author != 'None' and comment.author not in usernameList:
                    if comment.author not in df.iloc[:, 0].values:
                        usernameList.append(comment.author)
                count += 1
            except:
                break
        stats[page] = count
        print(str(page) + ":" + str(count))


def main():
    reddit = auth()
    df = usernameDf()
    getUsernames(reddit, df)
    writer()
    statWriter()


if __name__ == '__main__':
    main()
