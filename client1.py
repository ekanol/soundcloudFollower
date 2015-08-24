import sys
import soundcloud
import random
import time
import logging
import config_loader

min_time = 4
max_time = 8

logging.basicConfig(stream=sys.stdout, level=logging.WARN)

logger = logging.getLogger(name='souncloud-python')


def wait_on_action(min_time, max_time):
     wait_time = random.randint(min_time, max_time)
     if wait_time > 0:
            print("Choosing time between %d and %d - waiting %d seconds before action" % (min_time, max_time, wait_time))
            time.sleep(wait_time)

def remove_duplicates(list):
    # Remove duplicates from a list, return uniques
    original_length = len(list)
    ix = 0
    seen = []
    duplicates = []

    while ix < len(list):
        if list[ix] not in seen:
            seen.append(list[ix])
            ix += 1
        else:
            duplicates.append(list[ix])
            list.remove(list[ix])

    print str(len(duplicates)) + ' duplicates out of ' + str(original_length) + ' removed'
    return list

def get_users_from_tracks(tracks):
    users = []
    for track in tracks:
         users.append(track.user)
    return users

def get_ids_from_users(users):
    ids = []
    for user in users:
            ids.append(user["id"])
    return ids

def ask_which_group():
    index=0
    with open('favourite_groups.txt') as f:
        lines = f.read().splitlines()
    for line in lines:
        print(str(index) + ") " + line)
        index += 1
    return lines


class SoundcloudFollower:

    def __init__(self, config_file="config.json"):

        logger.info('Initialising...')

        try:
            config = config_loader.config_setup(config_file)
            self.client = soundcloud.Client(
                client_id=config['CLIENT_ID'],
                client_secret=config['CLIENT_SECRET'],
                username=config['USERNAME'],
                password=config['PASSWORD']
            )
        except Exception, e:
            logger.fatal('Failed to load configuration: %s', e)
            raise e

    def get_group(self, name):
        result = self.client.get('/resolve', url='http://soundcloud.com/groups/' + name)
        print("Group ID = " + str(result.id))
        return result.id

    def scrape_group(self, groupID):
        tracks = self.client.get("/groups/" + str(groupID) + "/tracks")
        return tracks



    def get_unique_ids_from_group(self, groupName):
        result = self.get_group(groupName)
        tracks = self.scrape_group(result)
        users = get_users_from_tracks(tracks)
        ids = get_ids_from_users(users)
        uniques = remove_duplicates(ids)
        return uniques

    def follow_list_of_users(self, list):
        for id in list:
            self.client.put('/me/followings/' + str(id))
            print("Followed user" + str(id))
            wait_on_action(min_time, max_time)






client = SoundcloudFollower()

group_list = ask_which_group()
user_input = input("Which group would you like to scrape?")
unique_ids = client.get_unique_ids_from_group(group_list[user_input])
client.follow_list_of_users(unique_ids)





















