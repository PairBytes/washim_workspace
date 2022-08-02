
# We’ll need to first import the requests library, and then download the page using the requests.get method:
import requests
from bs4 import BeautifulSoup
from csv import writer

url= "http://www.rajasthanindustries.org/ViewCompanyProfile.aspx?id=All&typet=alpha"

page = requests.get(url)
print("page:",page)

# This object has a status_code property, which indicates if the page was downloaded successfully:
print('Status Code:',page.status_code)

# We can print out the HTML content of the page using the content property:
# print('HTML Content:',page.content)

# We can now print out the HTML content of the page, formatted nicely, using the prettify method on the BeautifulSoup object.
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
# print('List',list(soup.children))

# If we want to extract a single tag, we can instead use the find_all method, which will find all the instances of a tag on a page
# print(soup.find_all('p')).get_text()

lists = soup.find_all(id="ContentPlaceHolder1_DataList1")

with open('rajasthanindustries.csv', 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f)
        header = ['Company Name', 'Adress', 'PH', 'Movie','Email','Website','Key Pax','Product']
        thewriter.writerow(header)

        for list in lists:
                CompanyName = list.find('span', id="ContentPlaceHolder1_DataList1_lbl_companyname_0").text.replace('\n', '')
                print("Company Name:",CompanyName)
                Adress = list.find('span', id="ContentPlaceHolder1_DataList1_lbl_address_0").text.replace('\n', '')
                print('Adress:',Adress)
                PH = list.find('span', id="ContentPlaceHolder1_DataList1_lbl_ph_0").text.replace('\n', '')
                print('PH:',PH)
                Mobile = list.find('span', id="ContentPlaceHolder1_DataList1_lbl_mobile_0").text.replace('\n', '')
                print('Mobile:',Mobile)
                Email = list.find('tr', id="ContentPlaceHolder1_DataList1_tremail_0").text.replace('\n', '')
                print(Email)
                Website = list.find('tr', id="ContentPlaceHolder1_DataList1_trwebsite_0").text.replace('\n', '')
                print(Website)
                KeyPax = list.find('tr', id="ContentPlaceHolder1_DataList1_trcontactperson_0").text.replace('\n', '')
                print(KeyPax)
                Product = list.find('tr', id="ContentPlaceHolder1_DataList1_trproduct_0").text.replace('\n', '')
                print(Product)

                info = ['Company Name', 'Adress', 'PH', 'Movie','Email','Website','Key Pax','Product']
                thewriter.writerow(info)