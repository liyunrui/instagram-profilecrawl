import os
from tqdm import tqdm
from collections import defaultdict
from util.settings import Settings
from crawl_followers import grab_followers
from util.dataloader import Dataloader
from util.datasaver import Datasaver

def grab_followers_of_followers(followers_list):
    followers_of_followers_dict = defaultdict(list) # default值以一個list()方法產生
    for username in tqdm(followers_list):
        # mock object
        followers_of_followers_list = grab_followers(username)
        followers_of_followers_dict["username"].append(username)
        followers_of_followers_dict["followers_list"].append(followers_of_followers_list)

    return followers_of_followers_dict


f_names = [os.path.join(Settings.followers_location,f_name) 
for f_name in os.listdir(Settings.followers_location) if '.txt' in f_name]


for path_followers_name in f_names:
    brand_name = path_followers_name.split("/")[-1].split("_followers_")[0]
    print ("brand_name : {}".format(brand_name))
    print ("=" * 100)
    followers_list = Dataloader.load_followers_txt(path_followers_name)
    print ("num_followers in this brand: {}".format(len(followers_list)))
    print ("=" * 100)
    followers_of_followers_dict = grab_followers_of_followers(followers_list)
    # save to a csv
    Datasaver.save_followers_of_followers_csv(brand_name,followers_of_followers_dict)
    print ("*" * 100)
