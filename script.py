import platform
import winreg
from selenium import webdriver
supported_os = ['windows', 'ubuntu']
supported_browsers = { 'windows' : {"chrome.exe":"", "iexplore.exe":"", "microsoftedge.exe":""} ,
                       'ubuntu'   : {"chrome":"", "firefox":""}
                     }
supported_webdrivers = { 'windows' : {
                                        "chrome.exe": None,
                                        "iexplore.exe": None,
                                        "microsoftedge.exe": None


                                     } ,
                       'ubuntu'    : { "chrome" : webdriver.Chrome,
                                       "firefox": webdriver.Firefox
                                      }
                     }
def get_os():
    return str.lower(platform.system())
def get_all_browsers(operating_system):
    if operating_system == 'windows':
        apps = 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'
        windows_browsers = supported_browsers['windows']
        access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
        access_key = winreg.OpenKey(access_registry, apps)
        acess_key_count = winreg.QueryInfoKey(access_key)[0]
        exe= []
        #accessing the key to open the registry directories under
        for n in range(acess_key_count):
            try:
                browser = str.lower(winreg.EnumKey(access_key, n))
                print(browser)
                if browser in windows_browsers.keys():
                    app_path = apps+str("\\")+browser
                    handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, app_path)
                    num_values = winreg.QueryInfoKey(handle)[1]
                    for i in range(num_values):
                        paths = winreg.EnumValue(handle, i)
                        windows_browsers[browser] = paths[1]

            except:
                break
    return windows_browsers

def get_browser_path(os_name, browser_name):
    all_browsers = get_all_browsers(os_name)
    print(all_browsers)
    if browser_name in all_browsers.keys():
            return str(all_browsers[browser_name] + "\\" + browser_name)
    else:
        print("error unsupported browser")
        return None
def get_web_driver(os_name, browser_name, browser_path):
    if os_name == 'windows':
        if browser_name == 'chrome.exe':
            supported_webdrivers[os_name][browser_name] = webdriver.Chrome(browser_path)
        elif browser_name == 'iexplore.exe':
            supported_webdrivers[os_name][browser_name] = webdriver.Ie(browser_path)
        elif browser_name == 'microsoftedge.exe':
            supported_webdrivers[os_name][browser_name] = webdriver.Edge(browser_path)
        return supported_webdrivers[os_name][browser_name]

def main(browser_name, url):
    print(supported_browsers)
    os_name = get_os()
    if os_name not in supported_os:
            print("unsupported os")
            return None
    browser_path = get_browser_path(os_name, browser_name)
    if browser_path == None:
        print("browser: ",browser," not found")
        return None
    driver = get_web_driver(os_name, browser_name, browser_path)
    driver.get(url)



if __name__ == '__main__':
    main("chrome.exe", 'https://www.linkedin.com')
