---
type: theorem
id: eulers-formula
domain: complex-analysis
level: undergraduate
difficulty: 6
language: en
prerequisites:
  - "[[complex-numbers]]"
  - "[[imaginary-unit]]"
  - "[[exponential-functions]]"
  - "[[eulers-number]]"
  - "[[trigonometric-functions]]"
  - "[[pi]]"
  - "[[taylor-series]]"
  - "[[power-series]]"
  - "[[calculus]]"
used-in:
  - "[[de-moivres-theorem]]"
  - "[[fourier-analysis]]"
  - "[[complex-exponential-function]]"
  - "[[trigonometric-identities]]"
  - "[[unit-circle]]"
  - "[[hyperbolic-functions]]"
  - "[[cauchys-formula]]"
  - "[[quantum-mechanics]]"
  - "[[polar-form-complex-numbers]]"
tags:
  - complex-analysis
  - theorems
  - euler
  - exponential-functions
  - trigonometry
  - mathematical-constants
created: 2025-10-15
---

# Euler's Formula

## Definition

**Euler's formula** establishes the fundamental relationship between the exponential function and trigonometric functions in the complex plane. For any real number $x$:

$$e^{ix} = \cos(x) + i\sin(x)$$

where:
- $e$ is [[eulers-number|Euler's number]] ($e \approx 2.71828$, the base of the natural logarithm)
- $i$ is the [[imaginary-unit]] ($i = \sqrt{-1}$, where $i^2 = -1$)
- $x$ is any real number (typically representing an angle in radians)
- $\cos(x)$ and $\sin(x)$ are the [[trigonometric-functions|cosine and sine functions]]

This formula reveals that the [[complex-exponential-function|complex exponential]] can be expressed entirely in terms of real trigonometric functions, creating a profound bridge between algebra, analysis, and geometry.

## The Formula

### General Form

$$e^{ix} = \cos(x) + i\sin(x)$$

### Euler's Identity (Special Case)

When $x = \pi$, Euler's formula yields what is often called **the most beautiful equation in mathematics**:

$$e^{i\pi} + 1 = 0$$

Or equivalently:

$$e^{i\pi} = -1$$

This remarkable identity connects five of the most fundamental constants in mathematics:
- $e$ (Euler's number, base of natural logarithm)
- $i$ (imaginary unit, foundation of [[complex-numbers]])
- $\pi$ ([[pi]], ratio of circle's circumference to diameter)
- $1$ (multiplicative identity)
- $0$ (additive identity)

### Other Important Forms

**Periodicity**: The complex exponential repeats every $2\pi$ radians:
$$e^{2\pi i} = 1$$

**Polar form of complex numbers**: For any complex number with magnitude $r$ and argument $\theta$:
$$z = re^{i\theta} = r(\cos(\theta) + i\sin(\theta))$$

**Inverse formulas**: Euler's formula can be inverted to express trigonometric functions using exponentials:
$$\cos(x) = \frac{e^{ix} + e^{-ix}}{2}$$

$$\sin(x) = \frac{e^{ix} - e^{-ix}}{2i}$$

**Unit circle property**: For all real $x$:
$$|e^{ix}| = \sqrt{\cos^2(x) + \sin^2(x)} = 1$$

This means $e^{ix}$ always lies on the [[unit-circle]] in the [[complex-plane]].

## Prerequisites

To understand Euler's formula, you need:

- **[[complex-numbers]]**: Understanding of complex numbers in the form $a + bi$ and their arithmetic operations
- **[[imaginary-unit]]**: Knowledge that $i = \sqrt{-1}$ with $i^2 = -1$, $i^3 = -i$, $i^4 = 1$
- **[[exponential-functions]]**: Properties of $e^x$ including $e^{x+y} = e^x \cdot e^y$
- **[[eulers-number]]**: The constant $e \approx 2.71828$ as the base of natural logarithms
- **[[trigonometric-functions]]**: Sine and cosine functions, their properties and graphs
- **[[pi]]**: Understanding $\pi$ as the fundamental circle constant
- **[[taylor-series]]**: Infinite series expansions of functions (needed for the standard proof)
- **[[power-series]]**: Convergence of infinite series
- **[[calculus]]**: Derivatives, limits, and infinite series

**Recommended background**:
- **[[complex-plane]]**: Geometric interpretation of complex numbers
- **[[polar-coordinates]]**: Representing points using radius and angle
- **[[complex-analysis]]**: Deeper understanding of complex functions
- **[[analytic-functions]]**: Extension of functions to the complex domain

## Intuition

### Geometric Interpretation

The most intuitive way to understand Euler's formula is through the [[complex-plane]]:

- **The unit circle**: As $x$ varies from $0$ to $2\pi$, the point $e^{ix}$ traces out the [[unit-circle]] in the complex plane
- **Angle representation**: The value $x$ represents the angle (in radians) from the positive real axis
- **Position on circle**: The real part $\cos(x)$ is the horizontal coordinate, the imaginary part $\sin(x)$ is the vertical coordinate
- **Rotation**: Multiplying by $e^{ix}$ rotates a complex number by angle $x$ counterclockwise

### Why It Matters

Euler's formula is not merely a curiosity—it is a fundamental tool that:

1. **Unifies mathematics**: Connects exponential functions, trigonometry, complex numbers, and geometry
2. **Simplifies calculations**: Converting between exponential and trigonometric forms makes many problems tractable
3. **Enables applications**: Foundation for Fourier analysis, quantum mechanics, signal processing, and electrical engineering
4. **Reveals structure**: Shows deep relationships between seemingly unrelated areas of mathematics
5. **Beautiful simplicity**: Euler's identity ($e^{i\pi} + 1 = 0$) elegantly connects fundamental constants

### Visual Understanding

Think of $e^{ix}$ as a **rotating arrow** in the complex plane:
- At $x = 0$: $e^{i \cdot 0} = 1$ (pointing right along real axis)
- At $x = \pi/2$: $e^{i\pi/2} = i$ (pointing up along imaginary axis)
- At $x = \pi$: $e^{i\pi} = -1$ (pointing left along real axis)
- At $x = 3\pi/2$: $e^{i \cdot 3\pi/2} = -i$ (pointing down)
- At $x = 2\pi$: $e^{i \cdot 2\pi} = 1$ (back to start—periodicity!)

## Proof

### Taylor Series Proof (Standard)

This is the most common and rigorous proof, accessible to students with [[calculus]] and [[taylor-series]] background.

**Step 1**: Start with the [[taylor-series]] expansion of $e^x$ for real $x$:

$$e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots$$

**Step 2**: Substitute $ix$ for $x$ (extending to complex domain):

$$e^{ix} = \sum_{n=0}^{\infty} \frac{(ix)^n}{n!} = 1 + ix + \frac{(ix)^2}{2!} + \frac{(ix)^3}{3!} + \frac{(ix)^4}{4!} + \frac{(ix)^5}{5!} + \cdots$$

**Step 3**: Simplify using powers of $i$:
- $i^0 = 1$
- $i^1 = i$
- $i^2 = -1$
- $i^3 = -i$
- $i^4 = 1$ (pattern repeats)

$$e^{ix} = 1 + ix + \frac{-x^2}{2!} + \frac{-ix^3}{3!} + \frac{x^4}{4!} + \frac{ix^5}{5!} - \frac{x^6}{6!} - \frac{ix^7}{7!} + \cdots$$

**Step 4**: Separate real and imaginary parts:

$$e^{ix} = \left(1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots\right) + i\left(x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots\right)$$

**Step 5**: Recognize the [[taylor-series]] for $\cos(x)$ and $\sin(x)$:

$$\cos(x) = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots$$

$$\sin(x) = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots$$

**Step 6**: Conclude:

$$e^{ix} = \cos(x) + i\sin(x) \quad \blacksquare$$

### Differential Equations Proof (Alternative)

This elegant proof uses the uniqueness theorem for differential equations.

**Define**: Let $f(x) = e^{ix}$ and $g(x) = \cos(x) + i\sin(x)$

**Show both satisfy the same ODE**:
- $f'(x) = ie^{ix} = if(x)$
- $g'(x) = -\sin(x) + i\cos(x) = i(\cos(x) + i\sin(x)) = ig(x)$

**Same initial condition**: $f(0) = e^0 = 1$ and $g(0) = \cos(0) + i\sin(0) = 1$

**By uniqueness**: Solutions to $y' = iy$ with $y(0) = 1$ are unique, so $f(x) = g(x)$ for all $x$. $\blacksquare$

### Geometric Proof (Intuitive)

Consider complex numbers as points in the plane with multiplication as rotation and scaling:

1. Show that multiplying by $e^{ix}$ corresponds to rotation by angle $x$
2. Use the exponential property: $e^{i(x+y)} = e^{ix} \cdot e^{iy}$
3. Demonstrate that $\cos(x) + i\sin(x)$ represents the same rotation
4. Conclude equality through geometric consistency

## Examples

### Example 1: Euler's Identity

Evaluate $e^{i\pi}$:

$$e^{i\pi} = \cos(\pi) + i\sin(\pi) = -1 + i \cdot 0 = -1$$

Therefore: $e^{i\pi} + 1 = 0$

This is **Euler's identity**, connecting five fundamental constants in one elegant equation.

### Example 2: Quarter Turn

Evaluate $e^{i\pi/2}$:

$$e^{i\pi/2} = \cos\left(\frac{\pi}{2}\right) + i\sin\left(\frac{\pi}{2}\right) = 0 + i \cdot 1 = i$$

This shows that $e^{i\pi/2} = i$, meaning multiplying by $i$ corresponds to a 90-degree counterclockwise rotation.

### Example 3: Full Rotation

Evaluate $e^{i \cdot 2\pi}$:

$$e^{i \cdot 2\pi} = \cos(2\pi) + i\sin(2\pi) = 1 + i \cdot 0 = 1$$

This demonstrates the periodicity: rotating by $2\pi$ radians (360 degrees) returns to the starting point.

### Example 4: Complex Number in Polar Form

Express $z = 1 + i$ in polar form using Euler's formula:

**Find magnitude**: $r = |z| = \sqrt{1^2 + 1^2} = \sqrt{2}$

**Find argument**: $\theta = \arctan(1/1) = \pi/4$

**Polar form**: $z = \sqrt{2} \cdot e^{i\pi/4}$

**Verify**: $\sqrt{2}e^{i\pi/4} = \sqrt{2}(\cos(\pi/4) + i\sin(\pi/4)) = \sqrt{2}\left(\frac{1}{\sqrt{2}} + i\frac{1}{\sqrt{2}}\right) = 1 + i$ ✓

### Example 5: Simplifying Trigonometric Identities

Use Euler's formula to derive $\cos(2x) = \cos^2(x) - \sin^2(x)$:

$$e^{i \cdot 2x} = (e^{ix})^2 = (\cos(x) + i\sin(x))^2$$

$$\cos(2x) + i\sin(2x) = \cos^2(x) + 2i\cos(x)\sin(x) - \sin^2(x)$$

Equating real parts: $\cos(2x) = \cos^2(x) - \sin^2(x)$ ✓

## Applications

Euler's formula is one of the most practically important theorems in mathematics, with applications across science and engineering:

### Signal Processing and [[Fourier-Analysis]]

Fourier transforms decompose signals into frequency components using complex exponentials $e^{i\omega t}$. This enables:
- Digital filtering (audio, images, communications)
- Spectrum analysis
- Signal compression (MP3, JPEG)
- Data transmission

### Electrical Engineering

AC circuit analysis uses phasors based on Euler's formula to represent sinusoidal voltages and currents:
- Complex impedance: $Z = R + iX$
- Power calculations in AC systems
- Resonance in RLC circuits
- Filter design

### [[Quantum-Mechanics]]

Wave functions are expressed using complex exponentials:
$$\psi(x,t) = Ae^{i(kx - \omega t)}$$

The Schrödinger equation, which governs quantum systems, fundamentally relies on Euler's formula. The time evolution operator uses $e^{-iHt/\hbar}$.

### Control Theory

System stability analysis uses Euler's formula to:
- Represent eigenvalues in the complex plane
- Analyze frequency response
- Design feedback controllers
- Convert between time and frequency domains

### Vibration Analysis

Mechanical oscillations are analyzed using complex exponentials:
- Structural dynamics
- Earthquake engineering
- Acoustics
- Modal analysis

### Optics and Wave Theory

Electromagnetic waves and light propagation use Euler's formula for:
- Interference and diffraction patterns
- Polarization analysis
- Wave superposition
- Optical coherence

### Computer Graphics

Rotations and transformations in 2D/3D graphics:
- Efficient rotation computations
- Quaternion representations (extended to 3D)
- Animation and interpolation
- Real-time rendering

### Differential Equations

Solutions to linear ODEs with constant coefficients:
$$y'' + \omega^2 y = 0 \implies y = Ae^{i\omega t} = A(\cos(\omega t) + i\sin(\omega t))$$

Complex characteristic roots lead to oscillatory solutions expressed via Euler's formula.

### Probability Theory

Characteristic functions of random variables:
$$\phi_X(t) = E[e^{itX}]$$

Used in proving the Central Limit Theorem and other fundamental results in probability theory.

### Number Theory

- Roots of unity: $e^{2\pi i k/n}$ for $k = 0, 1, \ldots, n-1$
- Cyclotomic polynomials
- Algebraic number theory
- Modular arithmetic and group theory

## Related Concepts

- **[[de-moivres-theorem]]**: States $(\cos(x) + i\sin(x))^n = \cos(nx) + i\sin(nx)$, which follows directly from Euler's formula: $(e^{ix})^n = e^{inx}$
- **[[fourier-analysis]]**: Fourier transforms rely fundamentally on Euler's formula to express periodic functions as sums of complex exponentials
- **[[complex-exponential-function]]**: Euler's formula defines how to extend the exponential function to complex arguments
- **[[trigonometric-identities]]**: Many trigonometric identities can be derived elegantly using Euler's formula
- **[[unit-circle]]**: $e^{ix}$ traces out the unit circle in the complex plane as $x$ varies
- **[[hyperbolic-functions]]**: Similar relationships exist: $e^x = \cosh(x) + \sinh(x)$
- **[[polar-form-complex-numbers]]**: Euler's formula enables the polar representation $z = re^{i\theta}$
- **[[cauchys-formula]]**: Complex integration results that rely on Euler's formula
- **[[complex-plane]]**: Geometric interpretation of complex numbers as points in the plane
- **[[polar-coordinates]]**: $(r, \theta)$ representation connected to $re^{i\theta}$
- **[[cis-function]]**: The notation $\text{cis}(\theta) = \cos(\theta) + i\sin(\theta) = e^{i\theta}$

## Properties

### Beauty and Elegance

Euler's identity $e^{i\pi} + 1 = 0$ is considered **the most beautiful equation in mathematics** because:
- Connects the five most fundamental constants: $e$, $i$, $\pi$, $1$, $0$
- Uses only basic operations: addition, multiplication, exponentiation, equality
- Profound simplicity hiding deep mathematical structure
- Voted "most beautiful" in multiple polls of mathematicians

### Periodicity

The complex exponential is periodic with period $2\pi$:
$$e^{i(x + 2\pi)} = e^{ix} \cdot e^{i \cdot 2\pi} = e^{ix} \cdot 1 = e^{ix}$$

This reflects the periodic nature of trigonometric functions and circular motion.

### Unit Circle Property

For all real $x$:
$$|e^{ix}| = \sqrt{\cos^2(x) + \sin^2(x)} = 1$$

Meaning $e^{ix}$ always lies on the unit circle in the complex plane.

### Rotation Interpretation

Multiplying by $e^{ix}$ rotates a complex number by angle $x$:
$$e^{ix} \cdot e^{iy} = e^{i(x+y)}$$

Addition of angles corresponds to multiplication of complex exponentials. This is the foundation for understanding complex multiplication geometrically.

### Derivative Property

$$\frac{d}{dx}e^{ix} = ie^{ix}$$

Differentiation corresponds to a 90-degree rotation (multiplication by $i$). This reveals the deep connection between rotation and differentiation.

### Conjugate Symmetry

$$e^{-ix} = \cos(x) - i\sin(x) = \overline{e^{ix}}$$

The complex conjugate corresponds to reflection across the real axis (negative angle), representing clockwise rotation.

## Historical Context

### Discovery

**Leonhard Euler** first published this formula in **1748** in his landmark work *Introductio in analysin infinitorum* (*Introduction to the Analysis of the Infinite*).

### Background

While Euler published the formula in 1748, he had been working with complex exponentials since the 1740s. The relationship between exponential and trigonometric functions had been explored by **Roger Cotes** in 1714, but Euler was the first to express it clearly in the form we use today using the notation $e^{ix}$.

The notation $e^{ix}$ itself reflects Euler's pioneering work on both the exponential function and complex numbers. Euler was instrumental in establishing $e$ as a fundamental constant and in developing the modern understanding of complex numbers.

### Significance

Euler's formula unified three major branches of mathematics:
- **Trigonometry** (sine and cosine)
- **Complex numbers** (the imaginary unit $i$)
- **Exponential functions** (base $e$)

This unification was revolutionary for mathematics and laid the foundation for modern complex analysis. It showed that seemingly disparate areas of mathematics were deeply interconnected.

### Cultural Impact

Euler's identity has transcended mathematics to become a cultural icon:
- Appears on t-shirts, tattoos, and merchandise
- Featured in popular science books and TV shows (*The Simpsons*, *The Net*)
- Ranked as "most beautiful theorem" by *Mathematical Intelligencer* (2004)
- Subject of numerous articles, videos, and educational content
- Symbol of mathematical beauty and elegance

### Notable Quotes

**Benjamin Peirce** (Harvard, 1800s): *"Gentlemen, that is surely true, it is absolutely paradoxical; we cannot understand it, and we don't know what it means. But we have proved it, and therefore we know it must be the truth."*

**Richard Feynman**: *"We summarize with this, the most remarkable formula in mathematics: $e^{i\theta} = \cos(\theta) + i\sin(\theta)$. This is our jewel."* (*The Feynman Lectures on Physics*, Vol. I)

**Keith Devlin**: *"Like a Shakespearean sonnet that captures the very essence of love, or a painting that brings out the beauty of the human form that is far more than just skin deep, Euler's equation reaches down into the very depths of existence."* (*The Mathematical Intelligencer*)

### Fun Facts

- Euler was blind in one eye for much of his life and completely blind in his later years, yet he made many of his greatest discoveries during this period
- Roger Cotes discovered an equivalent form in 1714, but Euler's exponential notation made it much more powerful and useful
- The formula provides a way to compute trigonometric function values using the exponential function
- Multiplication by $i$ in the complex plane corresponds to a 90-degree rotation, which Euler's formula explains geometrically
- Some mathematicians have gotten Euler's identity tattooed on their bodies as a tribute to its beauty

## Pedagogical Notes

### Typical Course Level

Euler's formula is typically taught in:
- Complex Analysis (undergraduate)
- Advanced Calculus
- Engineering Mathematics
- Mathematical Methods in Physics

### Common Misconceptions

1. **$i$ is just a symbol**: Students often think $i$ is merely notation rather than a number with algebraic properties
2. **Why $e^{i\pi} = -1$**: Confusion about why this specific value rather than something else
3. **Limited applicability**: Not recognizing the formula applies to all real $x$, not just special values
4. **Just a definition**: Believing it's a definition rather than a provable theorem
5. **Confusing general and special cases**: Mixing up $e^{ix}$ (general) with $e^{i\pi} + 1 = 0$ (special case)

### Teaching Approaches

- Start with [[taylor-series]] to build intuition and provide rigorous proof
- Use geometric interpretation in the [[complex-plane]] to visualize rotation
- Connect to prior knowledge of trigonometry and exponentials
- Show applications in signal processing or physics for motivation
- Demonstrate how [[trigonometric-identities]] become trivial using Euler's formula
- Build up gradually from real exponentials through complex numbers

### Visualization Suggestions

- Animate $e^{ix}$ tracing the unit circle as $x$ varies from $0$ to $2\pi$
- Show Taylor series partial sums converging to the exponential spiral
- Plot real and imaginary parts separately as functions of $x$
- Demonstrate complex multiplication as rotation: $e^{ix} \cdot e^{iy} = e^{i(x+y)}$
- Interactive sliders showing how changing $x$ affects position on unit circle
- 3D plots showing the spiral nature of $e^{(a+ib)t}$ for various $a$ and $b$

## Further Reading

### Books

- Euler, Leonhard (1748). *Introductio in analysin infinitorum*
- Nahin, Paul J. (2006). *Dr. Euler's Fabulous Formula: Cures Many Mathematical Ills*. Princeton University Press.
- Feynman, Richard. *The Feynman Lectures on Physics, Vol. I*
- Stillwell, John (2002). *Mathematics and Its History*. Springer.

### Online Resources

- [Wikipedia: Euler's Formula](https://en.wikipedia.org/wiki/Euler%27s_formula)
- [Wolfram MathWorld: Euler Formula](https://mathworld.wolfram.com/EulerFormula.html)
- [Better Explained: Intuitive Understanding of Euler's Formula](https://betterexplained.com/articles/intuitive-understanding-of-eulers-formula/)
- [Brilliant: Euler's Formula](https://brilliant.org/wiki/eulers-formula/)
- [Math is Fun: Euler's Formula](https://www.mathsisfun.com/algebra/eulers-formula.html)

### Related Topics to Explore

- **[[complex-analysis]]**: Full theory of complex functions and their properties
- **[[analytic-functions]]**: Functions that can be represented by convergent power series
- **[[fourier-transform]]**: Transform theory built on complex exponentials
- **[[laplace-transform]]**: Integral transform for solving differential equations
- **[[residue-theorem]]**: Advanced application using contour integration
- **[[conformal-mapping]]**: Geometric transformations using complex functions

---

**Summary**: Euler's formula $e^{ix} = \cos(x) + i\sin(x)$ is one of the most profound and widely-used formulas in mathematics. It bridges exponential functions, trigonometry, complex numbers, and geometry, with applications spanning signal processing, quantum mechanics, electrical engineering, control theory, and many other fields. The special case known as Euler's identity ($e^{i\pi} + 1 = 0$) is often called the most beautiful equation in mathematics, connecting five fundamental constants in one elegant relationship.

**Keywords**: Euler's formula, complex exponentials, trigonometric functions, complex analysis, Euler's identity, exponential form, unit circle, Taylor series, polar form, De Moivre's theorem, Fourier analysis

**See also**: [[exponential-functions]], [[complex-numbers]], [[trigonometric-functions]], [[de-moivres-theorem]], [[fourier-analysis]], [[complex-plane]], [[polar-coordinates]]
