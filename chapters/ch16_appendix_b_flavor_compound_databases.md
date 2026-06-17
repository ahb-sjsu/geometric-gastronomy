# Appendix B: Flavor Compound Databases

The geometric theory of flavor developed in this book rests on a claim that is, in the end, empirical: that the flavor of a food can be written as a vector, and that the components of that vector are recoverable from the molecules the food contains. Chapter 1 introduced the chain of projections $10^4 \to 400 \to \sim\!30$ — from the chemical inventory of a food, through the receptor responses, to the perceptual dimensions a trained human can report. The leftmost arrow of that chain is what this appendix is about. Before any geometry can be done, a food must be turned into a list of compounds, and that list must be turned into numbers.

There is no single oracle that performs this step. What exists instead is a small constellation of curated databases, assembled by different groups for different purposes, with different scopes, different identifiers, and different silences. To work in flavor space at all, one must know what these databases contain, how they join to one another, and — most importantly — what they leave out. This appendix surveys the three that matter most (FlavorDB, FooDB, and VCF), then gives the schema and the joins needed to assemble a compound vector, and closes with a fully worked construction of one ingredient's vector from raw records.

A standing caution, which the rest of the appendix will earn: **the compound vector is not the flavor vector.** It is the leftmost object in Chapter 1's chain — a point in the $\sim\!10^4$-dimensional chemical space, not the $\sim\!30$-dimensional perceptual space $\mathcal{F}$. The databases give us the chemistry honestly and the perception only by inference. Conflating the two is the single most common error in computational gastronomy, and it is the error Chapter 10 (§10.6) names as "the map is not the territory."

## B.1 The Three Databases: Contents, Scale, and Access

### FlavorDB

**FlavorDB** (Garg et al., *Nucleic Acids Research*, 2018; updated as FlavorDB2, 2022) is the database most directly aligned with the program of this book, because it is organized around exactly the bipartite structure Chapter 4 exploits: **ingredients on one side, flavor molecules on the other, edges where an ingredient contains a molecule.** It was assembled by the Bagler group at IIIT-Delhi specifically to support computational food-pairing research in the lineage of Ahn et al. (2011), and its design reflects that lineage.

**[Empirical.]** FlavorDB catalogs on the order of **25,000 flavor molecules** and roughly **900–1,000 natural ingredients**, the ingredients grouped into 34 categories (vegetables, fruits, spices, meats, dairy, and so on). For each molecule it stores a chemical identity (name, synonyms, PubChem CID, InChIKey, SMILES), a set of computed molecular descriptors, and — the part that matters for us — a list of **flavor descriptors** ("fruity," "green," "buttery," "sulfurous") drawn from the underlying sensory literature. For each ingredient it stores the set of molecules associated with it and the natural-source ontology (a FlavorDB "entity") that the ingredient belongs to.

Access is through a web interface (a searchable ingredient browser and molecule pages) and, for programmatic use, a REST-style JSON API and downloadable flat files. In practice most analyses download the full ingredient–molecule association table once and work locally; the API is convenient for spot lookups but rate-limited for bulk extraction. The natural unit of a FlavorDB record is the **(ingredient, molecule) association**, which is precisely the entry of the bipartite incidence matrix we will build in §B.2.

What FlavorDB does *not* give you is concentration. An edge means "this molecule has been reported in this ingredient," not "in this amount." This is the database's defining limitation and the source of the most important caveat in §B.2: FlavorDB is, by construction, a **presence/absence (binary) incidence structure.** The flavor network of Ahn et al. that motivated the whole enterprise is itself a presence/absence network, so for reproducing and extending that line of work FlavorDB is the natural home; for anything that depends on *how much* of a compound is present, it is insufficient on its own.

### FooDB

