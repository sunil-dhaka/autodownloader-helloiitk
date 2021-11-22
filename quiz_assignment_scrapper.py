import requests
from bs4 import BeautifulSoup as bs
import os
import json
import pdfkit
from PyInquirer import prompt
# import html_list
# import html2pdf
#==================================================================================

def jax2tex(text):
    text='$'.join(('$'.join(text.split('\('))).split('\)'))
    if '<img' in text:
        soup=bs(text,'html.parser')
        soup.img['src']='https://hello.iitk.ac.in'+soup.img['src']
        text=str(soup)
    return text

def html_list(json_data=None):
    if json_data is None:
        print(''.center(50,'='))
        print('This script can be used to get html formatted from "specific" json. With json structure changing have to change code.')
        print(''.center(50,'='))
    else:
        ques_str='''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width initial-scale=1.0">
<title>Quizzes</title>
<script type='text/x-mathjax-config'>MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]},config: ['MMLorHTML.js'],extensions: ['mml2jax.js','tex2math.js'],jax: ['input/MathML','input/TeX', 'output/HTML-CSS']});</script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
</head>
<body>
'''

        '''
        I want to show all questions their type wise collected in one place
        Possibilities:
            - truefalse
            - long_answer
            - short_answer
            - multichoice
            - others
        '''
        qid_order=[]
        ans_str='<hr>\n<hr>\n'
        ques_str+='<div>\n'
        ques_str+='<h1 style="text-align:center;">Questions</h1>\n'
        ques_str+='<div>\n'
        ans_str+='<div>\n'
        ans_str+='<h1 style="text-align:center;">Answers</h1>\n'
        ans_str+='<hr>\n'
        #==================================================================================
        if any(que.get('type',None)=='truefalse' for que in json_data.get('quiz',None)['questions']):
            ques_str+='<div>\n'
            ques_str+='<h2 style="text-align:center;">True False</h2>\n'
            ques_str+='<hr>\n'
            ans_str+='<div>\n'
            ans_str+='<h2 style="text-align:center;">True False</h2>\n'
            ans_str+='<hr>\n'
            for que in json_data.get('quiz',None)['questions']:
                que_type=que.get('type',None)
                if que_type=='truefalse':
                    qid_order.append(que['qid'])
                    ques_str+=f'<h4>Question: {len(qid_order)} | Score: {que["score"]} | Negative Score: -{que["negative_score"]}</h4>\n'
                    ques_str+=jax2tex(que.get('title'))
                    ques_str+='\n'

                    ans_str+=f'<h4>Answer: {len(qid_order)}</h4>\n'
                    for ans in json_data.get('correctSolutions',None):
                        if ans.get('qid')==qid_order[-1]:
                            answer=ans.get('correctAnswer',None)[0].get('aid',None)
                            if answer==1:
                                ans_str+='<h5>True</h5>\n'
                            elif answer==0:
                                ans_str+='<h5>False</h5>\n'
                            else:
                                ans_str+=f'<h5>{answer}</h5>\n'
                            break
            ques_str+='</div>\n'
            ans_str+='</div>\n'
        #==================================================================================
        if any(que.get('type',None)=='multichoice' for que in json_data.get('quiz',None)['questions']):
            ques_str+='<div>\n'
            ques_str+='<h2 style="text-align:center;">Muliple Choice</h2>\n'
            ques_str+='<hr>\n'
            ans_str+='<div>\n'
            ans_str+='<h2 style="text-align:center;">Multiple Choice</h2>\n'
            ans_str+='<hr>\n'
            for que in json_data.get('quiz',None)['questions']:
                que_type=que.get('type',None)
                if que_type=='multichoice':

                    # prepare answer ids
                    ans_str+=f'<h4>Answer: {len(qid_order)}</h4>\n'
                    answer_ids=[]
                    for ans in json_data.get('correctSolutions',None):
                        if ans.get('qid')==qid_order[-1]:
                            answer=ans.get('correctAnswer',None)
                            for a in answer:
                                answer_ids.append(a.get('aid',None))
                            break
                    # done
                    qid_order.append(que['qid'])
                    ques_str+=f'<h4>Question: {len(qid_order)} | Score: {que["score"]} | Negative Score: -{que["negative_score"]}</h4>\n'
                    ques_str+=jax2tex(que.get('title'))
                    ques_str+='<ol>\n'
                    for i,option in enumerate(que['options']):
                        ques_str+=f'<li>{jax2tex(option["value"])}</li>\n'
                        if option['aid'] in answer_ids:
                            ans_str+=f'<h5>{i+1}. {jax2tex(option["value"])}</h5>\n'
                    ques_str+='<ol>\n'
            ques_str+='</div>\n'
            ans_str+='</div>\n'
        #==================================================================================
        if any(que.get('type',None)=='short_answer' for que in json_data.get('quiz',None)['questions']):
            ques_str+='<div>\n'
            ques_str+='<h2 style="text-align:center;">Short Answer</h2>\n'
            ques_str+='<hr>\n'
            ans_str+='<div>\n'
            ans_str+='<h2 style="text-align:center;">Short Answer</h2>\n'
            ans_str+='<hr>\n'
            for que in json_data.get('quiz',None)['questions']:
                que_type=que.get('type',None)
                if que_type=='short_answer':
                    qid_order.append(que['qid'])
                    ques_str+=f'<h4>Question: {len(qid_order)} | Score: {que["score"]} | Negative Score: -{que["negative_score"]}</h4>\n'
                    ques_str+=jax2tex(que.get('title'))
                    ques_str+='\n'
                    ans_str+=f'<h4>Answer: {len(qid_order)}</h4>\n'
                    for ans in json_data.get('correctSolutions',None):
                        if ans.get('qid')==qid_order[-1]:
                            answer=ans.get('correctAnswer',None)
                            for a in answer:
                                ans_str+=f'<h5>{a}</h5>\n'
                            break
            ques_str+='</div>\n'
            ans_str+='</div>\n'
        #==================================================================================
        if any(que.get('type',None)=='long_answer' for que in json_data.get('quiz',None)['questions']):
            ques_str+='<div>\n'
            ques_str+='<h2 style="text-align:center;">Long Answer</h2>\n'
            ques_str+='<hr>\n'
            for que in json_data.get('quiz',None)['questions']:
                que_type=que.get('type',None)
                if que_type=='long_answer':
                    qid_order.append(que['qid'])
                    ques_str+=f'<h4>Question: {len(qid_order)} | Score: {que["score"]} | Negative Score: -{que["negative_score"]}</h4>\n'
                    ques_str+=jax2tex(que.get('title'))
                    ques_str+='\n'
            ques_str+='</div>\n'
        #==================================================================================
        if len(qid_order)==len(json_data.get('quiz',None)['questions']):
            pass
        else:
            ques_str+='<div>\n'
            ques_str+='<h2 style="text-align:center;">Other Types</h2>\n'
            ques_str+='<hr>\n'
            for que in json_data.get('quiz',None)['questions']:
                que_type=que.get('type',None)
                if que_type!='truefalse' and que_type!='multichoice' and que_type!='short_answer' and que_type!='long_answer':
                    qid_order.append(que['qid'])
                    ques_str+=f'<h4>Question: {len(qid_order)} | Score: {que["score"]} | Negative Score: -{que["negative_score"]}</h4>\n'
                    ques_str+=jax2tex(que.get('title'))
                    ques_str+='\n'
            ques_str+='</div>\n'
        
        # close bosy and html tags
        ans_str+='</body>\n</html>'
    return ques_str+ans_str
