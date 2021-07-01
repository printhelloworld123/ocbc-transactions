import streamlit as st
import pandas as pd

## Creating the backend transformations ##

class PayNowTransaction:
    def __init__(self, file):
        self.file = file
        self.date = str(date).split('-')[2] + str(date).split('-')[1] + str(date).split('-')[0]
        self.name_of_text_tile = name_of_file

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
        with open(str(self.name_of_text_tile + '.txt'), "w") as f:
            for field in fields:
                f.write(field)
                f.write('\n')

## Creating the front end interface ##

st.title('OCBC PayNow Transactions Prototype')

date = st.date_input('Date of transaction', value=None, min_value=None, max_value=None, key=None, help=None)

name_of_file = st.text_input("Name of file", 'Please include the name of your text file')

try:
    uploaded_file = st.file_uploader("Upload a CSV file",type=['csv'])
    df = pd.read_csv(uploaded_file)
    st.write('This is the uploaded CSV file')
    df
    transaction_file = PayNowTransaction(df)
    transaction_file.prepare_file()
    st.write('Please check that the data fields have been converted to the correct format')
    transaction_file.file
    result = st.button('Download')
    if result:
        transaction_file.download_file()
        st.write(str(transaction_file.name_of_text_tile + '.txt') + ' has been downloaded to your computer :smile:')
except ValueError or NameError:
    pass