**FooDB** (www.foodb.ca; Wishart group, the same group behind HMDB, DrugBank, and the Human Metabolome Database) is the largest and most chemically detailed of the three. Where FlavorDB is purpose-built for flavor pairing, FooDB is a general **food constituent** database: it aims to record every chemical that has been found in food, flavor-active or not — nutrients, macronutrients, pigments, contaminants, and metabolites alongside the volatiles and tastants we care about.

**[Empirical.]** FooDB covers roughly **800 foods** and on the order of **70,000+ chemical compounds** (the published figure is "over 70,000," with the great majority being constituents that are *not* flavor compounds in any narrow sense). For each compound it stores an exceptionally rich record: structure (SMILES, InChI, InChIKey), classification (the ChemOnt taxonomy from ClassyFire), physicochemical properties, external identifiers (PubChem, ChEBI, CAS, HMDB), and, where available, **concentration data** in specific foods with provenance back to the source literature. It also stores explicit **flavor** and **health-effect** annotations for many compounds.

This is the crucial complement to FlavorDB. FooDB's "Content" records can carry quantitative concentrations (e.g., a compound present at some mg/kg in a given food), with the heavy caveat that coverage is uneven — many food–compound pairs have a qualitative "detected but not quantified" flag rather than a number. FooDB is distributed as a full database dump (downloadable as CSV/JSON or a SQL dump) under terms that permit research use; there is no need to scrape the web interface for bulk work, and you should not.

The cost of FooDB's breadth is that **most of its compounds are noise for flavor purposes.** A naive vector built from "all FooDB compounds in this food" will be dominated by sugars, amino acids, lipids, and assorted metabolites that contribute little or nothing to aroma. Using FooDB well means filtering to the flavor-relevant subspace — which is exactly where its flavor annotations and its joins to FlavorDB and VCF (§B.2) become necessary.

### VCF (Volatile Compounds in Food)

**VCF — Volatile Compounds in Food** (originally the TNO database, Nijssen et al.; maintained commercially, current editions branded VCF Online / Triskelion-BoelensAroma) is the oldest and most specialized of the three, and in a precise sense the most authoritative for aroma. It restricts itself to **volatile** compounds — the molecules that reach the olfactory epithelium and therefore populate the aroma block $\mathbf{a}$ of the flavor vector — and it has been curated continuously since the 1960s from the primary analytical-chemistry literature.

**[Empirical.]** VCF documents on the order of **10,000 volatile compounds** across roughly **several hundred to ~1,000 food products**, with the records traced to **tens of thousands of literature references**. Each entry records the compound, the food in which it was detected, the analytical method, and — distinctively — frequently a **quantitative concentration range** and a literature citation, because VCF's reason for existing is to be a defensible reference for the flavor and fragrance industry. For aroma chemistry specifically, VCF is the gold standard: it is the database a flavorist actually trusts.

The trade-offs are scope and access. VCF is **volatiles only**, so it is silent on non-volatile tastants — it will tell you nothing about the glutamate or the organic acids that anchor the taste block $\mathbf{t}$. And it is a **commercial, subscription** product: there is no free bulk download, access is via a licensed web portal, and its terms generally prohibit redistribution of the underlying data. For reproducible academic pipelines this means VCF is typically used as a high-quality validation and enrichment layer against an open backbone (FlavorDB + FooDB), rather than as the primary corpus.

### Summary of scope

The three databases partition the problem cleanly enough to be worth tabulating. The recurring lesson is that **no single database is complete**: FlavorDB gives the bipartite structure but no quantities; FooDB gives quantities and breadth but mostly non-flavor noise; VCF gives authoritative volatiles but no tastants and no open access.

