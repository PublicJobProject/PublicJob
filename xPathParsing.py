import re
def xPathParse(xPath):
    # iframe 제거한 내용을 추출
    xPathPattern = r'<xPath>(.*?)</xPath>'
    xPathmatches = re.findall(xPathPattern, xPath, re.DOTALL)
    
    #세미콜론 숫자 확인
    indexPattern = r';'
    indexList = re.findall(indexPattern, xPath)

    #세미콜론이 2개 이상이면
    if len(indexList) > 1:
        divisionPattern = r';(\d+);?(\d+)?'
        divisionMatch = re.search(divisionPattern, xPath)
        
        if divisionMatch:
            # 문자열 패턴으로 2번째 세미콜론 숫자와 3번째 세미콜론 숫자 추출
            secondNumber = divisionMatch.group(1)
            thirdNumber = divisionMatch.group(2) if divisionMatch.group(2) else None
            
            # 2번째 세미콜론 숫자만 있는 경우
            FullxPathmatches = [match + ";" + secondNumber for match in xPathmatches]
            
            # 2번째와 3번째 세미콜론 숫자 모두 존재하는 경우
            if thirdNumber:
                FullxPathmatches = [match + ";" + thirdNumber for match in FullxPathmatches]
            
            # 리스트를 문자열로 결합
            FullxPathmatches = ''.join(FullxPathmatches)
            print(FullxPathmatches)
            return FullxPathmatches
        
    elif len(indexList) == 0 or len(indexList) == 1:
        FullxPathmatches = ''.join(xPathmatches)
        print(FullxPathmatches)
        return FullxPathmatches