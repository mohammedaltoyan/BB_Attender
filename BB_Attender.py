#  Pyinstaller -F --add-binary "./driver/chromedriver.exe;./driver" BB_Attender.py

Program_version = 'BB_Attender v3.01'
print(Program_version)

#todo check for access denied for blackboard if refresh rate was slow and fix it, then implement the time system it was on previous version. The problem was the program wait to the official hours and when it refreshed the access will be denied

def create_SS_folder(): #create screenshot folder
    import os
    # define the name of the directory to be created
    try:
        os.mkdir(screenshot_folder_name)
    except OSError:
        print ("Error 1 : Folder NOT created for some reason\n")
        alarm()
    else:
        print ("Successfully created the folder\n")

def Screenshot_folder_exist(): #if Screenshot folder exist
    import os.path
    Screenshot_folder_status = os.path.isdir(screenshot_folder_name)
    if Screenshot_folder_status == True:
        pass
    else:
        create_SS_folder()

def data_file_exist(): #check if file exist or not
    try:
        import os.path
        cred_file_status = os.path.isfile(data_file_name + '.json')
        #print('Credentials are stored!')
        return (cred_file_status)
    except:
        #print('Credentials are not stored!')
        return (cred_file_status)

def credentials():  # input credentials and data
    # todo add URL's maybe for different college for later
    username_dict = {}
    password_dict = {}
    groups_dict = {}
    delay_dict = {}
    username = input('What is you username?>>')
    password = input('What is your password?>>')
    course_name = input('Write your course name as it appears on Blackboard!>>')
    delay = int(input('How many seconds would you like the program to wait for page refreshing in seconds? (10 seconds or more is recommended?>>'))
    username_dict['username'] = username
    password_dict['password'] = password
    groups_dict['course_name'] = course_name
    delay_dict['delay'] = delay
    account_info = username_dict | password_dict | groups_dict | delay_dict
    print (account_info)
    return (account_info)


def cred_file_not_complete(): #check for data in cred file to make sure it is complete if not it will be deleted and created again
    try:
        from operator import itemgetter
        import json
        account_file_1 = open(data_file_name + ".json", "r")  # to open data file
        account_file_2 = account_file_1.read()
        account_file_3 = json.loads(account_file_2)
        itemgetter('username', 'password', 'course_name', 'delay')(account_file_3) # If error raised because the items are not there there will be an exception.
        print(json.dumps(account_file_3, indent=4))
        account_file_1.close()
    except:
        if data_file_exist() == True:
            account_file_1.close()
        delete_file()
        create_cred_file()

def create_cred_file():    # to save credentials into a file
    import json
    account_file = open(data_file_name + ".json", "w")
    json.dump(credentials(), account_file)
    account_file.close()

def get_data(cred): # cred variable = to call for username, password, groups, delay. # cred should be string.
    import json
    account_file_1 = open("account.json", "r")     #to open credential file
    account_file_2 = account_file_1.read()
    account_file_3 = json.loads(account_file_2)
    account_file_4 = account_file_3[cred]
    account_file_1.close()
    return (account_file_4)

def delete_file(): #delete file
    import os
    if os.path.exists(data_file_name + '.json'):
      os.remove(data_file_name + ".json")
    else:
      print("Error #2: The file does not exist\n")
      alarm()

def open_site():  # open & login
    if internet() == False:
        alarm()
        print('Error #55: Check internet connection\n')
    else:
        try:
            #browser.get('https://lms.ksau-hs.edu.sa/') #URL for KSAUHS (blackboard) log in page #shorten URL to have control
            browser.get('https://cutt.ly/ChGhBSA')
            delay = get_data('delay')  # seconds
            try:
                WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='myButton']")))
                log_in_button_1 = browser.find_element_by_xpath("//*[@id='myButton']") ##1st log in button on KSAUHS website
                time.sleep(2)
                log_in_button_1.click()
            except TimeoutException:
                #print('Error #3: Element not found! Try again!')
                open_site()
            except :
                #print('Error #3.1: Element not found! Try again!')
                open_site()
        except:
            #print("Error #4: Could not open site")
            open_site()

