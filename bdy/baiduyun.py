# coding: utf-8
##
# @file baiduyun.py
# @brief 
# @author scusjs@foxmail.com
# @version 0.1.00
# @date 2016-12-28
from __future__ import print_function, unicode_literals
import json
import requests
from . import utils


class BaiduYun(object):
    def __init__(self, oauth_info, verify = True):
        self.oauth_info = oauth_info
        self.base_url = utils.get_config("base_url")
        self.base_path = utils.get_config("base_path")
        self.verify = verify

    def space_info(self):
        params = {"method": "info",
                  "access_token": self.oauth_info['access_token']}
        response = requests.get(utils.get_config('quota_url'),
                                params=params, verify=self.verify)
        result = response.json()
        if 'error_code' in result:
            return False, result
        return True, result

    def list_dir(self, path="/", method='list', by='time'):
        path = self.base_path + path
        params = {"method": method,
                  "access_token": self.oauth_info['access_token'],
                  "by": by,
                  "path": path}
        response = requests.get(self.base_url,
                                params=params, verify=self.verify)
        result = response.json()
        if 'error_code' in result:
            return False, result
        result = self._get_result_list(result['list'])
        return True, result

    def search_file(self, keyword, path="/", re=1, method='search'):
        path = self.base_path + path
        params = {"method": method,
                  "access_token": self.oauth_info['access_token'],
                  "path": path,
                  "wd": keyword,
                  "re": re}
        response = requests.get(self.base_url,
                                params=params, verify=self.verify)
        result = response.json()
        if 'error_code' in result:
            return False, result
        result = self._get_result_list(result['list'])
        return True, result

    def _get_download_info(self, path):
        download_url_list = [
                "https://d.pcs.baidu.com/rest/2.0/pcs/file?" \
                "method=download&access_token={access_token}" \
                "&path={path}",
                "https://pcs.baidu.com/rest/2.0/pcs/file?" \
                "method=download&access_token={access_token}" \
                "&path={path}",
            ]
        return [i.format(access_token=self.oauth_info['access_token'], path=path) for i in download_url_list]

    def _get_result_list(self, file_list):
        for i, val in enumerate(file_list):
            val['download'] = self._get_download_info(val['path'])
            val['name'] = (val['path']).split('/')[-1]
            file_list[i] = val
        return file_list

