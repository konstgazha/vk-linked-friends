# -*- coding: utf-8 -*-
from pyvirtualdisplay import Display
import json
import crawlers
import vkapi
from functools import reduce


class VKManager:
    def __init__(self):
        self.redirect_uri = "https://oauth.vk.com/blank.html"
        self.url_auth = 'https://oauth.vk.com/authorize?client_id={0}&display=page&redirect_uri={1}&scope=friends&respоnse_type=token'.format(client_id, self.redirect_uri)
        self.login = ""
        self.password = ""
        self.crawler = ""
    
    def auth(self, login, password):
        self.login = login
        self.password = password
        if not self.crawler:
            self.crawler = crawlers.SeleniumCrawler()
        self.crawler.driver.get(self.url_auth)
        self.crawler.wait_loading_by_class('oauth_from_input')
        login_fields = self.crawler.driver.find_elements_by_class_name('oauth_form_input')
        login_fields[0].send_keys(self.login)
        login_fields[1].send_keys(self.password)
        self.crawler.driver.find_element_by_id('install_allow').click()
        try:
            self.crawler.driver.find_element_by_class_name('button_indent').click()
        except:
            pass

    def get_new_access_token(self, client_id, client_secret):
        if not self.crawler:
            self.crawler = crawlers.SeleniumCrawler()
            raise('OMG')
        response_url_auth = self.crawler.driver.current_url
        code = response_url_auth.split('=')[-1]
        url_access_token = 'https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&redirect_uri={2}&code={3}'
        soap_access_token = self.crawler.get_soup(url_access_token.format(client_id, client_secret, self.redirect_uri, code))
        access_token = json.loads(soap_access_token.text)['access_token']
        self.crawler.close()
        return access_token


def get_friends_intersection(users):
    return reduce(set.intersection, map(set, users))

login = ""
password = "$"
client_id = ""
client_secret = ""

vkm = VKManager()
vkm.auth(login, password)
access_token = vkm.get_new_access_token(client_id, client_secret)
print(access_token)
# access_token = ""

vk_api = vkapi.VKAPI(access_token)
friends = []
users = []
for u in users:
    friends.append((vk_api.get_user_friends(u)['response']['items']))

print(get_friends_intersection(friends))
