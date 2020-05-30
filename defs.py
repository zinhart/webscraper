supported_os = ['windows', 'ubuntu']
supported_browsers = { 'windows' : {"chrome.exe":"", "iexplore.exe":"", "microsoftedge.exe":""} ,
                       'ubuntu'   : {"chrome":"", "firefox":""}
                     }
supported_webdrivers = { 'windows' : {
                                        "chrome.exe": None,
                                        "iexplore.exe": None,
                                        "microsoftedge.exe": None


                                     } ,
                       'ubuntu'    : { "chrome" : None,
                                       "firefox": None
                                      }
                     }
logged_in = False
webdriver = None
csv_writer = None
