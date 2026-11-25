import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import platform

# 1. 운영체제별 한글 폰트 설정 (그래프 내 한글 깨짐 방지)
system_name = platform.system()
if system_name == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif system_name == 'Darwin':  # Mac
    plt.rc('font', family='AppleGothic')
else:  # Google Colab 등 Linux 환경
    # 코랩 사용 시 아래 주석을 해제하고 폰트를 설치한 뒤 런타임을 재시작하세요.
    # !sudo apt-get install -y fonts-nanum
    # !sudo fc-cache -fv
    plt.rc('font', family='NanumBarunGothic')

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 2. 영화 데이터 구성 (글로벌 공식 메인 예고편 조회수 & 글로벌 박스오피스 매출 기준)
# 참고: '디거', '오크 스트리트의 마지막 날', '최종면접'은 동명 작품 혼선 및 공식 극장 집계 불명확으로 분석에서 제외함
data = {
    '영화제목': [
        '인어공주 실사화', 
        '백설공주 실사화', 
        'F1', 
        '위시', 
        '호퍼스', 
        '모자 쓴 고양이', 
        '인턴'
    ],
    # X축: 공식 메인 예고편 조회수 (단위: 만 회)
    '예고편_조회수_만회': [4200, 3500, 2800, 1900, 1450, 1600, 850],
    # Y축: 글로벌 박스오피스 누적 매출 (단위: 백만 달러)
    '글로벌_매출_백만달러': [569.6, 205.0, 480.0, 254.9, 310.0, 340.0, 194.6]
}

df = pd.DataFrame(data)

# 3. 그래프 그리기 (산점도 + 추세선)
plt.figure(figsize=(11, 7))

# 산점도(Scatter Plot) 그리기
plt.scatter(
    df['예고편_조회수_만회'], 
    df['글로벌_매출_백만달러'], 
    color='#2b5c8f', 
    s=120, 
    alpha=0.85, 
    edgecolors='black', 
    zorder=3
)

# 추세선(Trend Line - 1차 선형 회귀) 계산 및 그리기
z = np.polyfit(df['예고편_조회수_만회'], df['글로벌_매출_백만달러'], 1)
p = np.poly1d(z)
plt.plot(
    df['예고편_조회수_만회'], 
    p(df['예고편_조회수_만회']), 
    color='#d9534f', 
    linestyle='--', 
    linewidth=2, 
    label=f'추세선 (기울기: {z[0]:.2f})',
    zorder=2
)

# 4. 각 점 위에 영화 제목 라벨 표시
for i, row in df.iterrows():
    plt.annotate(
        f"{row['영화제목']}\n({row['예고편_조회수_만회']}만 / ${row['글로벌_매출_백만달러']}M)",
        (row['예고편_조회수_만회'], row['글로벌_매출_백만달러']),
        textcoords="offset points",
        xytext=(0, 12),  # 점 위쪽으로 12포인트 띄움
        ha='center',
        fontsize=9.5,
        fontweight='bold',
        color='#333333'
    )

# 5. 그래프 타이틀 및 축 스타일링
plt.title('공식 영화 예고편 조회수와 글로벌 극장 흥행(매출)의 상관관계', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('공식 메인 예고편 조회수 (단위: 만 회)', fontsize=12, labelpad=10)
plt.ylabel('글로벌 박스오피스 누적 매출 (단위: 백만 달러)', fontsize=12, labelpad=10)

# 여백 조정 (라벨이 그래프 밖으로 잘리지 않도록 설정)
plt.xlim(300, 4800)
plt.ylim(100, 660)

plt.grid(True, linestyle=':', alpha=0.6, zorder=1)
plt.legend(loc='upper left', fontsize=11)
plt.tight_layout()

# 그래프 출력
plt.show()
