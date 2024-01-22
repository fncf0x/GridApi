import requests


class GridApi:
    def __init__(self, username, password, api_key, port):
        self.API_URL = 'https://gridpanel.net/api/'
        self.LOGIN_URL = 'https://gridpanel.net/login?next=/dashboard'
        self.PROXY_MANAGER_URL = 'https://gridpanel.net/dashboard/manage-order?o={}'
        self.PAGINATION_DASHBOARD = 'https://gridpanel.net/dashboard?page={}'
        self.REBOOT_URL = "https://gridpanel.net/api/reboot?token={}"
        self.headers = {
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                      "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Sec-Ch-Ua": "",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"\"",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9"
        }
        self.loggedIn = False
        self.username = username
        self.password = password
        self.api_key = api_key
        self.port = port
        self.proxy_host = ""
        self.proxy_user = ""
        self.proxy_pass = ""
        self.dashboard = ""
        self.proxy_token = ""
        self.sess = requests.Session()

    def login(self):
        r = self.sess.get(self.LOGIN_URL, headers=self.headers)
        csrfmiddlewaretoken = r.text.split('"csrfmiddlewaretoken" value="')[1].split('"')[0]
        data = {
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
            "username": self.username,
            "password": self.password}
        r = self.sess.post(self.LOGIN_URL, headers=self.headers, data=data)
        self.dashboard = r.text
        for i in range(2, 20):
            if str(self.port) in self.dashboard:
                break
            else:
                r = self.sess.get(self.PAGINATION_DASHBOARD.format(i), headers=self.headers)
                self.dashboard = r.text
        if "/dashboard/manage-order" not in self.dashboard:
            return False
        self.get_proxy_config()
        return True

    def get_proxy_config(self):
        proxy_part = self.dashboard.split(str(self.port))[1][:300]
        proxy_manage_id = proxy_part.split('/dashboard/manage-order?o=')[1].split('"')[0]
        r = self.sess.get(self.PROXY_MANAGER_URL.format(proxy_manage_id), headers=self.headers)
        self.proxy_token = r.text.split('https://gridpanel.net/api/reboot?token=')[1].split('"')[0]
        proxy_curl = r.text.split(
            'connection_string" type="text" class="form-control" readonly value="'
        )[1].split('"')[0]
        self.proxy_host = proxy_curl.split('@')[1].split(':')[0]
        self.proxy_user = proxy_curl.split('@')[0].split('//')[1].split(':')[0]
        self.proxy_pass = proxy_curl.split('@')[0].split('//')[1].split(':')[1]
        return True

    def reboot(self):
        self.sess.get(self.REBOOT_URL.format(self.proxy_token), headers=self.headers)

    def get_config(self):
        return {
            "ip": self.proxy_host,
            "port": self.port,
            "user": self.proxy_user,
            "password": self.proxy_pass
        }