def fill_cred(): #fill up account info to log in
    delay = get_data('delay')  # seconds
    if internet() == False:
        alarm()
        print('Error #56: Check internet connection\n')
    else:
        try:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='submitButton']")))
            time.sleep(2)
            username = get_data('username')
            password = get_data('password')
            username_elem = browser.find_element_by_xpath("//*[@id='userNameInput']")  # Username input element
            username_elem.send_keys(username)
            password_elem = browser.find_element_by_xpath("//*[@id='passwordInput']")  # password input element
            password_elem.send_keys(password)
            log_in_button_2 = browser.find_element_by_xpath("//*[@id='submitButton']")  # 2nd log in button on the website
            log_in_button_2.click()
        except TimeoutException:
            #print('Error #5: Timeout!')  # todo repeat 5 times then an alert should fire up
            fill_cred()
        except:
            #print('Error #5.1: Element not found! Try again!')
            fill_cred()

def terms_agree():  # Agree to website terms
    delay = get_data('delay')  # seconds
    if internet() == False:
        alarm()
        print('Error #57: Check internet connection\n')
    else:
        try:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='agree_button']")))
            terms_agree_button = browser.find_element_by_xpath("//*[@id='agree_button']")
            time.sleep(2)
            terms_agree_button.click()
        except TimeoutException:
            #print('Error #6: Agree button not found!')
            terms_agree()
        except:
            #print('Error #6.1: Element not found! Try again!')
            terms_agree()

def ultra_open():  # open Blackboard_ultra
    delay = get_data('delay')  # seconds
    if internet() == False:
        alarm()
        print('Error #58: Check internet connection\n')
    else:
        try:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.LINK_TEXT, "Courses" )))
            courses_button = browser.find_element_by_link_text('Courses')
            time.sleep(2)
            courses_button.click()
        except TimeoutException:
            #print('Error #11: Courses button not found!')
            pass
        except:
            #print('Error #11.1')
            pass
        try:
            course_name = get_data('course_name')
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.LINK_TEXT, course_name)))
            course_name_button = browser.find_element_by_partial_link_text(course_name)
            time.sleep(2)
            course_name_button.click()
        except TimeoutException:
            #print('Error #10')
            pass
        except:
            #print('Error #10.1')
            pass

        #try:
        #    WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='menuPuller']")))
        #    munu_bar = browser.find_element_by_xpath("//*[@id='menuPuller']")
        #    time.sleep(2)
        #    munu_bar.click()
        #except TimeoutException:
        #    #print('Error #9!')
        #    pass

        try:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Virtual Classes')))
            virtual_classes_button = browser.find_element_by_link_text('Virtual Classes')
            time.sleep(2)
            virtual_classes_button.click()
        except TimeoutException:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='menuPuller']")))
            munu_bar = browser.find_element_by_xpath("//*[@id='menuPuller']")
            time.sleep(2)
            munu_bar.click()
            time.sleep(2)
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Virtual Classes')))
            virtual_classes_button = browser.find_element_by_link_text('Virtual Classes')
            time.sleep(2)
            virtual_classes_button.click()
            #print('Error #9!')
        except:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='menuPuller']")))
            munu_bar = browser.find_element_by_xpath("//*[@id='menuPuller']")
            time.sleep(2)
            munu_bar.click()
            time.sleep(2)
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Virtual Classes')))
            virtual_classes_button = browser.find_element_by_link_text('Virtual Classes')
            time.sleep(2)
            virtual_classes_button.click()
            #print('Error #9.1')
        try:
            WebDriverWait(browser, 10 * delay).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Blackboard Collaborate Ultra')))
            ultra_button = browser.find_element_by_link_text('Blackboard Collaborate Ultra') #Blackboard Collaborate Ultra Button
            time.sleep(2)
            ultra_button.click()
        except TimeoutException:
            #print('Error #8')
            pass
        except:
            #print('Error #8.1')
            pass
        try:
            time.sleep(1)
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='collabUltraLtiFrame']")))
            time.sleep(1)
            BB_ultra_link = browser.find_element_by_xpath("//*[@id='collabUltraLtiFrame']").get_attribute('src')  # to get Ultra Frame URL
            time.sleep(1)
            while BB_ultra_link == 'None':
                time.sleep(1)
                WebDriverWait(browser, delay).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='collabUltraLtiFrame']")))
                time.sleep(1)
                BB_ultra_link = browser.find_element_by_xpath("//*[@id='collabUltraLtiFrame']").get_attribute(
                    'src')  # to get Ultra Frame URL
                time.sleep(1)
                browser.get(BB_ultra_link)
                time.sleep(1)
            time.sleep(2)
            browser.get(BB_ultra_link)
            time.sleep(2)
            return (BB_ultra_link)
        except TimeoutException:
            #print('Error #7')
            ultra_open()
        except:
            #print('Error #7.1')
            ultra_open()

