import platform
import winreg
from selenium import webdriver
supported_os = ['windows', 'ubuntu']
[]
supported_browsers = { 'windows' : {"chrome.exe":"", "iexplore.exe":"", "safari":""} ,
                       'ubuntu'   : {"chrome":"", "safari":""}
                     }
def get_os():
    return str.lower(platform.system())
def get_browsers(operating_system):
    if operating_system == 'windows':
        apps = 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'
        windows_browsers = supported_browsers['windows']
        print(windows_browsers)
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
                    print(app_path)
                    handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, app_path)
                    num_values = winreg.QueryInfoKey(handle)[1]
                    for i in range(num_values):
                        windows_browsers[browser] = winreg.EnumValue(handle, i)
            except:
                break

    print(windows_browsers)
    return None


def main(browser, url):
    print(supported_browsers)
    os_name = get_os()
    if os_name not in supported_os:
            print("unsupported os")
    else:
        browsers_and_paths = get_browsers(os_name)

if __name__ == '__main__':
    main("chrome", 'https://www.linkedin.com')
browsers = {}
{

"edge":"C:\Program Files (x86)\Google\Chrome\Application",
"chrome": "C:\Windows\SystemApps\Microsoft.MicrosoftEuuudge_8wekyb3d8bbwe"
}
