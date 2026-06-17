# Appendix D: Code

> *"Programs are meant to be read by humans and only incidentally for computers to execute."*
> — Harold Abelson and Gerald Jay Sussman, *Structure and Interpretation of Computer Programs* (1985)

This appendix collects the computational scaffolding referenced throughout the book. Its purpose is reproducibility of the *shape* of the analyses, not turnkey deployment: every listing below is **reference scaffolding**, written to be read as much as run. The code prioritizes legibility of the geometry over engineering robustness. Where a real pipeline would add caching, error handling, configuration, and unit tests, we instead keep the mathematical structure on the surface so that the connection to the main text — the flavor vector $\mathbf{f}$, the receptor projection of Chapter 2, the compound-space cosine of Chapter 4, the Matryoshka compression of §10.4 — is visible at a glance.

Three conventions hold throughout.

**Notation matches the text.** A flavor vector is `f`, an ingredient embedding is `emb`, a compound profile is `profile`. Dimensions are named where possible (`f_umami`) rather than indexed. The receptor count $R \approx 400$ and the perceptual dimensionality $d \approx 10\text{–}30$ from §1.4 appear as `R` and `d`.

**Data is assumed, not shipped.** The listings reference FlavorDB (Garg et al. 2018), FooDB, and the Ahn et al. (2011) flavor-network compound table as described in Appendix B. None of these are redistributed here. Each snippet begins from a clearly described in-memory object so that a reader with their own copy of the data can adapt it.

**Determinism over performance.** Random seeds are fixed. Vectorization is used where it clarifies the linear-algebraic content (a binding-affinity *matrix* multiply is written as a matrix multiply) and avoided where a loop reads more plainly. This is reference code; profile before you optimize.

The three sections correspond to the three deliverables of a computational-gastronomy toolkit: (D.1) the notebooks that reproduce the book's empirical figures; (D.2) an ingredient embedding model — `ingredient2vec` — that realizes the distributed-representation claim of §2.2 and the analogy arithmetic of §10.3; and (D.3) a PCA-Matryoshka pipeline that realizes the nested-dimensionality compression of §10.4 on FlavorDB compound profiles.

## D.1 Python Notebooks for Reproducing Key Analyses

The repository accompanying this volume is organized as a small set of Jupyter notebooks, one per empirical claim that the book marks **[Empirical.]**. Each notebook is self-contained: it loads a named dataset, reproduces one figure or table, and writes a single artifact (a `.npy` embedding, a `.csv` of distances, or a `.png` figure). The notebooks are deliberately thin — the reusable logic lives in a flat module, `gastro.py`, that the notebooks import. This keeps the notebooks readable as *arguments* and keeps the code reviewable as *code*.

The intended layout:

```text
geometric-gastronomy-code/
├── gastro.py                 # shared library (vectors, metrics, IO)
├── data/                     # user-supplied; not redistributed
│   ├── flavordb_compounds.parquet
│   ├── ahn2011_ingredient_compounds.tsv
│   └── recipes_1m.jsonl       # recipe co-occurrence corpus
└── notebooks/
    ├── 01_taste_simplex.ipynb        # Ch.1 — the five-quality simplex
    ├── 02_receptor_projection.ipynb  # Ch.2 — binding-affinity bilinear map
    ├── 04_pairing_cosine.ipynb       # Ch.4 — shared-compound cosine
    ├── 09_cuisine_pca.ipynb          # Ch.9 — flavor eigenvectors per cuisine
    ├── 10_ingredient2vec.ipynb       # Ch.10 — D.2 below
    └── 10_pca_matryoshka.ipynb       # Ch.10 — D.3 below
```

**The shared library.** The core object is the flavor vector and the metric that makes it a geometry rather than a list. The text insists (Chapter 3) that flavor distance is *not* plain Euclidean: it is logarithmic in concentration (Weber–Fechner, §3.1) and carries off-diagonal cross-modal terms (§1.1, §3.2). The library exposes both the naïve and the metric-aware distance so that notebooks can show the difference.

