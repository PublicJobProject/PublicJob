import re

def contentParse(contentData, notFoundValue):
    #print(contentData, notFoundValue)
    # 조건들을 동적으로 설정
    if notFoundValue == '신청기간':
        conditions = ["접수기간", "신청기간", "근로기간", "원서접수", "공고기간", "모집기간", "접수일시", "접수기간 :", "원서접수 기간 :", "채용공고 기간 :", "제출 마감기한 :", "서류접수:", "공고(접수)기간", "기 간", "기    간"]
    elif notFoundValue == '사업명':
        conditions = ["사업명"]
    elif notFoundValue == '근무지':
        conditions = ["근무지", "근무장소", "근 무 처 :", "근 무 지"]
    elif notFoundValue == '임금조건':
        conditions = ["임금조건(보수)", "급여:", "보수", "일 급", "보수수준 :", "보 수 :", "급여내용:", "인부임", "보 수:", "보수수준", "임금조건"]
    elif notFoundValue == '등록일':
        conditions = ["등록일"]
    elif notFoundValue == '문의처':
        conditions = ["전화", "문 의 처", "☎", "문의", "문의처", "문 의 :", "문의 :", "기타 문의사항 :", "문의전화 :", "연 락 처:", "문의사항:"]
    else:
        return None  # 처리할 수 없는 값이 들어왔을 경우 None 반환

    # 텍스트를 줄 단위로 분할하여 처리
    lines = contentData.split('\n')

    # 각 조건들을 포함하는 첫 번째 줄을 찾음
    resultLine = None

    # 신청기간 또는 등록일일 경우
    if notFoundValue == '신청기간' or notFoundValue == '등록일':
        for line in lines:
            for cond in conditions:
                if cond in line:
                    # 해당 줄에서 조건 부분을 제외한 내용을 추출
                    extractedText = line.replace(cond, '').strip()
                    
                    # 숫자를 포함하고 있는지 확인
                    if sum(char.isdigit() for char in extractedText) >= 4:
                        resultLine = extractedText
                        break  # 첫 번째 매칭된 줄을 찾으면 더 이상 검사하지 않음
            if resultLine is not None:
                break  # 외부 루프 종료
    else:
        # 신청기간 또는 등록일이 아닌 경우
        for line in lines:
            for cond in conditions:
                if cond in line:
                    resultLine = line.replace(cond, '').strip()
                    break  # 첫 번째 매칭된 줄을 찾으면 더 이상 검사하지 않음
            if resultLine is not None:
                break  # 외부 루프 종료
    
    return resultLine

    #print(ad)