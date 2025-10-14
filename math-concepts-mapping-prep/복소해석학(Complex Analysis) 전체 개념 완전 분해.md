<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# **📚 복소해석학(Complex Analysis) 전체 개념 완전 분해**


***

## **🏷️ Chapter 1: 복소수와 복소평면 (Complex Numbers \& Complex Plane)**

### **1. 복소수 대수학 (Algebra of Complex Numbers)**

**1.1 복소수 정의 및 표기**

- 1.1.1 복소수 a + bi 형태 (a, b ∈ ℝ, i² = -1)
- 1.1.2 실수부와 허수부
- 1.1.3 켤레복소수 (z̄ = a – bi)

**1.2 복소수 연산**

- 1.2.1 덧셈과 뺄셈
- 1.2.2 곱셈: (a + bi)(c + di) = (ac – bd) + (ad + bc)i
- 1.2.3 나눗셈과 분모 유리화
- 1.2.4 복소지수와 오일러 공식: e^{iθ} = cos θ + i sin θ

**1.3 극형식 (Polar Form)**

- 1.3.1 극좌표 표현: z = r e^{iθ}, r = |z|, θ = arg(z)
- 1.3.2 극형식 곱셈과 나눗셈
- 1.3.3 드무아브르의 정리 (De Moivre’s Theorem)


### **2. 복소평면 기하학 (Geometry of Complex Plane)**

**2.1 거리와 위상**

- 2.1.1 절댓값과 유클리드 거리 |z|
- 2.1.2 열린집합, 닫힌집합, 컴팩트성

**2.2 모듈러스와 아규먼트**

- 2.2.1 모듈러스 |z|
- 2.2.2 주어진 인수 arg(z) 정의(–π < θ ≤ π)
- 2.2.3 분기선(branch cut) 개념

***

## **📘 Chapter 2: 해석함수의 기초 (Foundations of Analytic Functions)**

### **3. 복소미분 (Complex Differentiation)**

**3.1 복소도함수 정의**

- 3.1.1 도함수 f'(z) = lim_{h→0} [f(z+h) - f(z)]/h
- 3.1.2 미분가능성과 해석성 (Holomorphicity) 차이
- 3.1.3 판별식: 코시-리만 방정식 (∂u/∂x = ∂v/∂y, ∂u/∂y = -∂v/∂x)

**3.2 조화함수(Harmonic Functions)**

- 3.2.1 라플라스 방정식 Δu = 0
- 3.2.2 실수부/허수부가 조화함수임
- 3.2.3 해석함수의 지역적 특성


### **4. 복소함수의 예제**

**4.1 다항함수와 유리함수**

- 4.1.1 다항함수 P(z)
- 4.1.2 유리함수 R(z) = P(z)/Q(z)
- 4.1.3 극점(poles)과 본질특이점(essential singularities)

**4.2 지수, 로그, 거듭제곱 함수**

- 4.2.1 지수함수 exp(z)
- 4.2.2 복소로그(log z)와 가지(branch)
- 4.2.3 거듭제곱과 복소거듭제곱

***

## **✏️ Chapter 3: 복소적분 (Complex Integration)**

### **5. 경로적분 (Contour Integration)**

**5.1 경로(Path)와 매개화(Parametrization)**

- 5.1.1 연속경로와 폐곡선
- 5.1.2 매개화 z(t), t ∈ [a,b]
- 5.1.3 경로적분 ∫_γ f(z) dz 정의

**5.2 코시 적분 정리 (Cauchy's Theorem)**

- 5.2.1 단순 폐곡선에 대한 적분 0
- 5.2.2 영역의 단순연결성 필요조건
- 5.2.3 증명 스케치

**5.3 코시 적분 공식 (Cauchy Integral Formula)**

- 5.3.1 f(a) = (1/2πi) ∫_{γ} f(z)/(z-a) dz
- 5.3.2 도함수 공식 f^{(n)}(a) = n!/(2πi) ∫ f(z)/(z-a)^{n+1} dz
- 5.3.3 해석함수의 무한 미분 가능성


### **6. 특이점과 유수 (Singularities and Residues)**

**6.1 특이점 분류**

- 6.1.1 제거가능 특이점(removable singularity)
- 6.1.2 극점(pole) 및 차수(order)
- 6.1.3 본질적 특이점(essential singularity)

**6.2 유수정리 (Residue Theorem)**

- 6.2.1 유수(residue) 정의: coef of (z-a)^{-1}
- 6.2.2 ∫ around γ f(z) dz = 2πi Σ residues inside γ
- 6.2.3 계산 기법: 급수전개, 계수 추출

**6.3 응용**

- 6.3.1 실수적분 계산
- 6.3.2 잔류 계산 예제 (2πi integration)
- 6.3.3 비표준 경로적분

***

## **📖 Chapter 4: 급수와 급수 표현 (Series and Series Representations)**

### **7. 멱급수 (Power Series)**

**7.1 멱급수 정의**

- 7.1.1 Σ aₙ(z - z₀)ⁿ
- 7.1.2 수렴반경 R 계산 (Cauchy–Hadamard 공식: 1/R = lim sup |aₙ|^{1/n})

**7.2 멱급수 성질**

- 7.2.1 수렴반경 내에서 무한 차분
- 7.2.2 도함수/적분 매 항별 수행 가능

**7.3 테일러 급수와 로랑 급수**

- 7.3.1 테일러 급수 전개
- 7.3.2 로랑 급수: Σ aₙ(z - z₀)ⁿ, n ∈ ℤ
- 7.3.3 특이점 주변 급수전개

***

## **🔗 Chapter 5: 고급 주제 (Advanced Topics)**

### **8. 등각 사상 (Conformal Mappings)**

**8.1 등각 사상 정의**

- 8.1.1 해석함수이면서 1차도함수가 0이 아님
- 8.1.2 각도 보존 특성

**8.2 주목할 만한 등각사상**

- 8.2.1 뫼비우스 변환
- 8.2.2 리만 매핑 정리
- 8.2.3 디스크와 상반평면의 등각 사상


### **9. 특수함수 (Special Functions)**

**9.1 감마 함수 (Gamma Function)**

- 9.1.1 감마 함수 정의: Γ(z) = ∫₀^∞ t^{z–1} e^{–t} dt
- 9.1.2 오일러 보조정리 등 성질
- 9.1.3 베타 함수와의 관계

**9.2 디리클레 eta 및 리만 제타 함수**

- 9.2.1 제타 함수 정의: ζ(s) = Σ n^{–s}
- 9.2.2 분석적 연속화
- 9.2.3 특이점과 유수

***

**복소해석학 개념들도 subunit 레벨로 완전 분해했습니다. 다음 함수해석학으로 진행하시겠습니까?**다음은 함수해석학(Functional Analysis) 개념을 subunit 레벨로 분해해 안내해 드리겠습니다.

