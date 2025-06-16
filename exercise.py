from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
from requests.api import get
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import requests
import base64
import io
import os
import pymssql


conn = pymssql.connect(
    server="localhost\\SQLEXPRESS",  # 如果是命名實例，請改為 "localhost\SQLEXPRESS"
    user="your_username",  # 替換為你的 SQL Server 使用者名稱
    password="your_password",  # 替換為你的 SQL Server 密碼
    database="school"  # 確保資料庫名稱正確
)
cursor = conn.cursor()
sql = "INSERT INTO school (SD_number, sd_year, area, County, school, department, Permission, Zhentest, Determine, result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# 變數宣告
values = {
    "臺北市": "北部-台北考區", "臺灣": "北部-台北考區", "新北市": "北部-新北考區", "華僑": "北部-新北考區", "新竹市": "北部-新竹考區",
    "臺中市": "中部-台中考區", "中興大": "中部-台中考區", "明德": "中部-台中考區", "靜宜": "中部-台中考區", "弘文": "中部-台中考區",            "中興大": "中部-台中考區",
    "高雄市": "南部-高雄考區", "鳳新": "南部-高雄考區", "道明": "南部-高雄考區", "臺南市": "南部-台南考區", "家齊": "南部-台南考區",
    "長榮": "南部-台南考區", "成功大": "南部-台南考區", "新營": "南部-台南考區", "桃園市": "北部-桃園考區", "海洋": "北部-基隆考區",
    "基隆市": "北部-基隆考區", "中壢": "北部-中壢考區", "育達": "北部-中壢考區", "平鎮": "北部-中壢考區", "復旦": "北部-中壢考區",
    "彰化縣": "中部-彰化考區", "員林": "中部-彰化考區", "雲林縣": "中部-雲林考區", "虎尾": "中部-雲林考區", "苗栗縣": "中部-苗栗考區",
    "南投縣": "中部-南投考區", "中興高": "中部-南投考區", "屏東縣": "南部-屏東考區", "嘉義市": "南部-嘉義考區", "臺東縣": "東部-台東考區",
    "宜蘭縣": "東部-宜蘭考區", "花蓮縣": "東部-花蓮考區", "海星": "東部-花蓮考區", "金門縣": "離島-金門考區", "澎湖縣": "離島-澎湖考區",
    "連江縣": "離島-馬祖考區", "新竹縣": "北部-新竹考區"
}
countyLink = []  # all考區的url
areaLink = []  # 該考區的所有區域
examLink = []  # 試場的所有url
allArea = []  # 縣市名字
areaDict = {}  # 考區的字典
specials1 = ['原住民', '澎湖縣', '金門縣', '連江縣', '離島']
areaName = ''
compareArea = ''  # 比對用
flagNum = 0  # 紀錄現在到哪個縣市 12
compareNum = 0
temp = ''
# 資料所需
SD_number = 0
sd_year = 113
determine = 0
permission = ''  # 考生號碼
area = ''  # 區域 北中南東
zhentest = ''  # 備正
school = ''  # 校名
result = ''  # 結果
department = ''  # 系所
country = ''  # 考區
# 添加options不被偵測為機器人，有必要需要加上headers
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")
# 設定要進入的網頁
service = Service(ChromeDriverManager().install())  # 自動下載或使用現有的 ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

# 設定要進入的網頁
headerUrl = "https://www.com.tw/cross/"  # 開頭網址
url = "https://www.com.tw/cross/test_county113.html"  # 交叉查榜
driver.get(url)



def get_number(SD_number, imgUrl):  # 獲得應試號碼
    # driver.get(imgUrl)
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    #img = soup.find_all('img')[0].get('src')
    img = imgUrl
    img_data = img.split(",")[-1]
    binaryData = base64.b64decode(img_data)
    file_like = io.BytesIO(binaryData)
    image = Image.open(file_like)
    try:
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(image, config=custom_config)

    except:
        text = "無法判斷編號：{}".format(SD_number)
        image = image.save('{}.jpg'.format(SD_number))
    if '.' in text:
        text2 = text.split('.')[0]
    else:
        text2 = text.split('\n')[0]
    return text2


try:
    driver.get(url)
except Exception as e:
    while True:
        driver.refresh()
        print('連結錯誤重新連結', e)
        sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if(soup.find_all('div')):
            break
sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
while True:
    if soup.find_all('div'):
        break
    else:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
test = soup.find_all('td', id='countylist')
for i in test:  # 取得所有考區url
    for link in i.find_all('a'):
        countyLink.append(link['href'])
        allArea.append(link.text.split(u'(')[0].rstrip())

