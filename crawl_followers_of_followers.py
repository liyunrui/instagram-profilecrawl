import os
from tqdm import tqdm
from collections import defaultdict
from util.settings import Settings
from crawl_followers import grab_followers
from util.dataloader import Dataloader
from util.datasaver import Datasaver
from instapy import InstaPy
from instapy import set_workspace
from instapy import smart_run
from tqdm import tqdm
import pandas as pd
import concurrent.futures
import functools
import itertools

# def grab_followers_of_followers(followers_list, amount = "full"):
#     followers_of_followers_dict = defaultdict(list) # default值以一個list()方法產生
#     for username in tqdm(followers_list):
#         try:
#             # mock object
#             followers_of_followers_list = grab_followers(username, live_match = False, amount=amount)
#             followers_of_followers_dict["username"].append(username)
#             followers_of_followers_dict["followers_list"].append(followers_of_followers_list)
#         except:
#             # Unable to save account progress, skipping data update Message: TypeError: window._sharedData is undefined
#             print("Error with user " + username)
#             followers_of_followers_dict["username"].append(username)
#             followers_of_followers_dict["followers_list"].append(["failed to get"])
#     return followers_of_followers_dict

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    out = []
    for i in range(0, len(l), n):
        out.append(l[i:i + n])
    return out

def get_followers_of_followers_dict(followers_list, followers_of_followers_list):

    followers_of_followers_dict = {
        "username":followers_list,
        "followers_list":followers_of_followers_list
    }

    return followers_of_followers_dict

def grab_followers_of_followers(followers_list, live_match = True, amount="full"):
    """
    return list of list(folowers)
    """
    # set workspace folder at desired location (default is at your home folder)
    set_workspace(path=None)

    # get an InstaPy session!
    session = InstaPy(username=Settings.login_username,
                      password=Settings.login_password,
                      headless_browser=False)

    with smart_run(session):
        followers_of_followers_list = []
        for target_user in tqdm(followers_list):
            try:
                selected_followers = session.grab_followers(
                    username=target_user,
                    amount=amount,
                    live_match=live_match,
                    store_locally=True)
            except:
                print("Error with user " + target_user)
                selected_followers = ["failed to get his followers"]

            followers_of_followers_list.append(selected_followers)
            
        return followers_of_followers_list

def grab_followers_of_following(followers_list, live_match = True, amount="full"):
    """
    return list of list(following)
    """
    # set workspace folder at desired location (default is at your home folder)
    set_workspace(path=None)

    # get an InstaPy session!
    session = InstaPy(username=Settings.login_username,
                      password=Settings.login_password,
                      headless_browser=False)

    with smart_run(session):
        followers_of_following_list = []
        for target_user in tqdm(followers_list):
            try:
                selected_following = session.grab_following(
                    username=target_user,
                    amount=amount,
                    live_match=live_match,
                    store_locally=True)
            except:
                print("Error with user " + target_user)
                selected_following = ["failed to get his followers"]

            followers_of_following_list.append(selected_following)
            
        return followers_of_following_list

if __name__ == '__main__':
    # set workspace folder at desired location (default is at your home folder)
    set_workspace(path=None)

    # get an InstaPy session!
    session = InstaPy(username=Settings.login_username,
                      password=Settings.login_password,
                      headless_browser=False)

    f_names = [os.path.join(Settings.followers_location,f_name) 
    for f_name in os.listdir(Settings.followers_location) if '.txt' in f_name]

    for path_followers_name in f_names:
        brand_name = path_followers_name.split("/")[-1].split("_followers_")[0]
        print ("brand_name : {}".format(brand_name))
        print ("=" * 100)
        if Settings.limit_followers_of_followers:
            followers_list = Dataloader.load_followers_txt(path_followers_name)[:Settings.limit_followers_of_followers]
        else:
            followers_list = Dataloader.load_followers_txt(path_followers_name)

        print ("num_followers in this brand: {}".format(len(followers_list)))
        print ("=" * 100)
        #----------------------------------
        # multi-processing
        #----------------------------------
        num_thread = 10
        #followers_list = ["2littybans","tixxit","sevenleafsupply","ashleymckinniee"]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            followers_list = chunks(followers_list, n = num_thread)
            print (followers_list)
            # return the result in the order they started not the order they finished
            results = executor.map(functools.partial(grab_followers_of_following, amount=500), followers_list)
        
        followers_list = list(itertools.chain(*followers_list))
        results = list(results)

        followers_of_following_dict = get_followers_of_followers_dict(followers_list, results)
        # save to a csv
        Datasaver.save_followers_of_followers_csv(brand_name,followers_of_following_dict)
        print ("*" * 100)
        print ("{} finished".format(brand_name))




