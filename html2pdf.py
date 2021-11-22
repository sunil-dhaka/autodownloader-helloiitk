import pdfkit

# styling can be changed in `main.css` file
# give full path of CSS file something goes wrong in your case
CSS='main.css'

def main(html_page=None):
    if html_page is None:
        print('This script can be used to convert html page str into a pdf.')
    else:
        pdf_name=html_page.split('.html')[0]+'.pdf'
        options = {
            'page-size': 'Letter',
            # 'margin-top': '0.75in',
            'margin-right': '0.75in',
            # 'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'javascript-delay':'5000' # give it time to render javascript
            # https://stackoverflow.com/questions/25757503/approach-python-pdfkit-convert-webpagejs-generated-into-pdf
        }
        try:
            pdfkit.from_file(html_page,pdf_name, options=options,css=CSS)
        except Exception as e:
            print(e)    

if __name__=='__main__':
    main()