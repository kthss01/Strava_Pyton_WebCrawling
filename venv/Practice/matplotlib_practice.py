"""
데이터 시각화하기 matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np

# figure, 즉 그래프를 표현할 액자를 먼저 만든다.
plt.figure()  # 안써도 되는 거 같음

x = np.arange(0, 5)
y = x ** 2

# plt.plot(x, y)
plt.bar(x, y)

# figure를 출력한다.
plt.show()
# figure 저장
# plt.savefig('plotting.png')