class Test:
    def __init__(self):
        self.result = False # false if test fails
        self.executed = False # false if test did not run
        self.title = 'XSS-Success' # string to check against
        self.html_content = ''

    def __str__(self):
        return "html: {} ,\n result: {},\n executed: {}".format(self.html_content, self.result, self.executed)

    def inject(self, html, xss, csp):
        try:
            js_return_func = """ <script> function getTitle() { return document.title; } </script> """

            self.html_content = html.format(inject_xss  = xss, inject_csp = csp, inject_return_func = js_return_func)
        except BaseException as error:
            print('An exception occurred in function inject of class Test: {}'.format(error))

    def evaluate(self, driver):
        try:
            #inject html code with script in browser
            driver.get("data:text/html;charset=utf-8," + self.html_content)
            #check if title has chganed, if so then test passed
            title = driver.execute_script('return getTitle()')
            if title == self.title:
                self.result = True
            self.executed = True
            return self.result, driver.page_source
        except BaseException as error:
            #check if injection failed due to CSP
            try:
                console_logs = driver.get_log('browser')
                check_csp = console_logs[-1]
                if 'Refused' in check_csp['message']: #if due to csp then do not print exception
                    return self.result, driver.page_source
                print('\nAn exception occurred in function evaluate of class Test: {}'.format(error))
            except BaseException as error:
                print('An exception occurred in function evaluate except block of class Test: {}'.format(error))
            
