<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# **📊 통계학(Statistics) 전체 개념 완전 분해**


***

## **🏷️ Chapter 1: 기술통계(Descriptive Statistics)**

### **1. 데이터 시각화 및 요약 (Data Visualization \& Summary)**

**1.1 도수분포표와 히스토그램**

- 1.1.1 도수분포표 작성법
- 1.1.2 빈도밀도와 상대도수
- 1.1.3 히스토그램 해석

**1.2 중심경향치(Measures of Central Tendency)**

- 1.2.1 산술평균(Mean)
- 1.2.2 중앙값(Median)
- 1.2.3 최빈값(Mode)
- 1.2.4 가중평균(Weighted Mean)

**1.3 산포도(MMeasures of Dispersion)**

- 1.3.1 범위(Range)
- 1.3.2 사분위수 범위(IQR)
- 1.3.3 분산(Variance)
- 1.3.4 표준편차(Standard Deviation)

**1.4 왜도와 첨도(Skewness \& Kurtosis)**

- 1.4.1 왜도 정의 및 해석
- 1.4.2 첨도 정의 및 해석
- 1.4.3 정규분포와의 비교

***

## **📈 Chapter 2: 추론통계(Inferential Statistics)**

### **2. 표본분포(Sampling Distributions)**

**2.1 표본평균의 분포**

- 2.1.1 모평균 μ와 표준오차 σ/√n
- 2.1.2 중심극한정리 적용

**2.2 χ² 분포, t 분포, F 분포**

- 2.2.1 χ² 분포 정의: 자유도 k
- 2.2.2 t 분포 정의 및 표본평균 비교
- 2.2.3 F 분포 정의 및 ANOVA 연계


### **3. 추정(Estimation)**

**3.1 점추정(Point Estimation)**

- 3.1.1 불편추정량(Unbiased Estimator)
- 3.1.2 분산과 효율성(Efficiency)
- 3.1.3 최대우도추정(MLE)

**3.2 구간추정(Interval Estimation)**

- 3.2.1 신뢰구간 생성법
- 3.2.2 모평균 신뢰구간 (σ 알려진/미알려진 경우)
- 3.2.3 비율과 분산의 신뢰구간


### **4. 가설검정(Hypothesis Testing)**

**4.1 기본 절차**

- 4.1.1 귀무가설 H₀ 설정
- 4.1.2 대립가설 H₁ 설정
- 4.1.3 유의수준 α 결정
- 4.1.4 검정통계량 계산 및 p-value 해석

**4.2 단일표본 검정**

- 4.2.1 평균에 대한 z 검정, t 검정
- 4.2.2 비율 검정

**4.3 두표본 검정**

- 4.3.1 독립표본 t 검정
- 4.3.2 대응표본 t 검정
- 4.3.3 분산 동질성 검정(Levene’s Test)

**4.4 비모수 검정(Nonparametric Tests)**

- 4.4.1 윌콕슨 순위합검정
- 4.4.2 맨-휘트니 검정 (Mann–Whitney U)
- 4.4.3 크루스칼-왈리스 검정 (Kruskal–Wallis)

***

## **📊 Chapter 3: 회귀분석(Regression Analysis)**

### **5. 단순선형회귀(Simple Linear Regression)**

**5.1 모형 설정**

- 5.1.1 Y = β₀ + β₁X + ε
- 5.1.2 최소제곱법(OLS) 추정

**5.2 진단과 가정검토**

- 5.2.1 잔차 분석
- 5.2.2 선형성, 등분산성, 독립성, 정규성 검정
- 5.2.3 영향치(Leverage)와 이상치(Outliers)


### **6. 다중선형회귀(Multiple Linear Regression)**

**6.1 모형 확장**

- 6.1.1 Y = β₀ + β₁X₁ + … + β_pX_p + ε
- 6.1.2 행렬표기법

**6.2 모형선택 및 진단**

- 6.2.1 단계적 회귀(Stepwise Regression)
- 6.2.2 AIC, BIC 기준
- 6.2.3 다중공선성(VIF) 검사

**6.3 정칙화(Regularization)**

- 6.3.1 릿지 회귀(Ridge)
- 6.3.2 라쏘 회귀(LASSO)
- 6.3.3 엘라스틱 넷(Elastic Net)

***

## **📐 Chapter 4: 분산분석(ANOVA, Analysis of Variance)**

### **7. 일원분산분석(One-Way ANOVA)**

**7.1 가정과 구성**

- 7.1.1 집단 간 평균 차이 검정
- 7.1.2 분산의 분해 (Between \& Within)
- 7.1.3 F 검정통계량

**7.2 사후검정(Post Hoc Tests)**

- 7.2.1 튜키의 HSD 검정
- 7.2.2 본페로니 교정


### **8. 이원분산분석(Two-Way ANOVA)**

**8.1 교호작용(Interaction)**

- 8.1.1 주효과(Main Effects)
- 8.1.2 교호작용 효과 분석

**8.2 반복측정 ANOVA(Repeated Measures)**

- 8.2.1 피험자 내 설계
- 8.2.2 구형성 가정(Sphericity)

***

## **📈 Chapter 5: 기타 회귀 및 모델 (Other Regression \& Modeling)**

### **9. 로지스틱 회귀(Logistic Regression)**

**9.1 이항 로지스틱 회귀**

- 9.1.1 로짓(로그 오즈) 함수
- 9.1.2 최대우도추정

**9.2 다항 로지스틱 회귀**

- 9.2.1 다항 분류
- 9.2.2 확률 예측


### **10. 베이지안 통계(Bayesian Statistics)**

**10.1 사전분포와 사후분포**

- 10.1.1 베이즈 정리 응용
- 10.1.2 컨쥬게이트 사전분포

**10.2 MCMC 기법**

- 10.2.1 Metropolis-Hastings
- 10.2.2 Gibbs Sampling

***

**통계학 전체 개념을 subunit 레벨로 완전 분해했습니다. 다음 Differential Equations 또는 Applied Mathematics로 진행하시겠습니까?**