def ultra_exist():  # check if BB Ultra is loaded
    delay = get_data('delay')  # seconds
    if internet() == False:
        alarm()
        print('Error #54: Check internet connection\n')
    else:
        try:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='body-content']")))
        except TimeoutException:
            #print('Error #12')
            ultra_exist()
        except:
            #print('Error #12.1')
            ultra_exist()

def session_attender_1(): #select and attend the sessions
    session_names_list = []
    session_number_names_dict = {} #show session's names and web a number in a dict to make the user choose in an easy way
    session_name_elements = sessions_elements()
    y = 1
    for x in session_name_elements:  # filling a dictionary for session names and corresponding number so the user can choose easily
        session_number_names_dict |= {y : x.text}
        y += 1
    time.sleep(2)
    [print(key, ' : ', value) for key, value in session_number_names_dict.items()] # Show session names for first page only.
    session_numbers_input = input("\n Enter the session's number that you would like to attend separated by comma '.' NO SPACES!>>")
    refresh_rate = float(input('\n Page Refresh rate? in minutes>>'))
    print('')
    session_numbers_list = session_numbers_input.split('.')
    session_numbers_list = [int (i) for i in session_numbers_list ] #make the number written integers so we can call them from different dict
    for s in session_numbers_list:
        session_names_list.append((session_number_names_dict[s]))
    return(session_names_list,refresh_rate)

