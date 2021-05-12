import docx2txt
import PyPDF2
import pyresparser
import smtplib
import os
import spacy
spacy.load('en_core_web_sm')
from resume_parser import resumeparse
from pyresparser import ResumeParser
import pandas as pd
from sklearn import datasets
from pprint import pprint
import shutil

resume_path = "C:\\Users\\prasa\\projects\\recruitment_project\\resumes\\"
accepted_path = "C:\\Users\\prasa\\projects\\recruitment_project\\resumes\\Accepted\\"
rejected_path = "C:\\Users\\prasa\\projects\\recruitment_project\\resumes\\Rejected\\"
# path = "C:\\Users\\prasa\\projects\\recruitment_project\\resumes\\pd.docx"

def read_doc(path):
    res_disc = {"data":"", "SI":"", "JD":"", "filename":path.split("\\")[-1]}
    _list = []
    # for i in dir_list:
    data = ResumeParser(path).get_extracted_data()

    #print(data)

    #data = ResumeParser('C:\\Users\\prasa\\projects\\recruitment_project\\resumes\\pd.docx').get_extracted_data()

    res = {key: data[key] for key in data.keys() & {'name','email', 'mobile_number'}}
    print(res)
    print("Name: " + str(res['name']) + '\n' + "Email: " + str(res['email']) + '\n' + "Mobile Number: " + str(res['mobile_number']) + '\n')
    temp = res_disc.copy()
    temp["data"] = res
    filename,ext = path.split(".")
    if ext.lower() == "docx":
        # # Load resume in word #
        resume = docx2txt.process(path)
    else:    
        # Load resume in pdf #
        resume = PyPDF2.PdfFileReader(path)
        # .getDocumentInfo()
        # continue

    
    for j in dir_list1:
        # load job description # 
        #job_desc1 = docx2txt.process("C:\\Users\\prasa\\projects\\recruitment_project\\JD\\ODA_JD1.docx")

        job_desc = docx2txt.process(os.path.join(JDpaths, j))
        temp["JD"] = os.path.join(JDpaths, j)
        #print(job_desc)


        # list of text to store resume and JD
        text = [resume,job_desc]

        from sklearn.feature_extraction.text import CountVectorizer
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)

        from sklearn.metrics.pairwise import cosine_similarity

        #print(cosine_similarity(count_matrix))    
        match = cosine_similarity(count_matrix)[0][1]
        match = match*100
        match = round(match, 2)
        temp["SI"] = match
        _list.append(temp)              # result store in data
        print("Your resume matches around " + str(match)+ "% of job description " + j)
        print()
        sendmail(temp, j)

def sendmail(res, j):

    name1 = res["data"]['name']            
    email1 = res["data"]['email']
    mobile1 = res["data"]['mobile_number']
    link = "https://docs.google.com/forms/d/e/1FAIpQLSdrgyGTnTJ56VUEKiwFl1gm05r2AEpyiaEfTlBy7MkU4cqPUw/viewform?usp=sf_link"
    match = res["SI"]
    if match > 50:

        # print("Application Accepted for the next round !!!")
        # print("Be ready for the test !!!!")
        print("\n")

        # Send Email #
        sender_email = "odatestrecruitment@gmail.com"
        rec_email = email1
        password = "oda@1234"
        msg = "Dear Candidate,\nGreetings from recruitement department of OnDemand Agility Solutions.\nWe are pleased to inform you that your application has cleared the screening round.\nYou are cordially invited to the next round of selection process which is the assessment round. Link to the assessment form has been attached below.\nKindly submit your assessment timely.\n\nRegards,\nODAHRD." "\nYour link for the Test is: " + "\n"+link
        subject = "HR:Recruitment Process"

        message = f'Subject: {subject}\n\n{msg}'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        #print("Login Successful")

        server.sendmail(sender_email,rec_email,message)
        print("Email sent !!!")
        print("")

        """ SMS Sending """
        

        """ Moving document """
        shutil.move(resume_path+res["filename"], accepted_path+res["filename"])
        # shutil.copyfile(resume_path+res["filename"], accepted_path+res["filename"])
        
        """ appdending 2 dictionary for JD Name in csv """
        res['data']['JD_Name'] = j

        """ CSV """
        from csv import DictWriter

        field_names = ['name', 'email', 'mobile_number', 'JD_Name']
        with open(resume_path+'Accepted_profile.csv', 'a') as csvfile:
            dictwriter_object = DictWriter(csvfile, fieldnames=field_names)
            dictwriter_object.writerow(res['data'])
            csvfile.close()

    else:
        print("Application Rejected we are sorry !!! \nAs resume match is less than the expected one.\nBetter luck next time")

        ## Send Email ##
        sender_email = "odatestrecruitment@gmail.com"
        rec_email = email1
        password = "oda@1234"
        msg = "Dear "+ name1 + "," + "\nApplication Rejected we are sorry !!!"
        subject = "HR:Recruitment Process"

        message = f'Subject: {subject}\n\n{msg}'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        #print("Login Successful")

        server.sendmail(sender_email,rec_email,message)
        print("Email sent !!!")
        print("")
        shutil.move(resume_path+res["filename"], rejected_path+res["filename"])
        # shutil.copyfile(resume_path+res["filename"], rejected_path+res["filename"])

# for resumes #
dir_list = os.listdir(r'C:\Users\prasa\projects\recruitment_project\resumes')
print("Total Resumes: ", len(dir_list))
print("")
paths = r'C:\Users\prasa\projects\recruitment_project\resumes'

# For JDs #
dir_list1 = os.listdir(r'C:\Users\prasa\projects\recruitment_project\JD')
print("")
print("Total Jd's: ", len(dir_list1))
print("")
JDpaths = r'C:\Users\prasa\projects\recruitment_project\JD'

# x = read_doc()
# sendmail(x)