| | FlavorDB | FooDB | VCF |
|---|---|---|---|
| Built for | Food pairing / flavor networks | Food constituents (general) | Aroma chemistry (industry) |
| Compounds | ~25,000 flavor molecules | ~70,000+ constituents | ~10,000 volatiles |
| Foods / ingredients | ~900–1,000 ingredients | ~800 foods | ~hundreds–1,000 products |
| Quantities? | No (presence/absence) | Sometimes (uneven) | Often (concentration ranges) |
| Scope | Flavor molecules | All constituents | Volatiles only |
| Access | Open (web + JSON + download) | Open (full DB dump) | Commercial subscription |
| Key IDs | PubChem CID, InChIKey, SMILES | PubChem, ChEBI, CAS, HMDB, InChIKey | CAS, compound name |

## B.2 Extracting and Working with Flavor-Compound Vectors

### The object we are building

Fix a vocabulary of $M$ compounds $\{c_1, \dots, c_M\}$ and a set of $N$ ingredients. The raw output of the databases is an **incidence matrix** $A \in \mathbb{R}^{N \times M}$ whose entry $A_{ij}$ records the relationship between ingredient $i$ and compound $j$. The $i$-th row,
$$ \mathbf{c}_i = (A_{i1}, A_{i2}, \dots, A_{iM}) \in \mathbb{R}^{M}, $$
is the **compound vector** of ingredient $i$. In the presence/absence regime (FlavorDB) every $A_{ij} \in \{0,1\}$; in the quantitative regime (FooDB/VCF) $A_{ij}$ is a concentration. This $\mathbf{c}_i$ is the chemical object of Chapter 1's leftmost space; it is not yet the perceptual $\mathbf{f}_i \in \mathcal{F}$, and §B.2's last subsection is about the gap between them.

### The canonical schema

Stripped to essentials, all three databases share the same three-table relational core, and writing it out explicitly is the fastest way to see how they join:

- **`ingredient`** — `(ingredient_id, name, category, source_entity)`. The node on the food side.
- **`compound`** — `(compound_id, name, inchikey, pubchem_cid, smiles, flavor_descriptors, is_volatile)`. The node on the molecule side. The `inchikey` and `pubchem_cid` are the join keys that survive across databases; the human-readable `name` does not (see the caveats).
- **`contains`** — `(ingredient_id, compound_id, concentration, concentration_unit, detection_method, reference)`. The edge. In FlavorDB this table is effectively `(ingredient_id, compound_id)` with the quantitative columns null; in FooDB and VCF the quantitative columns are populated where the source literature supported it.

The incidence matrix $A$ is just this `contains` table pivoted: rows indexed by `ingredient_id`, columns by `compound_id`, values from `concentration` (or $1$ in the binary regime).

### The joins, and why they are the hard part

The reason to learn all three schemas is that **a serious flavor vector is assembled by joining across them**, and the join is where the silent failures live.

**[Modeling Axiom.]** Join on **InChIKey**, never on compound name. The InChIKey is a hashed, canonical representation of molecular structure; it is the only identifier that is both present across FlavorDB, FooDB, and VCF and stable under the synonym chaos of trivial chemical names. "Linalool," "3,7-dimethyl-1,6-octadien-3-ol," and "β-linalool" are the same molecule and should collapse to one column; joining on the string `name` will scatter them across three columns and silently inflate your dimensionality. Where InChIKey is missing, fall back to PubChem CID; fall back to name only as a last resort and only after manual review.

A practical extraction pipeline is then:

1. **Backbone.** Take FlavorDB's `contains` table as the bipartite backbone — it defines which (ingredient, compound) edges are considered "flavor-relevant" at all. This already filters FooDB's 70,000+ constituents down toward the flavor-active subset.
2. **Quantify.** Left-join FooDB's `Content` records onto the backbone by `inchikey`, populating `concentration` where FooDB has it. Most edges will remain quantity-null; that is expected and must be handled deliberately (next subsection), not silently zero-filled.
3. **Enrich and validate aroma.** Where access permits, join VCF by `inchikey`/CAS to confirm volatility and to override FooDB concentrations for volatiles with VCF's better-curated ranges. VCF also supplies a clean `is_volatile` flag for partitioning the vector into its taste vs. aroma blocks.
4. **Vocabulary control.** Restrict the column set $\{c_j\}$ to a fixed vocabulary (e.g., compounds appearing in $\geq k$ ingredients, or compounds with a non-empty flavor descriptor) so that vectors across ingredients live in the same space and are comparable.

