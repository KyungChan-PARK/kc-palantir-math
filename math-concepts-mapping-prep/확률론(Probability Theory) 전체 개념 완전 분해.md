<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# **📊 확률론(Probability Theory) 전체 개념 완전 분해**


***

## **🏷️ Chapter 1: 확률공간의 기초 (Foundations of Probability Spaces)**

### **1. 확률공간 정의 (Probability Space Definition)**

**1.1 표본공간(Sample Space) Ω**

- 1.1.1 이산표본공간 vs 연속표본공간
- 1.1.2 사건(Events) 집합 σ-대수(σ-algebra) F 정의

**1.2 확률측도(Probability Measure) P**

- 1.2.1 측도의 공리(Axioms): 비음수성, 가법성, 전체집합 확률 1
- 1.2.2 가산가법성(Countable Additivity)
- 1.2.3 측도로서의 확률과 르베그 측도의 관계

**1.3 조건부확률과 독립성**

- 1.3.1 조건부확률 P(A|B) = P(A ∩ B)/P(B)
- 1.3.2 법칙: 전확률의 법칙, 베이즈 정리
- 1.3.3 사건의 독립성 정의 및 성질

***

## **📈 Chapter 2: 이산확률분포 (Discrete Probability Distributions)**

### **2. 확률질량함수(PMF)와 기대값**

**2.1 확률질량함수 p(x)**

- 2.1.1 정의: p(x) = P(X = x)
- 2.1.2 확률함수 성질: p(x) ≥ 0, Σ p(x) = 1
- 2.1.3 예제 분포: 베르누이, 이항, 포아송

**2.2 기대값(Expectation)과 분산(Variance)**

- 2.2.1 기댓값 정의: E[X] = Σ x p(x)
- 2.2.2 분산 정의: Var(X) = E[(X – E[X])²]
- 2.2.3 모멘트(Moments)와 표준화


### **3. 주요 이산분포 익히기**

**3.1 베르누이 분포**

- 3.1.1 정의와 PMF
- 3.1.2 기대값과 분산

**3.2 이항 분포**

- 3.2.1 정의: Bin(n,p)
- 3.2.2 기댓값 np, 분산 np(1–p)
- 3.2.3 근사: 포아송 근사 이론

**3.3 포아송 분포**

- 3.3.1 정의와 PMF
- 3.3.2 기댓값 λ, 분산 λ
- 3.3.3 응용: 사건 발생 모델링

**3.4 기하분포와 음이항분포**

- 3.4.1 기하분포 정의
- 3.4.2 음이항분포
- 3.4.3 메모리리스 성질

***

## **📊 Chapter 3: 연속확률분포 (Continuous Probability Distributions)**

### **4. 확률밀도함수(PDF)와 누적분포함수(CDF)**

**4.1 확률밀도함수 f(x)**

- 4.1.1 정의: P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx
- 4.1.2 성질: f(x) ≥ 0, ∫_{–∞}^{∞} f(x) dx = 1

**4.2 누적분포함수 F(x)**

- 4.2.1 정의: F(x) = P(X ≤ x)
- 4.2.2 F’(x) = f(x) 거의 모든 x
- 4.2.3 불연속점과 연속분포


### **5. 주요 연속분포 익히기**

**5.1 균등분포(Uniform Distribution)**

- 5.1.1 정의: U(a,b)
- 5.1.2 기댓값 (a+b)/2, 분산 (b–a)²/12

**5.2 지수분포(Exponential Distribution)**

- 5.2.1 정의: λe^{-λx}, x ≥ 0
- 5.2.2 메모리리스성
- 5.2.3 기댓값 1/λ, 분산 1/λ²

**5.3 정규분포(Normal Distribution)**

- 5.3.1 정의: (1/(σ√(2π))) e^{–(x–μ)²/(2σ²)}
- 5.3.2 표준정규분포와 Z변환
- 5.3.3 중앙극한정리(Central Limit Theorem)

**5.4 감마분포와 베타분포**

