# Corrections to Geometric Gastronomy, 2026-11-26

These corrections were made on 2026-11-26 at the author's direction after a review of the Geometric Series.

File names are under `chapters/` unless a root file is named. No figure exists in this volume, so no figure or caption is affected.

## Reconciled

1. **`ch02_the_receptor_basis.md`, Section 2.4.** The text said the second compression, from about 400 receptor channels to 10 to 30 perceptual dimensions, is "10-to-40-fold". It now says "13-to-40-fold". Established by arithmetic on the chapter's own figures: 400/30 is about 13 and 400/10 is 40.

2. **`ch04_similarity_and_complementarity.md`, Section 4.1.** The text gave the size of the compound database as "FlavorDB lists on the order of 2,000 shared volatiles across common ingredients". It now says "FlavorDB catalogs on the order of 25,000 flavor molecules". Established from the volume's own Appendix B (Section B.1 and its summary table) and Section 10.1, which both give FlavorDB about 25,000 flavor molecules. No source for the figure 2,000 is recorded in the repository.

3. **`ch04_similarity_and_complementarity.md`, Section 4.2.** The text said "about 56,000 recipes". It now says "56,498 recipes", the figure Section 9.1 gives for the same corpus of Ahn et al. (2011). The two were consistent, and the chapters now carry the more specific figure.

4. **`ch04_similarity_and_complementarity.md`, Section 4.7.** The text projected the compound vector "through the receptor-affinity matrix R of Section 2.3 into the 10 to 30 perceptual dimensions". Section 2.3 names that matrix A and maps to about 400 receptor channels, and Section 2.5 uses R for the individual rotation. The text now says the projection is through R, "the receptor-affinity matrix A of Section 2.3 followed by the perceptual reduction of Section 2.4". Established by reading Sections 2.3 to 2.5.

5. **`ch06_the_algebra_of_seasoning.md`, Section 6.2.** "In the metric of Chapter 1" now reads "In the metric of Chapter 3". The metric is introduced in Chapter 3.

6. **`ch07_transformations_under_heat.md`, closing section.** The text said the order of operations is "a non-abelian group structure on the maps". Section 8.2 states that the structure is a monoid and not a group, because most cooking operations have no inverse. The sentence now says "a non-abelian structure (strictly a monoid, since most of these maps have no inverse)".

7. **`ch09_the_eigenvalues_of_a_kitchen.md`, Section 9.6, `ch11_the_geometry_of_nutrition.md`, Section 11.5, and `OUTLINE.md`.** The section was headed "The Convergence Theorem" while its statement is tagged a conjecture and no proof is given, and Section 11.5 cited "the convergence theorem of Chapter 9.6". The heading, the citation and the outline line now say "conjecture", and Section 11.5 calls its nutritional reading a conjecture. The weaker form is the one the section itself states.

8. **`ch09_the_eigenvalues_of_a_kitchen.md`, Section 9.4, the running example revisited.** The successful dish is two-thirds dashi essence and one-third mole essence and is placed at t of about 0.5. The sentence now adds "halfway in the mouth, though two-to-one in the pot", which relates the two figures in the way the paragraph already argues (the straight line in ingredient space is not the geodesic in perceptual space).

9. **`ch10_flavor_embeddings.md`, Section 10.1.** The text said FooDB covers "roughly 1,000 foods". It now says "roughly 800 foods", the figure of Appendix B, Section B.1 and its summary table.

10. **`ch11_the_geometry_of_nutrition.md`, Section 11.3.** The text said "Recall from Chapter 5 that the hedonic manifold is rugged, it has many local optima". Chapter 5 describes a bounded, curved, thin region with a ridge and does not say this. Section 6.6 does say that a seasoning fixed point is a local maximum that a distant configuration can beat. The sentence now reads "Recall from Chapter 6 (Section 6.6) that the hedonic landscape is rugged, H has many local optima".

11. **`ch11_the_geometry_of_nutrition.md`, Section 11.6.** The text said supertasters "experience a higher-dimensional, more intense version of the same space". Section 2.6 states that the reading is not a higher-dimensional space but more effective dimensions of the same one. The sentence now says they "experience the same space at higher effective dimensionality and greater intensity".

