def jax2tex(text):
    text='$'.join(('$'.join(text.split('\('))).split('\)'))
    return text

def main(json_data=None):
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
        ques_str+='<h2 style="text-align:center;">True False</h2>\n'
        ques_str+='<hr>\n<br>'
        for que in json_data.get('quiz',None)['questions']:
            que_type=que.get('type',None)
            if que_type=='truefalse':
                qid_order.append(que['qid'])
                ques_str+=f'<h4>Question: {len(qid_order)+1} | Score: {que["score"]} | Negative Score: {que["negative_score"]}</h4>'

                ques_str+=jax2tex(que.get('title'))
                ques_str+='\n<br>'
        ques_str+='<h2 style="text-align:center;">Muliple Choice</h2>\n'
        ques_str+='<hr>\n<br>'
        for que in json_data.get('quiz',None)['questions']:
            que_type=que.get('type',None)
            if que_type=='multichoice':
                qid_order.append(que['qid'])
                ques_str+=f'<h4>Question: {len(qid_order)+1} | Score: {que["score"]} | Negative Score: {que["negative_score"]}</h4>'

                ques_str+=jax2tex(que.get('title'))
                ques_str+='<ol>\n'
                for option in que['options']:
                    ques_str+=f'<li>{jax2tex(option["value"])}</li>\n'
                ques_str+='<ol>\n'
                ques_str+='\n<br>'
                
        ques_str+='<h2 style="text-align:center;">Short Answer</h2>\n'
        ques_str+='<hr>\n<br>'
        for que in json_data.get('quiz',None)['questions']:
            que_type=que.get('type',None)
            if que_type=='short_answer':
                qid_order.append(que['qid'])
                ques_str+=f'<h4>Question: {len(qid_order)+1} | Score: {que["score"]} | Negative Score: {que["negative_score"]}</h4>'
                ques_str+=jax2tex(que.get('title'))
                ques_str+='\n<br>'
        ques_str+='<h2 style="text-align:center;">Long Answer</h2>\n'
        ques_str+='<hr>\n<br>'
        for que in json_data.get('quiz',None)['questions']:
            que_type=que.get('type',None)
            if que_type=='long_answer':
                qid_order.append(que['qid'])
                ques_str+=f'<h4>Question: {len(qid_order)+1} | Score: {que["score"]} | Negative Score: {que["negative_score"]}</h4>'
                ques_str+=jax2tex(que.get('title'))
                ques_str+='\n<br>'
        if len(qid_order)==len(json_data.get('quiz',None)['questions']):
            pass
        else:
            ques_str+='<h2 style="text-align:center;">Other Types</h2>\n'
            ques_str+='<hr>\n<br>'
            for que in json_data.get('quiz',None)['questions']:
                que_type=que.get('type',None)
                if que_type!='truefalse' and que_type!='multichoice' and que_type!='short_answer' and que_type!='long_answer':
                    qid_order.append(que['qid'])
                    ques_str+=f'<h4>Question: {len(qid_order)+1} | Score: {que["score"]} | Negative Score: {que["negative_score"]}</h4>'
                    ques_str+=jax2tex(que.get('title'))
                    ques_str+='\n<br>'

if __name__=='__main__':
    main()
