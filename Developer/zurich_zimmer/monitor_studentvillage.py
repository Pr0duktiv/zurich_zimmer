import smtplib
from lxml import html
import requests
import time

class Monitoring:
    url = 'http://studentvillage.ch/unterkunfte/'
    treepath = '//table[@class="wohnen_table type_is_all"]/tbody/tr'
    limitprice = 1000
    targetemail = "YOUR@EMAIL.HERE"

    def requestPage(self):
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        rows = tree.xpath(self.treepath)
        result = list()

        for row in rows:
            #result.append([x.text for x in row.getchildren()])
            flat = []
            flatlink = row.xpath(".//a")[0].get('href')

            for x in row.getchildren():
                flat.append(x.text)

            flat.append(flatlink)
            result.append(flat)
        #print(result)
        return result

    def lookForFreeRooms(self, tablecontent):
        freerooms = ''
        for element in tablecontent:
            totalprice = int(element[4][4:-2])
            occupation = element[7]
            #status = "Reserviert"
            status = "Verfügbar"
            if occupation == status and totalprice <= self.limitprice:
                freerooms += (element[len(element)-1]) + '\n'
        return freerooms

    def sendMail(self, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.connect("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("zurichzimmergithub@gmail.com", "amyr8apm8cy3")
        msg = "Hello! There are the following free rooms at StudentVillage: \n" + message
        server.sendmail("zurichzimmergithub@gmail.com", self.targetemail, msg)

if __name__ == "__main__":
    monObj = Monitoring()

    while True:
        result = monObj.requestPage()
        freerooms = monObj.lookForFreeRooms(result)
        if len(freerooms) > 0:
            monObj.sendMail(freerooms)
        time.sleep(1200)
