""" TODO
"""
import sys
from requests import request


class APEWSRequest(object):
    """ TODO
    """

    URL = "http://attempto.ifi.uzh.ch/ws/ape/apews.perl"

    def __init__(self, **kwargs):
        """ TODO
        """
        self._params = kwargs
        self._result = None
        print str(self._params)

    def _get_result(self):
        response = request("GET", self.URL, params=self._params)
        response.raise_for_status()
        if len(response.url) > 2000:
            sys.stderr.write("URL is " + len(response.url)
                             + " character long, switching to POST.")
            response = request("POST", self.URL, data=self._params)
        return response.text

    @property
    def result(self):
        """ TODO
        """

        if not self._result:
            self._result = self._get_result()
        return self._result

    def get_param_value(self, name):
        """ TODO
        """
        return self._params[name]

    def set_param_value(self, name, value):
        self._params[name] = value

    @classmethod
    def _get_default_params(cls):
        """ TODO
        """
        return {
            "text": "",
            "solo": "owlxml"
        }

    @classmethod
    def build(cls, text, **kwargs):
        params = kwargs if kwargs else cls._get_default_params()
        params["text"] = text
        return APEWSRequest(**params)

if __name__ == '__main__':
    r = APEWSRequest(**{
        "text": "Men are human being that have exactly 3 hands.",
        "solo": "owlxml"
    })
    print r.result