#==================================================================================

# styling can be changed in `main.css` file
# give full path of CSS file something goes wrong in your case
CSS='main.css'

def html2pdf(html_page=None):
    if html_page is None:
        print('This script can be used to convert html page str into a pdf.')
    else:
        pdf_name=html_page.split('.html')[0]+'.pdf'
        options = {
            'page-size': 'Letter',
            'margin-top': '0.01in',
            'margin-right': '0.75in',
            'margin-bottom': '0.01in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'javascript-delay':'5000' # give it time to render javascript
            # https://stackoverflow.com/questions/25757503/approach-python-pdfkit-convert-webpagejs-generated-into-pdf
        }
        # try:
        pdfkit.from_file(html_page,pdf_name, options=options) # can add CSS
        # except Exception as e:
            # print(e)    
#==================================================================================

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
#==================================================================================

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
print(f'collecting quiz and assignments data for course {courseName}')
#==================================================================================

folder=courseName.upper()
if os.path.isdir(os.path.join(os.getcwd(),folder)):
    if os.getcwd()==os.path.join(os.getcwd(),folder):
        pass
    else:
        os.chdir(os.path.join(os.getcwd(),folder))
else:
    os.mkdir(os.path.join(os.getcwd(),folder))
    os.chdir(os.path.join(os.getcwd(),folder))


