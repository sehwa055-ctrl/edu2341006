import streamlit as st
import numpy as np
# Matplotlib 설정
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def analyze_triangle(a, b, c):
    # 삼각형 성립 조건 확인
    if a + b <= c or b + c <= a or a + c <= b:
        return ("이 세 변으로는 삼각형을 만들 수 없습니다.", None)
    
    # 피타고라스 정리를 이용한 삼각형 분석
    sides = sorted([a, b, c])  # 작은 순서대로 정렬
    a2, b2, c2 = [x**2 for x in sides]
    
    # 각도 계산 (코사인 법칙)
    cos_angles = [
        (b2 + c2 - a2) / (2 * sides[1] * sides[2]),
        (a2 + c2 - b2) / (2 * sides[0] * sides[2]),
        (a2 + b2 - c2) / (2 * sides[0] * sides[1])
    ]
    angles = [np.arccos(np.clip(cos, -1.0, 1.0)) * 180 / np.pi for cos in cos_angles]
    
    # 풀이 과정 문자열 생성
    solution = f"""
    ▶ 입력된 세 변의 길이:
       a = {sides[0]}, b = {sides[1]}, c = {sides[2]} (길이 순)
    
    ▶ 피타고라스 정리를 이용한 삼각형 판별:
    1. 두 짧은 변의 제곱의 합 구하기
       * a² = {sides[0]}² = {a2}
       * b² = {sides[1]}² = {b2}
       * a² + b² = {a2 + b2}
    
    2. 가장 긴 변의 제곱 구하기
       * c² = {sides[2]}² = {c2}
    
    3. 피타고라스 정리로 삼각형 판별하기
       * a² + b² = {a2 + b2}
       * c² = {c2}
       
       → a² + b² {'>=' if a2 + b2 >= c2 else '<'} c² 이므로,
       {a2 + b2} {'>=' if a2 + b2 >= c2 else '<'} {c2}
       
       판정 기준:
       - a² + b² = c² 이면 직각삼각형
       - a² + b² > c² 이면 예각삼각형
       - a² + b² < c² 이면 둔각삼각형
       
       따라서 이 삼각형은 {
       "직각삼각형입니다 (두 값이 같음)" if abs(a2 + b2 - c2) < 0.0001
       else "예각삼각형입니다 (a² + b²가 c²보다 큼)" if a2 + b2 > c2
       else "둔각삼각형입니다 (a² + b²가 c²보다 작음)"
       }
    
    ▶ 각도 계산 (코사인 법칙):
       ∠A = {angles[0]:.1f}°
       ∠B = {angles[1]:.1f}°
       ∠C = {angles[2]:.1f}°
       각의 합: {sum(angles):.1f}° (삼각형의 내각의 합은 180°)
    """
    
    # 삼각형 유형 판단
    if abs(a2 + b2 - c2) < 0.0001:  # 부동소수점 오차 고려
        triangle_type = "직각삼각형 (a² + b² = c²)"
    elif a2 + b2 > c2:
        triangle_type = "예각삼각형 (a² + b² > c²)"
    else:
        triangle_type = "둔각삼각형 (a² + b² < c²)"
    
    return (triangle_type, solution)

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

# 분석 결과 및 풀이 과정 표시
result, solution = analyze_triangle(a, b, c)
if solution:
    st.write('### 삼각형 분석 결과')
    st.code(solution, language='text')

# 삼각형 그리기
fig = draw_triangle(a, b, c)
if fig:
    st.pyplot(fig)
else:
    st.error('입력한 길이로는 삼각형을 그릴 수 없습니다.')
