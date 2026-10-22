"""
@Goal: to copy multiple file into single file
@author:Sachin Bodage
@date: 08-12-2023
@version:0.1
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

#Creat an empty DataFrame
all_month_data=pd.DataFrame()

#Create a list of all file name in folder using List comprehension
files=[file for file in os.listdir("./Subway/Sales_Data")]

#Iterrate Each file in list
for file in files:
    #Creat a DataFram of Each file
    df=pd.read_csv("./Subway/Sales_Data/"+file)
    #concate each month DataFram and save in one file
    all_month_data=pd.concat([all_month_data,df])
    
    #print(all_month_data)

all_month_data.to_csv("all_data.csv",index=False)
all_data=pd.read_csv("all_data.csv")

#In a DataFrame add one colum "month" using "Order Date" column
all_data["month"]=all_data["Order Date"].str[:2]
#remove all NAN value using dropna function
all_data.dropna(how="all",inplace=True)

#remove all row having "Or" in column
all_data=all_data[all_data["month"]!="Or"]

#conver colum value from str to int using astype function
all_data["month"]=all_data["month"].astype("int32")
#conver colum value from str to int using pd.to_numeric method
all_data["Price Each"]=pd.to_numeric(all_data["Price Each"])
#conver colum value from str to int using pd.to_numeric method
all_data["Quantity Ordered"]=pd.to_numeric(all_data["Quantity Ordered"])
#add new colum sales using multiplication of Quantity Ordered and Price Each colum
all_data["sales"]=all_data["Quantity Ordered"] * all_data["Price Each"]
##print(all_data.head())
##print(all_data.tail())
#Question-->calcualate month wise sale 
Result=all_data.groupby("month").sum()

##print(Result)

months=range(1,13)
plt.bar(months,Result["sales"])
plt.xticks(months)
plt.ylabel("Sales in USD($)")
plt.xlabel("Month Number")
plt.show()                                  

#Question--> calculate city wise sales
#add city colum using Adress column

all_data["city"]=all_data["Purchase Address"].apply(lambda x:x.split(",")[1])
all_data["state"]=all_data["Purchase Address"].apply(lambda y:y.split(",")[2].split(" ")[1])
all_data["city_state"]=all_data["city"]+ " " + all_data["state"]


result_city=all_data.groupby("city").sum()
print(result_city)

#to get list of all uniqu city from dataframe
#city=all_data["city"].unique()  //random city

city=[city for city,df in all_data.groupby("city")]

plt.bar(city,result_city["sales"])
plt.xticks(city)
#plt.xticks(city,rotation="vertical",size=12)
plt.ylabel("Sales in USD($)")
plt.xlabel("City")
plt.show()
     
#Question-->What time should we display advertisement to maximize likehood of customer buying product

#all_data["Order Date"]=pd.to_datetime(all_data["Order Date"],format="%m%d%y")
#all_data["hour"]=all_data["Order Date"].dt.hour
#all_data["minute"]=all_data["Order Date"].dt.minute
all_data["hour"]=all_data["Order Date"].str[9:11].astype("int32")

hours=[hour for hour,df in all_data.groupby("hour")]
plt.plot(hours,all_data.groupby(["hour"]).count())
plt.xticks(hours)
plt.xlabel("hour")
plt.ylabel("Number of Orders")
plt.grid()
plt.show()


#Question--> which product mostly buy together
df=all_data[all_data["Order ID"].duplicated(keep=False)]

df["Grouped"]=df.groupby("Order ID")["Product"].transform(lambda x: ",".join(x))
df=df[["Order ID","Grouped"]].drop_duplicates()

from itertools import combinations
from collections import Counter

count=Counter()
for row in df["Grouped"]:
    row_list=row.split(",")
    count.update(Counter(combinations(row_list,3)))

for key,value in count.most_common(100):
    print(key,value)

#Question-->Whats product sold most,why do you think sold most
product_group=all_data.groupby("Product")
Quantyty_ordered=product_group.sum()["Qunatity Ordered"]
