import time
import ctypes

# 절전 모드 방지
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_AWAYMODE_REQUIRED = 0x00000040

def prevent_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED)

def allow_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

if __name__ == "__main__":
    print("Preventing sleep mode")
    prevent_sleep()
    time.sleep(60)  # 시스템이 절전 모드로 가지 않도록 60초 동안 대기
    print("Allowing sleep mode")
    allow_sleep()
