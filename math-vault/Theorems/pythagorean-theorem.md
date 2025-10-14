---
type: theorem
id: pythagorean-theorem
domain: geometry
level: middle-school
difficulty: 4
language: en
tags:
  - theorems
  - geometry
  - right-triangles
  - euclidean-geometry
  - algebraic-geometry
  - classical-mathematics
prerequisites:
  - "[[right-triangle]]"
  - "[[square-numbers]]"
  - "[[hypotenuse]]"
  - "[[legs-of-triangle]]"
  - "[[area]]"
  - "[[geometric-proof]]"
  - "[[algebraic-equations]]"
used-in:
  - "[[distance-formula]]"
  - "[[trigonometry]]"
  - "[[euclidean-geometry]]"
  - "[[coordinate-geometry]]"
  - "[[pythagorean-triples]]"
  - "[[law-of-cosines]]"
  - "[[vector-magnitude]]"
  - "[[complex-numbers]]"
  - "[[three-dimensional-geometry]]"
  - "[[physics-vectors]]"
  - "[[navigation]]"
  - "[[architectural-calculations]]"
related:
  - "[[pythagorean-identity]]"
  - "[[euclidean-distance-metric]]"
  - "[[inner-product-spaces]]"
  - "[[fermat-last-theorem]]"
  - "[[trigonometric-functions]]"
aliases:
  - Pythagoras' Theorem
  - Pythagorean Relation
  - Right Triangle Theorem
created: 2025-10-14
---

# Pythagorean Theorem

## Definition

The **Pythagorean Theorem** is one of the most fundamental theorems in Euclidean geometry. It states that in a [[right-triangle]], the square of the length of the [[hypotenuse]] (the side opposite the right angle) is equal to the sum of the squares of the lengths of the other two sides (called the [[legs-of-triangle]]).

**Algebraic Form:**

$$
a^2 + b^2 = c^2
$$

where:
- $a$ and $b$ are the lengths of the two legs (the sides that form the right angle)
- $c$ is the length of the hypotenuse (the longest side, opposite the right angle)

**Geometric Interpretation:**

The [[area]] of the square built upon the hypotenuse equals the sum of the areas of the squares built upon the two legs.

## Historical Context

The Pythagorean Theorem is named after the ancient Greek mathematician **Pythagoras** (c. 570 – c. 495 BCE), who founded a philosophical and mathematical school in Croton, southern Italy. While the theorem bears his name, evidence suggests that Babylonian and Indian mathematicians knew of the relationship centuries earlier.

**Historical Timeline:**

1. **Babylonian Clay Tablets (c. 1800 BCE)**: The tablet Plimpton 322 contains [[pythagorean-triples]], suggesting Babylonians knew the relationship.

2. **Indian Mathematics (c. 800 BCE)**: The Sulba Sutras, ancient Indian texts, contain statements of the theorem used for altar construction.

3. **Pythagoras (c. 500 BCE)**: Credited with the first rigorous proof, though no original writings survive. His school studied mathematics, philosophy, and music.

4. **Euclid's Elements (c. 300 BCE)**: Book I, Proposition 47 provides a famous geometric proof of the theorem.

5. **Chinese Mathematics (c. 100 BCE)**: The Zhou Bi Suan Jing contains a proof using geometric dissection.

**Cultural Impact:**

The theorem has been proven in over 370 different ways, making it one of the most proven theorems in mathematics. Notable contributors include:
- **Euclid**: Geometric proof using parallelograms
- **Leonardo da Vinci**: Visual proof using geometric rearrangement
- **James Garfield**: 20th U.S. President, created a trapezoid proof in 1876
- **Bhaskara II**: Indian mathematician, provided elegant visual proofs

## Prerequisites

To understand the Pythagorean Theorem, you need:

- **[[right-triangle]]**: A triangle with one angle measuring exactly 90 degrees (a right angle). Understanding which side is opposite the right angle is crucial.

- **[[square-numbers]]**: The operation of squaring a number ($n^2 = n \times n$). Must understand that $a^2$ represents "a squared" or $a$ multiplied by itself.

- **[[hypotenuse]]**: The longest side of a right triangle, always opposite the right angle. This is the side isolated on one side of the equation ($c^2$).

- **[[legs-of-triangle]]**: The two sides that form the right angle. These are the perpendicular sides of the triangle (represented as $a$ and $b$).

- **[[area]]**: Understanding area, particularly the area of a square ($s^2$ for a square with side length $s$), is essential for geometric proofs.