- 5.4.1 감마함수와 감마분포
- 5.4.2 베타함수와 베타분포
- 5.4.3 모멘트와 응용

***

## **📐 Chapter 4: 다변수 확률분포 (Multivariate Distributions)**

### **6. 결합분포(Joint Distributions)**

**6.1 이산형 다변수**

- 6.1.1 결합 PMF p(x,y)
- 6.1.2 주변분포(Marginal Distribution)

**6.2 연속형 다변수**

- 6.2.1 결합 PDF f(x,y)
- 6.2.2 주변 PDF와 조건부 PDF f(x|y)

**6.3 독립성과 상관관계**

- 6.3.1 독립성 정의 p(x,y)=p(x)p(y)
- 6.3.2 공분산(Covariance)과 상관계수(Correlation Coefficient)


### **7. 변환과 모멘트 생성함수**

**7.1 확률변수 변환**

- 7.1.1 일변수 함수 변환법칙
- 7.1.2 다변수 함수 변환(Jacobian 사용)

**7.2 모멘트 생성함수(MGF)와 특성함수**

- 7.2.1 MGF M(t) = E[e^{tX}]
- 7.2.2 특성함수 φ(t) = E[e^{itX}]
- 7.2.3 분포의 고유성

***

## **🧮 Chapter 5: 확률론적 극한 정리 (Limit Theorems in Probability)**

### **8. 약수렴과 거의 확실 수렴**

**8.1 거의 확실 수렴(Almost Sure Convergence)**

- 8.1.1 정의: P({ω: Xₙ(ω) → X(ω)}) = 1
- 8.1.2 성질 및 예제

**8.2 확률 수렴(Convergence in Probability)**

- 8.2.1 정의: ∀ε>0, P(|Xₙ–X|>ε)→0
- 8.2.2 상태 공간 해석

**8.3 Lᵖ 수렴(Convergence in Lᵖ)**

- 8.3.1 정의: E[|Xₙ–X|ᵖ]→0
- 8.3.2 관계: Lᵖ⇒ 확률⇒ 약수렴


### **9. 큰 수의 법칙(Laws of Large Numbers)**

**9.1 약한 큰 수의 법칙 (Weak LLN)**

- 9.1.1 정립: 샘플평균 → 모평균 in probability
- 9.1.2 Chebyshev 불등식 사용

**9.2 강한 큰 수의 법칙 (Strong LLN)**

- 9.2.1 정립: 샘플평균 → 모평균 거의 확실히
- 9.2.2 Kolmogorov의 SLLN 조건


### **10. 중심극한정리(Central Limit Theorem)**

**10.1 독립 동일분포 IID case**

- 10.1.1 정리: (ΣXᵢ – nμ)/(σ√n) ⇒ N(0,1)
- 10.1.2 립슨 중앙극한정리

**10.2 확장 버전**

- 10.2.1 린데버그–린트너 조건
- 10.2.2 다변수 CLT

***

## **📈 Chapter 6: 확률과정 개요 (Introduction to Stochastic Processes)**

### **11. 마르코프 연쇄(Markov Chains)**

**11.1 정의와 전이행렬**

- 11.1.1 상태공간과 전이확률 P_{ij}
- 11.1.2 Chapman-Kolmogorov 방정식
- 11.1.3 n-단계 전이확률

**11.2 분류와 정상분포**

- 11.2.1 재귀성, 소거성, 정상분포(Stationary Distribution)
- 11.2.2 장기행동과 에르고딕성


### **12. 기타 확률과정**

**12.1 포아송 과정(Poisson Process)**

- 12.1.1 독립 증가 성질
- 12.1.2 지수분포 간격
- 12.1.3 균일분포 사건 시각

**12.2 브라운 운동(Brownian Motion)**

- 12.2.1 정의와 연속성
- 12.2.2 확률 미분방정식 개요
- 12.2.3 응용: 금융 모형

***

**확률론 전 범위를 subunit 레벨로 완전 분해했습니다. 다음 통계학으로 진행하시겠습니까?**