def session_attender_2(url, session_names_list, refresh_rate):
    try:
        delay = get_data('delay')  # seconds
        main_handle = browser.current_window_handle #main tab for BB ultra to show the sessions
        session_names_elem_dict = {} #show session's names and web element in a dict

        while (session_names_list != []) or (opened_tabs_1 != []):
            for session_name in session_names_list:
                time.sleep(2)
                print(current_time() + " >> The following sessions will be attended, Stay tuned!>> ")
                print('')
                print(*session_names_list, sep="\n")
                print('')
                print(str(current_time() + ' >> Checking if the following session has opened:>> {x}\n').format(x=session_name))
                if internet() == False:
                    print('Error #14: Check internet connection\n')
                    alarm()
                else:
                    try:
                        browser.get(url)
                        ultra_exist()
                        if session_names_elem_dict != {} : #we should clear the list because the session IDs differs everytime the page refreshes!
                            session_names_elem_dict.clear()
                        session_name_elements = sessions_elements()
                        for x in session_name_elements:  # to get the new elements after refreshing the page
                            session_names_elem_dict |= {x.text: x}
                        elem = session_names_elem_dict[session_name]
                        elem.click()
                        time.sleep(2)
                        try:  # clicking on join session
                            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='offcanvas-wrap']/div[2]/div/div/div/div/div[2]/div")))
                            q = browser.find_element_by_xpath("//*[@id='offcanvas-wrap']/div[2]/div/div/div/div/div[2]/div")
                            time.sleep(5)
                            q.click()
                            browser.switch_to.window(browser.window_handles[-1])
                            time.sleep(20)
                            extended_dealy = delay * 1.5
                            try:  # clicking on mic notification to dismiss it
                                WebDriverWait(browser, extended_dealy).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='techcheck-modal']/button")))
                                #WebDriverWait(browser, 1.5 * delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='techcheck-modal']/button")))
                                q = browser.find_element_by_xpath("//*[@id='techcheck-modal']/button")
                                time.sleep(5)
                                q.click()
                            except:
                                #close_session_details( # 32)
                                print('Error: mic notification not clicked')
                                pass
                            time.sleep(20)
                            try:  # clicking on tour notification to dismiss it
                                WebDriverWait(browser, extended_dealy).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='announcement-modal-page-wrap']/button")))
                                #WebDriverWait(browser, 1.5 * delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='announcement-modal-page-wrap']/button")))
                                q = browser.find_element_by_xpath("//*[@id='announcement-modal-page-wrap']/button")
                                time.sleep(5)
                                q.click()
                                print(current_time() + ' >> ' + session_name + ' was entered successfully!\n')
                            except :
                                #close_session_details(#31)
                                pass
                            try:
                                time.sleep(5)
                                browser.find_element_by_xpath("//*[@id='side-panel-open']").click() #to press an icon to show the participants
                                time.sleep(5)
                                browser.find_element_by_xpath("//*[@id='panel-control-participants']").click() #to show the names of participants
                                time.sleep(5)
                                browser.find_element_by_xpath("// *[ @ id = 'session-menu-open']").click() #to show the side session for session name
                                time.sleep(5)
                            except:
                                pass
                            try:
                                characters_to_remove = '\/:*?"<>|' #prohibited by windows file name
                                filtered_session_name = session_name

                                for character in characters_to_remove:
                                    filtered_session_name = filtered_session_name.replace(character, " ")
                                session_name_png = str(screenshot_folder_name + '/' + filtered_session_name + '.png')
                                time.sleep(2)
                                browser.save_screenshot(session_name_png)
                                time.sleep(2)
                                print(current_time() + ' >> Screenshot was taken! for the following session: ' + session_name)
                                print('')
                            except:
                                print("Error 654: Couldn't take a screenshot for some reason\n")
                            try:
                                time.sleep(5)
                                browser.find_element_by_xpath("//*[@id='session-menu-close']").click() #to close the session menu
                                time.sleep(5)
                                browser.find_element_by_xpath("//*[@id='side-panel-close']").click() #to to  close the side panel menu of participation
                                time.sleep(5)
                            except:
                                pass
                            browser.switch_to.window(main_handle)
                            session_names_list.remove(session_name)
                            close_session_details()
                        except:
                            close_session_details()
                    except:
                        close_session_details()
            opened_tabs_1 = []
            for tab in browser.window_handles:
                if tab == main_handle:
                    pass
                else:
                    opened_tabs_1.append(tab)
            if opened_tabs_1 != []:
                for open_tab in opened_tabs_1:  # go through the opened tabs and check if there is any problem with them
                    if internet() == False:
                        print('Error #14: Check internet connection\n')
                        alarm()
                    try:
                        tabs_loop(open_tab, opened_tabs_1)
                        title = browser.title
                        print(current_time() + ' >> Done checking upon the following session >> ' + title + '\n')
                    except:
                        print('Error #706')
            else:
                print(current_time() + ' >> There is no windows opened')
            browser.switch_to.window(main_handle)
            print(
                str(current_time() + " >> We are gonna refresh the page in {y} minutes, stay calm!".format(y=refresh_rate)))
            print('')
            time.sleep((refresh_rate * 60))
        else:
            print(current_time() + ' >> All sessions have been attended successfully\n')
    except:
        time.sleep(5)
        session_attender_2(url, session_names_list, refresh_rate)


def close_session_details(): #close the session details
    delay = get_data('delay')
    try:
        WebDriverWait(browser, delay).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='offcanvas-wrap']/div[2]/div/button/span")))
        q = browser.find_element_by_xpath("//*[@id='offcanvas-wrap']/div[2]/div/button/span")  # close button of session info window
        time.sleep(5)
        q.click()
    except:
        #print(str("# {y}".format(y=x)))
        pass

