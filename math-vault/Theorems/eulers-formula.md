---
type: theorem
id: eulers-formula
domain: complex-analysis
level: undergraduate
difficulty: 6
language: en
tags:
  - theorems
  - complex-analysis
  - exponential-functions
  - trigonometry
  - mathematical-constants
prerequisites:
  - "[[complex-numbers]]"
  - "[[exponential-functions]]"
  - "[[trigonometric-functions]]"
  - "[[taylor-series]]"
  - "[[power-series]]"
  - "[[calculus]]"
  - "[[polar-coordinates]]"
  - "[[analytic-functions]]"
  - "[[mathematical-constants]]"
used-in:
  - "[[eulers-identity]]"
  - "[[de-moivres-theorem]]"
  - "[[complex-exponential-function]]"
  - "[[fourier-analysis]]"
  - "[[trigonometric-identities]]"
  - "[[polar-form-complex-numbers]]"
  - "[[harmonic-oscillators]]"
  - "[[quantum-mechanics]]"
  - "[[cis-function]]"
  - "[[complex-logarithm]]"
related:
  - "[[hyperbolic-functions]]"
  - "[[complex-analysis]]"
aliases:
  - Euler's Identity
  - e^(iπ)+1=0
  - Euler Formula
  - Complex Exponential
created: 2025-10-14
---

# Euler's Formula

## Definition

**Euler's formula** establishes the fundamental relationship between the exponential function and trigonometric functions in the complex plane. For any real number $x$:

$$
e^{ix} = \cos(x) + i\sin(x)
$$

where:
- $e$ is Euler's number (the base of natural logarithms, approximately 2.71828)
- $i$ is the imaginary unit ($i^2 = -1$ or $i = \sqrt{-1}$)
- $\cos(x)$ and $\sin(x)$ are the cosine and sine trigonometric functions

This formula provides the exponential form of complex numbers and bridges algebra, geometry, and analysis by connecting exponential and trigonometric functions.

## Historical Context

Euler's formula was first published by **Leonhard Euler** in 1748 in his work *"Introductio in analysin infinitorum"*. While Roger Cotes had worked with equivalent expressions earlier (1714), Euler was the first to publish the formula in its modern exponential form. The formula has become one of the most celebrated equations in mathematics, particularly its special case known as [[eulers-identity]].

## Prerequisites

To understand Euler's formula, you need:

- **[[complex-numbers]]**: Understanding of the complex plane, imaginary unit $i$, and arithmetic operations with complex numbers is essential for comprehending how exponential functions can have complex arguments.

- **[[exponential-functions]]**: Knowledge of $e^x$ and properties of exponential functions, including their behavior, derivatives, and series representations.

- **[[trigonometric-functions]]**: Familiarity with sine and cosine functions, their properties, periodicity, and graphical behavior.

- **[[taylor-series]]**: Understanding Taylor series expansions is crucial for the rigorous derivation of Euler's formula through power series analysis.

- **[[power-series]]**: Need to understand infinite series, their convergence properties, and how functions can be represented as power series.

- **[[calculus]]**: Derivatives, limits, and the fundamental concepts of calculus are necessary for understanding series expansions and the behavior of exponential and trigonometric functions.

- **[[polar-coordinates]]**: Helpful for understanding the geometric interpretation of complex numbers and how angles relate to complex exponentials.

- **[[analytic-functions]]**: Understanding analytic continuation helps appreciate the extension of real functions to the complex domain.

- **[[mathematical-constants]]**: Familiarity with $e$ and $\pi$ enriches appreciation of the formula's special cases.

## Mathematical Details

### Main Formula

$$
e^{ix} = \cos(x) + i\sin(x)
$$

Using angle notation $\theta$ instead of $x$:

$$
e^{i\theta} = \cos(\theta) + i\sin(\theta)
$$

### Alternative Form with Magnitude

For any complex number in polar form with magnitude $r$ and angle $\theta$:

$$
re^{i\theta} = r(\cos(\theta) + i\sin(\theta))
$$

### Magnitude Property

For any real number $x$:

$$
|e^{ix}| = 1
$$

This shows that $e^{ix}$ always lies on the unit circle in the complex plane.

### Key Properties

**Periodicity**: The complex exponential is periodic with period $2\pi$:

$$
e^{2\pi i} = 1
$$