### Caveats — the silences that bite

The geometry is only as honest as the matrix, and $A$ has four structural distortions that every downstream result inherits.

**Presence/absence is not concentration.** A binary $A_{ij}$ says strawberry "contains" furaneol and "contains" some trace ester at equal weight $1$, though one defines the fruit and the other is a rounding error. Cosine similarity (Chapter 4) computed on binary vectors therefore measures *chemical overlap of inventories*, not *perceptual similarity of flavor* — a fact that explains both the successes and the failures of the food-pairing hypothesis. When concentrations exist, use them; when they do not, be explicit that you are computing an inventory-overlap statistic.

**Missing data is not zero.** A null in the `contains` table almost always means "not measured in this food," not "measured and absent." Zero-filling — the default behavior of every pivot operation — fabricates absence. This biases $A$ toward whatever foods have been studied most (tomato, coffee, wine, and strawberry are exhaustively profiled; most ingredients are not), an instance of the reporting bias Chapter 4 (§4.7) flags when reanalyzing Ahn's network.

**Detection threshold $\neq$ perceptual threshold.** GC-MS (Appendix C) detects compounds far below the concentration at which a human could smell them, and conversely a compound near or below its **odor detection threshold** contributes nothing to perceived aroma regardless of how it weights the vector. The chemically correct vector and the perceptually correct vector differ by exactly this threshold nonlinearity. The principled fix is to weight each component not by raw concentration $A_{ij}$ but by its **odor activity value** $\text{OAV}_{ij} = A_{ij} / \theta_j$, where $\theta_j$ is compound $j$'s odor threshold; components with $\text{OAV} < 1$ are perceptually silent. This is the first, crudest step of Chapter 1's projection from chemistry toward perception.

**Matrix effects and nonlinearity.** Even OAV-weighting is linear, and perception is not: suppression, synergy, and the nonlinear summation that Chapter 1 (§1.1) called the curvature of the flavor metric all mean that $\mathbf{f}_i$ is a *curved* function of $\mathbf{c}_i$, not a linear readout. The databases give $\mathbf{c}_i$; recovering $\mathbf{f}_i$ requires the receptor model of Chapter 2 and the metric of Chapter 3. **The compound vector is where geometry starts, not where it ends.**

## B.3 Worked Construction: A Compound Vector for Strawberry

To make the pipeline concrete, we construct the compound vector for **strawberry** (*Fragaria × ananassa*) — a deliberately easy case, because strawberry is among the most exhaustively profiled foods in all three databases and its aroma chemistry is genuinely understood.

**Step 1 — Pull the backbone edges.** Query FlavorDB's `contains` table for `ingredient = "strawberry"`. The result is a list of associated flavor molecules — several hundred entries in FlavorDB's full record — each with a PubChem CID and InChIKey. Conceptually:

```
SELECT c.name, c.inchikey, c.pubchem_cid, c.flavor_descriptors, c.is_volatile
FROM contains ct
JOIN ingredient i ON ct.ingredient_id = i.id
JOIN compound  c ON ct.compound_id   = c.id
WHERE i.name = 'strawberry';
```

This yields rows including, among many others, furaneol (4-hydroxy-2,5-dimethyl-3(2H)-furanone; the "strawberry furanone"), methyl butanoate and ethyl butanoate (fruity esters), methyl anthranilate (grape-like), linalool (floral), $\gamma$-decalactone (peachy/creamy), and (E)-2-hexenal (green). At this stage every entry is presence/absence: $A_{ij} = 1$.

