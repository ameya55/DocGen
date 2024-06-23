import streamlit as st
import json
import os
from io import StringIO
import google.generativeai as palm
import langchain
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE

palm.configure(api_key='YOUR KEY')
model = palm.GenerativeModel('gemini-1.0-pro')
generation_config = {'temperature' : 0.9}

def doc_gemini(data):
    #Write a function
    data1 = ""
    for line in data[:10]:
        data1+=line
    prompt1 = f''' 
    Role : You are a programmer having prowess in all programming languages.
    Taks : Generate the name of the language in which given program is written
    Data : {data1}
    '''
    lang = model.generate_content(prompt1,generation_config=generation_config)
    for part in lang.parts:
        lang = part.text

    prompt = f'''
    Role : You are a {lang} developer having deep understanding of developing web applications,mobile applications and desktop applications.
    Task : Generate a comprehensive technical documentation for the given code.
    Data : {data}
    Instructions :
        
        A] Pre-requisites - database defaults
        B] Non-technical aspects :
                        1) Purpose of code
                        2) Flow of code
                            i. Input required
                            ii. Process
                            iii. Output required
        C] Technical aspects :
                        1) Global, local declarations

                        2) Type of declarations

                        3) Flow of code
                            i. Entry point
                            ii. Navigations ( menu-wise, code-wise)
                            iii. Processing
                            iv. Output
                        4) Connections
                            i. External resources (web API, etc.)
                            ii. Database connections ( DB objects used)
    '''   
    response = model.generate_content(prompt,generation_config=generation_config)
    output = ''
    for part in response.parts:
        output+=part.text
    return output

def string_to_word_doc(string_data, doc_filename):
    document = docx.Document()
    heading1_style = document.styles.add_style('Heading1', WD_STYLE_TYPE.PARAGRAPH)
    heading1_style.font.name = 'Calibri'
    heading1_style.font.size = Pt(16)
    heading1_style.font.bold = True
    heading1_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    heading2_style = document.styles.add_style('Heading2', WD_STYLE_TYPE.PARAGRAPH)
    heading2_style.base_style = document.styles['Normal']
    heading2_style.font.name = 'Calibri'
    heading2_style.font.size = Pt(14)
    heading2_style.font.bold = True
    heading2_style.paragraph_format.left_indent = Inches(0.5)

    heading3_style = document.styles.add_style('Heading3', WD_STYLE_TYPE.PARAGRAPH)
    heading3_style.base_style = document.styles['Normal']
    heading3_style.font.name = 'Calibri'
    heading3_style.font.size = Pt(12)
    heading3_style.font.italic = True
    heading3_style.paragraph_format.left_indent = Inches(1)

    bullet_point_style = document.styles.add_style('Bullet_Point', WD_STYLE_TYPE.PARAGRAPH)
    bullet_point_style.base_style = document.styles['Normal']
    bullet_point_style.font.name = 'Calibri'
    bullet_point_style.font.size = Pt(12)
    bullet_point_style.paragraph_format.left_indent = Inches(0.75)
    bullet_point_style.paragraph_format.list_indent = -Inches(0.25)  # Adjust indent for bullets

    #Applying syles
    for line in string_data.splitlines():
        paragraph = document.add_paragraph()
        if line.startswith('## '):
            paragraph.text = line[3:]
            paragraph.style = heading1_style
            paragraph.text = line.strip('#')
        elif line.startswith('### '):
            paragraph.text = line[4:]
            paragraph.style = heading2_style
            paragraph.text = line.strip('#')
        elif line.startswith('#### '):
            paragraph.text = line[5:]
            paragraph.style = bullet_point_style
            paragraph.text = line.strip('#')
        elif line.startswith('  *') or line.startswith('* '):
            paragraph.style = bullet_point_style
            paragraph.text = line.strip('*')
        else:
            paragraph.text = line.strip('*')
    document.save(doc_filename)        
def main():
    with st.sidebar:
        st.image('logo_image.jpg')
        st.subheader('DocForge', divider='grey')
        st.write("Submit a ANY code to generate documentation.")
    your_option = ["DocGen"]
    #option_chosen = st.selectbox("Select one:",options=your_option,index=None,placeholder="Choose an option")
    #if option_chosen=='DocGen':
    file_path = st.file_uploader("Please upload your file here")
    data= None
    if file_path is not None:
        doc_filename = file_path.name[:-3] + '.docx'
        string_data = StringIO(file_path.getvalue().decode("utf-8"))
        data = string_data.read()
        answer = doc_gemini(data)
        st.write("Below is the document: ")
#answer = doc_gemini(data)
        st.write(answer)      
        string_to_word_doc(answer, doc_filename)

if __name__ == '__main__':
    main()
