import os
from sys import platform as p_os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # return the path of parent directory
OS_ENV = "windows" if p_os == "win32" else "osx" if p_os == "darwin" else "linux"

class Settings:
    # saving address
    profile_location = os.path.join(BASE_DIR, 'profiles')
    profile_commentors_location = os.path.join(BASE_DIR, 'profiles')
    followers_location = os.path.join(BASE_DIR, 'followers')
    #
    profile_file_with_timestamp = True
    profile_commentors_file_with_timestamp = True
    followers_file_with_timestamp = True
    limit_followers_of_followers = 100

    limit_amount = 3
    scrape_posts_infos = False
    scrape_posts_likers = False
    scrape_follower = True
    output_comments = False
    sleep_time_between_post_scroll = 1.5
    sleep_time_between_comment_loading = 1.5
    mentions = True

    log_output_toconsole = True
    log_output_tofile = True
    log_file_per_run = False
    log_location = os.path.join(BASE_DIR, 'logs')

    #from Instpy
    # Set a logger cache outside object to avoid re-instantiation issues
    loggers = {}

    login_username = 'iwannagotofb'
    login_password = '811030'

    #chromedriver
    chromedriver_min_version = 2.36
    specific_chromedriver = "chromedriver_{}".format(OS_ENV)
    chromedriver_location = os.path.join(BASE_DIR, "assets", specific_chromedriver)

    if not os.path.exists(chromedriver_location):
        chromedriver_location = os.path.join(BASE_DIR, 'assets', 'chromedriver')
