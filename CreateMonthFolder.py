import os
from datetime import datetime



def CreateFolder():
    # 현재 날짜를 YYYY-MM 형식으로 변환
    current_date = datetime.now().strftime("%Y-%m")

    # 기본 폴더 경로 설정
    base_path = "C:/RPA/지자체 희망일자리"
    folder_path = os.path.join(base_path, current_date)

    # RPA 폴더가 존재하지 않으면 오류 반환
    if not os.path.exists("C:/RPA"):
        Msg = "RPA 폴더가 존재하지 않습니다."
        print(Msg)
        return Msg

    # 지자체 희망일자리 폴더가 존재하지 않으면 오류 반환
    if not os.path.exists(base_path):
        Msg = "지자체 희망일자리 폴더가 존재하지 않습니다."
        print(Msg)
        return Msg

    # 날짜 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        Msg = "성공"
        print(Msg)
    else:
        Msg = "성공"
        print(Msg)

    return current_date

#CreateFolder()