**Step 2 — Join concentrations from FooDB.** Left-join FooDB `Content` on `inchikey`. For the well-studied strawberry volatiles this populates concentration ranges (FooDB carries quantitative records for furaneol, the principal esters, and the major lactones); for the long tail of trace compounds the concentration remains null. Resist the urge to zero-fill the nulls — flag them as "present, unquantified" and handle them as a separate stratum.

**Step 3 — Confirm volatiles and thresholds.** Join VCF (where licensed) to confirm `is_volatile` and to attach odor detection thresholds $\theta_j$. Furaneol's threshold is extraordinarily low; its concentration in ripe strawberry is well above it, so its OAV is large. A trace ester present at near-threshold concentration receives an OAV near $1$ and is nearly silent regardless of being chemically present.

**Step 4 — Form the OAV-weighted vector.** For the quantified components, replace raw presence with odor activity value:
$$ A_{\text{straw},\,j} \;\longrightarrow\; \text{OAV}_{\text{straw},\,j} = \frac{[\,c_j\,]_{\text{strawberry}}}{\theta_j}. $$
The result is a vector in which a handful of components dominate. **[Empirical.]** Sensory-chemistry studies of strawberry (e.g., the aroma-recombination work in the Schieberle/Steinhaus tradition) converge on the same short list: furaneol and its methyl ether, a few esters (ethyl/methyl butanoate, methyl hexanoate), $\gamma$-decalactone, and linalool reconstruct most of the recognizable strawberry aroma. In OAV terms the several-hundred-dimensional chemical vector collapses to an effective dimensionality of perhaps a dozen — a concrete instance of the $10^4 \to \sim\!30$ compression Chapter 1 promised, performed here by the odor-threshold nonlinearity alone, before any receptor model is applied.

**Step 5 — Interpret what you have, and what you do not.** The OAV-weighted vector $\mathbf{c}_{\text{strawberry}}$ is now a defensible *chemical* description of strawberry aroma: comparable across ingredients (same vocabulary, same weighting), dominated by the perceptually live components, honest about its quantitative gaps. It is suitable as input to the cosine-similarity pairing analysis of Chapter 4 and as a row in the cuisine-PCA of Chapter 9. It is *not* the perceptual flavor vector $\mathbf{f}_{\text{strawberry}} \in \mathcal{F}$: it carries no taste block (the database aroma records say nothing about the berry's sweetness or acidity, which live in $\mathbf{t}$ and must come from compositional data on sugars and organic acids), and it has not yet been passed through the receptor map of Chapter 2 or the curved metric of Chapter 3 that would turn co-occurring chemistry into co-perceived flavor. The construction has carried us, faithfully and reproducibly, exactly one arrow along Chapter 1's chain — from the food to its chemistry. The remaining arrows are the subject of the main text.

## B.4 Practical Recommendations

For a reproducible flavor-space pipeline of the kind used throughout this book and released in Appendix D, the recommendations reduce to a short list:

- **Use FlavorDB as the bipartite backbone**, FooDB for breadth and concentrations, and VCF (where licensed) for authoritative aroma validation. Treat none of them as complete.
- **Join on InChIKey**, fall back to PubChem CID, and treat name-based joins as a manual-review-only last resort.
- **Never zero-fill missing concentrations.** Distinguish "absent," "present but unquantified," and "quantified" as three explicit strata.
- **Weight by odor activity value, not raw concentration**, whenever thresholds are available; components with $\text{OAV} < 1$ are perceptually silent and should be down-weighted toward zero.
- **State plainly which space you are in.** A result computed on compound vectors is a statement about chemistry; promoting it to a statement about perception requires the machinery of Chapters 2 and 3, and the promotion should be argued, not assumed.

The databases are the empirical floor on which the geometry of this book stands. They are partial, biased toward well-studied foods, and quantitatively uneven — and they are nonetheless enough, handled honestly, to recover the structure the rest of the volume describes. The geometry was always in the chemistry. The databases are how we finally get to count it.
