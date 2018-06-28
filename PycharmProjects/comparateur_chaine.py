import pandas as pd

df1=pd.read_csv("/home/francois/Documents/all_url_company.csv")
df2=pd.read_csv("/home/francois/Documents/all_employee_company.csv")


all_urls= df1.get('linkedinUrl').values
present_urls = df2.get('companyUrl').values
count= 0



for i in range(0, len(all_urls)):

    if all_urls[i] not in present_urls:
        print(all_urls[i])


