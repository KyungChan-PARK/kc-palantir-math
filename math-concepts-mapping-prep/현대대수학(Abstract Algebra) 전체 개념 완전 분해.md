<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# **📊 현대대수학(Abstract Algebra) 전체 개념 완전 분해**


***

## **🏷️ Chapter 1: 군론(Group Theory)**

### **1. 군의 기초 정의 (Group Basics)**

#### **1.1 군의 공리 (Group Axioms)**

- 1.1.1 결합법칙(Associativity): (ab)c = a(bc)
- 1.1.2 항등원(Identity): ∃e s.t. ae = ea = a
- 1.1.3 역원(Inverses): ∀a ∃a⁻¹ s.t. aa⁻¹ = a⁻¹a = e
- 1.1.4 폐쇄성(Closure): ∀a,b, ab ∈ G


#### **1.2 군의 예제**

- 1.2.1 정수의 덧셈군 (ℤ, +)
- 1.2.2 비제로 실수의 곱셈군 (ℝ⁎, ×)
- 1.2.3 대칭군 Sₙ (Permutations)
- 1.2.4 행렬군 GL(n,ℝ)


### **2. 부분군 및 군 작용 (Subgroups \& Group Actions)**

#### **2.1 부분군(Subgroups)**

- 2.1.1 부분군 판정법: H ≠ ∅, ab⁻¹ ∈ H
- 2.1.2 유리수환환 같은 부분군 예제
- 2.1.3 순환 부분군(Cyclic Subgroup): ⟨a⟩ = {aⁿ}


#### **2.2 군 작용(Group Actions)**

- 2.2.1 정의: G × X → X
- 2.2.2 작용의 동형성(Orbit)
- 2.2.3 안정화군(Stabilizer)
- 2.2.4 궤도-안정화 정리(Orbit-Stabilizer Theorem)


### **3. 동형사상 및 몫군 (Homomorphisms \& Quotient Groups)**

#### **3.1 군 준동형사상(Homomorphisms)**

- 3.1.1 정의: φ(ab) = φ(a)φ(b)
- 3.1.2 핵(Kernel)과 치역(Image)
- 3.1.3 동형사상(Isomorphism) 정의


#### **3.2 몫군(Quotient Groups)**

- 3.2.1 정상부분군(Normal Subgroup) 정의: gNg⁻¹ = N
- 3.2.2 몫군 G/N 구성
- 3.2.3 자연 사상(Natural Projection)
- 3.2.4 기본동형사상정리(Fundamental Homomorphism Theorem)

***

## **📐 Chapter 2: 환론(Ring Theory)**

### **4. 환의 기초 정의 (Ring Basics)**

#### **4.1 환 공리 (Ring Axioms)**

- 4.1.1 덧셈군 구조 (Abelian Group)
- 4.1.2 곱셈의 결합법칙(Associativity)
- 4.1.3 분배법칙(Distributive Laws)
- 4.1.4 단위환(Unital Ring)과 무단위환(Non-unital)


#### **4.2 환의 예제**

- 4.2.1 정수환 (ℤ)
- 4.2.2 다항환 F[x]
- 4.2.3 행렬환 Mₙ(F)
- 4.2.4 함수환 C([a,b])


### **5. 아이디얼(Ideals) 및 몫환 (Ideals \& Quotient Rings)**

#### **5.1 아이디얼 정의**

- 5.1.1 좌/우/양쪽 아이디얼
- 5.1.2 예: nℤ, (x)⊆F[x]
- 5.1.3 극대아이디얼(Maximal Ideal)


#### **5.2 몫환(Quotient Rings)**

- 5.2.1 R/I 정의와 연산
- 5.2.2 자연사상(Natural Projection)
- 5.2.3 환의 동형사상정리(Isomorphism Theorems)


### **6. 정역과 필드(Domains \& Fields)**

#### **6.1 정역(Integral Domain)**

- 6.1.1 영약(Zero Divisors) 없음
- 6.1.2 예: ℤ, 다항환 F[x]
- 6.1.3 정역에서의 몫환의 성질


#### **6.2 유클리드 환과 PID**

- 6.2.1 유클리드 환(Euclidean Domain) 정의
- 6.2.2 PID(Principal Ideal Domain)
- 6.2.3 유클리드 → PID → UFD


#### **6.3 UFD와 고유인수분해(Unique Factorization Domain)**

- 6.3.1 원자(Atom)와 기약원소(Irreducible Elements)
- 6.3.2 고유인수분해정리
- 6.3.3 예제: ℤ[√–5]의 비UFD 성질


#### **6.4 체(Field)**

- 6.4.1 체의 정의
- 6.4.2 유한체(Finite Fields) 구조
- 6.4.3 다항식환 위의 극대아이디얼

***

## **📐 Chapter 3: 가군(Module Theory)**

### **7. 가군의 기초 (Module Basics)**

#### **7.1 R-가군 정의**

- 7.1.1 가군 공리: 모듈러 곱셈
- 7.1.2 벡터공간 vs 가군 차이


#### **7.2 가군 예제**

- 7.2.1 ℤ-가군 = 아벨군
- 7.2.2 F[x]-가군 = 선형 변환 구조


### **8. 가군 사상 및 몫가군**

- 8.1 모듈 사상(Module Homomorphism)
- 8.2 부분가군(Submodule)
- 8.3 몫가군(Quotient Module)

***

## **🔢 Chapter 4: 다항식환 (Polynomial Rings)**

### **9. 다항식환 F[x]**

- 9.1 다항식 연산 (덧셈, 곱셈)
- 9.2 인수분해와 근의 개념
- 9.3 분할환(Fraction Field) 구성


### **10. 유한체 위의 다항식**

- 10.1 분해체(Extension Fields)
- 10.2 최소다항식(Minimal Polynomial)
- 10.3 갈루아 군(Galois Group) 기초

***

## **🔗 Chapter 5: 갈루아 이론 (Galois Theory)**

### **11. 갈루아 확장(Galois Extensions)**

- 11.1 정상확장(Normal Extension)
- 11.2 분리확장(Separable Extension)
- 11.3 갈루아확장 정의


### **12. 갈루아 군(Galois Group)**

- 12.1 정의: Gal(E/F)
- 12.2 군 이론적 성질
- 12.3 기본 대응정리(Fundamental Theorem of Galois Theory)

***

**현대대수학 전체 개념을 subunit 레벨로 완전 분해했습니다.**
**모든 주요 수학 과목들의 세부 분해가 완료되었습니다!**

