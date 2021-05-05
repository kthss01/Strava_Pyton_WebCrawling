"""
QtDesigner로 작업한 ui 파일을 py 파일로 변환

pyuic5 사용
    pyuic5 -x "login.ui" -o "login.py"
    이와 같은 방법으로 .ui -> .py로 변경

subprocess 이용하여 코드상에서 새로운 프로세스 실행

이거 말고도 리소드를 사용하는 경우
리소드도 하나 파이썬 코드로 만들어주어야하는 거 같음
pyrcc4 '리소스명.qrc' -o '리소스명_rc.py' -py3
"""
import subprocess

# subprocess.run('pyuic5 -x "login.ui" -o "login.py"')

subprocess.run('pyuic5 -x "strava.ui" -o "strava.py"')
subprocess.run('pyrcc5 "../../Resources/myres.qrc" -o "myres_rc.py"')

