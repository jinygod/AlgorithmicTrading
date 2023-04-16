import win32com.client
import pythoncom

# COM 객체를 사용하기 위해 초기화
pythoncom.CoInitialize()

# CpUtil.CpCybos 클래스 객체 생성
try:
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
except Exception as ex:
    print("Exception Occured : ", ex)
