import threading
from tkinter import *

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

import time
import datetime



class App(threading.Thread):
    def __init__(self):
        super().__init__()
        self.opt = webdriver.ChromeOptions()
        self.opt.add_argument('window-size=800,600')
        self.driver = webdriver.Chrome(service=Service("./chromedriver.exe"), options=self.opt)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://ticket.interpark.com/Gate/TPLogin.asp"
        self.driver.get(self.url)
        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("인터파크 티케팅 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()

        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, width=40)
        self.id_entry.grid(row=1, column=1)
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, width=40)
        self.pw_entry.grid(row=2, column=1)
        self.login_button = Button(self.object_frame, text="Login", width=3, height=2, command=self.login_go)
        self.login_button.grid(row=3, column=1)
        self.showcode_label = Label(self.object_frame, text="공연번호")
        self.showcode_label.grid(row=4, column=0)
        self.showcode_entry = Entry(self.object_frame, width=40)
        self.showcode_entry.grid(row=4, column=1)
        
        self.birthcode_label = Label(self.object_frame, text="생년월일")
        self.birthcode_label.grid(row=5, column=0)
        self.birthcode_entry = Entry(self.object_frame, width=40)
        self.birthcode_entry.grid(row=5, column=1)
        
        self.completed_button = Button(self.object_frame, text="전체과정", width=6, height=2, command=self.completed_go)
        self.completed_button.grid(row=6, column=1)
        self.showcode_button = Button(self.object_frame, text="직링", width=6, height=2, command=self.link_go)
        self.showcode_button.grid(row=7, column=1)
    
        self.string_button = Button(self.object_frame, text="자동문자", width=6, height=2, command=self.string_go)
        self.string_button.grid(row=8, column=1)
        
        self.seat_button = Button(self.object_frame, text="좌석수", width=6, height=2, command=self.seat_go)
        self.seat_button.grid(row=9, column=1)
        
        self.dp.mainloop()


    def login_go(self):
        def task():
            self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))
            self.driver.find_element(By.NAME, 'userId').send_keys(self.id_entry.get())
            self.driver.find_element(By.ID, 'userPwd').send_keys(self.pw_entry.get())
            self.driver.find_element(By.ID, 'btn_login').click()

        newthread = threading.Thread(target=task)
        newthread.start()
        
        
        
    def completed_go(self):
        def task():
            
            def check_element_and_execute(driver, element_id, callback):
                try:
                    driver.find_element(By.ID, element_id)
                    callback()
                    return True
                except NoSuchElementException:
                    return False

            def action_if_ifrmSeat_found():
                # 'ifrmSeat'을 찾은 후에 실행할 코드를 여기에 작성하세요
                
                # 만약에 대기화면에서도 ifrmSeat가 있다면 제대로 작동하지 않게 됨. 대기화면엔 없고 본화면에 있는 걸 기다리는 것으로 바꿔야함.
                # 그럴 때는 일단 자동문자부터 차례로 눌러서 임시로 조치해야 함.
                self.driver.switch_to.frame('ifrmSeat')


                self.driver.execute_script("""
                    window.fnCheck = function() {
                        capchaHide();
                        j$(".capchaFloating").hide();
                        vCaptchaFailCnt=0;
                        document.getElementById("rcckYN").value="Y";
                        //j$(".validationTxt").removeClass("setTxt").addClass("ok");
                        if(SeatBuffer.index>0) {
                            fnSelect();
                        }
                    };
                """)

                self.driver.find_element(By.LINK_TEXT, '입력완료').click()
                self.driver.find_element(By.CSS_SELECTOR, 'a[sgn="일반석"]').click()

                elements = self.driver.find_elements(By.XPATH, '//img[@alt="자동배정"]')
                elements[1].click()  # index는 0부터 시작하므로 elements[1]이 두 번째 요소를 의미합니다.


                self.driver.switch_to.default_content()
                self.driver.switch_to.frame('ifrmBookStep')

                self.driver.find_element(By.NAME, 'SeatCount').click()
                self.driver.find_element(By.XPATH, '//option[@value="2"]').click()

                self.driver.switch_to.default_content()

                self.driver.find_element(By.ID, 'SmallNextBtnImage').click()

                self.driver.switch_to.frame('ifrmBookCertify')

                self.driver.find_element(By.ID, 'Agree').click()
                self.driver.find_element(By.XPATH, '//img[@alt="저장"]').click()

                self.driver.switch_to.default_content()

                elements = self.driver.find_elements(By.XPATH, '//img[@alt="다음단계"]')
                elements[1].click()  # index는 0부터 시작하므로 elements[1]이 두 번째 요소를 의미합니다.


                # 뜰 때까지 기다리는 코드 넣어야 하나?
                time.sleep(0.5)               

                self.driver.switch_to.frame('ifrmBookStep')
                self.driver.find_element(By.ID, 'Delivery').click()
                self.driver.find_element(By.ID, 'YYMMDD').send_keys(self.birthcode_entry.get())
                self.driver.switch_to.default_content()

                elements = self.driver.find_elements(By.XPATH, '//img[@alt="다음단계"]')
                elements[1].click()  # index는 0부터 시작하므로 elements[1]이 두 번째 요소를 의미합니다.

                

            def action_if_root_found():
                # 'root'를 찾은 후에 실행할 코드를 여기에 작성하세요
                if self.driver.current_url == 'https://ordo.interpark.com/block':
                    self.driver.get('http://poticket.interpark.com/SportsBook/BookSession.asp?GroupCode=' + self.showcode_entry.get())
                
                wait = WebDriverWait(self.driver, 500)
                wait.until(EC.presence_of_element_located((By.ID, "ifrmSeat")))
                
                action_if_ifrmSeat_found()
            
            
            # 시간을 체크하며 무한 루프 실행
            
            while True:
                # 현재 시간을 가져옴
                now = datetime.datetime.now()

                # 현재 시간의 초와 마이크로초를 합친 값이 59.8 이상인지 확인
                if now.second + now.microsecond/1e6 >= 59.8:
                    break

                # CPU 사용률을 낮추기 위해 약간의 대기 시간을 추가
                time.sleep(0.001)
            
            
            self.driver.get('https://ordo.interpark.com/wait?pid=' + self.showcode_entry.get() +
                            '&k=&t=&d=s&pmcode&genreCode&GroupCode=' + self.showcode_entry.get() +
                            '&Tiki=&Point=&PlayDate=&PlaySeq=&BizCode=&BizMemberCode=&OneStopInfo&Language')
            

            wait = WebDriverWait(self.driver, 500)

            wait.until(lambda driver: check_element_and_execute(self.driver, "ifrmSeat", action_if_ifrmSeat_found) or
                                      check_element_and_execute(self.driver, "root", action_if_root_found))
            
            
        newthread = threading.Thread(target=task)
        newthread.start()
        
        

    def link_go(self):
        def task():
            
            # 대기열 없을 때 주소
            self.driver.get('http://poticket.interpark.com/SportsBook/BookSession.asp?GroupCode=' + self.showcode_entry.get())
            
            # 대기열 있을 때 주소
            #self.driver.get('https://ordo.interpark.com/wait?pid=' + self.showcode_entry.get() +
            #                '&k=&t=&d=s&pmcode&genreCode&GroupCode=' + self.showcode_entry.get() +
            #                '&Tiki=&Point=&PlayDate=&PlaySeq=&BizCode=&BizMemberCode=&OneStopInfo&Language')

        newthread = threading.Thread(target=task)
        newthread.start()
        
        
    # 자동입력방지 문자 넘는 단계
    def string_go(self):
        def task():
            # 페이지 로딩을 기다린 후 fnCheck 함수를 변경합니다.

            self.driver.switch_to.frame("ifrmSeat")

            self.driver.execute_script("""
                window.fnCheck = function() {
                    capchaHide();
                    j$(".capchaFloating").hide();
                    vCaptchaFailCnt=0;
                    document.getElementById("rcckYN").value="Y";
                    //j$(".validationTxt").removeClass("setTxt").addClass("ok");
                    if(SeatBuffer.index>0) {
                        fnSelect();
                    }
                };
            """)
            
            self.driver.find_element(By.LINK_TEXT, '입력완료').click()
            self.driver.find_element(By.CSS_SELECTOR, 'a[sgn="일반석"]').click()
            
            elements = self.driver.find_elements(By.XPATH, '//img[@alt="자동배정"]')
            elements[1].click()  # index는 0부터 시작하므로 elements[1]이 두 번째 요소를 의미합니다.

        newthread = threading.Thread(target=task)
        newthread.start()

        
    # 좌석 수 선택
    def seat_go(self):
        def task():
            # 페이지 로딩을 기다린 후 fnCheck 함수를 변경합니다.
            
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('ifrmBookStep')
            
            self.driver.find_element(By.NAME, 'SeatCount').click()
            self.driver.find_element(By.XPATH, '//option[@value="2"]').click()
            
            self.driver.switch_to.default_content()
            
            self.driver.find_element(By.ID, 'SmallNextBtnImage').click()
            
            self.driver.switch_to.frame('ifrmBookCertify')
            
            self.driver.find_element(By.ID, 'Agree').click()
            self.driver.find_element(By.XPATH, '//img[@alt="저장"]').click()
            
            self.driver.switch_to.default_content()
            
            elements = self.driver.find_elements(By.XPATH, '//img[@alt="다음단계"]')
            elements[1].click()  # index는 0부터 시작하므로 elements[1]이 두 번째 요소를 의미합니다.

        newthread = threading.Thread(target=task)
        newthread.start()

        

app = App()
app.start()
