import requests


class VKAPI:
    def __init__(self, access_token):
        self.version = "5.73"
        self.__access_token = access_token
        self.__request_template = 'https://api.vk.com/method/{method}?{parameters}&access_token={access_token}&v={version}'

    def get_user_friends(self, user_id):
        parameters = "user_id=" + str(user_id)
        return requests.get(self.__request_template.format(method="friends.get",
                                                           parameters=parameters,
                                                           access_token=self.__access_token,
                                                           version=self.version))
