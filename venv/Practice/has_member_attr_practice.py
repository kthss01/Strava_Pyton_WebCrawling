"""
    클래스내에서 멤버 변수 존재하는지 확인하는 테스트
"""


class Test:

    def __init__(self):
        if hasattr(self, 'x'):
            print('member is already find')

        self.x = 10

        if hasattr(self, 'x'):
            print('member is now find')


test = Test()