print("取得所有考區連結網址")
print(allArea)
print(countyLink)
for i in countyLink:
    if compareNum != flagNum:
        compareNum = compareNum + 1
        continue
    url = headerUrl + i
    try:
        driver.get(url)
    except Exception as e:
        while True:
            driver.refresh()
            print('連結錯誤重新連結', e)
            sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if(soup.find_all('div')):
                break
    sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    while True:
        if soup.find_all('div'):
            break
        else:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
    areaTable = soup.find_all('td', id='university_list_row_height')
    for area2 in areaTable:  # 所有試場Link有了
        for link in area2.find_all('a'):
            areaLink.append(link['href'])
            areaDict[link['href']] = link.text
    # print(soup)
    # print(areaDict)
    print("取得該區所有區域連結網址")
    print(areaLink)
    print(areaDict)
    print(allArea)
    for examArea in areaLink:
        areaName = areaDict[examArea]  # 我現在點進的學校
        print(areaName)
        url = headerUrl + examArea
        try:
            driver.get(url)
        except Exception as e:
            while True:
                driver.refresh()
                print('連結錯誤重新連結', e)
                sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if(soup.find_all('div')):
                    break
        sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        while True:
            if soup.find_all('div'):
                break
            else:
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
        examAreaTable = soup.find_all('table')
        for table in examAreaTable:
            for row in table.find_all('td', scope='row'):
                for rowLink in row.find_all('a'):
                    examLink.append(rowLink['href'])
        print("取得該區域所有試場連結網址")
        print(examLink)