### Inverse Relations (Derived from Euler's Formula)

From Euler's formula and its conjugate $e^{-ix} = \cos(x) - i\sin(x)$, we can derive:

**Cosine in terms of complex exponentials:**
$$
\cos(x) = \frac{e^{ix} + e^{-ix}}{2}
$$

**Sine in terms of complex exponentials:**
$$
\sin(x) = \frac{e^{ix} - e^{-ix}}{2i}
$$

These expressions are fundamental in [[fourier-analysis]] and signal processing.

## Rigorous Derivation (Taylor Series Method)

### Step 1: Taylor Series for Exponential Function

The exponential function has the Taylor series expansion:

$$
e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots
$$

### Step 2: Substitute $ix$ for $x$

$$
e^{ix} = \sum_{n=0}^{\infty} \frac{(ix)^n}{n!} = 1 + ix + \frac{(ix)^2}{2!} + \frac{(ix)^3}{3!} + \frac{(ix)^4}{4!} + \frac{(ix)^5}{5!} + \cdots
$$

### Step 3: Simplify Using Powers of $i$

Recall that:
- $i^0 = 1$
- $i^1 = i$
- $i^2 = -1$
- $i^3 = -i$
- $i^4 = 1$ (pattern repeats)

Substituting:

$$
e^{ix} = 1 + ix + \frac{-x^2}{2!} + \frac{-ix^3}{3!} + \frac{x^4}{4!} + \frac{ix^5}{5!} - \frac{x^6}{6!} - \frac{ix^7}{7!} + \cdots
$$

### Step 4: Separate Real and Imaginary Parts

$$
e^{ix} = \left(1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots\right) + i\left(x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots\right)
$$

### Step 5: Recognize Taylor Series

The real part is the Taylor series for cosine:

$$
\cos(x) = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots
$$

The imaginary part is the Taylor series for sine:

$$
\sin(x) = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots
$$

### Conclusion

$$
e^{ix} = \cos(x) + i\sin(x)
$$

This completes the proof. ∎

## Alternative Derivation Methods

1. **Differential Equations**: Solve the differential equation $f'(x) = if(x)$ with initial condition $f(0) = 1$

2. **Geometric Approach**: Using properties of complex multiplication and rotation in the complex plane

3. **Analytic Continuation**: Extending the real exponential function to the complex domain using properties of [[analytic-functions]]

## Geometric Interpretation

On the complex plane, $e^{i\theta}$ represents a point on the **unit circle** at angle $\theta$ from the positive real axis. As $\theta$ varies from $0$ to $2\pi$, $e^{i\theta}$ traces out the unit circle counterclockwise.

This provides a natural connection between:
- **Rotations** (geometric operations)
- **Exponentials** (algebraic operations)

The formula reveals that multiplication by $e^{i\theta}$ in the complex plane corresponds to rotation by angle $\theta$.

- The real part $\cos(\theta)$ is the $x$-coordinate
- The imaginary part $\sin(\theta)$ is the $y$-coordinate

## Special Cases

### Euler's Identity ($x = \pi$)

When $x = \pi$, Euler's formula yields **[[eulers-identity]]**, often called the most beautiful equation in mathematics:

$$
e^{i\pi} + 1 = 0
$$

or equivalently:

$$
e^{i\pi} = -1
$$

