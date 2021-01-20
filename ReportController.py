import json
from datetime import datetime
from itertools import count

class Result:
    _ids = count(0)
    
    def __init__(self):
        self.id = next(self._ids)
        self.inputString = ''
        self.regex_id = ''
        self.regex = ''
        self.regex_desc = ''
        self.csp_id = ''
        self.csp = '' 
        self.testResult = ''
        self.html_id = ''
        self.html_input = ''
        self.html_output = '' 
         

class Report:
    def __init__(self):
        self.results = []
        self.reportName = ''

    def addResult(self, inputString, regex_id, regex, regex_desc, csp_id, csp, testResult, html_id, html_input, html_output):
        try:
            result = Result()
            result.inputString = inputString
            result.regex_id = regex_id
            result.regex = regex
            result.regex_desc = regex_desc
            result.csp_id = csp_id
            result.csp = csp
            result.testResult = testResult
            result.html_id = html_id
            result.html_output = html_output
            result.html_input = html_input
            self.results.append(result)
        except BaseException as error:
            print('An exception occurred in function addResult of class Report: {}'.format(error))

    def writeReport(self):
        try:
            timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
            self.reportName = 'Reports//report_' + timestamp + '_.json'
            with open(self.reportName, 'w') as outfile:
                json.dump([obj.__dict__ for obj in self.results], outfile)
        except BaseException as error:
            print('An exception occurred in in function writeReport of class Report: {}'.format(error))
