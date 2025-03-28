import requests


def disable_ssl_verification():
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    old_send = requests.Session.send

    def new_send(*args, **kwargs):
        kwargs['verify'] = False
        return old_send(*args, **kwargs)

    requests.Session.send = new_send