- **[[geometric-proof]]**: Familiarity with logical reasoning and proof techniques helps appreciate why the theorem is true, not just memorizing the formula.

- **[[algebraic-equations]]**: Basic ability to manipulate equations, solve for unknowns, and work with squared terms.

## Mathematical Details

### Standard Form

For a right triangle with legs of length $a$ and $b$, and hypotenuse of length $c$:

$$
a^2 + b^2 = c^2
$$

### Alternative Forms

**Solving for the hypotenuse:**
$$
c = \sqrt{a^2 + b^2}
$$

**Solving for a leg:**
$$
a = \sqrt{c^2 - b^2}
$$
$$
b = \sqrt{c^2 - a^2}
$$

### Converse of the Pythagorean Theorem

If three positive numbers $a$, $b$, $c$ satisfy $a^2 + b^2 = c^2$, then a triangle with sides of lengths $a$, $b$, $c$ is a right triangle with hypotenuse $c$.

This converse is extremely useful for determining whether a triangle is a right triangle given only the side lengths.

### Extensions

**For Acute Triangles** (all angles less than 90°):
$$
a^2 + b^2 > c^2
$$

**For Obtuse Triangles** (one angle greater than 90°):
$$
a^2 + b^2 < c^2
$$

### Three-Dimensional Extension

In three-dimensional space, the distance $d$ from the origin to point $(x, y, z)$ is:
$$
d = \sqrt{x^2 + y^2 + z^2}
$$

This is a direct extension of the Pythagorean Theorem to [[three-dimensional-geometry]].

### n-Dimensional Extension

In $n$-dimensional Euclidean space, the distance from the origin to point $(x_1, x_2, \ldots, x_n)$ is:
$$
d = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2}
$$

## Proofs

The Pythagorean Theorem has been proven in over 370 different ways. Here are some of the most famous:

### Proof 1: Euclid's Geometric Proof

Euclid's proof (Elements, Book I, Proposition 47) uses the properties of parallelograms and triangles.

**Construction:**
1. Draw squares on all three sides of the right triangle
2. Draw altitude from the right angle to the hypotenuse
3. Prove that each leg's square equals the area of the corresponding rectangle on the hypotenuse square

**Key Insight:** The proof uses area equivalences and does not rely on algebra.

### Proof 2: Rearrangement Proof (Visual/Dissection)

**Setup:** Start with a square of side length $(a+b)$.

1. Place four identical right triangles inside the square, arranged so their hypotenuses form an inner square
2. The inner square has side length $c$ (the hypotenuse)
3. Calculate the area two ways:

**Method 1:** Total area = $(a+b)^2 = a^2 + 2ab + b^2$

**Method 2:** Total area = $4 \times \frac{1}{2}ab + c^2 = 2ab + c^2$

**Equating the two:**
$$
a^2 + 2ab + b^2 = 2ab + c^2
$$

**Simplify:**
$$
a^2 + b^2 = c^2
$$

This elegant visual proof requires no advanced mathematics and demonstrates the theorem beautifully. ∎

### Proof 3: Algebraic Proof Using Similar Triangles

When an altitude is drawn from the right angle to the hypotenuse:

1. The altitude creates two smaller triangles, both similar to the original triangle
2. Using proportions from similar triangles:
   - $\frac{a}{c} = \frac{h_1}{a}$ gives $a^2 = c \cdot h_1$
   - $\frac{b}{c} = \frac{h_2}{b}$ gives $b^2 = c \cdot h_2$
3. Add the equations: $a^2 + b^2 = c \cdot h_1 + c \cdot h_2 = c(h_1 + h_2) = c \cdot c = c^2$ ∎

### Proof 4: President Garfield's Trapezoid Proof (1876)

James A. Garfield, before becoming the 20th U.S. President, created this proof:

1. Arrange two identical right triangles and one rotated copy to form a trapezoid
2. Calculate the trapezoid area two ways:
   - **Trapezoid formula:** $\frac{1}{2}(a + b)(a + b) = \frac{1}{2}(a^2 + 2ab + b^2)$
   - **Sum of three triangles:** $\frac{1}{2}ab + \frac{1}{2}ab + \frac{1}{2}c^2 = ab + \frac{1}{2}c^2$
3. Equate and simplify: $a^2 + b^2 = c^2$ ∎

### Proof 5: Bhaskara's Visual Proof

The 12th-century Indian mathematician Bhaskara provided a simple visual proof:

1. Draw a square with side length $c$
2. Inside, place four right triangles arranged to leave a small square in the center
3. The area calculation directly yields $a^2 + b^2 = c^2$

