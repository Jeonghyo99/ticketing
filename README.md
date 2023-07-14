# ticketing

## selenium 설치
'''
pip install selenium
'''

## 공연번호 알기
예매 대상 경기 목록에서 개발자 도구에서 stresscount 찾으면 됨.

## AWS 서버시간으로 맞추기
명령 프롬프트 관리자 권한으로 실행하여
'''
net start w32time
'''
'''
w32tm /config /manualpeerlist:169.254.169.123 /syncfromflags:manual /update
'''
실행 후
'''
w32tm /query /configuration
'''
실행해서 169.254.169.123 확인하기
