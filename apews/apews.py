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

    def _getResult(self):
        response = request("GET", self.URL, params=self._params)
        response.raise_for_status()
        print response.status_code
        return response.text

    @property
    def result(self):
        """ TODO
        """

        if not self._result:
            self._result = self._getResult()
        return self._result

    def getParamValue(self, name):
        """ TODO
        """
        return self._params[name]

    def setParamValue(self, name, value):
        self._params[name] = value

    @classmethod
    def getParamsDictionary(cls):
        """ TODO
        """
        return {
            "text": "",
            "solo": "owlxml"
        }

if __name__ == '__main__':
    r = APEWSRequest(**{
        "text": "Men are human being that have exactly 3 hands.",
        "solo": "owlxml"
    })
    print r.result