Bhaskara's proof was accompanied by just one word: "Behold!" (or "Look!" in Sanskrit)

## Examples

### Example 1: Classic 3-4-5 Triangle

Given a right triangle with legs $a = 3$ and $b = 4$, find the hypotenuse $c$.

**Solution:**
$$
c^2 = a^2 + b^2 = 3^2 + 4^2 = 9 + 16 = 25
$$
$$
c = \sqrt{25} = 5
$$

The 3-4-5 triangle is the most famous [[pythagorean-triples|Pythagorean triple]].

### Example 2: Finding a Missing Leg

Given a right triangle with hypotenuse $c = 13$ and one leg $a = 5$, find the other leg $b$.

**Solution:**
$$
b^2 = c^2 - a^2 = 13^2 - 5^2 = 169 - 25 = 144
$$
$$
b = \sqrt{144} = 12
$$

This is the 5-12-13 Pythagorean triple.

### Example 3: Verifying a Right Triangle

Determine whether a triangle with sides 7, 24, and 25 is a right triangle.

**Solution:**
Check if $a^2 + b^2 = c^2$ (where $c = 25$ is the longest side):
$$
7^2 + 24^2 = 49 + 576 = 625 = 25^2
$$

Yes, this is a right triangle with legs 7 and 24, and hypotenuse 25. ✓

### Example 4: Ladder Problem (Practical Application)

A 10-foot ladder leans against a wall. The base of the ladder is 6 feet from the wall. How high up the wall does the ladder reach?

**Solution:**
- Hypotenuse (ladder): $c = 10$ feet
- Base (distance from wall): $a = 6$ feet
- Height (unknown): $b = ?$

$$
b^2 = c^2 - a^2 = 10^2 - 6^2 = 100 - 36 = 64
$$
$$
b = \sqrt{64} = 8 \text{ feet}
$$

The ladder reaches 8 feet up the wall.

### Example 5: Diagonal of a Rectangle

Find the diagonal of a rectangle with length 12 cm and width 5 cm.

**Solution:**
The diagonal forms the hypotenuse of a right triangle:
$$
d = \sqrt{12^2 + 5^2} = \sqrt{144 + 25} = \sqrt{169} = 13 \text{ cm}
$$

### Example 6: Distance Between Two Points

Find the distance between points $A(1, 2)$ and $B(4, 6)$ in the coordinate plane.

**Solution:**
Using the [[distance-formula]] (derived from the Pythagorean Theorem):
$$
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} = \sqrt{(4-1)^2 + (6-2)^2} = \sqrt{9 + 16} = \sqrt{25} = 5
$$

### Example 7: Television Screen Size

A TV advertised as "50 inches" refers to the diagonal measurement. If the screen is 43.6 inches wide and follows the 16:9 aspect ratio, what is the height?

**Solution:**
Let $h$ = height, $w = 43.6$ inches, diagonal $d = 50$ inches:
$$
h^2 = d^2 - w^2 = 50^2 - 43.6^2 = 2500 - 1900.96 = 599.04
$$
$$
h = \sqrt{599.04} \approx 24.5 \text{ inches}
$$

## Applications

The Pythagorean Theorem is one of the most practical theorems in mathematics with applications across numerous fields:

### 1. [[distance-formula]]

The distance formula in [[coordinate-geometry]] is a direct application:
$$
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
$$

This extends to three dimensions and higher-dimensional spaces, forming the basis of the [[euclidean-distance-metric]].

### 2. [[trigonometry]]

The Pythagorean Theorem is foundational to trigonometry. It leads directly to the [[pythagorean-identity]]:
$$
\sin^2\theta + \cos^2\theta = 1
$$

This identity is derived by applying the Pythagorean Theorem to the unit circle.

### 3. [[vector-magnitude]]

The magnitude (or length) of a vector $\vec{v} = \langle a, b \rangle$ is:
$$
|\vec{v}| = \sqrt{a^2 + b^2}
$$

In three dimensions: $|\vec{v}| = \sqrt{a^2 + b^2 + c^2}$

### 4. [[complex-numbers]]

The modulus (absolute value) of a complex number $z = a + bi$ is:
$$
|z| = \sqrt{a^2 + b^2}
$$

This represents the distance from the origin to the point $(a, b)$ in the complex plane.

### 5. [[navigation]]

Pilots and sailors use the Pythagorean Theorem to calculate direct distances when traveling along perpendicular paths (e.g., north then east).

### 6. [[architectural-calculations]] and Construction

