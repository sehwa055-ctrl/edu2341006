<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>삼각형 분석기</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>삼각형 분석기 (피타고라스 정리 활용)</h1>
        
        <div class="input-area">
            <label for="sideA">변 a:</label>
            <input type="number" id="sideA" min="1" step="1" value="3">
            
            <label for="sideB">변 b:</label>
            <input type="number" id="sideB" min="1" step="1" value="4">
            
            <label for="sideC">변 c:</label>
            <input type="number" id="sideC" min="1" step="1" value="5">
            
            <button onclick="analyzeTriangle()">분석 및 그리기</button>
        </div>
        
        <hr>

        <div class="result-area">
            <h2>분석 결과</h2>
            <p id="triangleType">결과를 확인하려면 변의 길이를 입력하세요.</p>
            <p id="explanation"></p>
        </div>

        <div class="canvas-area">
            <h2>삼각형 그림</h2>
            <canvas id="triangleCanvas" width="400" height="300" style="border:1px solid #ccc;"></canvas>
            <p id="drawMessage">캔버스에 삼각형이 그려집니다.</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    color: #333;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding: 20px;
}

.container {
    background-color: #fff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 600px;
}

h1, h2 {
    color: #007bff;
    text-align: center;
}

.input-area {
    margin-bottom: 20px;
    text-align: center;
}

.input-area label, .input-area input, .input-area button {
    margin: 5px;
    padding: 8px;
    border-radius: 4px;
}

.input-area input[type="number"] {
    width: 60px;
    border: 1px solid #ccc;
}

.input-area button {
    background-color: #28a745;
    color: white;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s;
}

.input-area button:hover {
    background-color: #218838;
}

hr {
    border: 0;
    height: 1px;
    background: #ccc;
    margin: 20px 0;
}

.result-area, .canvas-area {
    margin-top: 15px;
    text-align: center;
}

#triangleCanvas {
    display: block;
    margin: 15px auto;
    background-color: #ffffff;
}
// script.js

// 부동 소수점 오차를 고려하여 비교하는 상수
const EPSILON = 0.0001;

/**
 * 사용자 입력을 받아 삼각형의 종류를 분석하고 그립니다.
 */