##############上述結構都架好了只管以下你要做的(不過還不確定要稍微確認一下)#####################
# 可能要做字串比對，若考場不一致就直接跳出
        for info in examLink:  # 進入試場
            print('試場：', areaName)
            print('縣市：', allArea[flagNum])
            print('分類於：', values[allArea[flagNum]])
            area = values[allArea[flagNum]].split('-')[0]
            country = values[allArea[flagNum]].split('-')[1]
            url = headerUrl + info
            try:
                driver.get(url)
            except Exception as e:
                while True:
                    driver.refresh()
                    print('連結錯誤重新連結', e)
                    sleep(1)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    if(soup.find_all('div')):
                        break
            sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            while True:
                if soup.find_all('div'):
                    break
                else:
                    driver.get(url)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
            # 如果比對考區是對的就繼續爬、不對就跳到下一個
            for areaFlag in soup.find_all('td', colspan="6", scope='row'):
                for areaFlag2 in areaFlag.find_all('div'):
                    compareArea = areaFlag2.text
            if areaName in compareArea:
                print("考區：", compareArea, "\n爬取此區資料...")
                # 考生資料
                needInfo = soup.find('div', id='mainContent')
                infoTable = needInfo.find('tbody')
                for grayInfo in infoTable.find_all('tr', bgcolor='#DEDEDC'):  # 灰格
                    studentInfo = grayInfo.find_all('td')
                    for imagInfo in studentInfo[1].find_all('img'):  # 考生號碼
                        permission = get_number(SD_number, imagInfo['src'])
                        print("考生號碼：", permission)
                    for departmentTable in studentInfo[3].find_all('tbody'):
                        # 0 有無分發錄取 1 系所資料 2 二階甄試正備取
                        for departmentInfo in departmentTable.find_all('tr'):
                            departRow = departmentInfo.find_all('td')
                            # 0存放學校 1為系所
                            for departName in departRow[1].find_all('a'):
                                try:
                                    departmentName = departName.text.split(
                                        "\n")
                                    print(departmentName[0], departmentName[1])
                                except:
                                    if "學院" in departmentName[0]:
                                        departmentName = departmentName[0].split(
                                            "學院")
                                        departmentName[0] = departmentName[0] + "學院"
                                    elif "大學" in departmentName[0]:
                                        departmentName = departmentName[0].split(
                                            "大學")
                                        departmentName[0] = departmentName[0] + "大學"
                            school = departmentName[0]
                            department = departmentName[1]
                            # 處理正備取
                            # 還有特殊區域要處理
                            if departRow[2].find_all('div', 'red'):
                                for red in departRow[2].find_all('div', 'red'):
                                    zhentest = red.text
                                    result = '正取'
                                    if '-' in zhentest:
                                        temp = zhentest
                                        zhentest = zhentest.split('-')[1]
                                        for specLoop in specials1:
                                            if specLoop in temp:
                                                zhentest = '外加' + zhentest
                                                result = '外加正取'
                                                break
                                determine = 0
                            elif departRow[2].find_all('div', 'green'):
                                for green in departRow[2].find_all('div', 'green'):
                                    zhentest = green.text
                                    result = '備取'
                                    if '-' in zhentest:
                                        temp = zhentest
                                        zhentest = zhentest.split('-')[1]
                                        for specLoop in specials1:
                                            if specLoop in temp:
                                                zhentest = '外加' + zhentest
                                                result = '外加備取'
                                                break
                                determine = 0
                            else:
                                zhentest = '無'
                                result = '無'
                                determine = 2
                            # 有無分發錄取
                            for admission in departRow[0].find_all('img'):
                                print('錄取該系所')
                                determine = 1
                            print(list(permission))
                            print(
                                "permission:", permission, "\nschool:", school, "\ndepartment", department, "\narea:", area, "\ncountry:", country, "\nzhentest:", zhentest, "\ndetermine:", determine, "\nresult:", result
                            )
                            try:
                                cursor.execute("INSERT INTO crosscheck.dbo.[113Cross_check](SD_number, sd_year, area, County, school, department, Permission,Zhentest,Determine,result) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                    SD_number, str(sd_year), str(area), str(country), str(school), str(department), str(permission), str(zhentest), str(determine), str(result)))
                                conn.commit()
                            except Exception as e:
                                print('error:', e)
                            SD_number = SD_number + 1
                for whiteInfo in infoTable.find_all('tr', bgcolor='#FFFFFF'):  # 白格
                    studentInfo = whiteInfo.find_all('td')
                    for imagInfo in studentInfo[1].find_all('img'):  # 考生號碼
                        permission = get_number(SD_number, imagInfo['src'])
                        print("考生號碼：", permission)
                    for departmentTable in studentInfo[3].find_all('tbody'):
                        # 0 有無分發錄取 1 系所資料 2 二階甄試正備取
                        for departmentInfo in departmentTable.find_all('tr'):
                            departRow = departmentInfo.find_all('td')
                            # 0存放學校 1為系所
                            for departName in departRow[1].find_all('a'):
                                try:
                                    departmentName = departName.text.split(
                                        "\n")
                                    print(departmentName[0], departmentName[1])
                                except:
                                    if "學院" in departmentName[0]:
                                        departmentName = departmentName[0].split(
                                            "學院")
                                        departmentName[0] = departmentName[0] + "學院"
                                    elif "大學" in departmentName[0]:
                                        departmentName = departmentName[0].split(
                                            "大學")
                                        departmentName[0] = departmentName[0] + "大學"
                            school = departmentName[0]
                            department = departmentName[1]
                            # 處理正備取
                            # 還有特殊區域要處理
                            if departRow[2].find_all('div', 'red'):
                                for red in departRow[2].find_all('div', 'red'):
                                    zhentest = red.text
                                    result = '正取'
                                    if '-' in zhentest:
                                        temp = zhentest
                                        zhentest = zhentest.split('-')[1]
                                        for specLoop in specials1:
                                            if specLoop in temp:
                                                zhentest = '外加' + zhentest
                                                result = '外加正取'
                                                break
                                determine = 0
                            elif departRow[2].find_all('div', 'green'):
                                for green in departRow[2].find_all('div', 'green'):
                                    zhentest = green.text
                                    result = '備取'
                                    if '-' in zhentest:
                                        temp = zhentest
                                        zhentest = zhentest.split('-')[1]
                                        for specLoop in specials1:
                                            if specLoop in temp:
                                                zhentest = '外加' + zhentest
                                                result = '外加備取'
                                                break
                                determine = 0
                            else:
                                zhentest = '無'
                                result = '無'
                                determine = 2
                            # 有無分發錄取
                            for admission in departRow[0].find_all('img'):
                                print('錄取該系所')
                                determine = 1
                            print(list(permission))
                            print(
                                "permission:", permission, "\nschool:", school, "\ndepartment", department, "\narea:", area, "\ncountry:", country, "\nzhentest:", zhentest, "\ndetermine:", determine, "\nresult:", result
                            )
                            try:
                                cursor.execute("INSERT INTO crosscheck.dbo.[113Cross_check](SD_number, sd_year, area, County, school, department, Permission, Zhentest, Determine,result) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                    SD_number, str(sd_year), str(area), str(country), str(school), str(department), str(permission), str(zhentest), str(determine), str(result)))
                                conn.commit()
                            except Exception as e:
                                print('error:', e)
                            SD_number = SD_number + 1
            else:
                print("考區：", compareArea, "比對不符，跳過此區")
                continue
        print('該考區爬取完畢')
        examLink.clear()
    print("該縣市爬取成功，將相關存放Link的list清除")
    def clear(): return os.system('cls')  # 清除console
    clear()
    areaLink.clear()
    examLink.clear()
    areaDict.clear()
    flagNum = flagNum + 1
    compareNum = compareNum + 1
print('finish!')