Builders use the 3-4-5 ratio (or multiples like 6-8-10) to create perfect right angles for foundations, walls, and frames.

### 7. [[physics-vectors]]

Calculating resultant forces, velocities, and displacements when components are perpendicular:
$$
F_{\text{resultant}} = \sqrt{F_x^2 + F_y^2}
$$

### 8. Computer Graphics and Game Development

Distance calculations between objects, collision detection, and rendering use the Pythagorean Theorem extensively.

### 9. [[law-of-cosines]]

The Law of Cosines is a generalization of the Pythagorean Theorem to non-right triangles:
$$
c^2 = a^2 + b^2 - 2ab\cos C
$$

When $C = 90°$, $\cos C = 0$, reducing to the Pythagorean Theorem.

### 10. GPS and Location Services

Triangulation methods for determining position rely on distance calculations using the Pythagorean Theorem.

### 11. Signal Processing

Calculating the magnitude of signals with real and imaginary components (related to Fourier analysis).

### 12. Machine Learning

Distance metrics (Euclidean distance) for measuring similarity between data points in high-dimensional spaces.

## Pythagorean Triples

A **[[pythagorean-triples|Pythagorean triple]]** consists of three positive integers $a$, $b$, $c$ such that:
$$
a^2 + b^2 = c^2
$$

### Primitive Pythagorean Triples

Triples where $a$, $b$, $c$ have no common factor greater than 1:
- $(3, 4, 5)$
- $(5, 12, 13)$
- $(8, 15, 17)$
- $(7, 24, 25)$
- $(20, 21, 29)$
- $(9, 40, 41)$
- $(12, 35, 37)$
- $(11, 60, 61)$
- $(13, 84, 85)$
- $(36, 77, 85)$

### Generating Pythagorean Triples

**Euclid's Formula:** For any integers $m > n > 0$:
$$
a = m^2 - n^2, \quad b = 2mn, \quad c = m^2 + n^2
$$

**Example:** $m = 2, n = 1$:
$$
a = 4 - 1 = 3, \quad b = 2(2)(1) = 4, \quad c = 4 + 1 = 5
$$
yields the $(3, 4, 5)$ triple.

### Connection to [[fermat-last-theorem]]

Fermat's Last Theorem states that no three positive integers $a$, $b$, $c$ satisfy:
$$
a^n + b^n = c^n
$$
for any integer $n > 2$. Thus, Pythagorean triples ($n = 2$) are the **only** integer solutions to this type of equation.

## Related Concepts

- **[[pythagorean-identity]]**: The trigonometric identity $\sin^2\theta + \cos^2\theta = 1$, derived from the Pythagorean Theorem on the unit circle

- **[[distance-formula]]**: Direct application for finding distance between points in coordinate systems

- **[[law-of-cosines]]**: Generalization to non-right triangles: $c^2 = a^2 + b^2 - 2ab\cos C$

- **[[law-of-sines]]**: Another relationship in triangles, complementary to the Law of Cosines

- **[[euclidean-distance-metric]]**: The distance function in Euclidean space based on the Pythagorean Theorem

- **[[inner-product-spaces]]**: Generalization to abstract vector spaces where the Pythagorean Theorem defines orthogonality

- **[[pythagorean-triples]]**: Integer solutions $(a, b, c)$ to $a^2 + b^2 = c^2$

- **[[fermat-last-theorem]]**: States that $a^n + b^n = c^n$ has no integer solutions for $n > 2$

- **[[trigonometric-functions]]**: Sine, cosine, and tangent functions, fundamentally related through the Pythagorean Theorem

- **[[euclidean-geometry]]**: The branch of geometry where the Pythagorean Theorem holds

- **[[coordinate-geometry]]**: Uses the Pythagorean Theorem extensively for distance and slope calculations

- **[[vector-spaces]]**: Abstract spaces where the Pythagorean Theorem generalizes to orthogonal vectors

- **[[right-triangle-trigonometry]]**: The study of ratios in right triangles (SOH-CAH-TOA)

- **[[altitude-of-triangle]]**: The altitude to the hypotenuse creates similar triangles used in proofs

- **[[similar-triangles]]**: Used in one of the classic proofs of the Pythagorean Theorem

## Geometric Interpretation

The Pythagorean Theorem has a beautiful geometric interpretation:

**Area Interpretation:**

If squares are constructed on each side of a right triangle:
- The area of the square on the hypotenuse equals the sum of the areas of the squares on the two legs
- Visually: The blue square's area equals the sum of the red and green squares' areas

