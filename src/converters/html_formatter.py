"""
HTML formatter for quiz and assignment data.
"""
from typing import Dict, Any, Optional


class HtmlFormatter:
    """
    Class for formatting quiz data as HTML.
    """
    
    @staticmethod
    def jax2tex(text: str) -> str:
        """
        Convert MathJax notation to TeX for proper rendering.
        
        Parameters
        ----------
        text : str
            Text containing MathJax
            
        Returns
        -------
        str
            Text with MathJax converted to TeX
        """
        if text is None:
            return ""
            
        text = '$'.join(('$'.join(text.split('\\('))).split('\\)'))
        
        # Handle images in text
        if '<img' in text:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(text, 'html.parser')
            for img in soup.find_all('img'):
                if img['src'].startswith('/'):
                    img['src'] = 'https://hello.iitk.ac.in' + img['src']
            text = str(soup)
            
        return text
    
    @staticmethod
    def get_html_header(title: str = "Quizzes") -> str:
        """
        Generate HTML header with necessary styling and scripts.
        
        Parameters
        ----------
        title : str, optional
            Page title, by default "Quizzes"
            
        Returns
        -------
        str
            HTML header
        """
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width initial-scale=1.0">
<title>{title}</title>
<script type='text/x-mathjax-config'>MathJax.Hub.Config({{tex2jax: {{inlineMath: [['$','$'], ['\\\\(','\\\\)']]}},'
    'config: ['MMLorHTML.js'],extensions: ['mml2jax.js','tex2math.js'],jax: ['input/MathML','input/TeX', 'output/HTML-CSS']}});</script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<style>
    body {{ 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        line-height: 1.6;
    }}
    h1, h2 {{ text-align: center; color: #333; }}
    h4 {{ background-color: #f5f5f5; padding: 10px; border-left: 4px solid #007bff; }}
    hr {{ border: none; height: 1px; background-color: #ddd; margin: 30px 0; }}
    ol {{ padding-left: 20px; }}
    .question {{ margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #eee; }}
    .answer {{ color: #007bff; font-weight: bold; }}
</style>
</head>
<body>
"""
        
    @staticmethod
    def format_quiz_to_html(quiz_data: Dict[str, Any]) -> str:
        """
        Format quiz data as HTML.
        
        Parameters
        ----------
        quiz_data : Dict[str, Any]
            Quiz data from the API
            
        Returns
        -------
        str
            HTML representation of the quiz
        """
        if not quiz_data or 'quiz' not in quiz_data or 'questions' not in quiz_data['quiz']:
            return "<h2>No quiz data available</h2>"
            
        html = HtmlFormatter.get_html_header()
        
        # Start with questions section
        html += '<div>\n<h1>Questions</h1>\n<div>\n'
        
        # Check if solutions are available
        has_solutions = quiz_data.get('correctSolutions') is not None
        answers_html = '<hr>\n<hr>\n<div>\n<h1>Answers</h1>\n<hr>\n' if has_solutions else ''
        
        # Process questions by type
        question_types = ['truefalse', 'multichoice', 'short_answer', 'long_answer']
        qid_order = []
        
        # Process each type of question
        for q_type in question_types:
            questions = [q for q in quiz_data['quiz']['questions'] if q.get('type') == q_type]
            
            if questions:
                # Add section header for this question type
                section_title = {
                    'truefalse': 'True False',
                    'multichoice': 'Multiple Choice',
                    'short_answer': 'Short Answer',
                    'long_answer': 'Long Answer'
                }.get(q_type, q_type.replace('_', ' ').title())
                
                html += f'<div>\n<h2>{section_title}</h2>\n<hr>\n'
                if has_solutions:
                    answers_html += f'<div>\n<h2>{section_title}</h2>\n<hr>\n'
                
                # Process each question
                for question in questions:
                    qid_order.append(question['qid'])
                    q_num = len(qid_order)
                    
                    # Add question
                    html += (f'<div class="question">\n'
                            f'<h4>Question: {q_num} | Score: {question["score"]} | '
                            f'Negative Score: -{question["negative_score"]}</h4>\n'
                            f'{HtmlFormatter.jax2tex(question.get("title"))}\n')
                    
                    # Add options for multiple choice
                    if q_type == 'multichoice' and 'options' in question:
                        html += '<ol>\n'
                        for option in question['options']:
                            html += f'<li>{HtmlFormatter.jax2tex(option["value"])}</li>\n'
                        html += '</ol>\n'
                    
                    html += '</div>\n'
                    
                    # Add answer if available
                    if has_solutions:
                        answers_html += f'<h4>Answer: {q_num}</h4>\n'
                        
                        for sol in quiz_data['correctSolutions']:
                            if sol.get('qid') == question['qid']:
                                if q_type == 'truefalse':
                                    answer = sol.get('correctAnswer', [])[0].get('aid', None)
                                    if answer == 1:
                                        answers_html += '<h5 class="answer">True</h5>\n'
                                    elif answer == 0:
                                        answers_html += '<h5 class="answer">False</h5>\n'
                                    else:
                                        answers_html += f'<h5 class="answer">{answer}</h5>\n'
                                        
                                elif q_type == 'multichoice':
                                    answer_ids = [a.get('aid') for a in sol.get('correctAnswer', [])]
                                    
                                    for i, option in enumerate(question['options']):
                                        if option['aid'] in answer_ids:
                                            answers_html += (f'<h5 class="answer">{i+1}. '
                                                           f'{HtmlFormatter.jax2tex(option["value"])}</h5>\n')
                                            
                                elif q_type == 'short_answer':
                                    for a in sol.get('correctAnswer', []):
                                        answers_html += f'<h5 class="answer">{a}</h5>\n'
                                        
                                break
                
                html += '</div>\n'
                if has_solutions:
                    answers_html += '</div>\n'
        
        # Handle any remaining question types
        other_questions = [q for q in quiz_data['quiz']['questions'] 
                          if q.get('type') not in question_types]
        
        if other_questions:
            html += '<div>\n<h2>Other Types</h2>\n<hr>\n'
            
            for question in other_questions:
                qid_order.append(question['qid'])
                q_num = len(qid_order)
                
                html += (f'<h4>Question: {q_num} | Score: {question["score"]} | '
                        f'Negative Score: -{question["negative_score"]}</h4>\n'
                        f'{HtmlFormatter.jax2tex(question.get("title"))}\n')
            
            html += '</div>\n'
        
        # Close questions div
        html += '</div>\n'
        
        # Add answers if available
        if has_solutions:
            html += answers_html
            
        # Close body and html
        html += '</body>\n</html>'
        
        return html