function analyzeTriangle() {
    const a = parseFloat(document.getElementById('sideA').value);
    const b = parseFloat(document.getElementById('sideB').value);
    const c = parseFloat(document.getElementById('sideC').value);

    const typeElement = document.getElementById('triangleType');
    const explanationElement = document.getElementById('explanation');
    const drawMessageElement = document.getElementById('drawMessage');
    const canvas = document.getElementById('triangleCanvas');
    const ctx = canvas.getContext('2d');
    
    // 결과 초기화
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    typeElement.textContent = '';
    explanationElement.textContent = '';
    drawMessageElement.textContent = '캔버스에 삼각형이 그려집니다.';

    // 1. 입력 유효성 및 자연수/양수 확인
    if (isNaN(a) || isNaN(b) || isNaN(c) || a <= 0 || b <= 0 || c <= 0) {
        typeElement.textContent = '오류: 모든 변의 길이는 양의 자연수여야 합니다.';
        explanationElement.textContent = '';
        drawMessageElement.textContent = '유효하지 않은 입력입니다.';
        return;
    }

    // 2. 삼각형 성립 조건 (가장 긴 변 < 나머지 두 변의 합) 확인
    const sides = [a, b, c].sort((x, y) => x - y); // 오름차순 정렬
    const s1 = sides[0]; // a
    const s2 = sides[1]; // b
    const s3 = sides[2]; // c (가장 긴 변)

    if (s1 + s2 <= s3) {
        typeElement.textContent = '삼각형 아님';
        explanationElement.textContent = `가장 긴 변 (${s3})이 나머지 두 변의 합 (${s1} + ${s2} = ${s1 + s2})보다 같거나 길기 때문에 삼각형을 만들 수 없습니다. (삼각형 부등식 조건 불만족: $a + b > c$)`;
        drawMessageElement.textContent = '삼각형을 그릴 수 없습니다.';
        return;
    }

    // 3. 피타고라스 정리 응용하여 삼각형 종류 판별
    // $s1^2 + s2^2$ 와 $s3^2$ 비교
    const s1Sq = s1 * s1;
    const s2Sq = s2 * s2;
    const s3Sq = s3 * s3;
    const sumSq = s1Sq + s2Sq;

    let typeText;
    let explanationText;

    if (Math.abs(sumSq - s3Sq) < EPSILON) {
        // 직각 삼각형
        typeText = '직각삼각형 (Right Triangle)';
        explanationText = `피타고라스 정리: ${s1}^2 + ${s2}^2 = ${s1Sq} + ${s2Sq} = ${sumSq.toFixed(2)}와 ${s3}^2 = ${s3Sq.toFixed(2)}이(가) 거의 같습니다. ($a^2 + b^2 = c^2$)`;
    } else if (sumSq > s3Sq) {
        // 예각 삼각형
        typeText = '예각삼각형 (Acute Triangle)';
        explanationText = `가장 긴 변의 제곱이 나머지 두 변의 제곱의 합보다 작습니다. (${s3Sq.toFixed(2)} < ${sumSq.toFixed(2)}) ($a^2 + b^2 > c^2$)`;
    } else {
        // 둔각 삼각형
        typeText = '둔각삼각형 (Obtuse Triangle)';
        explanationText = `가장 긴 변의 제곱이 나머지 두 변의 제곱의 합보다 큽니다. (${s3Sq.toFixed(2)} > ${sumSq.toFixed(2)}) ($a^2 + b^2 < c^2$)`;
    }

    // 추가: 변의 길이 기반 종류 (이등변, 정삼각형)
    if (s1 === s2 && s2 === s3) {
        typeText = `정삼각형 (Equilateral)이자 ${typeText}`;
    } else if (s1 === s2 || s2 === s3) {
        typeText = `이등변삼각형 (Isosceles)이자 ${typeText}`;
    }

    typeElement.textContent = `결과: ${typeText}`;
    explanationElement.textContent = `[풀이]\n${explanationText}`;

    // 4. Canvas에 삼각형 그리기
    drawTriangle(ctx, canvas.width, canvas.height, s1, s2, s3, drawMessageElement);
}

/**
 * 세 변의 길이를 사용하여 Canvas에 삼각형을 그립니다.
 * 가장 긴 변(s3)을 밑변으로 하여 그립니다.
 * @param {CanvasRenderingContext2D} ctx - 캔버스 컨텍스트
 * @param {number} width - 캔버스 너비
 * @param {number} height - 캔버스 높이
 * @param {number} s1 - 가장 짧은 변
 * @param {number} s2 - 중간 변
 * @param {number} s3 - 가장 긴 변 (밑변으로 사용)
 * @param {HTMLElement} drawMessageElement - 그리기 상태 메시지를 표시할 요소
 */
