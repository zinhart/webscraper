import platform
import winreg
import sys
from time import sleep
from selenium import webdriver
from openpyxl import Workbook
import csv
import defs


def get_os():
    return str.lower(platform.system())
def get_all_browsers(operating_system):
    if operating_system == 'windows':
        apps = 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'
        windows_browsers = defs.supported_browsers['windows']
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
            defs.supported_webdrivers[os_name][browser_name] = webdriver.Chrome()
        elif browser_name == 'iexplore.exe':
            defs.supported_webdrivers[os_name][browser_name] = webdriver.Ie()
        elif browser_name == 'microsoftedge.exe':
            defs.supported_webdrivers[os_name][browser_name] = webdriver.Edge()
        return defs.supported_webdrivers[os_name][browser_name]

def login(browser_name, url, usr, pw):
    os_name = get_os()
    if os_name not in defs.supported_os:
            print("unsupported os")
            return False
    browser_path = get_browser_path(os_name, browser_name)
    if browser_path == None:
        print("browser: ",browser," not found")
        return False
    driver = get_web_driver(os_name, browser_name)
    driver.get(url)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(usr)
    password.send_keys(pw)
    sleep(0.75)
    # xpath from chropath
    sign_in_button = driver.find_element_by_xpath('//button[@type="submit"]')
    sign_in_button.click()
    defs.webdriver = driver

    return True

def go_to_my_jobs():
    if defs.logged_in is True:
        print("going to my jobs")
        defs.webdriver.find_element_by_xpath('//a[@href="/jobs/"]').click()

def get_saved_jobs():
    if defs.logged_in is True:
        print("getting saved jobs")
        defs.webdriver.get("https://www.linkedin.com/jobs/tracker/saved/")
        rows = []
        rows.append(['positions', 'companies', 'job locations', 'days old/current # of applicants', 'applied', 'date application sent', 'result', 'date received' ])
        scroll_pause_time = 2.0
        # Get scroll height
        last_height = defs.webdriver.execute_script("return document.body.scrollHeight")
        while True:
            position_titles = defs.webdriver.find_elements_by_xpath("//*[starts-with(@id, 'ember') and @class='jobs-job-card-content__title ember-view'] ")
            companies_names = defs.webdriver.find_elements_by_xpath("//*[starts-with(@id, 'ember') and @class='t-black jobs-job-card-content__company-name t-14 t-normal ember-view']")
            job_location = defs.webdriver.find_elements_by_xpath("//*[@class='t-12 t-black--light']")
            bullets = defs.webdriver.find_elements_by_xpath("//*[@class='jobs-job-card-content__info t-12 t-black--light mt2 pt3']")
            for (pt, cn, jl, bl) in zip(position_titles, companies_names, job_location, bullets):
                rows.append([pt.text, cn.text, jl.text, bl.text, '', '', '', ''])
            # Scroll down to bottom
            defs.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = defs.webdriver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return rows

def get_applied_jobs():
        defs.webdriver.get("https://www.linkedin.com/jobs/tracker/applied/")
        rows = []
        rows.append(['positions', 'companies', 'job locations'])
        scroll_pause_time = 2.0
        # Get scroll height
        last_height = defs.webdriver.execute_script("return document.body.scrollHeight")
        while True:
            position_titles = defs.webdriver.find_elements_by_xpath("//*[starts-with(@id, 'ember') and @class='jobs-job-card-content__title ember-view'] ")
            companies_names = defs.webdriver.find_elements_by_xpath("//*[starts-with(@id, 'ember') and @class='t-black jobs-job-card-content__company-name t-14 t-normal ember-view']")
            job_location = defs.webdriver.find_elements_by_xpath("//*[@class='t-12 t-black--light']")
            for (pt, cn, jl) in zip(position_titles, companies_names, job_location):
                rows.append([pt.text, cn.text, jl.text])
            # Scroll down to bottom
            defs.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = defs.webdriver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return rows
def main():
    if len(sys.argv) != 5:
        print("error")
        exit()
    browser_name = sys.argv[1]
    url = sys.argv[2]
    usr = sys.argv[3]
    pw  = sys.argv[4]
    print(browser_name, url, usr, pw)
    defs.logged_in  = login(browser_name, url, usr, pw)
    go_to_my_jobs()
    saved_jobs = get_saved_jobs()
    print(saved_jobs)
    print("===========================================================")
    applied_jobs = get_applied_jobs();
    print(applied_jobs)

    '''
    # check which jobs were applied to
    for ajob in applied_jobs:
        string = ajob[0] + ajob[1] +ajob[2]
        for sjob in saved_jobs:
            if string == str(sjob[0] + sjob[1] + sjob[2]):
                print("job applied: ", ajob[0])
    '''
    create_excel_workbook("job_search_data.xlsx", saved_jobs)
    #defs.csv_writer = csv.writer(open("job_data.csv", 'w'))
    #defs.csv_writer.writerows(saved_jobs)
def create_excel_workbook(sheetname, data):
    workbook = Workbook()
    worksheet = workbook.active
    for i in range(0,len(data)):
        for j in range(0, len(data[0])):
            sheetidx = i + 1
            sheetidy = j + 1
            cell = worksheet.cell(sheetidx, sheetidy)
            cell.value = data[i][j]
    '''
    max_col = [0]* len(saved_jobs)
    for i in range(0,len(saved_jobs)):
        for j in range(0, len(saved_jobs[0])):
            if max_col[i] < len(saved_jobs[j]):
                max_col[i] = len(saved_jobs[j])
    '''
    # make columns length of max field
    for column_cells in worksheet.columns:
        length = max(len(as_text(cell.value)) for cell in column_cells)
        print(length)
        worksheet.column_dimensions[column_cells[0].column_letter].width = length
    workbook.save(filename="job_search_data.xlsx")

def as_text(value):
    if value is None:
        return ""
    return str(value)
if __name__ == '__main__':
    main()