12. **`ch13_designing_flavors.md`, Section 13.4, the theorem.** The text said the inverse flavor problem "has a unique global minimizer", with proof "from strict convexity of the metric objective over a convex feasible set". The objective is strictly convex in the flavor point Bx, not in the dose vector x, when the palette has more vectors than the flavor space has dimensions, which is the case the chapter describes (thousands of palette materials, a few tens of dimensions). The statement now says the minimum is attained at a unique flavor point Bx, and that the dose vector is unique when the palette vectors are linearly independent. The proof sentence now says "strict convexity of the metric objective in Bx". This is the weaker, correct form. The reachability criterion is unchanged.

13. **`ch14_open_problems.md`, Section 14.1 and the closing section.** Geometric Aesthetics was called "Volume 7" twice. It is now "Volume 13". Established from the README's series list, in which this volume is twelfth and Geometric Aesthetics follows it, from `OUTLINE.md` ("Volume 12 of the Geometric Series"), and from the numbers the other chapters use for Volumes 3, 4 and 6, which follow the same list.

14. **`ch15_appendix_a_mathematical_preliminaries.md`, Section A.3, worked micro-example.** The covariance entry 2.04 is now 2.05 and the eigenvectors (0.76, 0.65) and (-0.65, 0.76) are now (0.75, 0.66) and (-0.66, 0.75). Recomputed from the three printed points: the covariance is [[2.667, 2.333], [2.333, 2.047]] and its leading eigenvector is (0.752, 0.659).

15. **`ch18_appendix_d_code.md`, Section D.1.** The prose said "FlavorDB sometimes provides" concentrations. Appendix B, Section B.1 states that FlavorDB gives no concentrations and that FooDB sometimes does. The prose now says "FooDB sometimes provides it; FlavorDB does not, Appendix B".

16. **`README.md`, Status.** "5 parts, 14 chapters" now reads "5 parts, 14 chapters, 4 appendices", which is what `OUTLINE.md` and the `chapters/` directory hold (18 files).

## Marked as illustrative or simulated

The README's epistemic-status note of 2026-07-14 classes the volume as posited, with no instrument evaluated. The repository holds no data, notebook, run record or output. The passages below reported analyses as carried out. They now say what they are.

1. **`ch04_similarity_and_complementarity.md`, Section 4.7, and the chapter's opening road map.** The section was tagged "[Empirical.]" and said that a reanalysis of Ahn's network with a perceptual embedding had been done, that "two findings emerge consistently", that the asymmetry "sharpens", and that a three-term model "tracks recipe co-occurrence and sensory-panel ratings substantially better than cosine alone". The heading is now "4.7 Experimental Validation: A Proposed Reanalysis", the tag is "[Proposed reanalysis; no run is recorded for this volume.]", and the outcomes are worded as predictions. The conjecture's clause "the cross-corpus validation being still partial" now reads "not yet being in hand". The road map sentence and the `OUTLINE.md` line for 4.7 say the same.

2. **`ch05_the_pairing_manifold.md`, Section 5.4.** "Chapter 4's finding that complementarity, not similarity, is the richer principle" now reads "Chapter 4's argument".

3. **`ch09_the_eigenvalues_of_a_kitchen.md`, Section 9.2.** The named axes of French, Japanese and Mexican corpora were introduced as "a stylized but representative reading" and followed by an "[Empirical.]" paragraph calling the low rank of recipe corpora, with five to ten components, "the robust and repeatedly observed fact". The reading is now called "stylized, illustrative", the tag is "[Expected result; no run is recorded for this volume.]", and the low-rank statement is worded as the claim the framework makes.

4. **`ch10_flavor_embeddings.md`, Section 10.4.** The "[Empirical.]" passage said that on FlavorDB profiles and recipe embeddings 10 to 15 principal components "recover the large majority of the variance" with named interpretable components, and a later sentence said a 12-dimensional prefix "predicts pairing nearly as well as the full vector". Both are now worded as expected results, with the tag "[Expected result; no run is recorded for this volume.]".