def time_verfiy():
    import time
    t = time.localtime()
    time_start
    time_ends
    current_time = time.strftime("%H:%M", t)
    result = current_time >= time_start and current_time <= time_ends
    return (result)



def sessions_elements(): #to check and retrieve session names
    delay = get_data('delay')  # seconds
    try:       #getting the sessions names
        WebDriverWait(browser, delay).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span[class = 'name ng-binding']")))
        table_content = browser.find_element_by_xpath('//*[@id="body-content"]/div[3]/ul')  # to locate the table content
        #table_content = browser.find_element_by_xpath('//*[@id="main-content"]/div[1]/div/div') #this is for testing #for course session not the real sessions # DELETE AND RETURN THE ABOPVE ONE
        session_name_elements = table_content.find_elements_by_css_selector("span[class = 'name ng-binding']")  # to locate each topic name
        return (session_name_elements)
    except TimeoutException:
        sessions_elements()
        #print('Error #13\n')
        #alarm()
    except:
        sessions_elements()
        #print('Error #13.1\n')
        #alarm()


def tabs_loop(t,all): #go through the tabs and search for errors #todo make the session names not the tabs title available
    delay = (get_data('delay')/2)  # seconds #no need to wait long since they are alreay loaded
    browser.switch_to.window(t)
    title = browser.title
    #found = False
    #while not found:
    try:
        WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='status-selector-toggle']/span[2]/span[1]/div/bb-svg-icon"))) #online icon
        print (current_time() + ' >> You are online for this session: ' + title)
        print('')
    except TimeoutException:
        #print('Error #19, we will try again: ' + title)
        pass
    except:
        #print('Error #19.1: ' + title)
        pass
    try:
        WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='status-selector-toggle']/span[2]/span[3]/bb-svg-icon"))) #offline icon
        #print ('Error #20, we will try again: ' + title)
        print(current_time() + ' >> It seems you are offline, we will try to refresh the page, hold tight! ' + title)
        print('')
    except TimeoutException:
        pass
    except:
        #print('Error #32.1: ' + title)
        pass

    try:
        overlay = browser.find_element_by_xpath("/html/body/div[4]") # click on the overlay screen to
        time.sleep(2)
        overlay.click()
    except :
        pass

    try:
        reload = browser.find_element_by_xpath("//*[@id='connection-status-alert']/div[2]/button") # reload the session while we are in, not yet discontinued
        time.sleep(2)
        reload.click()
        #print('Error #21: Trying to reload this session: ' + title)
    except :
        pass
    try:
        reconnect = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/button') # Reconnect button while we are out of the session
        time.sleep(2)
        reconnect.click()
        #print('Error #22: Trying to reconnect this session: ' + title)
    except :
        pass
    try:
        new_link = browser.find_element_by_xpath("//*[@id='main-container']/main/div[3]/div/div/div[1]/a") #a new link because of the previous link is broken
        time.sleep(2)
        new_link.click()
        #print('Error #23: Session is reconnecting with new link' + title)
    except :
        pass
    try:
        already_in = browser.find_element_by_xpath("//*[@id='main-container']/main/div[3]/div/div/h1")  #session already entered
        already_in.text == "Uh-oh. You've already joined the session."
        time.sleep(2)
        browser.refresh()
        #print('Error #24: The session is already entered, we will try again ' + title)
        print(current_time() + ' >> It seems that you already entered the session, we will try refresh it again. Hold tight! ' + title)
        print('')
    except :
        pass
    try:
        mic = browser.find_element_by_xpath("//*[@id='techcheck-modal']/button") #for mic
        time.sleep(2)
        mic.click()
    except :
        pass
    try:
        tour = browser.find_element_by_xpath("//*[@id='announcement-modal-page-wrap']/button") #for tour
        time.sleep(2)
        tour.click()
    except :
        pass

    try: #tesy
        disconnected = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/h1") #test for discontinue page
        disconnected.text == "Uh-oh. You're disconnected."
        time.sleep(2)
        disconnected.click()
        time.sleep(5)
        browser.find_element_by_xpath("/html/body/div[1]/div/div/div/button").click() #reconnect button
        time.sleep(2)
    except :
        pass

    try:
        a = browser.find_element_by_xpath('//*[@id="main-container"]/main/div[3]/div/div/h1').text
        a.text == 'Session no longer available' #session has ended
        all.remove(t)
        time.sleep(2)
        browser.close()
        print(current_time() + ' >> The following session has ended and closed successfully ' + title)
        print('')
    except :
        pass

