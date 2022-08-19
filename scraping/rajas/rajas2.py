from tokenize import Name
from bs4 import BeautifulSoup
import requests, openpyxl





url = 'http://www.rajasthanindustries.org/ViewCompanyProfile.aspx?id=All&typet=alpha'
source = requests.get(url)
source.raise_for_status()
soup = BeautifulSoup(source.text,'html.parser')
tags = soup.find_all(id = True, href= True)
title =soup.title
details = soup.find('table', id="ContentPlaceHolder1_DataList1")

for i in range(100):
        try:
            name = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_companyname_{i}"}).text
        except:
            name = ''
        print('Name:',name)

        try:
            mobile_number = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_mobile_{i}"}).text
        except:
            mobile_number= ''
        print('Mobile_Number:',mobile_number)

        try:
            email_id = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_email_{i}"}).text
        except:
            email_id = ''
        print('Email:',email_id)

        try:
            website = details.find('span', {'id':f"ContentPlaceHolder1_DataList1_lbl_website_{i}"}).text
        except :
            website = ''
        print('Website:',website)
        try:
            key_pax = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_contactper_{i}"}).text
        except:
            key_pax = ''
        print('Key Pax:',key_pax)
        try:
            product = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_products_{i}"}).text
        except:
            product =''
        print('product:',product)

        print('_______________________________________________________________________________')
        print()