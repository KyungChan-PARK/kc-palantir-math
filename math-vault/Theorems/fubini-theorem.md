---
type: theorem
id: fubini-theorem
domain: analysis
level: graduate
difficulty: 9
language: en
tags:
  - theorems
  - measure-theory
  - integration
  - analysis
  - real-analysis
  - functional-analysis
  - product-measures
  - multiple-integration
  - lebesgue-integration
prerequisites:
  - "[[measure-space]]"
  - "[[sigma-algebra]]"
  - "[[measurable-function]]"
  - "[[measure-theory]]"
  - "[[lebesgue-measure]]"
  - "[[lebesgue-integration]]"
  - "[[product-measure]]"
  - "[[product-sigma-algebra]]"
  - "[[sigma-finite-measure]]"
  - "[[integrable-function]]"
  - "[[l1-space]]"
  - "[[tonelli-theorem]]"
  - "[[almost-everywhere]]"
  - "[[iterated-integral]]"
  - "[[measurable-sets]]"
  - "[[complete-measure-space]]"
  - "[[null-set]]"
  - "[[absolute-integrability]]"
used-in:
  - "[[multiple-integration]]"
  - "[[probability-theory]]"
  - "[[stochastic-processes]]"
  - "[[joint-probability-distributions]]"
  - "[[partial-differential-equations]]"
  - "[[fourier-analysis]]"
  - "[[functional-analysis]]"
  - "[[convolution]]"
  - "[[product-measures]]"
  - "[[expectation-of-random-variables]]"
  - "[[moment-generating-functions]]"
  - "[[gaussian-integrals]]"
  - "[[statistical-independence]]"
related:
  - "[[tonelli-theorem]]"
  - "[[dominated-convergence-theorem]]"
  - "[[monotone-convergence-theorem]]"
  - "[[riemann-integration]]"
  - "[[cavalieri-principle]]"
  - "[[change-of-variables-theorem]]"
aliases:
  - Fubini's Theorem
  - Fubini-Tonelli Theorem
  - Fubini's Theorem on Product Measures
created: 2025-10-15
---

# Fubini's Theorem

## Definition

**Fubini's Theorem** is a fundamental result in [[measure-theory]] that provides conditions under which the order of [[iterated-integral|iterated integration]] can be interchanged, and when a double integral over a product space can be computed as an iterated integral. It is essential for evaluating multiple integrals in [[lebesgue-integration]] theory and forms the theoretical foundation for computing integrals in higher dimensions.

**Modern Statement (Measure-Theoretic Version):**

Let $(X, \mathcal{A}, \mu)$ and $(Y, \mathcal{B}, \nu)$ be [[sigma-finite-measure|σ-finite measure spaces]], and let $f: X \times Y \to \mathbb{R}$ (or $\mathbb{C}$) be a [[measurable-function]] with respect to the [[product-sigma-algebra]] $\mathcal{A} \otimes \mathcal{B}$.

**If $f$ is [[integrable-function|integrable]]** with respect to the [[product-measure]] $\mu \times \nu$ (i.e., $f \in L^1(X \times Y, \mu \times \nu)$), then:

1. For [[almost-everywhere|almost every]] $x \in X$, the function $y \mapsto f(x,y)$ is $\nu$-integrable
2. For almost every $y \in Y$, the function $x \mapsto f(x,y)$ is $\mu$-integrable
3. The functions:
   $$
   x \mapsto \int_Y f(x,y) \, d\nu(y) \quad \text{and} \quad y \mapsto \int_X f(x,y) \, d\mu(x)
   $$
   are integrable (defined almost everywhere)
4. The following equality holds:
   $$
   \int_{X \times Y} f \, d(\mu \times \nu) = \int_X \left( \int_Y f(x,y) \, d\nu(y) \right) d\mu(x) = \int_Y \left( \int_X f(x,y) \, d\mu(x) \right) d\nu(y)
   $$

**In notation:**
$$
\int_{X \times Y} f(x,y) \, d(\mu \times \nu) = \int_X \int_Y f(x,y) \, d\nu(y) \, d\mu(x) = \int_Y \int_X f(x,y) \, d\mu(x) \, d\nu(y)
$$

