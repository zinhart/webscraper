import platform
import winreg
import sys
from time import sleep
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
    if browser_name in all_browsers.keys():
            return str(all_browsers[browser_name] + "\\" + browser_name)
    else:
        print("error unsupported browser")
        return None
def get_web_driver(os_name, browser_name):
    if os_name == 'windows':
        if browser_name == 'chrome.exe':
            supported_webdrivers[os_name][browser_name] = webdriver.Chrome()
        elif browser_name == 'iexplore.exe':
            supported_webdrivers[os_name][browser_name] = webdriver.Ie()
        elif browser_name == 'microsoftedge.exe':
            supported_webdrivers[os_name][browser_name] = webdriver.Edge()
        return supported_webdrivers[os_name][browser_name]

def main(browser_name, url, usr, pw):
    os_name = get_os()
    if os_name not in supported_os:
            print("unsupported os")
            return None
    browser_path = get_browser_path(os_name, browser_name)
    if browser_path == None:
        print("browser: ",browser," not found")
        return None
    driver = get_web_driver(os_name, browser_name)
    driver.get(url)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(usr)
    sleep(0.5)
    password.send_keys(pw)
    sleep(0.5)

#    sign_in_button = driver.find_element_by_class_name('signin')
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()



if __name__ == '__main__':
    '''
    if len(sys.argv) != 5:
        print("error")
        exit()
    '''
    browser_name = sys.argv[1]
    url = sys.argv[2]
    usr = sys.argv[3]
    pw  = sys.argv[4]
    print(browser_name, url, usr, pw)
    main("chrome.exe", 'https://www.linkedin.com/login', usr, pw)
