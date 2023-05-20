import requests
import json
import csv


#--------------------------------------------
# Get data from csv
#-----------------------------------
filterValues = []
with open("trackingcodelist2.csv","r",encoding="utf-8") as source:
    read = csv.reader(source)
    for row in read:
        if row[2] != "":
            continue
        else:
            filterValues.append(row[0])

totalTCs = len(filterValues)        

print("Missing TCs = " + str(totalTCs))



#LOGIN

request_url = "https://api.nextsmartship.com/oms/v2/login"


def nss_logger(login, password):
    s = requests.Session()
    payload = {"email": login,
    "password": password}
    res = s.post(request_url,json=payload)
    s.headers.update({"Authorization":"Bearer "+json.loads(res.content)["data"]["token"]})
    success = json.loads(res.text)
    if success["code"] == 0:
        print("Login successful")
    return s

session = nss_logger("milena@div-brands.com","NSS01076")

link = "https://api.nextsmartship.com/oms/billings"
payload = {
  "filterName": "platformOrderNos",
  "transactionType": "checkout_deduction",
  "filterValues": filterValues,
  "pageSize": 10000,
  "current": 1,
  "sorter": {}
}

response = session.post(link,json = payload)

data = json.loads(response.text)['data']

lenData = len(data)

print("TCs found = " + str(lenData))

print("Still not available = " + str(totalTCs - lenData))



with open("tc-finder.csv","w",encoding="utf-8",newline="") as result:
    write = csv.writer(result)
    write.writerow(["Order Id","Tracking Code"])
    for obj in data:
        try:
            write.writerow([obj["order"]["platformOrderNo"],"'" + str(obj["order"]["trackingNumber"])])        
        except:
            write.writerow([obj["order"]["platformOrderNo"],"Still not Available"]) 
