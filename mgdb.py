import uuid

import pymongo
import logging


class Mgdb:

    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)

        # db test
        self.db = client.test
        # collection login
        self.logins = self.db.login

    def find_email(self, email):
        cursor = self.logins.find(email)
        if cursor.count() == 0:
            return False
        return True

    def is_exists(self, user):
        cursor = self.logins.find(user)
        if cursor.count() == 0:
            return False
        return True

    def add_register(self, user):
        if (self.is_exists({'username': user['username']}) or
                self.is_exists({'email': user['email']})) is not True:
            user['fsid'] = uuid.uuid1().hex
            self.logins.insert(user)
            return True

    def get_fsid(self, name):
        cursor = self.logins.find({"username": name})
        if cursor.count() == 1:
            for u in cursor:
                return u['fsid']

if __name__ == '__main__':
    db = Mgdb()
    user = {"username":"chris", "email": "tet@gmail.com"}
    cursor =  db.logins.find({})
    for u in cursor:
        logging.debug(u['fsid'])