from peewee import *
from passlib.hash import pbkdf2_sha256
import uuid
from time import time
from datetime import timedelta

db = SqliteDatabase('users.db')


class User(Model):

    username = CharField(unique=True)
    auth_token = CharField(null=True)
    ip_address = CharField(unique=True, null=True)
    ip_date = FloatField(null=True)
    password = CharField(null=False)

    class Meta:
        database = db

    @classmethod
    def find(cls, username):
        """
        query user based on their username
        :param username: user's username
        :return: User if found
        """

        try:
            return (cls.select()
                    .where(User.username == username.lower())
                    .get())
        except:
            return None

    @classmethod
    def register(cls, username, password):
        """
        register a new user
        :param username: user's username
        :param password: user's password
        :return: user instance on success
        """

        if cls.find(username.lower()):
            return None

        pswd = pbkdf2_sha256.hash(password)
        user = cls.create(username=username.lower(),
                          auth_token=None,
                          password=pswd)
        user.save()
        return user

    @classmethod
    def login(cls, username, password):
        """
        login user
        :param username: user's username
        :param password: user's password
        :return: auth token on success
        """

        user = cls.find(username.lower())
        if not user:
            raise Exception('user was not found')

        if not pbkdf2_sha256.verify(password, user.password):
            return Exception('password does not match')

        user.auth_token = uuid.uuid4()
        user.save()
        return user.auth_token

    def is_ip_valid(self):
        if not self.ip_date:
            return False
        if time() - self.ip_date > timedelta(minutes=1).seconds:
            return False
        return True

    def get_address(self):
        if not self.is_ip_valid():
            return None

        return self.ip_address

    def set_ip(self, ip_address):
        self.ip_address = ip_address
        self.ip_date = time()
        self.save()

