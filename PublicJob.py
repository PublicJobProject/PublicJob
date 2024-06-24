import pandas as pd  # Pandas 라이브러리 import
from selenium import webdriver  # Selenium에서 웹 드라이버 import
from selenium.webdriver import ChromeOptions  # Chrome 옵션 설정을 위한 import
from selenium.webdriver.chrome.service import Service as ChromeService  # Chrome 드라이버 서비스 설정을 위한 import
from webdriver_manager.chrome import ChromeDriverManager  # Chrome 드라이버 관리자 import
# from selenium.common.exceptions import WebDriverException, TimeoutException
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import CreateMonthFile  # 사용자 정의 모듈 import
import ContentParsing  # 사용자 정의 모듈 import
import time  # 시간 지연을 위한 import

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Selenium 자동화 방지 설정

class Scrap:
    def __init__(self):
        self.folderDate = CreateMonthFile.createFile()  # 폴더 생성 날짜 지정
        self.file_path = "C:/RPA/지자체 희망일자리/RPA 관리 리스트_한개시트.xlsx"  # 파일 경로 지정
        self.df = self.read_df_file(self.file_path)  # Excel 파일을 DataFrame으로 읽어오는 함수 호출
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)  # Chrome 웹 드라이버 설정
        self.driver.implicitly_wait(10)  # 웹 요소를 찾기 위한 암묵적 대기 시간 설정
        
        for item in range(len(self.df)):
            name = self.df.loc[item, '구청명']  # DataFrame에서 '구청명' 가져오기
            url = self.df.loc[item, '게시판 URL']  # DataFrame에서 '게시판 URL' 가져오기
            success = self.df.loc[item, '성공여부'] # DataFrame에서 '성공여부' 가져오기
            if success == "O":
                continue
            for i in range(3):
                GroupResult = self.dataCollect(url, item, name)  # 데이터 수집 함수 호출
                if GroupResult == "성공":
                    break
            #print(GroupResult)  # 그룹 결과 출력

    def dataCollect(self, url, item, name):
        DataList = []  # 데이터 저장을 위한 리스트 초기화
        검색어입력Xpath = self.df.loc[item, '검색어입력Xpath']  # DataFrame에서 '검색어입력Xpath' 가져오기
        클릭Xpath = self.df.loc[item, '클릭Xpath']  # DataFrame에서 '클릭Xpath' 가져오기
        게시물Xpath = self.df.loc[item, '게시물Xpath']  # DataFrame에서 '게시물Xpath' 가져오기
        검색어 = self.df.loc[item, '검색어']  # DataFrame에서 '검색어' 가져오기
        검색어List = 검색어.split(";")  # ';'을 기준으로 검색어를 리스트로 변환
        
        # DataFrame에서 각 항목의 XPath 가져오기
        게시물_사업명Xpath = self.df.loc[item, '게시물_사업명Xpath']
        게시물_신청기간Xpath = self.df.loc[item, '게시물_신청기간Xpath']
        게시물_근무지Xpath = self.df.loc[item, '게시물_근무지Xpath']
        게시물_임금조건_보수_Xpath = self.df.loc[item, '게시물_임금조건(보수)Xpath']
        게시물_본문Xpath = self.df.loc[item, '게시물_본문Xpath']
        게시물_등록일Xpath = self.df.loc[item, '게시물_등록일Xpath']
        게시물_문의처Xpath = self.df.loc[item, '게시물_문의처Xpath']
        게시물목록Xpath = self.df.loc[item, '게시물목록Xpath']

        a = self.driver.get(url)  # 주어진 URL로 이동

        for value in 검색어List:
            self.driver.find_element(By.XPATH, 검색어입력Xpath).clear()  # 검색어 입력란 초기화
            self.driver.find_element(By.XPATH, 검색어입력Xpath).send_keys(value)  # 검색어 입력
            self.driver.find_element(By.XPATH, 클릭Xpath).click()  # 검색 버튼 클릭

            for i in range(1, 11):
                TempList = []  # 임시 리스트 초기화
                Modified게시물Xpath = 게시물Xpath.replace(";", str(i))  # 게시물 XPath의 ';'를 숫자로 대체
                
                TempList = []
                Modified게시물Xpath = 게시물Xpath.replace(";", str(i))
                print("="*50)
                print(f"{name} : [{value}] 검색어의 {i}번째 게시물 입니다")
                try:
                    self.driver.find_element(By.XPATH, Modified게시물Xpath).click()  # 게시물 클릭 시도
                except:
                    continue  # 실패 시 다음 반복으로 넘어감

                try:
                    본문GetText = self.driver.find_element(By.XPATH, 게시물_본문Xpath).text  # 게시물 본문 텍스트 가져오기
                except:
                    pass  # 실패 시 아무 작업도 하지 않음
                
                # 각 항목의 데이터 가져오기 시도 및 실패 시 재시도
                for i in range(3):
                    businessName = self.get_element_text_or_none(게시물_사업명Xpath, '사업명', 본문GetText) # 사업명 가져오기
                    if businessName == None:
                        time.sleep(0.5)
                    else:
                        break
                for i in range(3):
                    period = self.get_element_text_or_none(게시물_신청기간Xpath, '신청기간', 본문GetText) # 신청기간 가져오기
                    if period == None:
                        time.sleep(0.5)
                    else:
                        break
                for i in range(3):
                    workPlace = self.get_element_text_or_none(게시물_근무지Xpath, '근무지', 본문GetText) # 근무지 가져오기
                    if workPlace == None:
                        time.sleep(0.5)
                    else:
                        break
                for i in range(3):
                    salary = self.get_element_text_or_none(게시물_임금조건_보수_Xpath, '임금조건', 본문GetText) # 임금조건 가져오기
                    if salary == None:
                        time.sleep(0.5)
                    else:
                        break
                current_url = self.driver.current_url  # 현재 페이지의 URL 가져오기
                for i in range(3):
                    contact = self.get_element_text_or_none(게시물_문의처Xpath, '문의처', 본문GetText) # 문의처 가져오기
                    if contact == None:
                        time.sleep(0.5)
                    else:
                        break
                for i in range(3):
                    registDate = self.get_element_text_or_none(게시물_등록일Xpath, '등록일', 본문GetText) # 등록일 가져오기
                    if registDate == None:
                        time.sleep(0.5)
                    else:
                        break
                
                # 임시 리스트에 데이터 추가
                TempList.extend([name, businessName, period, workPlace, salary, current_url, registDate, contact])
                DataList.append(TempList)  # 결과 리스트에 임시 리스트 추가
                
                # 게시물 목록으로 돌아가기 시도 (예외처리)
                for i in range(3):
                    try:
                        self.driver.find_element(By.XPATH, 게시물목록Xpath).click() # 목록 버튼 클릭
                    except:
                        continue
                    try:
                        GetText = self.driver.find_element(By.XPATH, Modified게시물Xpath).text # 목록 버튼 클릭 성공 여부 확인을 위해 메인화면 게시물 텍스트 수집
                    except:
                        continue
                    if GetText != None:
                        print("목록 버튼 클릭 성공")
                        break

        self.make_df_file(DataList)  # DataFrame으로 변환하여 파일로 저장
        return "성공" 

    def get_element_text_or_none(self, xpath, columnName, mainText):
        try:
            text = self.driver.find_element(By.XPATH, xpath).text  # 웹 요소에서 텍스트 가져오기 시도
        except:
            text = ContentParsing.contentParse(mainText, columnName)  # 실패 시 본문에서 데이터 파싱하기
        return text  # 가져온 텍스트 또는 파싱한 결과 반환

    def read_df_file(self, file_path):
        df = pd.read_excel(file_path)  # Excel 파일을 DataFrame으로 읽어오기
        return df  # DataFrame 반환

    def make_df_file(self, DataList):
        tempcolumns = ['구분', '사업명', '신청기간', '근무지', '임금조건(보수)', 'URL', '등록일', '문의전화'] # 열이름을 리스트에 저장
        tempdf = pd.DataFrame(DataList, columns=tempcolumns) # 데이터 리스트를 DataFrame으로 변환
        #totaldf = pd.concat([self.df, tempdf], axis=1)
        print(tempdf)
        
        # DataFrame을 지정된 폴더 경로에 엑셀 및 CSV 파일로 저장
        tempdf.to_excel(f'C:/RPA/지자체 희망일자리/{self.folderDate}/{self.folderDate}.xlsx',index=False)
        #tempdf.to_csv(f'C:/RPA/지자체 희망일자리/{self.folderDate}/{self.folderDate}.csv',index=False)

    def __del__(self):
        self.driver.quit() # 드라이버 종료

if __name__ == "__main__":
    Jobs = Scrap() # Scrap 클래스의 인스턴스를 생성하여 실행합니다.