import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def analyze_triangle(a, b, c):
    # 삼각형 성립 조건 확인
    if a + b <= c or b + c <= a or a + c <= b:
        return "이 세 변으로는 삼각형을 만들 수 없습니다."
    
    # 피타고라스 정리를 이용한 삼각형 분석
    sides = sorted([a, b, c])  # 작은 순서대로 정렬
    a2, b2, c2 = [x**2 for x in sides]
    
    # 각도 계산 (코사인 법칙)
    cos_A = (b2 + c2 - a2) / (2 * sides[1] * sides[2])
    angle_A = np.arccos(np.clip(cos_A, -1.0, 1.0)) * 180 / np.pi
    
    if abs(a2 + b2 - c2) < 0.0001:  # 부동소수점 오차 고려
        return "직각삼각형"
    elif a2 + b2 > c2:
        return "예각삼각형"
    else:
        return "둔각삼각형"

def draw_triangle(a, b, c):
    if a + b <= c or b + c <= a or a + c <= b:
        return None
    
    # 삼각형 좌표 계산 (코사인 법칙 사용)
    cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
    angle_C = np.arccos(np.clip(cos_C, -1.0, 1.0))
    
    # 삼각형 꼭지점 좌표
    points = [(0, 0), (a, 0), (b * np.cos(angle_C), b * np.sin(angle_C))]
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(6, 6))
    triangle = Polygon(points, fill=False)
    ax.add_patch(triangle)
    
    # 축 설정
    margin = max(a, b, c) * 0.1
    ax.set_xlim(-margin, max(a, b * np.cos(angle_C)) + margin)
    ax.set_ylim(-margin, b * np.sin(angle_C) + margin)
    ax.set_aspect('equal')
    
    # 변의 길이 표시
    ax.text(a/2, -margin, f'a = {a}', ha='center')
    ax.text(a + margin/2, b * np.sin(angle_C)/2, f'b = {b}', va='center')
    x_mid = (a + b * np.cos(angle_C))/2
    y_mid = b * np.sin(angle_C)/2
    ax.text(x_mid, y_mid, f'c = {c}', ha='center')
    
    return fig

# Streamlit UI
st.title('삼각형 분석기')
st.write('각 변의 길이를 입력하면 삼각형을 그리고 분석해드립니다.')

# 입력 필드
col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input('변 a의 길이', min_value=1, value=3)
with col2:
    b = st.number_input('변 b의 길이', min_value=1, value=4)
with col3:
    c = st.number_input('변 c의 길이', min_value=1, value=5)

# 분석 결과
result = analyze_triangle(a, b, c)
st.write(f'### 분석 결과: {result}')

# 삼각형 그리기
fig = draw_triangle(a, b, c)
if fig:
    st.pyplot(fig)
else:
    st.error('입력한 길이로는 삼각형을 그릴 수 없습니다.')
