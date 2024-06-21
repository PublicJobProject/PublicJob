import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import CreateMonthFile
import ContentParsing
options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
class Scrap:
    def __init__(self):
        self.folderDate = CreateMonthFile.createFile()
        
        self.file_path = "C:/RPA/지자체 희망일자리/RPA 관리 리스트_한개시트.xlsx"
        self.df = self.read_df_file(self.file_path)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = options)
        self.driver.implicitly_wait(10)
        
        for item in range(len(self.df)):
            name = self.df.loc[item, '구청명']
            url = self.df.loc[item, '게시판 URL']
            GroupResult = self.dataCollect(url, item, name)
            print(GroupResult)

    def dataCollect(self, url, item, name):
        DataList = []

        검색어입력Xpath = self.df.loc[item, '검색어입력Xpath']
        클릭Xpath = self.df.loc[item, '클릭Xpath']
        게시물Xpath = self.df.loc[item, '게시물Xpath']
        검색어 = self.df.loc[item, '검색어']
        검색어List = 검색어.split(";")
        게시물_사업명Xpath = self.df.loc[item, '게시물_사업명Xpath']
        게시물_신청기간Xpath = self.df.loc[item, '게시물_신청기간Xpath']
        게시물_근무지Xpath = self.df.loc[item, '게시물_근무지Xpath']
        게시물_임금조건_보수_Xpath = self.df.loc[item, '게시물_임금조건(보수)Xpath']
        게시물_본문Xpath = self.df.loc[item, '게시물_본문Xpath']
        게시물_등록일Xpath = self.df.loc[item, '게시물_등록일Xpath']
        게시물_문의처Xpath = self.df.loc[item, '게시물_문의처Xpath']
        게시물목록Xpath = self.df.loc[item, '게시물목록Xpath']

        self.driver.get(url)
        for value in 검색어List:
            self.driver.find_element(By.XPATH, 검색어입력Xpath).clear()
            self.driver.find_element(By.XPATH, 검색어입력Xpath).send_keys(value)
            self.driver.find_element(By.XPATH, 클릭Xpath).click()

            for i in range(1, 11):
                TempList = []
                Modified게시물Xpath = 게시물Xpath.replace(";", str(i))
                try:
                    self.driver.find_element(By.XPATH, Modified게시물Xpath).click()
                except:
                    continue

                try:
                    본문GetText = self.driver.find_element(By.XPATH, 게시물_본문Xpath).text
                except:
                    pass
                businessName = self.get_element_text_or_none(게시물_사업명Xpath,'사업명',본문GetText) # 사업명 가져오기
                period = self.get_element_text_or_none(게시물_신청기간Xpath,'신청기간',본문GetText) # 신청기간 가져오기
                workPlace = self.get_element_text_or_none(게시물_근무지Xpath,'근무지',본문GetText) # 근무지 가져오기
                salary = self.get_element_text_or_none(게시물_임금조건_보수_Xpath,'임금조건',본문GetText) #임금조건 가져오기
                current_url = self.driver.current_url # 현재 페이지의 url 가져오기 
                contact = self.get_element_text_or_none(게시물_문의처Xpath,'문의처',본문GetText) # 문의처 가져오기
                registDate = self.get_element_text_or_none(게시물_등록일Xpath,'등록일',본문GetText)
                TempList.extend([name, businessName, period, workPlace, salary, current_url, registDate, contact])
                DataList.append(TempList)
                for i in range(3):
                    try:
                        self.driver.find_element(By.XPATH, 게시물목록Xpath).click()
                    except:
                        continue
                    try:
                        GetText = self.get_element_text_or_none(Modified게시물Xpath) # 목록 버튼 클릭
                    except:
                        continue    
                    if GetText != "":
                        print("목록 버튼 클릭 성공")
                        break
        self.make_df_file(DataList)

    def get_element_text_or_none(self, xpath,columnName,mainText):
        #text = None
        try:
            text = self.driver.find_element(By.XPATH, xpath).text
        except :
            # 수집할 데이터 없을 시 본문에서 데이터 파싱하기
            ContentParsing.contentParse(mainText,columnName)
        return text

    def read_df_file(self, file_path):
        df = pd.read_excel(file_path)
        return df

    def make_df_file(self, DataList):
        tempcolumns = ['구분', '사업명', '신청기간', '근무지', '임금조건(보수)', 'URL', '등록일', '문의전화']
        tempdf = pd.DataFrame(DataList, columns=tempcolumns)
        #totaldf = pd.concat([self.df, tempdf], axis=1)
        print(tempdf)
        
        tempdf.to_excel(f'C:/RPA/지자체 희망일자리/{self.folderDate}/{self.folderDate}.xlsx',index=False)
        tempdf.to_csv(f'C:/RPA/지자체 희망일자리/{self.folderDate}/{self.folderDate}.csv',index=False)

    def __del__(self):
        self.driver.quit()

if __name__ == "__main__":
    Jobs = Scrap()