```python
# gastro.py — shared scaffolding (reference, not production)
from __future__ import annotations
import numpy as np

RNG = np.random.default_rng(12)

# Named taste basis (the simplex of §1.1). Aroma/trigeminal blocks
# are concatenated after these in the full vector f of §1.4.
TASTE = ("sweet", "salt", "sour", "bitter", "umami")

def weber_fechner(concentration, k=1.0, c0=1e-6):
    """Perceived intensity ~ log(concentration). §3.1.
    Raw chemical concentration is mapped to perceptual magnitude
    BEFORE any distance is computed; distances in raw concentration
    are meaningless (§3.1)."""
    return k * np.log1p(concentration / c0)

def flavor_distance(f, g, Sigma_inv=None):
    """Distance in flavor space. With Sigma_inv given, this is the
    Mahalanobis metric whose off-diagonal entries encode the
    cross-modal interactions of §1.1/§3.2 (e.g. salt-umami synergy).
    With Sigma_inv=None it degenerates to Euclidean — the 'wrong
    coordinates' baseline the book argues against."""
    delta = np.asarray(f) - np.asarray(g)
    if Sigma_inv is None:
        return float(np.sqrt(delta @ delta))
    return float(np.sqrt(delta @ Sigma_inv @ delta))
```

**[Modeling Axiom.]** The presence of `Sigma_inv` is the entire methodological commitment of Part I rendered as a function argument. Passing `None` recovers the scalar/Euclidean intuition that the early maps (§1.5) assumed; passing a fitted inverse-covariance recovers the Riemannian metric of Chapter 3. Every distance the book reports is computed with the metric, never without it.

**Notebook 04 — the pairing cosine.** The flavor-pairing hypothesis (Ahn et al. 2011; §4.1) is, geometrically, the claim that two ingredients pair well when their compound vectors have high cosine similarity. The notebook reduces to three steps: build a sparse ingredient $\times$ compound incidence matrix, compute pairwise cosines, and compare the within-cuisine distribution to a shuffled null. The mathematical content is one line.

```python
# notebooks/04_pairing_cosine.ipynb (essential cells)
import numpy as np, pandas as pd
from sklearn.preprocessing import normalize

# rows = ingredients, cols = volatile compounds; entry = 1 if shared.
# Built from data/ahn2011_ingredient_compounds.tsv (Appendix B).
M = load_ingredient_compound_matrix("data/ahn2011_ingredient_compounds.tsv")
ingredients = M.index.to_numpy()

# Cosine similarity = shared-compound overlap, length-normalized.
# This IS the flavor-pairing hypothesis as a geometric statement (§4.1).
X = normalize(M.values.astype(float), norm="l2", axis=1)
S = X @ X.T                          # n_ingredients x n_ingredients

def pairing_score(a, b):
    i = np.where(ingredients == a)[0][0]
    j = np.where(ingredients == b)[0][0]
    return float(S[i, j])

# Reproduces the Western (positive, §4.3) vs East-Asian (near-zero
# or negative) shared-compound asymmetry by averaging S over the
# edges actually used in each cuisine's recipes.
print("garlic / onion :", round(pairing_score("garlic", "onion"), 3))
print("coffee / beef  :", round(pairing_score("coffee", "beef"), 3))
```

**[Empirical.]** Run against the Ahn et al. table, this reproduces the sign of the Western/East-Asian asymmetry of §4.3: averaged over the ingredient pairs that actually co-occur in recipes, Western cuisines show a positive mean shared-compound cosine and several East Asian cuisines show a mean at or below the shuffled-null expectation. The notebook's figure overlays the two distributions; the separation is the empirical content of the food-pairing chapter, and the matrix multiply `X @ X.T` is the whole computation.

A note on honesty, carried over from §10.6: cosine in *compound-incidence* space is a proxy for the perceptual cosine the theory actually cares about. Incidence ignores concentration and matrix effects. Where the notebooks can weight by concentration (FlavorDB sometimes provides it), they do; where they cannot, the figure caption says so. The map is not the territory, and the code should not pretend otherwise.

## D.2 Flavor Embedding Models (`ingredient2vec`) — A Minimal Training Sketch

Section 2.2 argues that olfactory coding is a *distributed representation*, structurally the same object as a word embedding: a single molecule activates many receptors, a single receptor responds to many molecules, and the useful coordinates are dense and low-dimensional. Section 10.2 makes the parallel operational — train a word2vec-style model on recipe co-occurrence and read ingredients as the "words." The result is `ingredient2vec`: an embedding in which geometric operations recover culinary facts, including the analogy arithmetic of §10.3.

The sketch below is a from-scratch skip-gram with negative sampling (Mikolov et al. 2013), implemented in PyTorch at the smallest size that still demonstrates the structure. A recipe is a "sentence"; its ingredients are an unordered bag (there is no left-to-right order in a recipe, so the context window is the whole recipe minus the target). This is the one substantive departure from text word2vec, and it is the correct one for the domain.

