import base64 
import time
import pandas as pd 
import streamlit as st

timestr = time.strftime("%d%m%y-%H%M%S")

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


    def prepare_file(self):
        
        def convert_amount(amount):
            new_value = str(int(float(amount) * 100))
            nos_zeros = 17 - len(new_value)
            return "0" * nos_zeros + new_value 
        
        self.file['phone'] = self.file.apply(lambda x: '+65' + str(int(x['phone'])), axis=1)
        self.file['amount'] = self.file.apply(lambda x: convert_amount(x['amount']),axis=1)
        
    def download_file(self):
        fields = ['10' + 11 * ' ' + 'OCBCSGSGXXX695271080001'+ 169 * ' ' + 'GIRO' + 16 * ' ' + self.date + 767 * ' ']
        for i in range(len(df)):
            amount_final = 188 * ' ' + df.loc[i,'amount']
            proxy_type_final = 610 * ' ' + 'MSISDN'
            proxy_value_final = 6 * ' ' + df.loc[i,'phone'] + 162 * ' '
            info = [amount_final + proxy_type_final + proxy_value_final]
            fields += info
        final = ''
        for item in fields:
            final += item
        return final


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
