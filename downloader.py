import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
# import glob
import youtube_dl
from PyInquirer import prompt

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

sessionHello=requests.Session() #<--class object instatization

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
        'course link':course.a['href'].split('/')[-1][:-2]
    }
    courseList.append(courseItem)
    #print(courseItem)

customHeaders={
    'uid':cookieHello['uid'],
    'token':cookieHello['token']
}

# courseName=input('course name? ')
courseChoice=[
    {
        'type':'list',
        'name':'choice',
        'message':'Which course',
        'choices':[courseItem['course link'] for courseItem in courseList]
    }
]

answer=prompt(courseChoice)
courseName=answer['choice']
print(f'collecting videos and resources data for course {courseName}')

# get suppl resources in resources tab
suppList=[]
suppURL=f'https://hello.iitk.ac.in/api/{courseName}21/resources'
suppData=sessionHello.get(suppURL,headers=customHeaders).json() #<-- nice json
if len(suppData)>0:
    for data in suppData:
        suppList.extend(data['resources'])
else:
    print(f'There are no suppl data for {courseName}')

videosList=[]
resourcesList=[]
summaryURL=f'https://hello.iitk.ac.in/api/{courseName}21/lectures/summary'
data=sessionHello.get(summaryURL,headers=customHeaders).json() #<-- nice json
if len(data)>0:

    for i,lec in enumerate(data):
        # get video
        if lec['videoURL'] is None:
            if len(lec['videosUploaded'])>0:
                videoItem={
                    'fileName':str(i+1)+'_'+'-'.join((lec.get('title','noTitle')).split(' '))+'.mp4',
                    'fileURL':lec['videosUploaded'][-1]['path']
                }
                videosList.append(videoItem)
        else:
            # link=lec['videoURL']
            videoItem={
                    'fileName':str(i+1)+'_'+'-'.join((lec.get('title','noTitle')).split(' '))+'.mp4',
                    'fileURL':lec['videoURL']
                }
            videosList.append(videoItem)
        # get all resources for lec
        if len(lec['resources'])>0:
            resourcesList.extend(lec['resources'])

    print(f'total lectures found for course {courseName} are {len(videosList)}.')
    print(f'total resources found for course {courseName} are {len(resourcesList)}.')
    
else:
    print(f'no lectures found for course {courseName}.')
    # exit()


# forumsDF=pd.DataFrame(forumsQuestionList)
# print('forums questions dataframe shape is: ',forumsDF.shape)
# folder=input('name of the folder where you want to store them? ')

folder=courseName.upper()
if os.path.isdir(os.path.join(os.getcwd(),folder)):
    if os.getcwd()==os.path.join(os.getcwd(),folder):
        pass
    else:
        os.chdir(os.path.join(os.getcwd(),folder))
else:
    os.mkdir(os.path.join(os.getcwd(),folder))
    os.chdir(os.path.join(os.getcwd(),folder))

choice=[
    {
        'type':'list',
        'name':'type',
        'message':'Which type',
        'choices':['Resources','Videos','Supp']
    }
]

answer=prompt(choice)
choiceName=answer['type']

print(f'choicename {choiceName}')

if os.path.isdir(os.path.join(os.getcwd(),choiceName)):
    if os.getcwd()==os.path.join(os.getcwd(),choiceName):
        pass
    else:
        os.chdir(os.path.join(os.getcwd(),choiceName))
else:
    os.mkdir(os.path.join(os.getcwd(),choiceName))
    os.chdir(os.path.join(os.getcwd(),choiceName))

def downloader(fileList=[],existsList=[]):

    for item in fileList:
        fileName=item['fileName']
        if fileName in existsList:
            print(f'Already downloaded ... {fileName}')
            pass
        else:
            print(f'Downloading ... {fileName}')
            # add youtube-dl download support
            if 'youtu.be' in item['fileURL'] or 'youtube' in item['fileURL']:
                ydl_opts = {
                    'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]', # these specific options can be changed to get full-hd downloads
                    'vcodec': 'avc1.4d401e',
                    'outtmpl': fileName # '%(title)s.%(ext)s' # <-- rather than using auto templates; custom name is given [it works!!]
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([item['fileURL']])
            else:
                with open(fileName,'wb') as file:
                    r=requests.get(item['fileURL'])
                    if r.status_code==200:
                        for chunk in r.iter_content(chunk_size=100000):
                            if chunk:
                                file.write(chunk)
                        print(f'Downloaded {fileName}')
                    else:
                        print(f'bad request. could not download {fileName}')
    return None
    

print(f'downloading {choiceName} for {courseName}. Press `Ctrl+Z` to stop the programme.')

if choiceName=='Videos':
    mp4files = [file for file in os.listdir() if os.path.getsize(file)!=0]
    '''
    # could use listdir() rather than glob as we are in Videos dir
    for file in glob.glob("*.mp4"):
        mp4files.append(file)
    '''
    downloader(videosList,mp4files)

elif choiceName=='Resources':
    resourceFiles=[file for file in os.listdir() if os.path.getsize(file)!=0]
    '''
    resourceFiles=[]
    fileTypes=['*.pdf','*.ppt','*.doc'] #<-- can be added other types
    for type in fileTypes:
        resourceFiles.extend(glob.glob(type))
    '''
    downloader(resourcesList,resourceFiles)
else:
    suppFiles=[file for file in os.listdir() if os.path.getsize(file)!=0]
    downloader(suppList,suppFiles)
'''
when stopped in between the file name will be in dir but file would be corrupt(in-fact no content)
Manual:
- can avoid this either not stopping or manually deleting before running again
Automated solutions is:
- when stopped in between only file name will be there but file size will be zero
- so can check os.path.getsize('path') against zero; and only include files that does not have size zero
'''

'''
another problem is that when videos are YT embbeded links then requests can not be used directly
- rather we can use other modules like yputube-dl or you-get
    - to do that just need to check if link is .mp4 or not
    - if it is not then can use modules to download video

## things can be improved always ##
'''