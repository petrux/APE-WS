""" Interface to the APE web service.

The apews module implements the interface to the APE
Web Service (see http://attempto.ifi.uzh.ch/site/resources/).
The available configurations are (tab separated):

text	string	ACE text
file	URL	URL of an ACE text
ulextext	string	User lexicon
ulexfile	URL	URL of a user lexicon
ulexreload	on | off	Reload the user lexicon. This has effect only if ulexfile is specified.
noclex	on | off	Ignore the lexicon entries that are built into into the webservice (i.e. rely only on the user lexicon and/or guessing).
guess	on | off	Guess the word-class (common noun, verb, adjective, adverb) of unknown words. I.e. a text containing unknown words is not rejected, instead, the parser tries to figure out the word-class of such words automatically. Note that the parser does not try to lemmatize such words, e.g. unknown plural nouns would be stored in the DRS in the plural form, not in their lemma (i.e. singular) form.
uri	URI	Ontology URI (only used in the OWL outputs).
cdrs	on | off	Output the DRS as a Prolog term.
cdrsxml	on | off	Output the DRS in XML.
cdrspp	on | off	Output the DRS in pretty-printed form in plain text.
cdrshtml	on | off	Output the DRS in pretty-printed form in HTML.
cparaphrase	on | off	Output a paraphrase that is a ``best-effort'' combination of paraphrase1 and paraphrase2.
cparaphrase1	on | off	Output a paraphrase that uses full sentences instead of relative clauses.
cparaphrase2	on | off	Output a paraphrase that uses relative clauses instead of full sentences. This paraphrase can currently handle if-then sentences that do not contain any modifiers, of-constructions, ditransitive verbs and noun phrase coordination. Note: experimental.
ctokens	on | off	Output tokens as a Prolog list of lists of atoms.
csentences	on | off	Output sentences as a Prolog list of atoms.
csyntax	on | off	Output simplified syntax trees as a Prolog list.
csyntaxpp	on | off	Output simplified syntax trees in pretty-printed form.
csyntaxd	on | off	Output plain syntax trees as a Prolog list (for debugging).
csyntaxdpp	on | off	Output plain syntax trees in pretty-printed form (for debugging).
cowlfss	on | off	Output OWL/SWRL in the functional representation as a Prolog term.
cowlfsspp	on | off	Output OWL/SWRL in the functional representation pretty-printed.
cowlrdf	on | off	Output OWL/SWRL in the RDF/XML representation. DEPRECATED
cowlxml	on | off	Output OWL/SWRL in the XML representation.
cfol	on | off	Output the standard first-order logic (FOL) representation of the DRS (as a Prolog term).
cpnf	on | off	Output the standard FOL representation (Prenex Normal Form) of the DRS (as a Prolog term).
ctptp	on | off	Output the TPTP representation of the DRS. This format is directly usable as the input format for most FOL theorem provers.
cruleml	on | off	Output the RuleML representation of the DRS.
solo	drs | drsxml | drspp | drshtml | paraphrase | paraphrase1 | paraphrase2 | tokens | sentences | syntax | syntaxpp | syntaxd | syntaxdpp | owlfss | owlfsspp | owlrdf | owlxml | fol | pnf | tptp | ruleml	Output just one output component. For drspp, paraphrase, paraphrase1, paraphrase2, syntaxpp, syntaxdpp, owlfsspp, the output is in plain text; for drs, tokens, sentences, syntax, syntaxd, owlfss, fol, pnf, the output is in Prolog term notation, for drsxml, drshtml, owlrdf, owlxml, ruleml the output is in XML. For tptp, the output is in TPTP.
"""

import sys
from requests import request


class APEWSRequest(object):
    """ HTTP Web Request to APE Web Service."""

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