def alarm():
    import winsound
    filename = 'Alarm.wav'
    winsound.PlaySound(filename, winsound.SND_FILENAME)


def internet(host="8.8.8.8", port=53, timeout=3): # check internet connection https://stackoverflow.com/questions/3764291/checking-network-connection
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        #print ('Error #25: No internet connection!')
        return False

def current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return (current_time)


def program_true(): #input names of courses to be entered
    import time
    if internet() == False:
        alarm()
        print('Error #54: Check internet connection\n')
    else:
        try:
            open_site()
            fill_cred()
            terms_agree()
            url = ultra_open() #URL = Blackboard Ultra separate URL to be opened standalone
            ultra_exist()
            session_names_list,refresh_rate= session_attender_1() #to get the session names to attend
            session_attender_2(url,session_names_list,refresh_rate)
            browser.quit()
        except:
            print('Error:454')
            while True:
                alarm()



import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
#from selenium.common.exceptions import NoSuchElementException
from logging.handlers import RotatingFileHandler
import time
import logging
import logging.handlers


opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--start-maximized") #start-maximized
opt.add_argument("--disable-extensions")
opt.add_argument("--mute-audio")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2
  })


#https://www.kite.com/python/docs/logging.handlers.RotatingFileHandler
# Set up logger with appropriate handler
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
LOG_FILENAME = "LOGS"
my_logger = logging.getLogger()
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, mode='a', maxBytes=20*1024*1024,
                                 backupCount=1, encoding=None, delay=0)
handler.setFormatter(log_formatter)
my_logger.setLevel(logging.DEBUG)
my_logger.addHandler(handler)
# Rolling over to simulate log exceeding maxBytes size
handler.doRollover()

if __name__ == "__main__":
  if getattr(sys, 'frozen', False):
    # executed as a bundled exe, the driver is in the extracted folder
    chromedriver_path = os.path.join(sys._MEIPASS, "driver/chromedriver.exe")
    browser = webdriver.Chrome(chrome_options=opt,executable_path=chromedriver_path)
    #browser.minimize_window()
  else:
    # executed as a simple script, the driver should be in `PATH`
    browser = webdriver.Chrome(chrome_options=opt)
    #browser.minimize_window()

print('\n\n\n\n                    DEADPOOL is your UNCLE\n\n\n\n')
screenshot_folder_name = "Session's Screenshots"  #name of the screenshot folder
data_file_name = 'Account' #without the extension

#testing the sound alaram
print ('Testing Alarm sound:\n')
alarm()


#time_start = '07:45' #str(input())
#time_ends = '17:15' #str(input())

#print(str('The program will start searching for open sessions on {x} and stop working on {y} EVERYDAY as long as it '
      #    'is open.\n').format(x=time_start,y=time_ends))



if data_file_exist() == True:
    cred_file_not_complete()
    Screenshot_folder_exist()
    program_true()

else:
    create_cred_file()
    Screenshot_folder_exist()
    program_true()


# to compile to exe with Pyinstaller use this command in the project folder "Pyinstaller -F --add-binary "./driver/chromedriver.exe;./driver" BB_Attender.py"
#https://www.zacoding.com/en/post/python-selenium-to-exe/
#https://stackoverflow.com/questions/47690548/running-pyinstaller-another-pc-with-chromedriver
#https://cryptolens.io/
#https://www.sendowl.com/