**Key Insight:** The critical hypothesis is **integrability** of $f$ on the product space. This is stronger than merely requiring measurability.

## Historical Context

Fubini's Theorem is named after Italian mathematician **Guido Fubini** (1879-1943), who published the result in 1907. The theorem resolved fundamental questions about when multiple integrals could be evaluated as iterated integrals, extending classical results from [[riemann-integration|Riemann integration]] to the more general setting of [[lebesgue-integration]].

**Historical Timeline:**

1. **Classical Results (17th-18th century)**: Informal interchange of integration order in calculus (Leibniz, Euler)

2. **Riemann (1854)**: Developed [[riemann-integration|Riemann integration]] theory, but limitations for multiple integration

3. **Lebesgue (1902)**: Created [[lebesgue-integration|Lebesgue integration theory]], enabling integration of much broader classes of functions

4. **Fubini (1907)**: Proved the theorem for [[lebesgue-measure]] on $\mathbb{R}^n$, establishing when iterated integrals equal double integrals

5. **Tonelli (1909)**: Extended to non-negative measurable functions (see [[tonelli-theorem]])

6. **Modern Measure Theory (1930s+)**: Generalized to abstract [[sigma-finite-measure|σ-finite measure spaces]] (Carathéodory, Halmos)

**Significance:** Before Fubini's work, mathematicians knew that changing integration order "usually" worked but lacked rigorous conditions. Fubini provided the precise theoretical framework, showing that [[absolute-integrability]] is the key condition.

## Prerequisites

To understand Fubini's Theorem, you need:

### Core Measure Theory

- **[[measure-space]]**: A triple $(X, \mathcal{A}, \mu)$ where $X$ is a set, $\mathcal{A}$ is a [[sigma-algebra]], and $\mu$ is a measure. This is the fundamental structure for modern integration theory.

- **[[sigma-algebra]]**: A collection of subsets closed under countable unions, intersections, and complements. Defines which sets are measurable.

- **[[measure-theory]]**: The systematic study of measures, measurable spaces, and integration. Provides the framework for generalizing Riemann integration.

- **[[lebesgue-measure]]**: The standard measure on $\mathbb{R}^n$ that extends length/area/volume. Most common application context for Fubini's Theorem.

- **[[sigma-finite-measure]]**: A measure where the whole space can be written as a countable union of sets with finite measure. This is a critical hypothesis for Fubini's Theorem.

### Measurability Concepts

- **[[measurable-function]]**: Functions where preimages of measurable sets are measurable. Essential for defining integration.

- **[[measurable-sets]]**: Sets belonging to the [[sigma-algebra]]. Only measurable sets can be assigned measures.

- **[[product-sigma-algebra]]**: The smallest σ-algebra on $X \times Y$ making projection maps measurable. Denoted $\mathcal{A} \otimes \mathcal{B}$.

- **[[almost-everywhere]]**: A property holding except on a [[null-set]] (set of measure zero). Many results in measure theory hold "almost everywhere."

### Integration Theory

- **[[lebesgue-integration]]**: Integration theory based on measures, more powerful than [[riemann-integration]]. Allows integration of more functions and better convergence theorems.

- **[[integrable-function]]**: A measurable function $f$ with $\int |f| \, d\mu < \infty$. The key hypothesis for Fubini's Theorem.

- **[[l1-space]]**: The space $L^1(X, \mu)$ of integrable functions. Fubini's Theorem requires $f \in L^1(X \times Y, \mu \times \nu)$.

- **[[absolute-integrability]]**: The condition $\int |f| \, d\mu < \infty$. Stronger than integrability of $f$ itself (in complex-valued case).

- **[[iterated-integral]]**: Integrals of the form $\int_X \int_Y f(x,y) \, dy \, dx$, where integration is performed sequentially.

### Product Measures

- **[[product-measure]]**: The unique measure $\mu \times \nu$ on $X \times Y$ satisfying $(\mu \times \nu)(A \times B) = \mu(A) \cdot \nu(B)$ for measurable rectangles.

