import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from pl import plot
import pandas as pd

conn=sqlite3.connect('patient.db',check_same_thread=False)
cur=conn.cursor()

def home():
    st.title('WELCOME TO PATIENT INFORMATION SYSTEM')
    #maybe add an image here
    img=Image.open('resources/logo.png')
    st.image(img)

def display_all():
    dat=cur.execute("SELECT * from patient_detail;")
    cols=[c[0] for c in dat.description]

    df=pd.DataFrame.from_records(data=dat.fetchall(),columns=cols)
    
    st.write(df.head())

def display(id=1):
    #to store in dataframe
    dat=cur.execute("SELECT * from patient_detail where ID=?;",(id))
    cols=[c[0] for c in dat.description]
    

    df=pd.DataFrame.from_records(data=dat.fetchall(),columns=cols)
    df.style.apply(lambda x: "background-color: red")
    st.write(df.head())

    plot()
    
    

def form():
    st.title("PATIENT DETAIL FORM")
    with st.form(key="patient form"):
        id=st.text_input("Id")
        name=st.text_input("Full Name")
        age=st.text_input("Age")
        gender=st.radio("Gender",('Male','Female'))
        address=st.text_input("Address")
        mobile=st.text_input("Mobile Number")
        dob=st.date_input("Date of Birth")
        remarks=st.text_input("Remarks")

        

        submit=st.form_submit_button(label="Insert Record")

        if submit==True:
            store_data(id,name, age,gender, address, mobile, dob,remarks)
        
def store_data(id,name,age,gender,address,mobile,dob,remarks):
    cur.execute("""CREATE TABLE IF NOT EXISTS patient_detail(ID TEXT(50) PRIMARY KEY,
                                                            NAME TEXT(100) NOT NULL,
                                                            AGE TEXT(5) NOT NULL,
                                                            GENDER TEXT(10) NOT NULL,
                                                            ADDRESS TEXT(200) NOT NULL,
                                                            MOBILE TEXT(10) NOT NULL,
                                                            DOB TEXT(50) NOT NULL,
                                                            REMARKS TEXT(500));""")

    cur.execute("INSERT INTO patient_detail values (?,?,?,?,?,?,?,?);",(id,name,age,gender,address,mobile,dob,remarks))
    
    conn.commit()#to save changes
    #conn.close()
    st.success("successfully submitted")


st.sidebar.title("Navigation")

options=st.sidebar.radio("Navigation",['Home','Insert new record','View record'])

if options=='Home':
    home()
elif options=='View record':
    with st.form(key="patient id"):
        
        id=st.text_input("Enter ID")
        submit=st.form_submit_button("SEARCH")
        disall=st.form_submit_button("Display All Patients")

        if(disall==True):
            display_all()
        if submit==True:
            display(id)

elif options=='Insert new record':
    form()