5. **`ch14_open_problems.md`, Section 14.5.** "the very cuisine eigenvectors that Chapter 9 extracted from recipe databases" now reads "that Chapter 9 defines on recipe databases".

6. **`ch16_appendix_b_flavor_compound_databases.md`, Sections B.2 and B.4.** "Chapter 4 (Section 4.7) flags when reanalyzing Ahn's network" now reads "flags in its proposed reanalysis of Ahn's network". "a reproducible flavor-space pipeline of the kind used throughout this book and released in Appendix D" now reads "described throughout this book and sketched in Appendix D".

7. **`ch18_appendix_d_code.md`, Sections D.1, D.2 and D.3.** The appendix said "The repository accompanying this volume is organized as a small set of Jupyter notebooks" and gave three "[Empirical.]" paragraphs reporting what the notebooks produce. No notebook or output is in the repository. The text now says the code repository is planned and the notebooks are a design, not yet released. The three paragraphs carry the tag "[Expected result; no run is recorded for this volume.]" and are worded as expectations. The D.1 paragraph notes that the sign of the asymmetry is the published result of Ahn et al. (2011). "Every distance the book reports is computed with the metric" now reads "Every distance the book speaks of is meant with the metric". The closing sentence of D.3 now treats the low dimensionality "as a testable claim", where it said "as a finding". No code listing was changed.

## Withdrawn or updated

Nothing. The volume does not use the dihedral group D4, the Hohfeldian positions, Conservation of Harm, the SU(2) gauge prediction, or the hysteresis result of Geometric Ethics. The word "hysteresis" in Section 14.2 names a candidate model of palate adaptation and is unrelated. The results it cites from Volume 4 (Scalar Irrecoverability, Chapter 6, and the connection of Chapter 8) are at the chapters cited.

## Unresolved

1. **Effective dimensionality from the compound side, Section 10.4 against Appendix D.3.** Section 10.4 expects "10 to 15" principal components to carry most of the variance and a "12-dimensional" prefix to suffice. Appendix D.3 expects four-fifths of the variance "within the first few tens of components" and saturation at "m of about 20 to 30". Both are now worded as expectations, and they still differ. No run exists to settle it. The author would need to run the pipeline or choose one expectation.

2. **Appendix D.3 code against Appendix B.** The listing reads a `concentration` column from FlavorDB profiles and pivots with `fill_value=0.0`. Appendix B states that FlavorDB carries no concentrations and that missing concentrations must never be zero-filled. Code listings were not edited. The author would need to change the listing (FooDB concentrations joined onto the FlavorDB backbone, with the three strata of Section B.4) or the prose.

3. **Forward references that are not delivered.** Section 2.6 and Section 13.5 refer to "robustness of the seasoning fixed point" across a distribution of palates as posed formally in Chapter 6. Chapter 6 does not pose it. Section 2.4 promises "the formal definition of a trained palate in Chapter 12" as recovery of trailing principal components. Chapter 12 has no such definition (Section 12.5 treats expert tasting as a sequence of projections). The author would need to add the material or reword the promises.

4. **Section 4.6, "B is its second fundamental form".** The bilinear interaction term is identified with the second fundamental form of flavor space. The second fundamental form belongs to an embedded submanifold, and the chapter defines no embedding for which B would be it. The loose sense is "a second-order correction to the linear sum". Restating it needs the author.

5. **Uncited statements tagged empirical.** Section 5.5 ("the evidence says three to five ... sensory hedonic studies, factor-analyzed, repeatedly recover"), Section 10.3 ("analogies of this family resolve well above chance"), and the opening of Chapter 10 ("the geometry falls out almost exactly as the perceptual theory predicts", "agrees with the perceptual one on every structural point") describe a literature without a citation or a record in the repository. They were left as they are because they do not claim an analysis of this volume. The author would need to supply the sources or lower the wording.

6. **Ahn et al. (2011) ingredient and compound counts.** Section 4.2 gives "about 380 ingredients" and "about 1,021 compounds". The repository records no exact ingredient count, so the approximate figure was left.

7. **`OUTLINE.md`, line 8.2.** The outline still says "non-abelian group structure". It is a plan and was left, apart from the lines for 4.7 and 9.6.