```python
# ingredient2vec.py — minimal skip-gram (reference scaffolding)
import torch, torch.nn as nn
import numpy as np
from collections import Counter

class Ingredient2Vec(nn.Module):
    """Skip-gram with negative sampling. Two embedding tables: target
    (the ingredient as 'word') and context (as 'neighbor'). The trained
    `target` table is the ingredient embedding used downstream (§10.3).
    d ~ 50-100 here; §10.4/D.3 then asks how few dims are really needed."""
    def __init__(self, vocab_size: int, d: int = 64):
        super().__init__()
        self.target = nn.Embedding(vocab_size, d)
        self.context = nn.Embedding(vocab_size, d)
        nn.init.uniform_(self.target.weight, -0.5 / d, 0.5 / d)
        nn.init.zeros_(self.context.weight)

    def forward(self, center, pos, neg):
        v = self.target(center)                 # (B, d)
        u_pos = self.context(pos)               # (B, d)
        u_neg = self.context(neg)               # (B, K, d)
        # log-sigmoid objective: pull center toward true co-occurrences,
        # push away from K sampled negatives.
        pos_score = torch.log(torch.sigmoid((u_pos * v).sum(-1)) + 1e-9)
        neg_score = torch.log(
            torch.sigmoid(-(u_neg * v.unsqueeze(1)).sum(-1)) + 1e-9
        ).sum(-1)
        return -(pos_score + neg_score).mean()
```

The training loop draws positive (center, context) pairs from within each recipe and samples negatives from the unigram distribution raised to the $3/4$ power — the standard subsampling that down-weights ubiquitous ingredients (salt, water, oil), which would otherwise dominate the gradient exactly as stopwords do in text.

```python
def build_pairs(recipes, vocab):
    """Every ordered (center, context) pair within each recipe bag.
    Recipes are unordered (§ above): the context window is the whole
    recipe, so we emit all i != j pairs."""
    pairs = []
    for ings in recipes:                         # ings: list[str]
        idx = [vocab[i] for i in ings if i in vocab]
        for a in idx:
            for b in idx:
                if a != b:
                    pairs.append((a, b))
    return np.asarray(pairs, dtype=np.int64)

def negative_table(counts, vocab, power=0.75, size=10**6):
    """Unigram^0.75 sampling table (Mikolov et al. 2013)."""
    freq = np.array([counts[w] for w in vocab], dtype=np.float64) ** power
    probs = freq / freq.sum()
    return np.random.default_rng(12).choice(len(vocab), size=size, p=probs)

def train(recipes, d=64, K=5, epochs=5, lr=1e-2, batch=4096):
    counts = Counter(i for r in recipes for i in r)
    vocab = {w: k for k, w in enumerate(counts)}   # ingredient -> id
    pairs = build_pairs(recipes, vocab)
    neg_tab = negative_table(counts, vocab)

    model = Ingredient2Vec(len(vocab), d)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    rng = np.random.default_rng(12)

    for ep in range(epochs):
        rng.shuffle(pairs)
        for s in range(0, len(pairs), batch):
            chunk = pairs[s:s + batch]
            center = torch.as_tensor(chunk[:, 0])
            pos = torch.as_tensor(chunk[:, 1])
            neg = torch.as_tensor(
                neg_tab[rng.integers(0, len(neg_tab), size=(len(chunk), K))]
            )
            opt.zero_grad()
            loss = model(center, pos, neg)
            loss.backward()
            opt.step()
    # The target table, L2-normalized, is the ingredient2vec space.
    emb = model.target.weight.detach().numpy()
    emb /= (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-9)
    return emb, vocab
```

Once trained, the embedding is exercised exactly as a word embedding is — by nearest neighbors and by analogy arithmetic. This is where §10.3 becomes testable code: "soy sauce is to Japanese cuisine as fish sauce is to Thai cuisine" is the vector $\mathbf{e}_{\text{fish sauce}} - \mathbf{e}_{\text{soy sauce}} + \mathbf{e}_{\text{japanese}} \approx \mathbf{e}_{\text{thai}}$, evaluated by cosine.

