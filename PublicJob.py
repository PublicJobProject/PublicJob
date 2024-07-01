import pandas as pd  # Pandas 라이브러리 import
from selenium import webdriver  # Selenium에서 웹 드라이버 import
from selenium.webdriver import ChromeOptions  # Chrome 옵션 설정을 위한 import
from selenium.webdriver.chrome.service import Service as ChromeService  # Chrome 드라이버 서비스 설정을 위한 import
from webdriver_manager.chrome import ChromeDriverManager  # Chrome 드라이버 관리자 import
from selenium.webdriver.common.by import By  # 웹 요소 검색을 위한 By import
import CreateMonthFile  # 사용자 정의 모듈 import
import ContentParsing  # 사용자 정의 모듈 import
import time  # 시간 지연을 위한 import
import StyleSetting
import xPathParsing

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Selenium 자동화 방지 설정

class Scrap:
    def __init__(self):
        self.DataList = []  # 데이터 저장을 위한 리스트 초기화

        self.folderDate = CreateMonthFile.createFile()  # 폴더 생성 날짜 지정
        self.file_path = "C:/RPA/지자체 희망일자리/RPA 관리 리스트_한개시트.xlsx"  # 파일 경로 지정
        self.df = self.read_df_file(self.file_path)  # Excel 파일을 DataFrame으로 읽어오는 함수 호출
        self.result_file_path = f'C:/RPA/지자체 희망일자리/{self.folderDate}/{self.folderDate}.xlsx'  # 결과 파일 경로 지정
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)  # Chrome 웹 드라이버 설정
        self.driver.implicitly_wait(10)  # 웹 요소를 찾기 위한 암묵적 대기 시간 설정

        for item in range(len(self.df)):
            name = self.df.loc[item, '구청명']
            url = self.df.loc[item, '게시판 URL']
            success = self.df.loc[item, '성공여부']
            if success == "O":
                continue
            for i in range(3):
                GroupResult = self.dataCollect(url, item, name)
                if GroupResult == "성공":
                    self.df.loc[item, '성공여부'] = "O"
                    break
                else:
                    print(f"X: {GroupResult}")
                    self.df.loc[item, '성공여부'] = f"X: {GroupResult}"
            
            self.df.to_excel(self.file_path, index=False)
            StyleSetting.styleSet(self.file_path, self.df)

    def dataCollect(self, url, item, name):
        self.driver.get(url)  # 주어진 URL로 이동
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

        # xPath에 iframe이 포함되어 있는지 확인
        xPathPattern = '<xPath>'
        xPathmatch = False # False로 초기화
        
        if  xPathPattern in 검색어입력Xpath:
            xPathmatch = True
            
        # iframe 이포함되어 있다면 모든 엑스페스 전부 ifrmae 벗기기
        if xPathmatch:
            검색어입력Xpath = xPathParsing.xPathParse(검색어입력Xpath)
            클릭Xpath = xPathParsing.xPathParse(클릭Xpath)
            게시물Xpath = xPathParsing.xPathParse(게시물Xpath)
            게시물_사업명Xpath = xPathParsing.xPathParse(게시물_사업명Xpath)
            게시물_신청기간Xpath = xPathParsing.xPathParse(게시물_신청기간Xpath)
            게시물_근무지Xpath = xPathParsing.xPathParse(게시물_근무지Xpath)
            게시물_임금조건_보수_Xpath = xPathParsing.xPathParse(게시물_임금조건_보수_Xpath)
            게시물_본문Xpath = xPathParsing.xPathParse(게시물_본문Xpath)
            게시물_등록일Xpath = xPathParsing.xPathParse(게시물_등록일Xpath)
            게시물_문의처Xpath = xPathParsing.xPathParse(게시물_문의처Xpath)
            게시물목록Xpath = xPathParsing.xPathParse(게시물목록Xpath)
            
            # iframe 스위치 하기 switch()

            try:
                iframe = self.driver.find_element(By.TAG_NAME, 'iframe')
                self.driver.switch_to.frame(iframe)
            except:
                return "iframe 전환 실패"
        
        for value in 검색어List:
            try:
                getText = ""
                for i in range(3):
                    self.driver.find_element(By.XPATH, 검색어입력Xpath).clear()  # 검색어 입력란 초기화
                    getText = self.driver.find_element(By.XPATH, 검색어입력Xpath).get_attribute("value")
                    if getText == "":
                        break
            except:
                return "검색어입력Xpath를 찾을 수 없습니다"

            try:
                for i in range(3):
                    self.driver.find_element(By.XPATH, 검색어입력Xpath).send_keys(value)  # 검색어 입력
                    self.driver.find_element(By.XPATH, 클릭Xpath).click()
                    getText = self.driver.find_element(By.XPATH, 검색어입력Xpath).get_attribute("value")
                    if getText == value:
                        break
            except:
                return "검색어 입력 실패"

            for i in range(1, 2):
                TempList = []  # 임시 리스트 초기화
                Modified게시물Xpath = 게시물Xpath.replace(";", str(i))  # 게시물 XPath의 ';'를 숫자로 대체

                TempList = []
                Modified게시물Xpath = 게시물Xpath.replace(";", str(i))
                print("="*50)
                print(f"{name} : [{value}] 검색어의 {i}번째 게시물 입니다")
                try:  # 게시물 클릭
                    for i in range(3):
                        self.driver.find_element(By.XPATH, Modified게시물Xpath).click()  # 게시물 클릭 시도
                        getText = self.driver.find_element(By.XPATH, 게시물_본문Xpath).text
                        if getText != "":
                            break
                except:
                    return "Modified게시물Xpath를 찾을 수 없습니다."

                try:
                    for i in range(3):
                        본문GetText = self.driver.find_element(By.XPATH, 게시물_본문Xpath).text  # 게시물 본문 텍스트 가져오기
                        if 본문GetText != "":
                            break
                except:
                    return "본문 가져오기 실패"

                # 수집할 정보 가져오기
                businessName = self.get_element_text_or_none(게시물_사업명Xpath, '사업명', 본문GetText)  # 사업명 가져오기
                period = self.get_element_text_or_none(게시물_신청기간Xpath, '신청기간', 본문GetText)  # 신청기간 가져오기
                workPlace = self.get_element_text_or_none(게시물_근무지Xpath, '근무지', 본문GetText)  # 근무지 가져오기
                salary = self.get_element_text_or_none(게시물_임금조건_보수_Xpath, '임금조건', 본문GetText)  # 임금조건 가져오기
                current_url = self.driver.current_url  # 현재 페이지의 URL 가져오기
                contact = self.get_element_text_or_none(게시물_문의처Xpath, '문의처', 본문GetText)  # 문의처 가져오기
                registDate = self.get_element_text_or_none(게시물_등록일Xpath, '등록일', 본문GetText)  # 등록일 가져오기

                # 임시 리스트에 데이터 추가
                TempList.extend([name, businessName, period, workPlace, salary, current_url, registDate, contact])
                self.DataList.append(TempList)  # 결과 리스트에 임시 리스트 추가

                # 게시물 목록으로 돌아가기 시도 (예외처리)
                try:
                    for i in range(3):
                        self.driver.find_element(By.XPATH, 게시물목록Xpath).click()  # 목록 버튼 클릭
                        GetText = 게시물Xpath.replace(";", "6")
                        if GetText is not None:
                            print("목록 버튼 클릭 성공")
                            break
                except:
                    return "목록 버튼 클릭 실패"

        self.make_df_file(self.DataList)  # DataFrame으로 변환하여 파일로 저장
        self.driver.switch_to.default_content()
        self.driver.switch_to.default_content()
        return "성공"

    def get_element_text_or_none(self, xpath, columnName, mainText):
        for i in range(3):
            try:
                text = self.driver.find_element(By.XPATH, xpath).text  # 웹 요소에서 텍스트 가져오기 시도
            except:
                text = ContentParsing.contentParse(mainText, columnName)  # 실패 시 본문에서 데이터 파싱하기
            if text is None:
                time.sleep(0.5)
            else:
                return text  # 가져온 텍스트 또는 파싱한 결과 반환

    def read_df_file(self, file_path):  # 주어진 파일 경로에서 엑셀 파일을 읽어와 DataFrame으로 반환합니다.
        df = pd.read_excel(file_path)
        return df

    def make_df_file(self, DataList):  # 주어진 데이터 리스트를 DataFrame으로 변환한 후 지정된 경로에 엑셀 파일로 저장합니다.
        tempcolumns = ['구분', '사업명', '신청기간', '근무지', '임금조건(보수)', 'URL', '등록일', '문의전화']  # 열 이름 설정
        tempdf = pd.DataFrame(DataList, columns=tempcolumns)  # 데이터 리스트를 DataFrame으로 변환
        print(tempdf)  # 변환된 DataFrame 출력

        # 기존 파일이 존재하는 경우 기존 데이터와 병합
        try:
            existing_df = pd.read_excel(self.result_file_path)
            combined_df = pd.concat([existing_df, tempdf], ignore_index=True).drop_duplicates()
        except FileNotFoundError:
            combined_df = tempdf

        # DataFrame을 엑셀 파일로 저장
        combined_df.to_excel(self.result_file_path, index=False)

        # 스타일 설정
        StyleSetting.styleSet(self.result_file_path, combined_df)

    def __del__(self):  # Scrap 클래스가 삭제될 때 웹 드라이버를 종료합니다.
        self.driver.quit()

if __name__ == "__main__":
    Jobs = Scrap()  # Scrap 클래스의 인스턴스를 생성하여 실행합니다.