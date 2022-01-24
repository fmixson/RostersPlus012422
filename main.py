import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
# import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
from easygui import *
import openpyxl
import lxml




class CheckForSyllabus():

    def __init__(self, instructor, course, section, term):
        self.term = term
        self.instructor = instructor
        self.course = course
        self.section = section

    def syllabus_in_rostersplus(self):

        syllabus = driver.find_element_by_xpath('//*[@id="Syllabus_form"]/a').click()

        # This waits until syllabus upload page loads
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'DownloadRoster_form')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        check_for_syllabus = soup.find('input', {'type': 'file'})

        if check_for_syllabus == None:
            pass
        else:
            length = len(df)
            df.loc[length, "term"] = self.term
            df.loc[length, "instructor"] = self.instructor
            df.loc[length, "course"] = self.course
            df.loc[length, "section"] = self.section

        driver.back()
        driver.back()


class Report():

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def save_report(self):
        pass

def section_number(course):
    cut_up = course.split()
    list_part = len(cut_up)-3
    list_part = list_part
    section = cut_up[list_part]
    section = section[1:]
    return section

def set_the_term(term):
    cut_up = term.split()
    list_part = cut_up[3:6]
    list_part2 = list_part[1]
    list_part3 = list_part[2]
    return list_part[0] + ' ' + list_part2 + ' ' + list_part3

def course_name (course):
    cut_up = course.split()
    course2 = cut_up[:2]
    course3 = course2[1]
    course3 = course3[:-1]
    return course2[0] + ' ' + course3

def eliminate_labs(course):
    cut_up = course.split()
    # print(cut_up[:])
    if "LEC)" in cut_up[:]:
        return True
    else:
        return False


columns = ["term", "instructor", "course", "section"]
df = pd.DataFrame(columns=columns)
driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome("C:/Users/fmixson/PycharmProjects/chromedriver.exe")
driver.get('https://secure.cerritos.edu/rosters/login.cgi')
text = "Allow the Computer to Login to your RostersPlus Account"
title = "RostersPlus Login"
fields = ['Username', 'Password']
output = multpasswordbox(text, title, fields)
login = driver.find_element_by_name('login')
# username = input('Enter your username: ')
login.send_keys(output[0])
print(output[0])
# df.to_csv('C:/Users/' + output[0] + '/Desktop/RostersPlus_Review.csv')
login = driver.find_element_by_name('passwd')
# password = input('Enter your password: ')
login.send_keys(output[1])
button = driver.find_element_by_xpath('//*[@id="login_form"]/table/tbody/tr[3]/td[2]/input').click()
# This waits for list of courses to load
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clform')))
session = driver.find_element(By.XPATH, 'html/body/table[2]/tbody/tr/td[2]/form[1]/p/select/option[1]').click()




page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
table = soup.find('table', {'bgcolor': 'white'})
# print(table)
table2 = table.find_all('tr')
print(len(table2))
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Roster_form')))

for i in range(1, len(table2)):
    # This clicks on radio button to open roster
    button2 = driver.find_element(By.XPATH,'//*[@id="clform"]/table/tbody/tr['+str(i)+']/td[1]/input').click()
    # This waits until roster open to run
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'college')))
    instructor = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[1]/td[3]').text
    course = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[3]').text
    term = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr[4]/td[3]').text
    labs = eliminate_labs(course)
    if labs == False:
        driver.back()
        continue
    term2 = set_the_term(term=term)
    section = section_number(course=course)
    course2 = course_name(course=course)
    check = CheckForSyllabus(instructor, course2, section, term2)
    check.syllabus_in_rostersplus()

df.to_csv('C:/Users/' + output[0] + '/Desktop/RostersPlus_Review.csv')
df.to_csv('D:/Work/Division/Syllabi_Not_In_RostersPlus.csv')