**This can be extended to any similar shapes:**

If similar figures (not just squares) are constructed on each side, the area relationship still holds:
$$
\text{Area}(\text{figure on } c) = \text{Area}(\text{figure on } a) + \text{Area}(\text{figure on } b)
$$

This works for semicircles, equilateral triangles, or any similar shapes built on the three sides.

## Limitations and Extensions

### Non-Euclidean Geometries

The Pythagorean Theorem does **not** hold in non-Euclidean geometries:

- **Spherical Geometry** (positive curvature): $a^2 + b^2 > c^2$ for right triangles
- **Hyperbolic Geometry** (negative curvature): $a^2 + b^2 < c^2$ for right triangles

These differences arise because straight lines behave differently on curved surfaces.

### Only for Right Triangles

The theorem applies **only** to right triangles. For other triangles:
- Use the [[law-of-cosines]]: $c^2 = a^2 + b^2 - 2ab\cos C$
- Use the [[law-of-sines]]: $\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}$

## Significance

The Pythagorean Theorem is significant because it:

1. **Connects algebra and geometry**: Relates numerical relationships to geometric shapes

2. **Enables measurement**: Allows indirect measurement of distances that cannot be measured directly

3. **Foundation for higher mathematics**: Underlies calculus, vector analysis, and abstract algebra

4. **Universal applicability**: Used in virtually every field involving measurement or distance

5. **Simple yet profound**: Accessible to middle school students yet crucial for advanced research

6. **Historical importance**: One of the oldest known mathematical theorems, central to the development of mathematics

7. **Proof diversity**: The variety of proofs demonstrates the richness of mathematical thinking

The German mathematician Carl Friedrich Gauss remarked that the Pythagorean Theorem and the proof methods surrounding it demonstrate the beauty and power of mathematical reasoning.

## Pedagogical Notes

**Common Student Misconceptions:**

1. **Confusing which side is the hypotenuse**: Remember, it's always the longest side and opposite the right angle

2. **Forgetting to take the square root**: $c^2 = 25$ means $c = 5$, not $c = 25$

3. **Applying to non-right triangles**: The theorem only works for right triangles

4. **Adding sides instead of squared sides**: It's $a^2 + b^2$, not $a + b$

**Teaching Tips:**

1. Start with concrete examples using graph paper
2. Use the 3-4-5 triangle as a reference
3. Demonstrate multiple proofs to show mathematical creativity
4. Connect to real-world applications early
5. Practice identifying which variable to solve for
6. Use visual/interactive demonstrations

## Further Reading

- **[[euclidean-geometry]]**: The geometric framework where the Pythagorean Theorem lives
- **[[trigonometry]]**: The entire field built on the foundation of right triangles
- **[[coordinate-geometry]]**: Applications to the Cartesian plane
- **[[vector-spaces]]**: Abstract generalization to higher dimensions
- **[[non-euclidean-geometry]]**: Where the theorem doesn't hold
- **[[fermat-last-theorem]]**: The famous generalization question
- **[[pythagorean-triples]]**: Integer solutions and number theory
- **[[law-of-cosines]]**: Generalization to all triangles

## References

1. Euclid. (c. 300 BCE). *Elements*, Book I, Proposition 47.
2. Maor, E. (2007). *The Pythagorean Theorem: A 4,000-Year History*. Princeton University Press.
3. Loomis, E. S. (1940). *The Pythagorean Proposition*. National Council of Teachers of Mathematics. (Contains 370+ proofs)
4. Heath, T. L. (1908). *The Thirteen Books of Euclid's Elements*. Cambridge University Press.
5. [Cut-the-Knot: Pythagorean Theorem](https://www.cut-the-knot.org/pythagoras/)
6. [Wikipedia: Pythagorean Theorem](https://en.wikipedia.org/wiki/Pythagorean_theorem)
7. [Khan Academy: Pythagorean Theorem](https://www.khanacademy.org/math/geometry/hs-geo-trig/hs-geo-pythagorean-theorem/)
8. [Wolfram MathWorld: Pythagorean Theorem](https://mathworld.wolfram.com/PythagoreanTheorem.html)

---

**Keywords**: Pythagorean theorem, right triangle, hypotenuse, Euclidean geometry, distance formula, Pythagorean triples, geometric proof, trigonometry, coordinate geometry

**See also**: [[right-triangle]], [[distance-formula]], [[trigonometry]], [[pythagorean-triples]], [[law-of-cosines]], [[euclidean-geometry]], [[coordinate-geometry]]
