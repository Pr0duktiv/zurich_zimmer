from lxml import html
import requests

class Monitoring:
    url = 'http://studentvillage.ch/unterkunfte/'
    treepath = '//table[@class="wohnen_table type_is_all"]/tbody/tr'
    limitprice = 1000

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
        for element in tablecontent:
            totalprice = int(element[4][4:-2])
            occupation = element[7]
            #status = "Reserviert"
            status = "Verfügbar"
            if occupation == status and totalprice <= self.limitprice:
                print(element[len(element)-1])

    def sendMail(self):
        print("Sending Application")

if __name__ == "__main__":
    monObj = Monitoring()
    result = monObj.requestPage()
    monObj.lookForFreeRooms(result)