function drawTriangle(ctx, width, height, s1, s2, s3, drawMessageElement) {
    // 캔버스 중앙에 오도록 스케일 조정 및 오프셋 계산
    const padding = 20;
    const maxSide = Math.max(s1, s2, s3);
    
    // 캔버스 크기에 맞게 스케일링
    const scale = Math.min(
        (width - 2 * padding) / s3,  // 밑변 s3 기준 스케일
        (height - 2 * padding) / s3 // 높이를 고려하여 보수적으로 s3로 나눔
    );
    
    const scaledS1 = s1 * scale;
    const scaledS2 = s2 * scale;
    const scaledS3 = s3 * scale;

    // 코사인 법칙을 이용하여 세 번째 꼭짓점의 x 좌표(x_p)를 계산
    // s3를 밑변으로 가정하고, s1을 왼쪽, s2를 오른쪽 변으로 가정
    // $s1^2 = s2^2 + s3^2 - 2 \cdot s2 \cdot s3 \cdot \cos(\gamma)$ -> 이건 코사인 법칙.
    // 높이(h)와 밑변 s3에 내린 수선의 발 위치 (x_p)를 구하기 위해 피타고라스 정리 응용:
    // $s1^2 - h^2 = x_p^2$
    // $s2^2 - h^2 = (s3 - x_p)^2$
    // $s1^2 - x_p^2 = s2^2 - (s3 - x_p)^2$
    // $s1^2 - x_p^2 = s2^2 - (s3^2 - 2 \cdot s3 \cdot x_p + x_p^2)$
    // $s1^2 - x_p^2 = s2^2 - s3^2 + 2 \cdot s3 \cdot x_p - x_p^2$
    // $s1^2 = s2^2 - s3^2 + 2 \cdot s3 \cdot x_p$
    // $2 \cdot s3 \cdot x_p = s1^2 - s2^2 + s3^2$
    // $x_p = (s1^2 - s2^2 + s3^2) / (2 \cdot s3)$

    const xp_unscaled = (s1 * s1 - s2 * s2 + s3 * s3) / (2 * s3);
    const xp_scaled = xp_unscaled * scale;

    // 높이 계산: $h = \sqrt{s1^2 - x_p^2}$
    const h_unscaled_sq = s1 * s1 - xp_unscaled * xp_unscaled;
    // 부동소수점 오차로 인해 음수가 될 수 있으므로, 0보다 작으면 0으로 처리 (거의 둔각삼각형인 경우)
    const h_unscaled = Math.sqrt(Math.max(0, h_unscaled_sq));
    const h_scaled = h_unscaled * scale;

    if (h_scaled <= EPSILON) {
        drawMessageElement.textContent = '삼각형이 너무 납작하여 거의 직선처럼 보입니다.';
        // 이 경우, 그리기 건너뛰거나 최소한의 높이로 그릴 수 있음 (여기서는 납작하게 그립니다)
    } else {
        drawMessageElement.textContent = '삼각형이 캔버스에 그려졌습니다.';
    }

    // 캔버스에 그릴 세 꼭짓점 좌표 계산
    // 캔버스에 그릴 때, (0, 0)이 좌상단이므로 y좌표는 캔버스 높이에서 빼야 합니다.
    const offsetX = (width - scaledS3) / 2; // 중앙 정렬을 위한 x축 오프셋
    const offsetY = (height - h_scaled) / 2; // 중앙 정렬을 위한 y축 오프셋 (캔버스 상단 패딩)

    const A = { x: offsetX + xp_scaled, y: offsetY }; // 높이점
    const B = { x: offsetX, y: offsetY + h_scaled }; // 밑변 시작점
    const C = { x: offsetX + scaledS3, y: offsetY + h_scaled }; // 밑변 끝점

    // 그리기 실행
    ctx.beginPath();
    ctx.moveTo(A.x, A.y);
    ctx.lineTo(B.x, B.y);
    ctx.lineTo(C.x, C.y);
    ctx.closePath(); // A로 돌아와 닫기

    ctx.strokeStyle = '#007bff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 꼭짓점에 작은 점 찍기
    ctx.fillStyle = '#dc3545';
    [A, B, C].forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
        ctx.fill();
    });
    
    // 각 변의 길이 텍스트 표시
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    
    // s1 (A-B) 표시
    const midAB_x = (A.x + B.x) / 2;
    const midAB_y = (A.y + B.y) / 2;
    ctx.fillText(`s1: ${s1}`, midAB_x - 10, midAB_y - 5);

    // s2 (A-C) 표시
    const midAC_x = (A.x + C.x) / 2;
    const midAC_y = (A.y + C.y) / 2;
    ctx.fillText(`s2: ${s2}`, midAC_x + 5, midAC_y - 5);
    
    // s3 (B-C) 표시
    const midBC_x = (B.x + C.x) / 2;
    const midBC_y = (B.y + C.y) / 2;
    ctx.fillText(`s3: ${s3}`, midBC_x - 10, midBC_y + 15);
}

// 페이지 로드 후 바로 분석 함수 실행 (기본값으로)
document.addEventListener('DOMContentLoaded', analyzeTriangle);