This elegantly connects five fundamental mathematical constants:
- $e$ (Euler's number, base of natural logarithms)
- $i$ (imaginary unit)
- $\pi$ (pi, ratio of circle's circumference to diameter)
- $1$ (multiplicative identity)
- $0$ (additive identity)

### Full Rotation ($x = 2\pi$)

$$
e^{2\pi i} = \cos(2\pi) + i\sin(2\pi) = 1 + 0i = 1
$$

This demonstrates the $2\pi$ periodicity of complex exponentials, reflecting the periodic nature of trigonometric functions.

### Quarter Rotation ($x = \pi/2$)

$$
e^{i\pi/2} = \cos(\pi/2) + i\sin(\pi/2) = 0 + i = i
$$

This shows that $i$ can be expressed as $e^{i\pi/2}$, revealing $i$ as a rotation operator by 90 degrees.

### Half Rotation ($x = \pi$)

$$
e^{i\pi} = \cos(\pi) + i\sin(\pi) = -1 + 0i = -1
$$

## Examples

### Example 1: Computing $e^{i\pi/4}$

Using Euler's formula with $x = \pi/4$:

$$
e^{i\pi/4} = \cos(\pi/4) + i\sin(\pi/4) = \frac{\sqrt{2}}{2} + i\frac{\sqrt{2}}{2} = \frac{\sqrt{2}}{2}(1 + i)
$$

This represents a point on the unit circle at 45 degrees from the positive real axis.

### Example 2: Converting Complex Number to Polar Form

Convert $z = 1 + i$ to polar form using Euler's formula.

**Step 1:** Find magnitude $r$:
$$
r = |z| = \sqrt{1^2 + 1^2} = \sqrt{2}
$$

**Step 2:** Find angle $\theta$:
$$
\theta = \arctan(1/1) = \pi/4
$$

**Step 3:** Express using Euler's formula:
$$
z = \sqrt{2} e^{i\pi/4}
$$

### Example 3: Simplifying $(1+i)^{10}$

First convert to polar form: $1 + i = \sqrt{2} e^{i\pi/4}$

Then:
$$
(1+i)^{10} = \left(\sqrt{2} e^{i\pi/4}\right)^{10} = (\sqrt{2})^{10} e^{i10\pi/4} = 2^5 e^{i5\pi/2} = 32 e^{i\pi/2} = 32i
$$

This demonstrates how Euler's formula simplifies complex number exponentiation.

### Example 4: Proving Trigonometric Identity

Using Euler's formula to prove $\cos(2x) = \cos^2(x) - \sin^2(x)$:

$$
e^{2ix} = \cos(2x) + i\sin(2x)
$$

Also:
$$
e^{2ix} = (e^{ix})^2 = (\cos(x) + i\sin(x))^2 = \cos^2(x) - \sin^2(x) + 2i\cos(x)\sin(x)
$$

Comparing real parts: $\cos(2x) = \cos^2(x) - \sin^2(x)$ ✓

### Example 5: Deriving Sum Formula

Using Euler's formula to derive $\cos(A+B)$:

$$
e^{i(A+B)} = e^{iA} \cdot e^{iB}
$$

$$
\cos(A+B) + i\sin(A+B) = (\cos A + i\sin A)(\cos B + i\sin B)
$$

Expanding the right side and equating real parts:

$$
\cos(A+B) = \cos A \cos B - \sin A \sin B
$$

## Applications

Euler's formula is fundamental across mathematics, physics, and engineering:

### 1. [[polar-form-complex-numbers]]
Allows expressing complex numbers as $z = re^{i\theta}$, which simplifies:
- **Multiplication**: $r_1e^{i\theta_1} \cdot r_2e^{i\theta_2} = r_1r_2 e^{i(\theta_1+\theta_2)}$
- **Division**: $\frac{r_1e^{i\theta_1}}{r_2e^{i\theta_2}} = \frac{r_1}{r_2} e^{i(\theta_1-\theta_2)}$
- **Exponentiation**: $(re^{i\theta})^n = r^n e^{in\theta}$ (leads to [[de-moivres-theorem]])

### 2. [[fourier-analysis]]
Complex exponentials $e^{2\pi i f t}$ form the basis for Fourier transforms:
$$
F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt
$$

Used extensively in signal processing, image processing, and data compression.

### 3. [[quantum-mechanics]]
Wave functions are expressed using complex exponentials:
$$
\psi(x,t) = A e^{i(kx - \omega t)}
$$

The time evolution operator in the Schrödinger equation relies on $e^{-iHt/\hbar}$.

### 4. Alternating Current (AC) Circuit Analysis
Electrical engineers use phasor analysis where voltages and currents are represented as:
$$
V(t) = V_0 e^{i\omega t}
$$

This simplifies the analysis of [[harmonic-oscillators]] and RLC circuits.

### 5. Differential Equations with Complex Roots
Solutions to differential equations with complex characteristic roots are expressed using Euler's formula:
$$
y(t) = e^{\alpha t}(C_1 \cos(\beta t) + C_2 \sin(\beta t))
$$

### 6. [[trigonometric-identities]]
Many trigonometric identities become trivial to prove using Euler's formula and complex exponentials.

### 7. [[complex-exponential-function]]
Euler's formula provides the definition for extending the exponential function from real to complex arguments, enabling [[complex-analysis]].

### 8. Control Systems and Stability Analysis
System transfer functions are analyzed using complex exponentials and the Laplace transform, which relies on Euler's formula.

### 9. Wave Phenomena
Description of electromagnetic waves, acoustic waves, and mechanical vibrations all utilize Euler's formula for representing oscillatory behavior.

### 10. Signal Processing
Digital and analog signal analysis, filters, and transforms all build on Euler's formula as a fundamental tool.

## Related Concepts

- **[[eulers-identity]]**: Special case when $x = \pi$, yielding $e^{i\pi} + 1 = 0$
- **[[de-moivres-theorem]]**: States that $(\cos\theta + i\sin\theta)^n = \cos(n\theta) + i\sin(n\theta)$, elegantly proven using Euler's formula
- **[[cis-function]]**: Alternative notation where $\text{cis}(\theta) = \cos(\theta) + i\sin(\theta) = e^{i\theta}$
- **[[complex-logarithm]]**: The inverse of the complex exponential function
- **[[hyperbolic-functions]]**: Analogous relationships exist between exponentials and hyperbolic functions ($\cosh$ and $\sinh$)
- **[[complex-exponential-function]]**: General extension to complex arguments $e^{z}$ where $z = x + iy$
- **[[fourier-series]]**: Representation of periodic functions using complex exponentials
- **[[laplace-transform]]**: Integral transform that uses complex exponentials for solving differential equations
- **[[phasor-representation]]**: Representation of sinusoidal signals using complex exponentials in electrical engineering
- **[[conformal-mapping]]**: Geometric transformations using complex functions
- **[[residue-theorem]]**: Advanced application of complex analysis using contour integration
- **[[wave-equations]]**: Differential equations describing wave phenomena using Euler's formula

## Significance

Euler's formula is considered one of the most important and elegant formulas in mathematics because it:

1. **Unifies different branches**: Connects algebra (complex numbers), geometry (unit circle), and analysis (exponential and trigonometric functions)

2. **Simplifies calculations**: Transforms difficult trigonometric problems into easier exponential manipulations

3. **Reveals deep structure**: Shows that trigonometric functions are projections of circular motion in the complex plane

4. **Enables applications**: Makes advanced techniques in physics and engineering tractable

5. **Aesthetic beauty**: Especially in its special case ([[eulers-identity]]), it connects fundamental constants in an unexpectedly simple relationship

Richard Feynman called Euler's formula "one of the most remarkable, almost astounding, formulas in all of mathematics."

Euler's formula represents a major breakthrough in mathematics, bridging previously separate areas of study:
- Exponential functions (algebra)
- Trigonometric functions (geometry)
- Complex numbers (abstract algebra)
- Analysis (calculus and infinite series)

## Further Reading

- [[complex-analysis]]: Full theory of complex functions and their properties
- [[analytic-functions]]: Functions that can be represented by convergent power series
- [[conformal-mapping]]: Geometric transformations using complex functions
- [[residue-theorem]]: Advanced application of complex analysis using contour integration
- [[fourier-transform]]: Transform theory built on complex exponentials
- [[wave-equations]]: Differential equations describing wave phenomena using Euler's formula

## References

1. Euler, L. (1748). *Introductio in analysin infinitorum*. Lausanne.
2. Nahin, P. J. (2006). *Dr. Euler's Fabulous Formula*. Princeton University Press.
3. Stillwell, J. (2002). *Mathematics and Its History*. Springer.
4. [Wikipedia: Euler's Formula](https://en.wikipedia.org/wiki/Euler%27s_formula)
5. [Wolfram MathWorld: Euler's Formula](https://mathworld.wolfram.com/EulersFormula.html)
6. [Brilliant.org: Euler's Formula](https://brilliant.org/wiki/eulers-formula/)
7. [Better Explained: Intuitive Understanding](https://betterexplained.com/articles/intuitive-understanding-of-eulers-formula/)

---

**Keywords**: Euler's formula, complex exponentials, trigonometric functions, complex analysis, Euler's identity, exponential form, unit circle, Taylor series, polar form

**See also**: [[exponential-functions]], [[complex-numbers]], [[trigonometric-functions]], [[eulers-identity]], [[de-moivres-theorem]], [[fourier-analysis]]
