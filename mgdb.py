import uuid

import pymongo
import logging
import time
import os
import gvars


class Mgdb:
    '''
    login: {
        'username':
        'password':
        'email'
        'fsid'
        }

    user: {
        'name'
        'fsid'
        'avatar'
        'age'
        'city'
        'quote'
    }
    '''

    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)

        # db test
        self.db = client.test
        # collection login
        self.logins = self.db.login
        self.users = self.db.user

    def find_email(self, email):
        cursor = self.logins.find(email)
        if cursor.count() == 0:
            return False
        return True

    def find_login(self, user):
        return self.logins.find_one(user)

    def find_user(self, user):
        return self.users.find_one(user)

    def add_login(self, user):
        if self.find_login({'username': user['username']}) is None:
            if self.find_login({'email': user['email']}) is None:
                user['fsid'] = uuid.uuid1().hex
                # add to db.login
                self.logins.insert(user)

                # add to db.user
                r_time = time.strftime('%y-%m-%d', time.localtime(time.time()))
                self.users.insert({'name': user['username'], 'fsid': user['fsid'], 'register_time': r_time})
                return True

    def get_fsid(self, name):
        one = self.find_login({"username": name})
        if one:
            return one['fsid']

    def get_avatar(self, name):
        one = self.find_user({"name": name})
        if one and 'avatar' in one:
            return gvars.image_url + one['avatar']

    def update_avatar(self, name, avatar):
        user = self.users.find_one({'name': name})
        if 'avatar' in user:
            old_avatar = os.path.join(gvars.image_dir, user['avatar'])
            if os.path.exists(old_avatar): # remove old image
                os.remove(old_avatar)
        self.users.update({'name': name}, {'$set': {'avatar': avatar}})

    def update_user(self, name, user):
        result = self.users.update({'name': name}, {'$set': user})
        if result['nModified'] > 0:
            return True
        return False


if __name__ == '__main__':
    name = 'chris'
    user = {'avatar':'xxxx'}
    r = Mgdb().get_avatar('1')
    print r
