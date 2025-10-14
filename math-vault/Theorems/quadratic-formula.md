---
title: Quadratic Formula
type: Theorem/Formula
difficulty: Intermediate
tags:
  - algebra
  - quadratic-equations
  - formulas
  - polynomials
  - theorem
related:
  - "[[completing-the-square]]"
  - "[[discriminant]]"
  - "[[vietas-formulas]]"
  - "[[quadratic-equations]]"
  - "[[complex-numbers]]"
  - "[[polynomial-roots]]"
prerequisites:
  - "[[algebra-basics]]"
  - "[[square-roots]]"
  - "[[factoring]]"
---

# Quadratic Formula

## Overview

The **Quadratic Formula** provides the solutions to any quadratic equation of the form $ax^2 + bx + c = 0$ where $a \neq 0$. It is one of the most fundamental formulas in algebra and is derived by completing the square.

## Formula

For a quadratic equation $ax^2 + bx + c = 0$ with $a \neq 0$, the solutions are:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

## Components

### Discriminant

The expression $\Delta = b^2 - 4ac$ is called the **discriminant** and determines the nature of the roots:

- **$\Delta > 0$**: Two distinct real roots
- **$\Delta = 0$**: One repeated real root (double root)
- **$\Delta < 0$**: Two complex conjugate roots

## Derivation

Starting with the general quadratic equation:

$$ax^2 + bx + c = 0$$

1. Divide by $a$ (assuming $a \neq 0$):
   $$x^2 + \frac{b}{a}x + \frac{c}{a} = 0$$

2. Complete the square:
   $$x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = \left(\frac{b}{2a}\right)^2 - \frac{c}{a}$$

3. Simplify:
   $$\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}$$

4. Take the square root of both sides:
   $$x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2a}$$

5. Solve for $x$:
   $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

## Properties

- The sum of the roots is $-\frac{b}{a}$ (Vieta's formulas)
- The product of the roots is $\frac{c}{a}$ (Vieta's formulas)
- The formula works for all quadratic equations, including those with complex coefficients

## Applications

- Solving projectile motion problems in physics
- Finding intersections of parabolas with other curves
- Optimization problems in calculus
- Engineering and computer graphics

## Examples

### Example 1: Two Distinct Real Roots

Solve $x^2 - 5x + 6 = 0$

Here $a = 1$, $b = -5$, $c = 6$:

$$x = \frac{-(-5) \pm \sqrt{(-5)^2 - 4(1)(6)}}{2(1)} = \frac{5 \pm \sqrt{25 - 24}}{2} = \frac{5 \pm 1}{2}$$

Solutions: $x = 3$ or $x = 2$

### Example 2: Double Root

Solve $x^2 - 4x + 4 = 0$

Here $a = 1$, $b = -4$, $c = 4$:

$$x = \frac{4 \pm \sqrt{16 - 16}}{2} = \frac{4 \pm 0}{2} = 2$$

Solution: $x = 2$ (double root)

### Example 3: Complex Roots

Solve $x^2 + 2x + 5 = 0$

Here $a = 1$, $b = 2$, $c = 5$:

$$x = \frac{-2 \pm \sqrt{4 - 20}}{2} = \frac{-2 \pm \sqrt{-16}}{2} = \frac{-2 \pm 4i}{2} = -1 \pm 2i$$

Solutions: $x = -1 + 2i$ or $x = -1 - 2i$

## Related Concepts

- [[completing-the-square|Completing the Square]]
- [[discriminant|Discriminant]]
- [[vietas-formulas|Vieta's Formulas]]
- [[quadratic-equations|Quadratic Equations]]
- [[complex-numbers|Complex Numbers]]
- [[polynomial-roots|Polynomial Roots]]

## Prerequisites

- [[algebra-basics|Algebra Basics]]
- [[square-roots|Square Roots]]
- [[factoring|Factoring]]

## Historical Note

While methods for solving quadratic equations date back to ancient Babylonian mathematicians (circa 2000 BCE), the general formula as we know it was developed over centuries. The modern algebraic form was established during the Islamic Golden Age by mathematicians like al-Khwarizmi (9th century) and was further refined during the Renaissance.
