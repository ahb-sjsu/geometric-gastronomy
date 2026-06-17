# Appendix A: Mathematical Preliminaries

> *"It is the harmony of the diverse parts, their symmetry, their happy balance; in a word it is all that introduces order, all that gives unity, that permits us to see clearly and to comprehend at once both the ensemble and the details."*
> — Henri Poincaré, *The Value of Science* (1905)

This appendix is a self-contained primer on the three mathematical tools the book leans on most heavily: the differential geometry of curved spaces (Riemannian manifolds, metric tensors, geodesics), the optimization geometry of constraints and trade-offs (convex sets, the simplex, Pareto frontiers), and the linear algebra of dimensionality reduction (principal component analysis). None of it is original. The aim is modest: to give a reader without a graduate background enough working vocabulary to follow the geometric arguments of the main text, and to make explicit the standard results those arguments quietly assume.

The treatment is deliberately informal. Where the body of the book writes "the flavor metric is curved" or "balance is a fixed point on a low-dimensional manifold," this appendix supplies the definitions that make such sentences precise. Each section closes with a single worked micro-example and a list of the chapters where the tool does real work, so the reader can read the preliminary and then go straight to the application.

A note on notation, consistent with the main text. Flavor vectors are written $\mathbf{f}$, with named components such as $f_{\text{umami}}$ or $f_{\text{sour}}$; the flavor space itself is $\mathcal{F}$. Bold lowercase letters are vectors, uppercase letters are matrices, and Greek indices $\mu, \nu$ run over coordinate directions. We work throughout over the real numbers.

## A.1 Riemannian Manifolds, Metric Tensors, and Geodesics

### Manifolds: curved spaces that are flat up close

A **manifold** is a space that looks like ordinary flat Euclidean space $\mathbb{R}^n$ in any small neighborhood, even though its global shape may be curved. The surface of the Earth is the standard example: locally it looks flat (a city map works fine), but globally it is a sphere, and no flat map of the whole thing avoids distortion. The number $n$ is the **dimension** of the manifold — the number of independent coordinates needed to specify a point locally. On the Earth's surface, $n = 2$ (latitude and longitude).

The book's central object, the flavor space $\mathcal{F}$, is modeled as a manifold of dimension on the order of a few tens (Chapter 1, §1.4): each point is a distinct flavor percept, and the coordinates are perceptual directions — taste components, olfactory-manifold coordinates, trigeminal axes, texture. The reason $\mathcal{F}$ is treated as a *manifold* rather than as plain $\mathbb{R}^n$ is that, as we will see, distances and angles in it are not uniform — the space is curved.

A **chart** is a local coordinate system, a way of labeling points in some patch of the manifold by tuples of numbers. The transition between two overlapping charts is required to be smooth, which is what lets us do calculus on the manifold. The **tangent space** at a point $p$, written $T_p$, is the vector space of all directions one can move in from $p$; intuitively it is the flat plane that just touches the manifold at $p$ (the tangent plane to a sphere at one point). Velocities, gradients, and the "fix vectors" of Chapter 1 (lime as $+f_{\text{sour}}$, miso as $+f_{\text{umami}}$) all live in tangent spaces.

### The metric tensor: how to measure length and angle locally

On flat $\mathbb{R}^n$, the distance between nearby points and the angle between two directions come from the familiar dot product. On a curved manifold the dot product itself varies from point to point, and the object that encodes it is the **metric tensor** $g$. At each point $p$, the metric is a symmetric, positive-definite matrix $g_{\mu\nu}(p)$ that defines an inner product on the tangent space $T_p$:

$$ \langle \mathbf{u}, \mathbf{v} \rangle_p = \sum_{\mu,\nu} g_{\mu\nu}(p)\, u^\mu v^\nu. $$

The squared length of an infinitesimal displacement $d\mathbf{x}$ with components $dx^\mu$ is the **line element**

$$ ds^2 = \sum_{\mu,\nu} g_{\mu\nu}(p)\, dx^\mu\, dx^\nu. $$

**[Modeling Axiom.]** When $g_{\mu\nu}$ is the identity matrix everywhere, $ds^2 = \sum_\mu (dx^\mu)^2$ and we recover ordinary Euclidean geometry. The book's claim is that flavor space is *not* of this form. Two features of $g$ carry the geometry:

