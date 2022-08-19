from tokenize import Name
from bs4 import BeautifulSoup
import requests, openpyxl



excel = openpyxl.Workbook()
sheet = excel.active
sheet.title ='Rajasthan_industry_data'
sheet.append(["name", "mobile_number", "email_id","website","key_pax","product"])
try:
    url = 'http://www.rajasthanindustries.org/ViewCompanyProfile.aspx?id=All&typet=alpha'
    source = requests.get(url)
    source.raise_for_status()
    soup = BeautifulSoup(source.text,'html.parser')
    tags = soup.find_all(id = True, href= True)
    title =soup.title
    details = soup.find('table', id="ContentPlaceHolder1_DataList1")
    for i in range(1000):
        try:
            name = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_companyname_{i}"}).text
        except:
            name = ''
        
        try:
            mobile_number = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_mobile_{i}"}).text
        except:
            mobile_number= ''
        
        try:
            email_id = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_email_{i}"}).text
        except:
            email_id = ''

        try:
            website = details.find('span', {'id':f"ContentPlaceHolder1_DataList1_lbl_website_{i}"}).text
        except :
            website = ''
        try:
            key_pax = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_contactper_{i}"}).text
        except:
            key_pax = ''
        try:
            product = details.find('span',{'id':f"ContentPlaceHolder1_DataList1_lbl_products_{i}"}).text
        except:
            product =''
        sheet.append([name,mobile_number,email_id,website,key_pax,product])
        # print(email_id, mobile_number)
        

except Exception as e:
    print(e)


excel.save('Rajastha_industries_data.xlsx')