sub_folder='Quizzes'

if os.path.isdir(os.path.join(os.getcwd(),sub_folder)):
    if os.getcwd()==os.path.join(os.getcwd(),sub_folder):
        pass
    else:
        os.chdir(os.path.join(os.getcwd(),sub_folder))
else:
    os.mkdir(os.path.join(os.getcwd(),sub_folder))
    os.chdir(os.path.join(os.getcwd(),sub_folder))

#==================================================================================
summaryURL=f'https://hello.iitk.ac.in/api/{courseName}21/quiz/summary'
data=sessionHello.get(summaryURL,headers=customHeaders).json()
if len(data)>0:
    print('Total Quizzes Found --',len(data))
    with open('quizzes-summary.json','w') as file:
        json.dump(data,file)
    for quiz in data:
        qid=quiz.get('qid',-1)
        if qid!=-1:
            quiz_url=f'https://hello.iitk.ac.in/api/{courseName}21/quiz/{qid}'
            quiz_data=sessionHello.get(quiz_url,headers=customHeaders).json()
            # print(quiz_data)
            # get html data
            ques_list=html_list(quiz_data)
            if quiz_data.get('quiz',None) is None:
                quiz_title='No-Title'
            else:
                quiz_title='-'.join(quiz_data['quiz'].get('title','no-title').lower().split(' '))
            with open(f'{quiz_title}.html','w') as f:
                f.write(ques_list)

            # convert into html for better experience
            html_page=f'{quiz_title}.html'
            html2pdf(html_page)
            print(f'Stored {quiz_title}.pdf')
else:
    print(f'no lectures found for course {courseName}.')
    with open('quizzes-summary.json','w') as file:
        json.dump({'response':f'No Quiz data Found for course {courseName}'},file)
#==================================================================================


summaryURL=f'https://hello.iitk.ac.in/api/{courseName}21/assignments/summary'
data=sessionHello.get(summaryURL,headers=customHeaders).json()
if len(data)>0:
    print('Total Assignments Found --',len(data))
    with open('assignments-summary.json','w') as file:
        json.dump(data,file)
    for assignment in data:
        qid=assignment.get('aid',-1)
        if qid!=-1:
            assignment_url=f'https://hello.iitk.ac.in/api/{courseName}21/assignments/{qid}'
            assignment_data=sessionHello.get(assignment_url,headers=customHeaders).json()

            if assignment.get('title',None) is None:
                assignment_title='No-Title'
            else:
                assignment_title='-'.join(assignment.get('title','no-title').lower().split(' '))
            with open(f'{assignment_title}.json','w') as f:
                json.dump(assignment_data,f)

            assignment_url=f'https://hello.iitk.ac.in/api/{courseName}21/assignments/submissions/{qid}'
            assignment_data=sessionHello.get(assignment_url,headers=customHeaders).json()

            with open(f'{assignment_title}_submission.json','w') as f:
                json.dump(assignment_data,f)

            print(f'Stored {assignment_title} files')    
else:
    print(f'no lectures found for course {courseName}.')
    with open('quizzes-summary.json','w') as file:
        json.dump({'response':f'No Quiz data Found for course {courseName}'},file)
    