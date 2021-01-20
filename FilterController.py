import json
import re

class RegexFilter:
    def __init__(self):
        self.description = ''
        self.id = ''
        self.regex = ''
        self.ignore_case = False #if false ignorecase in regex
        self.url_encoding = False #if true then perform url decoding
        self.html_encoding = False #if true then perform html decoding

    def __str__(self):
        return "description: {}, id: {}, regex: {} , url_encoding: {}, html_encoding: {}".format(self.description, self.level, self.regex, self.url_encoding, self.html_encoding)

class CSPFilter:
    def __init__(self):
        self.id = ''
        self.csp = ''

    def __str__(self):
        return "id: {}, csp: {}".format(self.id, self.csp)

class HTML:
    def __init__(self):
        self.id = ''
        self.html_content = ''
        self.description = ''

    def __str__(self):
        return "id: {}, description: {}, html_content: {}".format(self.id, self.description, self.html_content)


class FilterController:
    def __init__(self):
        self.regexFilters = []
        self.cspFilters = []
        self.htmlTypes = []

    def loadRegexFilters(self):
        try:
            #load filters from file
            with open('regex_filters.json') as json_file:
                filters = json.load(json_file)
                for filter in filters['filters']:
                    f = RegexFilter()
                    f.description = filter['description']
                    f.id = filter['id']
                    f.regex = filter['regex']
                    f.ignore_case = eval(filter['ignore_case'])
                    f.url_encoding = eval(filter['url_encoding'])
                    f.html_encoding = eval(filter['html_encoding'])
                    self.regexFilters.append(f)
        except BaseException as error:
            print('An exception occurred in function addResloadRegexFilters of class FilterController: {}'.format(error))

    def loadCSPFilters(self):
        try:
            #load filters from file
            with open('csp_filters.json') as json_file:
                filters = json.load(json_file)
                for filter in filters['filters']:
                    f = CSPFilter()
                    f.id = filter['id']
                    f.csp = filter['csp']
                    self.cspFilters.append(f)
        except BaseException as error:
            print('An exception occurred in function loadCSPFilters of class FilterController: {}'.format(error))

    def loadHtmlTypes(self):
        try:
            #load html types from file
            with open('html_types.json') as json_file:
                html_types = json.load(json_file)
                for html in html_types['html_types']:
                    h = HTML()
                    h.id = html['id']
                    h.html_content = html['html']
                    h.description = html['description']
                    self.htmlTypes.append(h)
        except BaseException as error:
            print('An exception occurred in function loadHtmlTypes of class FilterController: {}'.format(error))

    def applyRegexFilter(self,level_index, injectionString):
        try:
            #based on regex remove matching characters
            regex = self.regexFilters[level_index].regex
            if regex == '':
                return injectionString #if regex is empty return string as it is
            if self.regexFilters[level_index].ignore_case: #check for ignorecase
                return re.sub(regex, '***anti-hacker***' ,injectionString, flags=re.IGNORECASE)
            return re.sub(regex, '***anti-hacker***' ,injectionString)
        except BaseException as error:
            print('An exception occurred in function applyRegexFilter of class FilterController: {}'.format(error))
