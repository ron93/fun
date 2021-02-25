
import os
from os.path import isfile
import praw
import pandas as pd 
from time import sleep
import requests
import urllib.request
from pathlib import Path

#get credentiald from DEFAULT instance of praw.ini
reddit = praw.Reddit()
csv_file = Path('../../data/csv/')

class SubredditScraper:
    def __init__(self, sub, sort='new', lim=900, mode='w'):
        self.sub = sub
        self.sort = sort 
        self.lim = lim
        self.mode = mode

        print (
            f'SubredditScraper instance created with values '
            f'sub = {sub}, sort = {sort}, lim = {lim}, mode = {mode}'
        )

    def set_sort(self):
        if self.sort == 'new':
            return self.sort, reddit.subreddit(self.sub).new(limit=self.lim)
        elif self.sort == 'top':
            return self.sort, reddit.subreddit(self.sub).top(limit=self.lim)
        elif self.sort == 'hot':
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)
        else:
            self.sort = 'hot'
            print('Sort method was not recognized, defaulting to hot.')
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)

    def get_posts(self):
        """get unique posts from a specified subreddit"""
        sub_dict = {
            'selftext':[],"title":[],"id":[],"sorted_by":[],"num_comments":[],"score" :[], "ups":[], "downs":[] ,"url":[]
            }
            #-->start debug
    #    csv_file = os.listdir('../../data/csv/')
        csv = os.path.join(csv_file, f'{self.sub}_post.csv')
        #todo: create sub-reddit image folder--->
        
        #sorting method 
        sort, subreddit = self.set_sort()

        #set csv loaded to true 
        df , csv_loaded = (pd.read_csv(csv), 1) if isfile(csv) else('',0)
        

        print(f'csv = {csv}')
        print(f'After set_sort(), sort = {sort} and sub = {self.sub}')

        print(f'csv_loaded = {csv_loaded}')
        print(f'Collecting information from r/{self.sub}.')

        for post in subreddit:

        # Check if post.id is in df and set to True if df is empty.
        # This way new posts are still added to dictionary when df = ''
            unique_id = post.id not in tuple(df.id) if csv_loaded else True

            # Save any unique posts to sub_dict.
            if unique_id:
                sub_dict['selftext'].append(post.selftext)
                sub_dict['title'].append(post.title)
                sub_dict['id'].append(post.id)
                sub_dict['sorted_by'].append(sort)
                sub_dict['num_comments'].append(post.num_comments)
                sub_dict['score'].append(post.score)
                sub_dict['ups'].append(post.ups)
                sub_dict['downs'].append(post.downs)
                sub_dict['url'].append(post.url)
            sleep(0.1)


            new_df = pd.DataFrame(sub_dict)


            if 'DataFrame' in str(type(df)) and self.mode == 'w':
                pd.concat([df, new_df], axis=0, sort=0).to_csv(csv, index=False)
                print(
                    f'{len(new_df)} new posts collected and added to {csv}')
            elif self.mode == 'w':
                new_df.to_csv(csv, index=False)
                print(f'{len(new_df)} posts collected and saved to {csv}')
            else:
                print(
                    f'{len(new_df)} posts were collected but they were not '
                    f'added to {csv} because mode was set to "{self.mode}"')
if __name__ == '__main__':
    SubredditScraper(
        'earthporn',
         lim=997,
         mode='w',
         sort='new').get_posts()
        