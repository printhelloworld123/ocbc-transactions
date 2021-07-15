import base64 
import time
import pandas as pd 
import streamlit as st

timestr = time.strftime("%d%m%y-%H%M%S")

# Function to allow download of prepared csv file as txt file #
def text_downloader(raw_text):
	b64 = base64.b64encode(raw_text.encode()).decode()
	new_filename = "ocbc_paynow_{}.txt".format(timestr)
	st.markdown("#### Download txt File ###")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click here</a>'
	st.markdown(href,unsafe_allow_html=True)

class PayNowTransaction:
    def __init__(self, file):
        self.file = file
        self.date = str(date).split('-')[2] + str(date).split('-')[1] + str(date).split('-')[0]

    # Function to prepare name column into a standard accepted by OCBC #
    ## (remove empty spaces, capitalize all words) ##
    def standardize_name_column(self, name):
        new_name = str(name)
        new_name = new_name.replace(' ', '')
        new_name = new_name.upper()
        return new_name
    
    # Function to prepare amount column into a standard accepted by OCBC #
    ## (remove empty spaces, remove "$", fill up 17 char count req) ##
    def standardize_amount_column(self, amount):
        new_amount = str(amount)
        new_amount = new_amount.replace(' ','')
        if new_amount[0] == "$":
            new_amount = new_amount[1:]
        else:
            pass
        new_amount = str(int(float(new_amount) * 100))
        nos_zeros = 17 - len(new_amount)
        return "0" * nos_zeros + new_amount 
    
    # Function to prepare phone column into a standard accepted by OCBC #
    ## (remove empty spaces, ensure +65 is provided) ##
    def standardize_phone_column(self, phone):
        new_phone = str(phone)
        new_phone = new_phone.replace(' ','')
        if new_phone[0:3] == "+65":
            pass
        elif new_phone[0:2] == "65":
            new_phone = "+" + new_phone
        elif new_phone[0:4] == "'+65":
            new_phone = new_phone[1:]
        else:
            new_phone = "+65" + new_phone
        return new_phone
        
    # Function to standardize all required columns (name, phone, amount) #
    def prepare_file(self):
        self.file['Name'] = list(map(lambda x: self.standardize_name_column(x), list(self.file['Name'])))
        self.file['Amount'] = list(map(lambda x: self.standardize_amount_column(x), list(self.file['Amount'])))
        self.file['Phone'] = list(map(lambda x: self.standardize_phone_column(x), list(self.file['Phone'])))
    
    # Function to convert data into a file format accepted by OCBC # 
    def download_file(self):
        fields = ['10' + 11 * ' ' + 'OCBCSGSGXXX695271080001'+ 169 * ' ' + 'GIRO' + 16 * ' ' + self.date + 767 * ' ']
        for i in range(len(self.file)):
            name_final = 45 * ' ' + self.file.loc[i,'Name']
            after_name_space = 188 - len(self.file.loc[i,'Name']) - 45
            amount_final = after_name_space * ' ' + self.file.loc[i,'Amount']
            proxy_type_final = 610 * ' ' + 'MSISDN'
            proxy_value_final = 6 * ' ' + self.file.loc[i,'Phone'] + 162 * ' '
            info = [name_final + amount_final + proxy_type_final + proxy_value_final]
            fields += info
        final = ''
        for item in fields:
            final += item + '\n'
        return final


# Creating the user interface #

st.title('OCBC PayNow Transactions Prototype')
date = st.date_input('Date of transaction', value=None, min_value=None, max_value=None, key=None, help=None)
try:
    uploaded_file = st.file_uploader("Upload a CSV file",type=['csv'])
    df = pd.read_csv(uploaded_file)
    st.write('This is the uploaded CSV file')
    df
    transaction_file = PayNowTransaction(df)
    transaction_file.prepare_file()
    st.write('Please check that the data fields have been converted to the correct format')
    transaction_file.file
    text_downloader(transaction_file.download_file())
except ValueError or NameError:
    pass
