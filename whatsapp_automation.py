import sys
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()

# create a new user profile in chrome and provide its path to user-data-dir so that you need to scan the QR code only once
options.add_argument("user-data-dir=C:\\Users\\BHAVIK DODIA\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")

# opens the chrome browser
driver = webdriver.Chrome(options=options)

# opens WhatsApp Web in browser
driver.get('http://web.whatsapp.com')

# sends multiple messages to a single user
def single_user():
    user = input('\nEnter the name of user or group: ')
    print('Enter messages (enter ctrl+z on windows / command+d on mac and enter key to proceed):')
    # to take multiline input from terminal press (ctrl+z / command+d) on (windows / mac) then press enter to proceed to next step
    msgs = [line.replace('\n', '') for line in sys.stdin]

    try:
        profile = driver.find_element_by_xpath(f'//span[@title = "{user}"]')
        profile.click()

        for msg in msgs:
            msg_box = driver.find_element_by_class_name('_1Plpp')
            msg_box.send_keys(msg)
            driver.find_element_by_class_name('_35EW6').click()
    except Exception as e:
        print(e)
    else:
        print('\nMessage(s) sent successfully...')

# sends multiple messages to multiple users
def multi_user():
    print('\nEnter the names of users or groups (enter ctrl+z on windows / command+d on mac to proceed):')
    users = [line.replace('\n', '') for line in sys.stdin]
    print('Enter messages (enter ctrl+z on windows / command+d on mac and enter key to proceed):')
    msgs = [line.replace('\n', '') for line in sys.stdin]

    try:
        for user in users:
            profile = driver.find_element_by_xpath(f'//span[@title = "{user}"]')
            profile.click()

            for msg in msgs:
                msg_box = driver.find_element_by_class_name('_1Plpp')
                msg_box.send_keys(msg)
                driver.find_element_by_class_name('_35EW6').click()
    except Exception as e:
        print(e)
    else:
        print('\nMessage(s) sent successfully...')

# sends contents of a text file to multiple users
def send_file_contents():
    print('\nEnter the names of users or groups (enter ctrl+z on windows / command+d on mac to proceed):')
    users = [line.replace('\n', '') for line in sys.stdin]
    file_path = input('\nEnter path of the file: ')

    with open(file_path, encoding='utf-8') as f:
        msg = [line.strip('\n') for line in f.readlines()]

    try:
        for user in users:
            profile = driver.find_element_by_xpath(f'//span[@title = "{user}"]')
            profile.click()

            msg_box = driver.find_element_by_class_name('_1Plpp')

            # WhatsApp sends the message when it detacts '\n' character at the end of any line, so perform (shift+enter) operation to give line break at the end of each line
            for line in msg:
                ActionChains(driver).send_keys(line).perform()
                ActionChains(driver).key_down(keys.Keys.SHIFT).key_down(keys.Keys.ENTER).key_up(keys.Keys.SHIFT).key_up(keys.Keys.ENTER).perform()
            driver.find_element_by_class_name('_35EW6').click()
    except Exception as e:
        print(e)
    else:
        print('\nMessage(s) sent successfully...')

# sends multiple messages to multiple users repeatedly
def repeat_messages():
    print('\nEnter the names of users or groups (enter ctrl+z on windows / command+d on mac to proceed):')
    users = [line.replace('\n', '') for line in sys.stdin]
    print('Enter messages (enter ctrl+z on windows / command+d on mac to proceed):')
    msgs = [line.replace('\n', '') for line in sys.stdin]
    count = int(input('Enter how many times you want to repeat messages: '))

    try:
        for user in users:
            profile = driver.find_element_by_xpath(f'//span[@title = "{user}"]')
            profile.click()

            # to repeat messages in the same order in which they are given
            for i in range(count):
                for msg in msgs:
                    msg_box = driver.find_element_by_class_name('_1Plpp')
                    msg_box.send_keys(msg)
                    driver.find_element_by_class_name('_35EW6').click()
    except Exception as e:
        print(e)
    else:
        print('\nMessage(s) sent successfully...')

# terminates the program
def terminate():
    global c
    c = False

c = True
switcher = {
        1 : single_user,
        2 : multi_user,
        3 : send_file_contents,
        4 : repeat_messages,
        5 : terminate
    }

# main loop of the program
while c:
    print('\nMenu:\n1. Send messages to a single user\n2. Send messages to multiple users\n3. Send contents of a file as a message to users\n4. Send messages multiple times\n5. Exit')
    choice = int(input('\nEnter your choice: '))
    # terminates the program if given choice is invalid
    func = switcher.get(choice, terminate)
    # executes appropriate function
    func()

# closes the browser
driver.close()