- **[[null-set]]**: A set of measure zero. Important because properties holding almost everywhere are defined via null sets.

- **[[complete-measure-space]]**: A measure space where all subsets of null sets are measurable. Lebesgue measure is complete; product measures may need completion.

### Related Results

- **[[tonelli-theorem]]**: The "non-negative version" of Fubini. For non-negative measurable functions, integration order can be interchanged without requiring integrability. Often used to verify integrability before applying Fubini.

## Mathematical Details

### Precise Statement for σ-Finite Measures

**Theorem (Fubini):** Let $(X, \mathcal{A}, \mu)$ and $(Y, \mathcal{B}, \nu)$ be [[sigma-finite-measure|σ-finite]] [[measure-space|measure spaces]]. Let $f: X \times Y \to \mathbb{R}$ be $(\mathcal{A} \otimes \mathcal{B})$-[[measurable-function|measurable]].

**Hypothesis:** $f \in L^1(X \times Y, \mu \times \nu)$, i.e.,
$$
\int_{X \times Y} |f(x,y)| \, d(\mu \times \nu) < \infty
$$

**Conclusions:**

(i) For $\mu$-almost every $x \in X$, the function $f_x: y \mapsto f(x,y)$ is $\nu$-integrable:
$$
\int_Y |f(x,y)| \, d\nu(y) < \infty
$$

(ii) For $\nu$-almost every $y \in Y$, the function $f^y: x \mapsto f(x,y)$ is $\mu$-integrable:
$$
\int_X |f(x,y)| \, d\mu(x) < \infty
$$

(iii) The integral functions are integrable:
$$
\phi(x) := \int_Y f(x,y) \, d\nu(y) \in L^1(X, \mu)
$$
$$
\psi(y) := \int_X f(x,y) \, d\mu(x) \in L^1(Y, \nu)
$$

(iv) The equality of iterated integrals holds:
$$
\int_{X \times Y} f \, d(\mu \times \nu) = \int_X \phi(x) \, d\mu(x) = \int_Y \psi(y) \, d\nu(y)
$$

### Tonelli's Theorem (The Non-Negative Case)