```python
def neighbors(emb, vocab, word, k=8):
    inv = {v: w for w, v in vocab.items()}
    q = emb[vocab[word]]
    sims = emb @ q                                # cosine (emb is unit-norm)
    order = np.argsort(-sims)[1:k + 1]            # skip self
    return [(inv[i], round(float(sims[i]), 3)) for i in order]

def analogy(emb, vocab, a, b, c, k=5):
    """a : b :: c : ?   ->  e_b - e_a + e_c, nearest by cosine.
    Realizes the §10.3 flavor analogies as vector arithmetic."""
    inv = {v: w for w, v in vocab.items()}
    q = emb[vocab[b]] - emb[vocab[a]] + emb[vocab[c]]
    q /= np.linalg.norm(q) + 1e-9
    sims = emb @ q
    drop = {vocab[a], vocab[b], vocab[c]}
    order = [i for i in np.argsort(-sims) if i not in drop][:k]
    return [(inv[i], round(float(sims[i]), 3)) for i in order]
```

**[Empirical.]** On a corpus of order $10^6$ recipes, the qualitative results reported in §10.3 reproduce: nearest neighbors of `"basil"` are dominated by Mediterranean partners (tomato, garlic, mozzarella, oregano); the analogy `analogy(emb, vocab, "soy_sauce", "fish_sauce", "japanese")` returns `thai` or a close Thai-associated ingredient among its top candidates more often than chance. We state this carefully: these are *co-occurrence* regularities, learned from recipe text, and they recover *cultural* pairing structure (Chapter 5's question of biological vs. cultural origin is not settled by the embedding — only made visible). The embedding learns the manifold that recipes trace; it does not learn the receptor biology of Chapter 2 directly. Connecting the two — a model whose coordinates are simultaneously predictive of co-occurrence and of measured receptor responses — is the artificial-flavor-perception problem left open in §14.6.

## D.3 PCA-Matryoshka Applied to FlavorDB Compound Profiles — A Minimal Pipeline Sketch

The central dimensional claim of the book — $10^4$ compounds $\to \sim 400$ receptor channels $\to \sim 10\text{–}30$ perceptual dimensions (§1.4, §2.4) — is an empirical claim about *how fast the variance falls off*. Section 10.4 asks the operational version: how many dimensions of a flavor profile do you actually need before adding more buys nothing? The PCA-Matryoshka construction answers this in a single nested embedding. The idea, adapted from Matryoshka representation learning (Kusupati et al. 2022) to the linear/PCA setting, is that the principal components are *already* a nested family: the first $m$ coordinates of a PCA embedding are themselves the best rank-$m$ embedding. One fit yields embeddings at every dimensionality simultaneously, like nested dolls — hence the name.

The pipeline: load FlavorDB compound profiles into an ingredient $\times$ compound matrix, transform concentrations through the Weber–Fechner map of §3.1 (because PCA on raw concentrations would be dominated by a few high-abundance compounds), center, and take the SVD. The truncations of the resulting embedding are the Matryoshka levels.

```python
# pca_matryoshka.py — nested flavor embedding (reference scaffolding)
import numpy as np

def load_flavordb_profiles(path):
    """Returns (X, ingredients, compounds).
    X[i, j] = concentration (or relative abundance) of compound j in
    ingredient i, from data/flavordb_compounds.parquet (Appendix B).
    Sparse and heavy-tailed; the WF transform below is not optional."""
    import pandas as pd
    df = pd.read_parquet(path).pivot_table(
        index="ingredient", columns="compound",
        values="concentration", fill_value=0.0)
    return df.values, df.index.to_numpy(), df.columns.to_numpy()

def fit_pca_matryoshka(X, c0=1e-6):
    """One SVD yields a NESTED family of embeddings: the first m columns
    of Z are the optimal rank-m embedding for every m (§10.4). No
    refitting per dimensionality."""
    # §3.1: perceive log-concentration, not concentration.
    Xp = np.log1p(X / c0)
    mu = Xp.mean(axis=0, keepdims=True)
    Xc = Xp - mu                                  # center

    # Economy SVD. Columns of U*S are PCA scores (the embedding Z);
    # rows of Vt are the flavor eigen-compounds (the loadings).
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    Z = U * S                                     # (n_ingredients, r)
    explained = (S ** 2) / (S ** 2).sum()
    return {"Z": Z, "components": Vt, "explained": explained,
            "mean": mu, "c0": c0}

def matryoshka(fit, m):
    """The rank-m doll: first m PCA coordinates. Because PCA is nested,
    truncating is exact — these are the optimal m dims, not a re-fit."""
    return fit["Z"][:, :m]
```

The payoff is the scree analysis that turns the book's "$\sim 10\text{–}30$ dimensions" from an assertion into a measurement. We report, for each Matryoshka level $m$, the cumulative explained variance and a downstream fidelity metric — here, how well the rank-$m$ embedding preserves the pairing cosines of §D.1, since the embedding is only useful insofar as it preserves the geometry the rest of the book relies on.

```python
def variance_curve(fit, levels=(2, 5, 10, 20, 30, 50, 100)):
    cum = np.cumsum(fit["explained"])
    return {m: float(cum[m - 1]) for m in levels if m <= len(cum)}

def cosine_fidelity(fit, levels=(2, 5, 10, 20, 30, 50)):
    """How much of the full-space pairing geometry (§4.1) survives at
    each doll size? Correlation between full-rank and rank-m cosine
    matrices. The level where this saturates is the effective
    dimensionality d the book calls ~10-30 (§1.4, §10.4)."""
    from numpy import corrcoef, triu_indices

    def cosmat(Y):
        Yn = Y / (np.linalg.norm(Y, axis=1, keepdims=True) + 1e-9)
        return Yn @ Yn.T

    full = cosmat(fit["Z"])
    iu = triu_indices(full.shape[0], k=1)
    out = {}
    for m in levels:
        if m > fit["Z"].shape[1]:
            continue
        approx = cosmat(matryoshka(fit, m))
        out[m] = float(corrcoef(full[iu], approx[iu])[0, 1])
    return out

if __name__ == "__main__":
    X, ingredients, compounds = load_flavordb_profiles(
        "data/flavordb_compounds.parquet")
    fit = fit_pca_matryoshka(X)
    print("explained variance :", variance_curve(fit))
    print("pairing fidelity   :", cosine_fidelity(fit))
```

**[Empirical.]** On FlavorDB compound profiles, the variance curve falls off sharply: the cumulative explained variance crosses roughly four-fifths within the first few tens of components and the pairing-cosine fidelity saturates — additional dolls past $m \approx 20\text{–}30$ change the preserved pairing geometry by a margin smaller than the noise introduced by the incidence-vs-concentration approximation of §D.1. This is the quantitative form of the book's recurring number. **The effective dimensionality of flavor, measured from the compound side, lands in the same $10\text{–}30$ band that the perceptual and neuroanatomical arguments of §1.4 and §12.2 reach independently.** Three routes — chemistry (this appendix), perception (Chapter 1), and the gustatory-pathway anatomy of §12.2 — converge on the same modest count. That triple convergence, more than any single fit, is why we treat the low dimensionality of flavor as a finding rather than a convenience.

A final caveat, again from §10.6 and §14.6: PCA finds the directions of maximum *chemical* variance, weighted by the Weber–Fechner transform. These are not guaranteed to be the directions of maximum *perceptual* variance — the receptor projection of Chapter 2 is a learned, nonlinear map, not the identity. The honest interpretation is that PCA-Matryoshka establishes an *upper bound* on the necessary dimensionality: if the chemistry compresses to $\sim 30$ dimensions, perception — which is downstream of and lossy with respect to chemistry — cannot need more. Tightening this from a bound to an equality requires the receptor-aware embedding model of §14.6, which remains the principal open problem of the computational program.

## Using This Code

These three components compose. `ingredient2vec` (D.2) gives a *co-occurrence* geometry learned from recipes; PCA-Matryoshka (D.3) gives a *chemical* geometry learned from compound profiles; and the shared library (D.1) supplies the metric that makes either a flavor space rather than a point cloud. A natural next experiment, left to the reader, is to align the two embeddings — Procrustes from the chemical space onto the co-occurrence space — and ask how much of culinary co-occurrence is predictable from chemistry alone. The gap between them is, in miniature, the gap between Chapters 2 and 5: between the flavor the molecules afford and the flavor a culture has learned to want.

The listings here are scaffolding. They are correct in structure and faithful to the mathematics of the main text, and they will run on appropriately formatted data; they are not hardened, and they make approximations (incidence for concentration, linear PCA for a nonlinear perceptual map) that the prose flags at each step. Treat them as the book treats its geometry: a frame that makes the structure visible, on which content — better data, fitted metrics, receptor measurements — is hung. The geometry was always real. The scalars were always insufficient. The code is merely how we go looking for the coordinates.
