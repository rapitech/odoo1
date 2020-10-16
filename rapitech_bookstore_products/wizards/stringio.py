url = 'https://static.megustaleer.com.ar//images//libros_650_x//9788420435404.jpg'

import base64
import requests


def get_as_base64(url):

    return base64.b64encode(requests.get(url).content)


print (get_as_base64(url))