**[[tonelli-theorem|Tonelli's Theorem]]** is often stated together with Fubini because it provides a practical way to verify integrability:

**Theorem (Tonelli):** Under the same setup, if $f \geq 0$ is a non-negative measurable function, then:
$$
\int_{X \times Y} f \, d(\mu \times \nu) = \int_X \left( \int_Y f(x,y) \, d\nu(y) \right) d\mu(x) = \int_Y \left( \int_X f(x,y) \, d\mu(x) \right) d\nu(y)
$$

**No integrability hypothesis needed!** The integrals may be infinite, but the equality still holds (with $\infty = \infty$ allowed).

**Practical Strategy:**
1. Apply [[tonelli-theorem|Tonelli]] to $|f|$ (which is non-negative) to compute $\int_{X \times Y} |f| \, d(\mu \times \nu)$
2. If this integral is finite, then $f$ is integrable
3. Now apply Fubini to $f$ to interchange integration order

### Classical Version (Lebesgue Measure on $\mathbb{R}^n$)

For [[lebesgue-measure]] on $\mathbb{R}^{m+n} = \mathbb{R}^m \times \mathbb{R}^n$:

If $f: \mathbb{R}^m \times \mathbb{R}^n \to \mathbb{R}$ is Lebesgue integrable, then:
$$
\int_{\mathbb{R}^{m+n}} f(x,y) \, dx\,dy = \int_{\mathbb{R}^m} \left( \int_{\mathbb{R}^n} f(x,y) \, dy \right) dx = \int_{\mathbb{R}^n} \left( \int_{\mathbb{R}^m} f(x,y) \, dx \right) dy
$$

This is the form most commonly encountered in analysis and probability courses.

### Importance of σ-Finiteness

The [[sigma-finite-measure|σ-finiteness]] hypothesis is essential. Without it, Fubini's Theorem **fails**.

**Counterexample (Non-σ-finite case):**

Let $X = Y = \mathbb{R}$ with $\mu$ = Lebesgue measure and $\nu$ = counting measure. The counting measure on $\mathbb{R}$ is **not σ-finite**.

Consider the diagonal function:
$$
f(x,y) = \begin{cases}
1 & \text{if } x = y \\
0 & \text{otherwise}
\end{cases}
$$

Then:
$$
\int_X \left( \int_Y f(x,y) \, d\nu(y) \right) d\mu(x) = \int_{\mathbb{R}} \infty \, dx = \infty
$$
$$
\int_Y \left( \int_X f(x,y) \, d\mu(x) \right) d\nu(y) = \int_{\mathbb{R}} 0 \, d\nu(y) = 0
$$

The iterated integrals are **not equal**! Fubini fails without σ-finiteness.

### Importance of Integrability

The integrability hypothesis cannot be weakened to mere measurability.

**Counterexample (Measurable but not integrable):**

Consider $f: [0,1] \times [0,1] \to \mathbb{R}$ defined by:
$$
f(x,y) = \frac{x^2 - y^2}{(x^2 + y^2)^2} \quad \text{for } (x,y) \neq (0,0)
$$
$$
f(0,0) = 0
$$

This function is measurable, and the iterated integrals exist but are **not equal**:
$$
\int_0^1 \left( \int_0^1 f(x,y) \, dy \right) dx = \frac{\pi}{4}
$$
$$
\int_0^1 \left( \int_0^1 f(x,y) \, dx \right) dy = -\frac{\pi}{4}
$$

The function is **not integrable**: $\int_{[0,1]^2} |f| = \infty$. Without integrability, Fubini fails.

## Proof Sketch

The proof of Fubini's Theorem uses the standard measure-theoretic technique of proving results in stages:

**Step 1: Characteristic functions of measurable rectangles**

For $A \in \mathcal{A}, B \in \mathcal{B}$, consider $f = \chi_{A \times B}$ (indicator function).

Then:
$$
\int_{X \times Y} \chi_{A \times B} \, d(\mu \times \nu) = (\mu \times \nu)(A \times B) = \mu(A) \cdot \nu(B)
$$

And:
$$
\int_X \left( \int_Y \chi_{A \times B}(x,y) \, d\nu(y) \right) d\mu(x) = \int_X \chi_A(x) \nu(B) \, d\mu(x) = \mu(A) \cdot \nu(B)
$$

Equality holds for rectangles.

**Step 2: Simple functions**

By linearity, extend to simple functions (finite linear combinations of characteristic functions):
$$
s = \sum_{i=1}^n c_i \chi_{E_i}
$$

where $E_i \in \mathcal{A} \otimes \mathcal{B}$.

**Step 3: Non-negative measurable functions**

Use the [[monotone-convergence-theorem]]: approximate any non-negative measurable $f$ by an increasing sequence of simple functions $s_n \uparrow f$.

By monotone convergence:
$$
\int_{X \times Y} f = \lim_{n \to \infty} \int_{X \times Y} s_n = \lim_{n \to \infty} \int_X \int_Y s_n
$$

By dominated convergence (or monotone convergence again):
$$
= \int_X \lim_{n \to \infty} \int_Y s_n = \int_X \int_Y f
$$

This proves **[[tonelli-theorem|Tonelli's Theorem]]**.

**Step 4: Integrable functions**

Decompose $f = f^+ - f^-$ where $f^+(x) = \max(f(x), 0)$ and $f^-(x) = \max(-f(x), 0)$.

Both $f^+$ and $f^-$ are non-negative and integrable (since $|f| = f^+ + f^-$ is integrable).

Apply Tonelli to both $f^+$ and $f^-$, then use linearity:
$$
\int_{X \times Y} f = \int_{X \times Y} f^+ - \int_{X \times Y} f^- = \int_X \int_Y f^+ - \int_X \int_Y f^- = \int_X \int_Y (f^+ - f^-) = \int_X \int_Y f
$$

This completes the proof of **Fubini's Theorem**. ∎

## Examples

### Example 1: Computing a Double Integral via Iteration

Compute:
$$
\int_0^1 \int_0^1 xy \, e^{xy} \, dy \, dx
$$

**Solution:**

Set $f(x,y) = xy e^{xy}$ on $[0,1] \times [0,1]$. Since $f$ is continuous on a compact set, it is integrable.

By Fubini, we can evaluate as an iterated integral:
$$
\int_0^1 \left( \int_0^1 xy e^{xy} \, dy \right) dx
$$

**Inner integral** (fix $x$, integrate over $y$):

Let $u = xy$, $du = x \, dy$:
$$
\int_0^1 xy e^{xy} \, dy = \int_0^x u e^u \, du = [ue^u - e^u]_0^x = xe^x - e^x + 1
$$

Wait, let me recalculate. For fixed $x$:
$$
\int_0^1 xy e^{xy} \, dy
$$

Use integration by parts: Let $u = y$, $dv = x e^{xy} \, dy$:
$$
v = e^{xy}, \quad du = dy
$$
$$
= [y e^{xy}]_0^1 - \int_0^1 e^{xy} \, dy = e^x - \left[ \frac{1}{x} e^{xy} \right]_0^1 = e^x - \frac{e^x - 1}{x} = \frac{xe^x - e^x + 1}{x}
$$

**Outer integral:**
$$
\int_0^1 \frac{xe^x - e^x + 1}{x} \, dx = \int_0^1 (e^x - \frac{e^x - 1}{x}) \, dx
$$

This integral requires special functions. The key point is that Fubini **guarantees** we can compute it as an iterated integral.

### Example 2: Interchanging Integration Order

Consider:
$$
I = \int_0^1 \int_y^1 f(x,y) \, dx \, dy
$$

We can change the order using Fubini. The region is $\{(x,y) : 0 \leq y \leq x \leq 1\}$.

Rewriting with $x$ first: $0 \leq x \leq 1$ and $0 \leq y \leq x$:
$$
I = \int_0^1 \int_0^x f(x,y) \, dy \, dx
$$

**Example application:** Compute $\int_0^1 \int_y^1 e^{x^2} \, dx \, dy$.

The inner integral $\int_y^1 e^{x^2} \, dx$ has no elementary antiderivative.

**Change order:**
$$
\int_0^1 \int_0^x e^{x^2} \, dy \, dx = \int_0^1 x e^{x^2} \, dx
$$

Now use $u = x^2$, $du = 2x \, dx$:
$$
= \frac{1}{2} \int_0^1 e^u \, du = \frac{1}{2}(e - 1)
$$

Fubini enables solving an otherwise intractable problem!

### Example 3: Verifying Integrability with Tonelli

Determine if $f(x,y) = \frac{e^{-x}}{1+y^2}$ on $[0,\infty) \times \mathbb{R}$ is integrable.

**Apply Tonelli to** $|f| = f$ (since $f \geq 0$):
$$
\int_0^\infty \int_{\mathbb{R}} \frac{e^{-x}}{1+y^2} \, dy \, dx = \int_0^\infty e^{-x} \left( \int_{\mathbb{R}} \frac{1}{1+y^2} \, dy \right) dx
$$

$$
= \int_0^\infty e^{-x} \cdot \pi \, dx = \pi \int_0^\infty e^{-x} \, dx = \pi
$$

Since $\int |f| = \pi < \infty$, the function **is integrable**, and Fubini applies.

### Example 4: Product of Functions (Independence in Probability)

In [[probability-theory]], if $X$ and $Y$ are independent random variables with densities $f_X$ and $f_Y$, their joint density is:
$$
f_{X,Y}(x,y) = f_X(x) f_Y(y)
$$

The [[expectation-of-random-variables|expectation]] of $g(X,Y)$ is:
$$
E[g(X,Y)] = \int_{\mathbb{R}^2} g(x,y) f_X(x) f_Y(y) \, dx \, dy
$$

**By Fubini** (assuming integrability):
$$
= \int_{\mathbb{R}} f_X(x) \left( \int_{\mathbb{R}} g(x,y) f_Y(y) \, dy \right) dx
$$

This enables computing expectations via iterated integrals, fundamental in [[statistical-independence]].

### Example 5: Computing Gaussian Integrals

The famous Gaussian integral relies on Fubini:
$$
I = \int_{-\infty}^\infty e^{-x^2} \, dx
$$

**Trick:** Consider $I^2$:
$$
I^2 = \left( \int_{-\infty}^\infty e^{-x^2} \, dx \right) \left( \int_{-\infty}^\infty e^{-y^2} \, dy \right)
$$

**By Fubini:**
$$
= \int_{-\infty}^\infty \int_{-\infty}^\infty e^{-x^2} e^{-y^2} \, dx \, dy = \int_{\mathbb{R}^2} e^{-(x^2 + y^2)} \, dx \, dy
$$

Switch to polar coordinates: $x^2 + y^2 = r^2$, $dx \, dy = r \, dr \, d\theta$:
$$
= \int_0^{2\pi} \int_0^\infty e^{-r^2} r \, dr \, d\theta = 2\pi \int_0^\infty e^{-r^2} r \, dr
$$

Let $u = r^2$, $du = 2r \, dr$:
$$
= 2\pi \cdot \frac{1}{2} \int_0^\infty e^{-u} \, du = \pi
$$

Therefore $I = \sqrt{\pi}$.

Fubini is **essential** for this classic calculation!

### Example 6: Fubini Fails Without Integrability

Consider:
$$
f(x,y) = \frac{x^2 - y^2}{(x^2 + y^2)^2}
$$

on the unit square $[0,1] \times [0,1]$ (set $f(0,0) = 0$).

**Iterated integral 1:**
$$
\int_0^1 \left( \int_0^1 \frac{x^2 - y^2}{(x^2 + y^2)^2} \, dy \right) dx = \frac{\pi}{4}
$$

**Iterated integral 2:**
$$
\int_0^1 \left( \int_0^1 \frac{x^2 - y^2}{(x^2 + y^2)^2} \, dx \right) dy = -\frac{\pi}{4}
$$

**Why different?** Because $f$ is **not integrable**:
$$
\int_0^1 \int_0^1 |f(x,y)| \, dy \, dx = \infty
$$

Fubini's hypothesis fails, so the theorem does not apply.

## Applications

Fubini's Theorem is ubiquitous in analysis, probability, and applied mathematics:

### 1. [[multiple-integration]]

Evaluating integrals over higher-dimensional regions by reducing to iterated one-dimensional integrals. Essential in calculus, physics, and engineering.

### 2. [[probability-theory]]

Computing probabilities and expectations for multi-dimensional random variables. The foundation for:
- [[joint-probability-distributions]]
- [[expectation-of-random-variables]]
- [[moment-generating-functions]]
- [[statistical-independence]]

**Example:** If $X, Y$ are independent, $E[XY] = E[X]E[Y]$ follows from Fubini.

### 3. [[convolution]]

The convolution of functions $f$ and $g$ is:
$$
(f * g)(x) = \int_{\mathbb{R}} f(x-y) g(y) \, dy
$$

Properties like associativity and commutativity rely on Fubini to interchange integration orders.

### 4. [[fourier-analysis]]

The [[fourier-analysis|Fourier transform]] interchanges with integration:
$$
\mathcal{F}\left( \int f(x,y) \, dy \right) = \int \mathcal{F}_x(f(x,y)) \, dy
$$

This requires Fubini to justify interchanging the Fourier integral with the $y$-integral.

### 5. [[partial-differential-equations]]

Solution representations using Green's functions often involve double integrals that are evaluated via Fubini.

### 6. [[stochastic-processes]]

Computing expectations of functionals of stochastic processes, integrating over product probability spaces.

### 7. [[gaussian-integrals]]

Evaluating multidimensional Gaussian integrals, fundamental in physics (path integrals), statistics (multivariate normal distributions), and quantum field theory.

### 8. Changing Integration Order for Simplification

Many integrals are intractable in one order but simple in another. Fubini guarantees when this interchange is valid.

### 9. [[change-of-variables-theorem]]

Combined with change of variables (Jacobian formula), Fubini enables powerful integral transformations.

### 10. Volume Calculations

Computing volumes of regions in $\mathbb{R}^n$ using iterated integrals (Cavalieri's principle generalized).

## Relationship to Tonelli's Theorem

**[[tonelli-theorem|Tonelli's Theorem]]** and Fubini's Theorem are closely related:

| **Aspect** | **Fubini** | **Tonelli** |
|------------|-----------|------------|
| **Functions** | Integrable (possibly sign-changing) | Non-negative measurable |
| **Hypothesis** | $f \in L^1(X \times Y)$ | $f \geq 0$ measurable |
| **Conclusion** | Iterated integrals equal double integral | Same, but may be $\infty$ |
| **Use case** | Computing integrals when integrability is known | Verifying integrability |

**Practical workflow:**

1. **Want to apply Fubini** to function $f$
2. **Check integrability:** Apply Tonelli to $|f|$ (non-negative):
   $$
   \int_{X \times Y} |f| = \int_X \int_Y |f(x,y)| \, d\nu \, d\mu
   $$
3. **If finite:** $f$ is integrable, apply Fubini
4. **If infinite:** Fubini does not apply; be careful!

**Mnemonic:** "Tonelli to check, Fubini to compute."

## Common Pitfalls and Misconceptions

### Pitfall 1: Forgetting to check integrability

**Wrong:** "The function is continuous, so I can interchange integrals."

**Correct:** Even continuous functions may not be integrable on unbounded domains. Always verify $\int |f| < \infty$.

### Pitfall 2: Assuming measurability implies integrability

Measurable functions need not be integrable. The counterexample $f(x,y) = \frac{x^2 - y^2}{(x^2+y^2)^2}$ is measurable but not integrable.

### Pitfall 3: Ignoring σ-finiteness

On non-σ-finite spaces, Fubini fails. Always check that measures are σ-finite.

### Pitfall 4: Confusing Fubini with Tonelli

- **Fubini:** Requires integrability, allows sign-changing functions
- **Tonelli:** Requires non-negativity, does not require integrability

Use Tonelli to verify integrability, then apply Fubini.

### Pitfall 5: Applying to infinite sums incorrectly

Interchanging sum and integral is a special case of Fubini (with counting measure), but requires absolute summability:
$$
\sum_{n=1}^\infty \int f_n < \infty
$$

## Generalizations and Extensions

### Fubini for Complex-Valued Functions

For $f: X \times Y \to \mathbb{C}$, Fubini applies if:
$$
\int_{X \times Y} |f| \, d(\mu \times \nu) < \infty
$$

Decompose into real and imaginary parts and apply Fubini to each.

### Fubini for Vector-Valued Functions

For $f: X \times Y \to \mathbb{R}^n$ (or Banach space), Fubini applies if:
$$
\int_{X \times Y} \|f\| \, d(\mu \times \nu) < \infty
$$

Apply component-wise.

### Multiple Products

For $k$ spaces $(X_i, \mathcal{A}_i, \mu_i)$, $i = 1, \ldots, k$, Fubini extends to:
$$
\int_{X_1 \times \cdots \times X_k} f \, d(\mu_1 \times \cdots \times \mu_k) = \int_{X_1} \cdots \int_{X_k} f(x_1, \ldots, x_k) \, d\mu_k \cdots d\mu_1
$$

All permutations of integration order give the same result.

### Radon-Nikodým and Conditional Expectations

In probability, Fubini underlies the [[radon-nikodym-theorem]] and the tower property of [[conditional-expectation]].

## Pedagogical Notes

**Common Student Difficulties:**

1. **Understanding product measures:** Students often struggle with $\mu \times \nu$ vs. iterated integrals
2. **Checking integrability:** Forgetting to verify $\int |f| < \infty$ before applying Fubini
3. **Tonelli vs. Fubini:** Confusion about when to use which theorem
4. **Measure theory prerequisite:** Fubini requires solid foundation in measure theory

**Teaching Recommendations:**

1. **Start with Tonelli:** Use Tonelli to motivate Fubini (non-negative case first)
2. **Emphasize integrability:** Show counterexamples where Fubini fails without integrability
3. **Connect to calculus:** Show how classical calculus results are special cases
4. **Use probability examples:** Independence and expectations provide intuitive applications
5. **Practice changing integration order:** Give exercises on sketching regions and rewriting limits

**Conceptual Understanding:**

- Fubini says: "Integration over a product space can be done one variable at a time"
- The price: Must check that $f$ is integrable on the product
- The reward: Reduces high-dimensional integrals to iterated one-dimensional integrals

## Related Theorems and Concepts

- **[[tonelli-theorem]]**: Non-negative version; used to verify integrability for Fubini

- **[[dominated-convergence-theorem]]**: Allows interchanging limits and integrals; often used with Fubini

- **[[monotone-convergence-theorem]]**: Used in proving Fubini for non-negative functions

- **[[cavalieri-principle]]**: Classical geometric version (volumes via cross-sectional areas)

- **[[product-measure]]**: The measure $\mu \times \nu$ on product spaces; Fubini's domain

- **[[change-of-variables-theorem]]**: Combined with Fubini for advanced integral transformations

- **[[riemann-integration]]**: Classical integration theory; Fubini provides the measure-theoretic generalization

## Historical Note: Why "Fubini-Tonelli"?

Some authors refer to "Fubini-Tonelli Theorem" to emphasize both contributions:

- **Fubini (1907):** Integrable functions, interchanging integration order
- **Tonelli (1909):** Non-negative functions, no integrability required

Together, they provide a complete theory for iterated integration in measure theory.

## Further Reading

- **[[measure-theory]]**: The foundational framework for Fubini's Theorem
- **[[lebesgue-integration]]**: The integration theory where Fubini is most powerful
- **[[product-measure]]**: Understanding $\mu \times \nu$ is essential
- **[[tonelli-theorem]]**: The companion result for non-negative functions
- **[[probability-theory]]**: Major application domain (independence, expectations)
- **[[fourier-analysis]]**: Uses Fubini extensively for transforms
- **[[convolution]]**: Relies on Fubini for properties
- **[[dominated-convergence-theorem]]**: Another fundamental result in integration theory

## References

1. Rudin, W. (1987). *Real and Complex Analysis* (3rd ed.). McGraw-Hill. (Chapter 8: Integration on Product Spaces)
2. Folland, G. B. (1999). *Real Analysis: Modern Techniques and Their Applications* (2nd ed.). Wiley. (Chapter 2: Integration)
3. Royden, H. L., & Fitzpatrick, P. M. (2010). *Real Analysis* (4th ed.). Prentice Hall. (Chapter 7: Measure and Integration)
4. Dudley, R. M. (2002). *Real Analysis and Probability*. Cambridge University Press. (Chapter 4: Product Measures)
5. Tao, T. (2011). *An Introduction to Measure Theory*. American Mathematical Society. (Section 1.7: Fubini and Tonelli theorems)
6. Halmos, P. R. (1950). *Measure Theory*. Van Nostrand. (Chapter 36: Product Measures)
7. Fubini, G. (1907). "Sugli integrali multipli." *Rendiconti Accademia Nazionale dei Lincei*, 16(1), 608-614. (Original paper)
8. [Wikipedia: Fubini's Theorem](https://en.wikipedia.org/wiki/Fubini%27s_theorem)
9. [Wolfram MathWorld: Fubini's Theorem](https://mathworld.wolfram.com/FubinisTheorem.html)
10. [nLab: Fubini Theorem](https://ncatlab.org/nlab/show/Fubini+theorem)

---

**Keywords**: Fubini's theorem, iterated integrals, product measures, measure theory, Lebesgue integration, Tonelli theorem, σ-finite measures, multiple integration, probability theory, interchange of integration order

**See also**: [[tonelli-theorem]], [[product-measure]], [[lebesgue-integration]], [[measure-theory]], [[iterated-integral]], [[sigma-finite-measure]], [[dominated-convergence-theorem]], [[probability-theory]]
