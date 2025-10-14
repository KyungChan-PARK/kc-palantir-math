<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# **📊 미분방정식(Differential Equations) 전체 개념 완전 분해**


***

## **🏷️ Chapter 1: 상미분방정식(Ordinary Differential Equations)**

### **1. 1계 상미분방정식(First-Order ODEs)**

#### **1.1 변수분리형 방정식(Separable Equations)**

- 1.1.1 정의: dy/dx = g(x)h(y)
- 1.1.2 해법: ∫1/h(y) dy = ∫g(x) dx + C
- 1.1.3 초기조건 문제(Initial Value Problem)
- 1.1.4 예제: logistic equation, Newton’s law of cooling


#### **1.2 선형 1계 방정식(Linear First-Order)**

- 1.2.1 형태: dy/dx + P(x)y = Q(x)
- 1.2.2 적분인자(Integrating Factor): μ(x)=e^{∫P(x)dx}
- 1.2.3 해법 과정
- 1.2.4 예제: mixing problems


#### **1.3 정확방정식(Exact Equations)**

- 1.3.1 형태: M(x,y)dx + N(x,y)dy = 0
- 1.3.2 정확성 조건: ∂M/∂y = ∂N/∂x
- 1.3.3 해법: 잠재함수 Φ(x,y)
- 1.3.4 적분인자 찾기


#### **1.4 기타 1계 방정식**

- 1.4.1 베르누이 방정식(Bernoulli): dy/dx + P(x)y = Q(x)y^n
- 1.4.2 리카티 방정식(Riccati)
- 1.4.3 대수적 기법과 변환


### **2. 고계 상미분방정식(Higher-Order ODEs)**

#### **2.1 선형 상미분방정식(Linear ODEs)**

**2.1.1 동차 선형 방정식 제차 n**

- 형태: y^{(n)} + a_{n-1}(x)y^{(n-1)} + … + a₀(x)y = 0
- 특성방정식(Characteristic Equation) 해법(상수 계수 경우)
- 해의 선형 독립성: Wronskian

**2.1.2 비동차 선형 방정식**

- 형태: L[y] = f(x), L 선형 연산자
- 일반해 = 동차해 + 특수해
- 특수해 구하기: 상수변화법(Method of Variation of Parameters), 미정계수법(Method of Undetermined Coefficients)


#### **2.2 연립 상미분방정식(Systems of ODEs)**

- 2.2.1 벡터-행렬 형태: X' = A X + F(x)
- 2.2.2 고윳값·고유벡터 해법
- 2.2.3 해의 구조: 지수 행렬(exp(At))

***

## **📐 Chapter 2: 편미분방정식(Partial Differential Equations)**

### **3. 1계 편미분방정식(First-Order PDEs)**

#### **3.1 선형 1계 PDE**

- 3.1.1 형태: a(x,y)u_x + b(x,y)u_y = c(x,y,u)
- 3.1.2 특성곡선(Method of Characteristics)
- 3.1.3 해의 일반형과 특이해
- 3.1.4 예제: 교통밀도 방정식, 라그랑주 방정식


#### **3.2 비선형 1계 PDE**

- 3.2.1 버거스 방정식(Burgers’ Equation)
- 3.2.2 해의 충격파(Shock Waves)
- 3.2.3 포텐셜 흐름 방정식


### **4. 2계 편미분방정식(Second-Order PDEs)**

#### **4.1 타원형 방정식(Elliptic Equations)**

- 4.1.1 라플라시안(Δu = 0): 라플라스 방정식
- 4.1.2 포아송 방정식(Δu = f)
- 4.1.3 경계값 문제(Boundary Value Problems): 디리클레, 노이만 조건
- 4.1.4 최대·최소 원리(Maximum-Minimum Principles)


#### **4.2 포물선형 방정식(Parabolic Equations)**

- 4.2.1 열 방정식(u_t = kΔu)
- 4.2.2 초기-경계값 문제(Initial-Boundary Value Problems)
- 4.2.3 분리 변수법(Separation of Variables)
- 4.2.4 그린 함수와 근사해법


#### **4.3 쌍곡선형 방정식(Hyperbolic Equations)**

- 4.3.1 파동 방정식(u_{tt} = c²Δu)
- 4.3.2 초기값 문제(Cauchy Problem)
- 4.3.3 특징 해법(Method of Characteristics)
- 4.3.4 데이비슨 공식과 해의 전파 속도

***

## **🧮 Chapter 3: 수치해법(Numerical Methods for DEs)**

### **5. 상미분 기본 수치해법(ODE Solvers)**

- 5.1 오일러 방법(Euler’s Method)
- 5.2 개량 오일러(Runge-Kutta 2nd Order)
- 5.3 룬게-쿠타 4차(RK4)
- 5.4 다단법(Multi-step Methods): 아담스-배쉬포스(Adams-Bashforth)


### **6. 편미분 수치해법(PDE Solvers)**

- 6.1 유한차분법(Finite Difference Method)
- 6.2 유한요소법(Finite Element Method)
- 6.3 유한체적법(Finite Volume Method)

***

**미분방정식 전 범위를 subunit 레벨로 완전 분해했습니다. 다음 Applied Mathematics로 진행하시겠습니까?**

