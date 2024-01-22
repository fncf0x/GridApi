import requests
from GridApi import GridApi as GApi

if __name__ == "__main__":

    api = GApi(
        'grid_email',
        'grid_password',
        'grid_token',
        'port')
    api.login()
    proxy_config = api.get_config()
    proxy_host = proxy_config['ip']
    proxy_port = proxy_config['port']
    proxy_user = proxy_config['user']
    proxy_pass = proxy_config['password']
    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    r = requests.get("http://ifconfig.io/all.json", proxies=proxies)
    print(f"IP: {r.json()['ip']}")
