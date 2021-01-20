from selenium import webdriver
from TestController import Test
from FilterController import FilterController
from ReportController import Report


def __init__():
    print('Initaializing')
    
    #init selenium chrome
    options = webdriver.ChromeOptions();
    options.add_argument("--headless");
    global driver
    driver = webdriver.Chrome('D:\chromedriver.exe', options = options)
    
    #init filters
    global filters
    filters = FilterController()
    filters.loadRegexFilters() #load xss filters
    filters.loadCSPFilters() #load csp filters
    filters.loadHtmlTypes() #load html types

    #report handler,
    global report
    report = Report()


def PerformXSS(regex_id, csp_id, html_id, inputString):
    try:
        #apply xss filter on input
        filteredString = filters.applyRegexFilter(regex_id, inputString)
        
        #build html with filtered string, csp filter and html type 
        html = filters.htmlTypes[html_id].html_content
        csp = filters.cspFilters[csp_id].csp
        tester = Test()
        tester.inject(html,filteredString,csp)

        #evaluate xss injection
        testResult, html_output = tester.evaluate(driver) #testResult true if xss is successfull

        #build input html page for report; without applying filteration
        html = filters.htmlTypes[html_id].html_content
        csp = filters.cspFilters[csp_id].csp
        tester = Test()
        tester.inject(html,inputString,csp)
        html_input = tester.html_content

        #append results to report
        report.addResult(inputString, regex_id, filters.regexFilters[regex_id].regex, filters.regexFilters[regex_id].description ,csp_id, csp, testResult, html_id, html_input, html_output)

    except BaseException as error:
        print('An exception occurred function applyRegexFilter: {}'.format(error))

def main():
    print('Starting tests')
    #inputs from here
    actions = {
      0: """ "/><script>document.title="XSS-Success"</script> """,
      1: """ "/><SCRIPT>document.title="XSS-Success"</SCRIPT> """,
      2: """ '/><script>document.title="XSS-Success"</script> """,
      3: """ '/><SCRIPT>document.title="XSS-Success"</SCRIPT> """,
      4: """ "/><script src="data:;base64,ZG9jdW1lbnQudGl0bGU9J1hTUy1TdWNjZXNzJw=="></script> """,
      5: """ "/><SCRIPT src="data:;base64,ZG9jdW1lbnQudGl0bGU9J1hTUy1TdWNjZXNzJw=="></SCRIPT> """,
      6: """ '/><script src="data:;base64,ZG9jdW1lbnQudGl0bGU9J1hTUy1TdWNjZXNzJw=="></script> """,
      7: """ '/><SCRIPT src="data:;base64,ZG9jdW1lbnQudGl0bGU9J1hTUy1TdWNjZXNzJw=="></SCRIPT> """,
      8: """ '/<img src="a" onerror="document.title='XSS-Success'" /> """,
      9: """ '/<IMG src="a" onerror="document.title='XSS-Success'" /> """,
      10: """ "/<img src="a" onerror="document.title='XSS-Success'" /> """,
      11: """ "/<IMG src="a" onerror="document.title='XSS-Success'" /> """,
      12: """ '/<img src="a" onerror="document.title='XSS-Success'" > """,
      13: """ '/<IMG src="a" onerror="document.title='XSS-Success'" > """,
      14: """ "/<img src="a" onerror="document.title='XSS-Success'" > """,
      15: """ "/<IMG src="a" onerror="document.title='XSS-Success'" > """,
      16: """ '/<img src="a" onerror="document.title='XSS-Success'"  """,
      17: """ '/<IMG src="a" onerror="document.title='XSS-Success'"  """,
      18: """ "/<img src="a" onerror="document.title='XSS-Success'"  """,
      19: """ "/<IMG src="a" onerror="document.title='XSS-Success'"  """,
      20: """ "/><body onload="document.title='XSS-Success'"> """,
      21: """ "/><body ONLOAD="document.title='XSS-Success'"> """,
      22: """ '/><body onload="document.title='XSS-Success'"> """,
      23: """ '/><body ONLOAD="document.title='XSS-Success'"> """,
      24: """ "/><iframe src="javascript:parent.document.title='XSS-Success'"> </iframe> """,
      25: """ "/><iframe src="JAVASCRIPT:parent.document.title='XSS-Success'"> </iframe> """,
      26: """ '/><iframe src="javascript:parent.document.title='XSS-Success'"> </iframe> """,
      27: """ '/><iframe src="JAVASCRIPT:parent.document.title='XSS-Success'"> </iframe> """,
      28: """ "/><iframe src="&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;&#x70;&#x61;&#x72;&#x65;&#x6E;&#x74;&#x2E;&#x64;&#x6F;&#x63;&#x75;&#x6D;&#x65;&#x6E;&#x74;&#x2E;&#x74;&#x69;&#x74;&#x6C;&#x65;&#x3D;&#x27;&#x58;&#x53;&#x53;&#x2D;&#x53;&#x75;&#x63;&#x63;&#x65;&#x73;&#x73;&#x27;"> </iframe> """,
      29: """ "/><iframe src="&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;&#x70;&#x61;&#x72;&#x65;&#x6E;&#x74;&#x2E;&#x64;&#x6F;&#x63;&#x75;&#x6D;&#x65;&#x6E;&#x74;&#x2E;&#x74;&#x69;&#x74;&#x6C;&#x65;&#x3D;&#x27;&#x58;&#x53;&#x53;&#x2D;&#x53;&#x75;&#x63;&#x63;&#x65;&#x73;&#x73;&#x27;"> </iframe> """,
      30: """ '/><iframe src="&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;&#x70;&#x61;&#x72;&#x65;&#x6E;&#x74;&#x2E;&#x64;&#x6F;&#x63;&#x75;&#x6D;&#x65;&#x6E;&#x74;&#x2E;&#x74;&#x69;&#x74;&#x6C;&#x65;&#x3D;&#x27;&#x58;&#x53;&#x53;&#x2D;&#x53;&#x75;&#x63;&#x63;&#x65;&#x73;&#x73;&#x27;"> </iframe> """,
      31: """ '/><iframe src="&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;&#x70;&#x61;&#x72;&#x65;&#x6E;&#x74;&#x2E;&#x64;&#x6F;&#x63;&#x75;&#x6D;&#x65;&#x6E;&#x74;&#x2E;&#x74;&#x69;&#x74;&#x6C;&#x65;&#x3D;&#x27;&#x58;&#x53;&#x53;&#x2D;&#x53;&#x75;&#x63;&#x63;&#x65;&#x73;&#x73;&#x27;"> </iframe> """
      
    }
   
    #Stage 1
    PerformXSS(regex_id = 1, csp_id = 1, html_id = 1, inputString = actions[0])
    PerformXSS(regex_id = 1, csp_id = 1, html_id = 1, inputString = actions[2])
    PerformXSS(regex_id = 1, csp_id = 1, html_id = 1, inputString = actions[1])

    #Stage 2
    PerformXSS(regex_id = 1, csp_id = 1, html_id = 2, inputString = actions[1])
    PerformXSS(regex_id = 1, csp_id = 1, html_id = 2, inputString = actions[2])
    PerformXSS(regex_id = 1, csp_id = 1, html_id = 2, inputString = actions[3])
    
    #to do 
    #create stages by looping

    #test end
    print("Done..., writing report...")
    report.writeReport()
    print("Report: " + report.reportName)
    print("Done... exiting...")
    driver.quit()
    print("Bye")

__init__()
main()
