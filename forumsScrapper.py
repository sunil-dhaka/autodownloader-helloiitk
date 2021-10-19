import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os

print('Enter your hello iitk username:')
username=input('username:')
print('Enter you hello iitk password:')
password=input('password:')

login_details={
    'name':username,
    'pass':password,
    'form_id':'user_login_form',
    'op':'SIGN+IN'
}

sessionHello=requests.Session() #<--class object

login_url='https://hello.iitk.ac.in/user/login'

r=sessionHello.post(login_url,data=login_details) # <-- it is a post requests
cookieHello=sessionHello.cookies.get_dict() #<-- gets cookie dict
if ('uid' in cookieHello and 'token' in cookieHello):
    print('Successfully logged into the session.')
else:
    sessionHello.cookies.clear() #<-- in next run we are clear
    print('Ocuured some problem during sign in action.')
    print('try again. exiting the programme')
    exit()

coursesLink='https://hello.iitk.ac.in/index.php/courses'

courseData=sessionHello.get(coursesLink)
print('status codes is: ',courseData.status_code)
courseSoup=bs(courseData.text,'html.parser')
#print(courseSoup.title.text)
courseList=[]

for course in courseSoup.find_all('span',class_='field-content'):
    courseItem={
        'course name':course.h3.text,
        'course instructor':course.a.text.strip().split('\n')[1],
        'course link':course.a['href']
    }
    courseList.append(courseItem)
    #print(courseItem)

customHeaders={
    'uid':cookieHello['uid'],
    'token':cookieHello['token']
}

courseName=input('course name? ')
forumsQuestionList=[]
for page in range(1,7):
    forumURL=f'https://hello.iitk.ac.in/api/{courseName}21/forums/fetch/general?pager='+str(page) #<--pagination
    forumsdata=sessionHello.get(forumURL,headers=customHeaders).json() #<-- nice json
    if len(forumsdata['data'])>0:
        for question in forumsdata['data']:
            forumsQuestionList.append({'title':question['title'],'desc':question['description'],'username':question['username']})
        print('question so far ',len(forumsQuestionList),'-- page no:',page)
    else:
        break

forumsDF=pd.DataFrame(forumsQuestionList)
print('forums questions dataframe shape is: ',forumsDF.shape)
folder=input('name of the folder where you want to store them? ')
if os.path.isdir(os.path.join(os.getcwd(),folder)):
    if os.getcwd()==os.path.join(os.getcwd(),folder):
        pass
    else:
        os.chdir(os.path.join(os.getcwd(),folder))
else:
    os.mkdir(os.path.join(os.getcwd(),folder))
    os.chdir(os.path.join(os.getcwd(),folder))
forumsDF.to_csv(os.getcwd()+'/forums.csv',index=False)