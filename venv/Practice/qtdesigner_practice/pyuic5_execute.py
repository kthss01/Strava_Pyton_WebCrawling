"""
QtDesigner로 작업한 ui 파일을 py 파일로 변환

pyuic5 사용
    pyuic5 -x "login.ui" -o "login.py"
    이와 같은 방법으로 .ui -> .py로 변경

subprocess 이용하여 코드상에서 새로운 프로세스 실행
"""
import subprocess

subprocess.run('pyuic5 -x "login.ui" -o "login.py"')

