""" TODO
"""
import sys
from requests import request


class APEWSRequest(object):
    """ TODO
    """

    __url = "http://attempto.ifi.uzh.ch/ws/ape/apews.perl"
    __default = {
        'text': '',
        'file': '',
        'ulextext': '',
        'ulexfile': '',
        'ulexreload': 'off',
        'uri': '',
        'guess': 'off',
        'noclex': 'off',
        'solo': '',
        'cdrs': 'off',
        'cdrshtml': 'off',
        'cdrspp': 'off',
        'cdrsxml': 'off',
        'cfol': 'off',
        'cowlfss': 'off',
        'cowlfsspp': 'off',
        'cowlrdf': 'off',
        'cowlxml': 'off',
        'cparaphrase': 'off',
        'cparaphrase1': 'off',
        'cparaphrase2': 'off',
        'cpnf': 'off',
        'cruleml': 'off',
        'csentences': 'off',
        'csyntax': 'off',
        'csyntaxd': 'off',
        'csyntaxdpp': 'off',
        'csyntaxpp': 'off',
        'ctokens': 'off',
        'ctptp': 'off',
    }

    def __init__(self, **kwargs):
        """ TODO
        """

        self._result = None

        # SET THE REQUEST PARAMS
        # only the allowed arguments must be kept
        # i.e. only those with the key in the default
        # params dictionary. The params with a default
        # value will be discarded in order to keep the
        # request URL/payload as small as possible
        self._params = {}
        for k, v in kwargs.iteritems():
            if k in self.__default and v != self.__default[k]:
                self._params[k] = v

    def _get_result(self):
        response = request("GET", self.__url, params=self._params)
        response.raise_for_status()
        if len(response.url) > 2000:
            # if the url is longer than 2000 chars, then the
            # HTTP protocol denies the possibilities of a GET
            # request, so it must be switch to POST. This
            # operation is notified with a stderr message.
            sys.stderr.write("URL is " + str(len(response.url))
                             + " character long, switching to POST.")
            response = request("POST", self.__url, data=self._params)
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

        if name in self._params:
            return self._params[name]
        if name in self.__default:
            return self.__default[name]
        raise ValueError("Illegal parameter name: '" + name + "'")

    def set_param_value(self, name, value):
        """ TODO
        """

        if name not in self.__default:
            ValueError("Illegal parameter name: '" + name + "'")
        if self.__default[name] != value:
            self._params[name] = value

    @classmethod
    def build(cls, text, **kwargs):
        params = kwargs if kwargs else {}
        params["text"] = text
        return APEWSRequest(**params)

if __name__ == '__main__':
    r = APEWSRequest(**{
        "text": "Men are human being that have exactly 3 hands.",
        "solo": "owlxml"
    })
    print r.result
    print

    r = APEWSRequest.build("Every human being is mortal.",
                           **{"solo": "owlxml"})
    print r.result
    print
