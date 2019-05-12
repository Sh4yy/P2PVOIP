import requests
import json


class API:

    def __init__(self, address, puncher):
        self.address = "http://" + address
        self.puncher = puncher
        self._auth = None

    def login(self, username, password):
        path = self.address + "/login"
        json = requests.post(path, auth=(username, password)).json()

        if not json['ok']:
            raise Exception("something went wrong")

        self._auth = json['token']
        return self._auth

    def register(self, username, password):
        path = self.address + "/register"
        json = requests.post(path, auth=(username, password)).json()

        if not json['ok']:
            raise Exception("something went wrong")

        return True

    def create_header(self):
        if not self._auth:
            raise Exception("missing auth token, please login")
        return {"Authorization": "Bearer " + self._auth,
                "Content-Type": "application/json"}

    def get_address(self, username):
        """
        get user's address
        :param username: target user
        :return: ip address in success
        """
        path = self.address + f"/user/{username}/address"
        json = requests.get(path, headers=self.create_header()).json()

        if not json['ok']:
            raise Exception("something went wrong")

        return json['address']

    def my_address(self, sock):
        """
        get my ip address
        :param sock: socket instance
        :return: address
        """
        return self.puncher.get_addr(sock)

    def update_my_address(self, sock):

        path = self.address + f"/user/me/address"
        data = json.dumps({'address': self.my_address(sock)})
        resp = (requests.post(path,
                              data=data,
                              headers=self.create_header())
                        .json())

        if not resp['ok']:
            raise Exception("something went wrong")

        return True