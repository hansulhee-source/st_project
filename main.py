
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 예고편 조회수 분석",
    page_icon="🎬",
    layout="wide"
)

# 제목
st.title("🎬 영화 예고편 조회수가 실제 관객수에 미치는 영향")
st.write("영화 예고편 조회수와 실제 영화 관객수 사이의 관계를 분석합니다.")

st.info("※ 관객수는 만 명 단위이며, 일부 수치는 반올림한 값입니다.")

# 1. 데이터 만들기
data = {
    "영화 제목": [
        "최종면접",
        "오크 스트리트의 마지막 날",
        "인어공주",
        "백설공주",
        "위시",
        "인턴",
        "F1 더 무비",
        "디거",
        "모자 쓴 고양이"
    ],

    "예고편 조회수": [
        166, 13, 202, 100, 156,
        385, 208, 410, 170
    ],

    "실제 관객수": [
        32.8, 13.5, 64.4, 19, 140,
        92, 521.3, 10.8, 6.7
    ]
}

df = pd.DataFrame(data)

# 2. 데이터 개요
st.header("1. 데이터 미리보기")

col1, col2, col3 = st.columns(3)

col1.metric("전체 영화 수", f"{df.shape[0]}편")
col2.metric("전체 열 수", f"{df.shape[1]}개")
col3.metric("결측치 개수", f"{df.isnull().sum().sum()}개")

st.dataframe(df, use_container_width=True)

st.caption("조회수 단위: 만 회 / 관객수 단위: 만 명")

# 3. 산점도 그래프
st.header("2. 예고편 조회수와 실제 관객수의 관계")

fig1 = px.scatter(
    df,
    x="예고편 조회수",
    y="실제 관객수",
    text="영화 제목",
    hover_data=["영화 제목", "예고편 조회수", "실제 관객수"],
    title="예고편 조회수와 실제 영화 관객수의 관계",
    labels={
        "예고편 조회수": "예고편 조회수 (만 회)",
        "실제 관객수": "실제 관객수 (만 명)"
    },
    color="실제 관객수",
    color_continuous_scale="Blues"
)

fig1.update_traces(
    textposition="top center",
    marker=dict(size=13)
)

fig1.update_layout(
    xaxis_title="예고편 조회수 (만 회)",
    yaxis_title="실제 관객수 (만 명)"
)

st.plotly_chart(fig1, use_container_width=True)

st.caption(
    "점 하나는 영화 한 편을 의미합니다. "
    "점에 마우스를 올리면 영화 제목과 수치를 확인할 수 있습니다."
)

# 4. 영화별 관객수 막대그래프
st.header("3. 영화별 실제 관객수 비교")

sorted_df = df.sort_values(
    by="실제 관객수",
    ascending=False
)

fig2 = px.bar(
    sorted_df,
    x="영화 제목",
    y="실제 관객수",
    color="실제 관객수",
    text="실제 관객수",
    title="영화별 실제 관객수 비교",
    labels={
        "영화 제목": "영화 제목",
        "실제 관객수": "실제 관객수 (만 명)"
    },
    color_continuous_scale="Blues"
)

fig2.update_traces(texttemplate="%{text:.1f}만")

st.plotly_chart(fig2, use_container_width=True)

# 5. 상관계수 계산
st.header("4. 상관관계 분석")

correlation = df["예고편 조회수"].corr(
    df["실제 관객수"]
)

st.metric(
    "예고편 조회수와 관객수의 상관계수",
    f"{correlation:.3f}"
)

# 상관계수 해석
if correlation >= 0.7:
    result = "강한 양의 상관관계"
    explanation = "예고편 조회수가 높을수록 관객수도 증가하는 경향이 강합니다."

elif correlation >= 0.4:
    result = "중간 정도의 양의 상관관계"
    explanation = "예고편 조회수가 증가할수록 관객수도 증가하는 경향이 있습니다."

elif correlation >= 0.2:
    result = "약한 양의 상관관계"
    explanation = "두 변수 사이에 약한 증가 경향이 나타납니다."

elif correlation > -0.2:
    result = "뚜렷한 선형 상관관계가 거의 없음"
    explanation = "예고편 조회수와 관객수 사이에 뚜렷한 선형 관계가 나타나지 않습니다."

elif correlation > -0.7:
    result = "음의 상관관계"
    explanation = "예고편 조회수가 높을수록 관객수가 감소하는 경향이 있습니다."

else:
    result = "강한 음의 상관관계"
    explanation = "예고편 조회수가 높을수록 관객수가 감소하는 경향이 강합니다."

st.subheader(result)
st.write(explanation)

# 6. 추가 분석
st.header("5. 데이터에서 발견한 특징")

max_audience = df.loc[
    df["실제 관객수"].idxmax()
]

max_views = df.loc[
    df["예고편 조회수"].idxmax()
]

st.write(
    f"""
    - 실제 관객수가 가장 많은 영화는 **{max_audience['영화 제목']}**이며,
      관객수는 약 {max_audience['실제 관객수']}만 명입니다.

    - 예고편 조회수가 가장 높은 영화는 **{max_views['영화 제목']}**이며,
      조회수는 {max_views['예고편 조회수']}만 회입니다.

    - 예고편 조회수가 가장 높은 영화와 실제 관객수가 가장 많은 영화가
      서로 다르다는 점을 확인할 수 있습니다.
    """
)

# 7. 최종 결론
st.header("6. 최종 결론")

st.success(
    f"상관계수는 {correlation:.3f}으로, "
    "이번 데이터에서는 뚜렷한 선형 상관관계가 거의 나타나지 않았습니다."
)

st.write(
    """
    이번 분석을 통해 영화 예고편 조회수가 높다고 해서
    반드시 실제 관객수가 많은 것은 아니라는 점을 알 수 있었습니다.

    영화의 실제 관객수에는 예고편 조회수 외에도
    배우, 장르, 영화 평점, 홍보 활동, 관객들의 입소문 등
    다양한 요인이 영향을 미칠 수 있습니다.

    따라서 예고편 조회수만으로 영화의 흥행 여부를
    정확하게 예측하기는 어렵다는 결론을 내릴 수 있습니다.
    """
)

st.caption("본 분석은 총 9편의 영화 데이터를 이용한 탐구이며, 상관관계가 인과관계를 의미하지는 않습니다.")

st.success("🎉 영화 데이터 분석이 완료되었습니다!")