- The **diagonal entries** $g_{\mu\mu}$ set the local scale of each axis — how much perceptual "distance" a unit step along that coordinate costs. A logarithmic metric, in which a fixed *ratio* of concentrations rather than a fixed *difference* counts as one step, is exactly the Weber–Fechner structure developed in Chapter 3 (§3.1).
- The **off-diagonal entries** $g_{\mu\nu}$ ($\mu \neq \nu$) encode interaction between axes — the degree to which moving along one direction changes the cost or meaning of moving along another. The book uses these to model cross-modal taste interactions: salt–glutamate synergy, sweet suppressing bitter (Chapter 1, §1.1; Chapter 3, §3.2). An off-diagonal metric is the precise statement that the five tastes are not an orthonormal frame.

That the metric **varies with position** — $g_{\mu\nu}$ is a function of $p$, not a constant — is the defining property of a **Riemannian manifold**, and the source of all curvature. "Adding salt near sweetness feels different from adding salt near bitterness" (Chapter 3, §3.2) is the kitchen-level statement that $g_{\mu\nu}(p)$ depends on where in $\mathcal{F}$ you are standing.

### Geodesics: straight lines on a curved space

The length of a curve $\gamma$ running from point $a$ to point $b$ is obtained by integrating the line element along it:

$$ L[\gamma] = \int_a^b \sqrt{\sum_{\mu,\nu} g_{\mu\nu}(\gamma(t))\, \dot{\gamma}^\mu(t)\, \dot{\gamma}^\nu(t)} \; dt, $$

where $\dot{\gamma}$ is the velocity along the curve. A **geodesic** is a locally length-minimizing curve — the manifold's notion of a straight line. On a flat plane, geodesics are ordinary straight lines; on a sphere, they are great-circle arcs (which is why long-haul flight paths bow toward the poles). Geodesics satisfy a second-order differential equation, the geodesic equation, whose coefficients (the Christoffel symbols) are built from derivatives of the metric; one does not need the equation to use the concept, only the idea that the shortest path between two flavors bends according to the local metric.

This is the precise content of the book's recurring claim that **expertise is the ability to follow geodesics**. The line cook of Chapter 1 does not search a list; she moves along the short, metric-respecting path from the flat purée $\mathbf{f}_0$ to the balanced target $\mathbf{f}^\star$. Because the metric is curved, the efficient correction is not "equal parts of everything" but a direction weighted by the local $g_{\mu\nu}$ — which is what years of training encode.

**Worked micro-example.** Consider a tiny two-dimensional flavor patch with coordinates $(x^1, x^2) = (\text{salt}, \text{umami})$ and a constant metric

$$ g = \begin{pmatrix} 1 & 0.6 \\ 0.6 & 1 \end{pmatrix}. $$

The positive off-diagonal $0.6$ encodes salt–umami synergy: the axes are correlated. Take a displacement of one unit along each axis, $d\mathbf{x} = (1, 1)$. Under the Euclidean metric (identity matrix) its squared length would be $1^2 + 1^2 = 2$. Under $g$,

$$ ds^2 = 1\cdot 1^2 + 2\,(0.6)(1)(1) + 1\cdot 1^2 = 2 + 1.2 = 3.2, $$

so $ds \approx 1.79$. Moving along the *joint* salt-and-umami direction covers more perceptual ground than the Euclidean count suggests — a small pinch of salt makes the glutamate "leap forward," and the metric records that the two moves reinforce. Had we instead moved along $d\mathbf{x} = (1, -1)$ (more salt, less umami), we would get $ds^2 = 2 - 1.2 = 0.8$, a *shorter* perceptual step: trading one savory axis against the other partly cancels. The same Euclidean displacement, two different perceptual lengths — that is curvature doing tasteable work.

