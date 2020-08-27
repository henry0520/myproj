"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

API libs for urllib
"""

import urllib.parse

class QueryUrl:
    """
    Query Url
    """
    def __init__(self, uri=None, *args, **kwargs):
        self.uri = uri

    def parsed(self):
        """
        parse
        """
        return urllib.parse.urlparse(self.uri)

    def parse_qs(self):
        """
        parse qs
        """
        data = {}
        if self.parsed().query:
            data = urllib.parse.parse_qs(self.parsed().query)
        return data

    def dict(self):
        """
        to dictionary
        """
        data = {}
        for key, value in urllib.parse.parse_qs(
                 self.parsed().query, True).items():
            data[key]= "".join(map(str,value))
        return data

    def urlencode(self, dictionary={}):
        """
        url encode
        """
        return urllib.parse.urlencode(dictionary)
