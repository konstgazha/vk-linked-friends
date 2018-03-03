# -*- coding: utf-8 -*-
from pyvirtualdisplay import Display
import crawlers
import json
import requests


class VKManager:
    def __init__(self, login, password, client_id):
        self.login = login
        self.password = password
        self.client_id = client_id
        self.url_auth = 'https://oauth.vk.com/authorize?client_id={0}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&respоnse_type=token'.format(client_id)
    
    def get_new_access_token(self):
        crawler = crawlers.SeleniumCrawler()
        crawler.driver.get(self.url_auth)
        crawler.wait_loading_by_class('oauth_from_input')
        
        login_fields = crawler.driver.find_elements_by_class_name('oauth_form_input')
        login_fields[0].send_keys(self.login)
        login_fields[1].send_keys(self.password)
        crawler.driver.find_element_by_id('install_allow').click()
        try:
            crawler.driver.find_element_by_class_name('button_indent').click()
        except:
            pass
        
        response_url_auth = crawler.driver.current_url
        
        code = response_url_auth.split('=')[-1]
        
        # fill headers
        url_access_token = 'https://oauth.vk.com/access_token?client_id=&client_secret=&redirect_uri=https://oauth.vk.com/blank.html&code='
        soap_access_token = crawler.get_soup('{0}{1}'.format(url_access_token, code))
        access_token = json.loads(soap_access_token.text)['access_token']
        crawler.close()
        return access_token