**Where this is used.** Riemannian structure is the backbone of Chapter 3 (the metric of flavor: Weber–Fechner as a logarithmic metric, position-dependent $g_{\mu\nu}$, Stevens' power law as curvature of iso-intensity surfaces). The olfactory manifold of Chapter 1 (§1.2) and Chapter 2 (§2.4) is a curved sheet inside receptor space. Geodesics reappear as fusion-cuisine interpolation in Chapter 9 (§9.4) and as the seasoning fixed point and stability arguments in Chapter 6 (§6.6). The path-dependence of the metric is flagged as an open problem in Chapter 14 (§14.2). The same differential-geometric apparatus is developed at length in sibling volumes — *Geometric Economics* (Volume 4) treats the decision manifold and its metric tensor in its Chapter 3–4, and *Geometric Cognition* (Volume 6) uses it for representational geometry.

## A.2 Convex Optimization, Simplex Geometry, and Pareto Frontiers

### Convex sets and convex functions

A set $C \subseteq \mathbb{R}^n$ is **convex** if, for any two points $\mathbf{x}, \mathbf{y} \in C$, the entire line segment between them lies in $C$:

$$ \lambda \mathbf{x} + (1-\lambda)\mathbf{y} \in C \quad \text{for all } \lambda \in [0,1]. $$

A disk is convex; a crescent is not. A function $h: \mathbb{R}^n \to \mathbb{R}$ is **convex** if its graph never bulges above any of its chords — formally, $h(\lambda \mathbf{x} + (1-\lambda)\mathbf{y}) \le \lambda h(\mathbf{x}) + (1-\lambda) h(\mathbf{y})$. The decisive practical fact is that **a convex function over a convex set has no local minima other than its global minimum**: if you are at a low point and every nearby direction goes up, you are at *the* low point. This is what makes convex optimization tractable — local search cannot get stuck — and it is why the book repeatedly distinguishes genuinely convex problems (solvable) from non-convex ones with multiple basins (where "junk food is a local optimum," Chapter 11, §11.3).

A **convex optimization problem** has the form: minimize a convex objective $h(\mathbf{x})$ subject to the constraint that $\mathbf{x}$ lie in a convex feasible set, typically specified by convex inequalities $c_i(\mathbf{x}) \le 0$ and linear equalities. The nutritional-requirements set of Chapter 11 (§11.1) — minimum protein, capped sodium, calorie band — is precisely an intersection of such constraints, hence a convex **feasible region**, and the "geometric diet" problem is the search for a point inside it that is also close to the hedonic manifold (§11.5). The inverse-design problem of Chapter 13 (§13.4) — given a target flavor point, find the closest reachable blend of available ingredients — is a convex projection onto the set of feasible mixtures.

### The simplex

The **standard simplex** in $n$ dimensions is the set of non-negative weights that sum to one:

$$ \Delta^{n-1} = \Big\{ \mathbf{w} \in \mathbb{R}^n : w_i \ge 0, \; \sum_{i=1}^n w_i = 1 \Big\}. $$

It is the convex hull of the $n$ unit basis vectors (its **vertices**), which are the pure components; its edges are two-component mixtures, its faces are three-component mixtures, and its interior holds blends that use every component. The simplex is the natural home of any quantity that represents *proportions*: probabilities, mixture fractions, or — in this book — the distribution of perceptual weight across taste qualities. Chapter 1 (§1.1) is explicit that the five cardinal tastes are "not the coordinates of a cube but the vertices of a simplex": a ripe tomato is an interior point weighted toward umami and sweet, not a pure corner. The recipe-as-weighted-sum picture of Chapter 8 (§8.1), $\mathbf{f}_{\text{dish}} = \sum_i a_i \mathbf{f}_i$ with non-negative coefficients, lives on (a scaled version of) the simplex of ingredient proportions.

The simplex also organizes the algorithmic side: the historical **simplex method** of linear programming walks vertex-to-vertex along the boundary of a polytope to optimize a linear objective. **[Theorem.]** A linear function on a bounded convex polytope attains its optimum at a vertex (the fundamental theorem of linear programming). We invoke this only conceptually — to note that boundary/corner solutions (a dish that maxes out one quality) are the linear-programming extreme, while balanced interior solutions require a curved or higher-order objective.

### Pareto frontiers

When two or more objectives conflict and cannot be reduced to a single number, the right notion of "best" is **Pareto optimality**. A point is **Pareto optimal** (or Pareto efficient) if no other feasible point is at least as good on every objective and strictly better on at least one — you cannot improve any objective without sacrificing another. The set of all such points is the **Pareto frontier**.

This is the geometry of trade-offs without a forced exchange rate, and it is the spine of Chapter 11 (§11.2): the palatability–nutrition trade-off has no single "correct" weighting of taste against health, so the honest object is the frontier of diets that are not dominated — each a different, defensible balance. The same structure underlies the design trade-offs of Chapter 13 (mimicking beef flavor while respecting a plant-only ingredient set is a constrained multi-objective problem). The refusal to collapse incommensurable objectives into one scalar is a theme shared with *Geometric Economics* (Volume 4), where the Pareto frontier and the failure of monetary scalarization are developed at length.

**Worked micro-example.** A formulator balances two objectives for a low-sodium broth: maximize perceived savoriness $S$ and minimize sodium $N$. Four candidate formulations score as follows.

| Formula | Savoriness $S$ (higher better) | Sodium $N$ (lower better) |
|---------|-------------------------------|----------------------------|
| A | 0.9 | 0.9 |
| B | 0.7 | 0.5 |
| C | 0.5 | 0.3 |
| D | 0.4 | 0.6 |

Compare D and C: C is both more savory (0.5 > 0.4) and lower sodium (0.3 < 0.6), so **C dominates D** — D is off the frontier. Now compare A, B, C among themselves: A is the most savory but the saltiest; C is the least salty but least savory; B sits between. None of A, B, C dominates another (each wins on one objective), so **{A, B, C} is the Pareto frontier**. There is no formula-independent "winner": choosing among A, B, C means choosing a slope of acceptable trade between salt and savor — exactly the metric choice that Chapter 11 argues must be made explicitly rather than smuggled in through a single palatability score.

**Where this is used.** Convexity and the simplex underlie Chapter 1 (§1.1, taste simplex), Chapter 8 (§8.1, recipes as weighted mixtures), and the constraint sets of Chapter 11 (§11.1) and Chapter 13 (§13.4, inverse design as convex projection). Pareto frontiers are the central object of Chapter 11 (§11.2–11.5, the palatability–nutrition trade-off and the geometric diet) and recur in the design trade-offs of Chapter 13.

## A.3 PCA and Dimensionality Reduction

### The problem: too many coordinates, few real directions

Real data often live in a space of nominally high dimension while actually clustering near a much lower-dimensional subspace. **[Empirical.]** Flavor is the book's leading case: the chemical description of a food runs to thousands of compound concentrations, the receptor layer compresses this to a few hundred channels (roughly 400 functional olfactory receptor types), and the *perceived* flavor varies along only a few tens of effectively independent directions (Chapter 1, §1.4; Chapter 2, §2.4). **Dimensionality reduction** is the family of techniques that recover those few real directions from the many measured ones. **Principal Component Analysis (PCA)** is the workhorse linear method.

### PCA: the directions of maximum variance

Given a dataset of points $\mathbf{x}_1, \dots, \mathbf{x}_m \in \mathbb{R}^n$ (say, $m$ recipes each described by $n$ compound concentrations), PCA proceeds as follows.

1. **Center** the data by subtracting the mean $\bar{\mathbf{x}}$, so the cloud is positioned around the origin.
2. Form the **covariance matrix** $\Sigma = \frac{1}{m}\sum_i (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{x}_i - \bar{\mathbf{x}})^\top$, an $n \times n$ symmetric matrix whose entry $\Sigma_{\mu\nu}$ measures how coordinates $\mu$ and $\nu$ vary together.
3. Compute the **eigenvectors** $\mathbf{v}_1, \mathbf{v}_2, \dots$ and **eigenvalues** $\lambda_1 \ge \lambda_2 \ge \dots \ge 0$ of $\Sigma$. The eigenvectors are the **principal components** — orthogonal directions in the data space; the eigenvalue $\lambda_k$ is the **variance** captured along $\mathbf{v}_k$.

The first principal component $\mathbf{v}_1$ is the single direction along which the data vary most; $\mathbf{v}_2$ is the most-variable direction orthogonal to $\mathbf{v}_1$, and so on. **[Theorem.]** Because the eigenvalues are sorted, keeping the first $k$ components retains as much variance as any $k$-dimensional linear projection can — equivalently, the rank-$k$ truncation is the best rank-$k$ approximation in Frobenius norm (the Eckart–Young theorem). The fraction of total variance explained by the first $k$ components is

$$ \frac{\lambda_1 + \cdots + \lambda_k}{\lambda_1 + \cdots + \lambda_n}, $$

and one chooses $k$ by demanding this fraction be high (often via a "scree" plot, where the eigenvalues drop sharply and then flatten). Projecting each data point onto the top $k$ eigenvectors yields a low-dimensional **embedding** that preserves the dominant structure while discarding small-variance noise directions.

This is exactly the operation the book calls "flavor PCA" (Chapter 2, §2.4): the compression from thousands of compounds to ten to thirty perceptual dimensions is, to first approximation, projection onto the leading principal components of food-compound variation. The "flavor eigenvectors of a cuisine" in Chapter 9 (§9.2) are the principal components of a regional recipe distribution; signature ingredients (soy sauce for Japanese cuisine, cumin for Indian) appear as extreme loadings along particular components (§9.3).

### Relation to the metric, and to nonlinear reduction

PCA is intimately tied to the metric tensor of §A.1. The covariance matrix $\Sigma$ and its inverse define the **Mahalanobis distance** $d(\mathbf{x},\mathbf{y}) = \sqrt{(\mathbf{x}-\mathbf{y})^\top \Sigma^{-1}(\mathbf{x}-\mathbf{y})}$, which is precisely a flat (constant) Riemannian metric whose $g_{\mu\nu}$ is $\Sigma^{-1}$. PCA can be read as finding the coordinate axes in which this metric is diagonal — decorrelating the dimensions. The book's curved flavor metric (Chapter 3) is the local, position-dependent generalization: PCA gives the *global average* geometry, while the Riemannian metric describes how that geometry deforms as one moves through $\mathcal{F}$.

PCA is **linear**, and the olfactory manifold is curved (§A.1, Chapter 1 §1.2). When the low-dimensional structure is a curved sheet rather than a flat subspace, linear PCA must either keep extra components or distort distances. The book accordingly notes nonlinear successors — manifold-learning and embedding methods, and the "Matryoshka" nested-dimension compression of Chapter 10 (§10.4) — that recover curved low-dimensional structure. The same compression philosophy ("how many dimensions do you actually need?") connects to the receptor compression of Chapter 2 and is shared with the embedding work of sibling Volume 6, *Geometric Cognition*.

**Worked micro-example.** Take three foods described by two crudely correlated coordinates, sweetness and perceived ripeness, after centering:

$$ \mathbf{x}_1 = (-2, -1.8), \quad \mathbf{x}_2 = (0, 0.1), \quad \mathbf{x}_3 = (2, 1.7). $$

The points lie almost along the line $y \approx x$ — sweetness and ripeness rise together. The covariance matrix is approximately

$$ \Sigma \approx \begin{pmatrix} 2.67 & 2.33 \\ 2.33 & 2.04 \end{pmatrix}, $$

whose leading eigenvector is close to $\mathbf{v}_1 \approx (0.76, 0.65)$ — the diagonal "ripe-and-sweet" direction — carrying essentially all the variance, while the orthogonal eigenvector $\mathbf{v}_2 \approx (-0.65, 0.76)$ carries almost none. PCA therefore reports that these "two" measured coordinates are really **one** perceptual dimension plus negligible noise: projecting onto $\mathbf{v}_1$ alone loses almost nothing. That is the toy version of the book's recurring finding — nominal flavor dimensions collapse to far fewer effective ones because the underlying biochemistry and perception are correlated (Chapter 2, §2.4).

**Where this is used.** PCA and dimensionality reduction are foundational to Chapter 2 (§2.4, perceptual compression to ten to thirty dimensions), Chapter 9 (§9.2–9.3, the principal components and signature directions of a cuisine), and Chapter 10 (§10.4, flavor compression and the Matryoshka method). The covariance/Mahalanobis connection links back to the metric of Chapter 3, and the pairing-dimension analysis of Chapter 5 (§5.5) is a PCA of human preference data. The reduction $10^4 \to 400 \to {\sim}30$ asserted in Chapter 1 (§1.2) is, layer by layer, a chain of such projections.

## How to Read the Rest of the Book with These Tools

These three toolkits are not independent; they are three views of one idea. The metric tensor of §A.1 measures distance; the covariance matrix of §A.3 is a particular (flat) metric, and PCA is the search for coordinates in which it is diagonal; the convex geometry of §A.2 describes which regions of the space are feasible and which trade-offs are forced. A reader who holds all three in mind will see the book's main argument as a single move repeated in different settings: a problem that looks intractably high-dimensional and combinatorial — thousands of compounds, tens of thousands of ingredient combinations — is in truth low-dimensional, curved, and structured, and the right geometry makes it navigable.

When the main text says a flavor is a point, a fix is a vector, a cuisine is a distribution, balance is a fixed point, and harmony is a manifold, every one of those claims cashes out in the definitions above. The mathematics is standard; what the book contributes is the recognition that flavor was always living inside it. The geometry was always real. The scalars — a single "tastiness" score, a flat list of ingredients — were always insufficient.
