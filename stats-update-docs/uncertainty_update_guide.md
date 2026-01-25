# Understanding the Statistical Engine: Heterogenous Evidence Integration and Uncertainty Classes

## Introduction: What This Document Addresses

The Image Analyser project aims to predict how architectural spaces affect human wellbeing—outcomes such as stress, cognitive performance, wayfinding ability, and satisfaction. To make such predictions responsibly, we require a statistical framework that can handle a fundamental problem: the research literature on environment-behaviour relationships comprises studies of vastly different quality and type. Some studies randomly assigned people to different environments (experiments), whilst others merely observed existing associations (surveys). These study types provide categorically different kinds of evidence, and our statistical engine must respect this distinction.

This document explains how we integrate diverse research findings into a coherent predictive system. The core insight is that uncertainty is not monolithic—we may be uncertain about different things for different reasons, and conflating these forms of uncertainty leads to poor predictions and misguided design recommendations.

---

## Types of Uncertainty

When we read that "natural light is associated with better mood" (Boubekri et al.,), we might ask several distinct questions. Does any relationship exist at all? If so, does light actually *cause* mood changes, or might happier people simply choose brighter spaces? Even if causal, how large is the effect? And does this effect hold across different buildings, climates, and cultures? Each question concerns a different dimension of uncertainty.

**Structural Uncertainty (π)** asks whether any systematic relationship connects two variables. The Greek letter π (pi) represents the probability that an edge exists in our causal diagram—that is, the probability that Variable X and Variable Y are connected at all. Consider the question of whether ceiling height relates to creativity. If several studies find correlations (even modest ones), our confidence that *some* relationship exists increases, regardless of whether we understand the mechanism.

**Causal Identification Uncertainty (γ)** addresses a more demanding question: given that a relationship exists, does X actually cause changes in Y? The Greek letter γ (gamma) represents this probability. This is where study design becomes decisive. A cross-sectional survey finding that people in open-plan offices report more distraction cannot tell us whether the layout causes distraction or whether easily-distracted people happen to work in open-plan offices (perhaps because their organisations differ systematically). An experiment that randomly assigns workers to different layouts can address this question directly.

**Between-Study Heterogeneity (τ²)** captures the possibility that true effects vary across contexts. The symbol τ² (tau-squared) represents the variance of true effects across different settings. A study might find that plants reduce stress in Danish offices, but this effect could be larger or smaller in Brazilian hospitals or Japanese schools. Even with perfect causal identification, we face uncertainty about whether findings generalise.

**Parametric Uncertainty (σ²)** is the familiar uncertainty arising from sampling—the variance around our estimate of the effect size. Larger samples reduce σ² (sigma-squared), but they do not address the other three dimensions. A survey of 10,000 people provides a precise estimate of the association, but it remains merely an association.

**Model Specification Uncertainty (φ)** addresses the question: have we correctly characterised the mathematical form of the relationship between X and Y? The Greek letter φ (phi) represents our confidence that the assumed functional form is appropriate. This dimension is logically prior to the others—if we have misspecified the functional form, our estimates of effect size (θ), heterogeneity (τ²), and even structural existence (π) may be systematically biased.

Consider an environmental attribute such as visual complexity. If the true relationship between complexity and preference follows an inverted-U curve (as Berlyne's arousal theory predicts), but we model it as linear, several problems arise. First, fitting a straight line to curvilinear data will yield an attenuated slope estimate because the positive effects at low-to-moderate complexity partially cancel the negative effects at moderate-to-high complexity. Second, the residual variance will be inflated, making the relationship appear noisier than it truly is. Third, predictions at the extremes will be systematically wrong—we might predict that a maximally complex space produces maximal satisfaction when in fact it produces aversion.
The consequences of model misspecification are not merely statistical but practical. An architect using our system to optimise a healthcare waiting room might receive the recommendation to maximise natural light, when in fact extremely bright spaces produce glare and discomfort. The correct recommendation—to provide moderate, well-diffused daylight—requires that the model capture the curvilinear nature of the underlying relationship.

The expected causal effect now becomes:
E[ΔY | do(X)] = π × γ × φ × θ_correct + π × γ × (1 − φ) × θ_misspecified
where θ_correct represents the effect estimate under the true functional form and θ_misspecified represents the (potentially biased) estimate under an incorrect specification. 

The critical insight is that these dimensions are independent. A massive cross-sectional study has low σ² but low γ. A small randomised experiment has high σ² but high γ. Conflating them produces systematically misleading predictions.

**GRADE Rating (κ)** The GRADE (Grading of Recommendations, Assessment, Development and Evaluation) system provides a standardised method for rating the certainty of evidence in systematic reviews and clinical guidelines, and it serves a complementary function within our framework. Developed initially for medical research synthesis, GRADE classifies evidence into four levels—High, Moderate, Low, and Very Low—based on factors including study design, risk of bias, inconsistency across studies, indirectness of evidence, imprecision, and publication bias (Guyatt et al.,). In our framework, the GRADE rating (denoted κ) functions as an integrative quality indicator that captures aspects of evidence strength not fully represented by the individual uncertainty parameters. Whilst γ specifically addresses causal identification and τ² captures heterogeneity, κ provides a holistic assessment that influences how confidently we should interpret the entire evidence package for a given relationship. Randomised controlled trials begin at "High" certainty and may be downgraded if poorly executed, whilst observational studies begin at "Low" and may be upgraded under specific conditions such as large effect sizes or dose-response gradients. The GRADE-CERQual extension (Lewin et al.,) adapts these principles for qualitative evidence, assessing methodological limitations, coherence, adequacy of data, and relevance. Within the Image Analyser's statistical engine, κ serves as both a summary communication device—allowing users to quickly gauge evidence quality—and a factor in determining how aggressively we update our priors when new evidence arrives. Evidence rated "Very Low" warrants more conservative updating than evidence rated "High," even when holding study design constant, because κ captures implementation quality that design classification alone cannot reflect.

---

## How Different Study Types Inform Different Uncertainties

Research designs vary in what they can tell us. The following classification organises study types by their ability to establish causal relationships.

**Tier 1: High Causal Identification (γ = 0.80–0.95)**

| Type | Description | γ | GRADE Rating | Updates |
|------|-------------|---|--------------|---------|
| RCT | Random assignment to conditions | 0.85–0.95 | High | γ, θ, π, ψ |
| Crossover | Participants experience both conditions in sequence | 0.80–0.90 | High | γ, θ, π, ψ |
| Validated VR | Virtual reality with behavioural validation | 0.75–0.85 | Moderate | γ, θ, π |

Randomised controlled trials (RCTs) achieve high γ because random assignment ensures that, on average, groups differ only in the manipulated variable. Kwallek et al. randomly assigned workers to offices painted different colours and measured productivity—this design permits strong causal inference because pre-existing differences between people were balanced by randomisation.

**Tier 2: Moderate Causal Identification (γ = 0.45–0.80)**

| Type | Description | γ | GRADE Rating | Updates |
|------|-------------|---|--------------|---------|
| Regression Discontinuity | Treatment determined by threshold | 0.70–0.85 | Low→Moderate | γ, θ, π |
| Instrumental Variables | Uses exogenous variation | 0.60–0.80 | Low→Moderate | γ, θ |
| Difference-in-Differences | Before-after with comparison group | 0.55–0.75 | Low→Moderate | γ, θ, π |
| Interrupted Time Series | Multiple measurements before and after | 0.50–0.70 | Low→Moderate | γ, θ, π |
| Prospective Cohort | Follows people over time | 0.45–0.65 | Low | θ, π, ψ, γ |

These quasi-experimental designs approach randomisation through clever use of natural variation. A difference-in-differences study might compare stress levels in two office buildings before and after one building adds a green roof, using the unchanged building as a comparison. This design controls for overall time trends but cannot eliminate all confounds.

**Tier 3: Low Causal Identification (γ = 0.15–0.45)**

| Type | Description | γ | GRADE Rating | Updates |
|------|-------------|---|--------------|---------|
| Cross-sectional (adjusted) | Simultaneous measurement with statistical controls | 0.25–0.45 | Very Low | π, θ, γ (weak) |
| Cross-sectional (unadjusted) | Simple correlations | 0.15–0.30 | Very Low | π, θ |
| Post-Occupancy Evaluation | Comprehensive multi-method assessment | 0.30–0.45 | Low–Moderate | π, θ, mechanisms |
| Before-After (no control) | Pre-post without comparison | 0.25–0.40 | Low | θ (biased), π |

Cross-sectional surveys, however large and carefully conducted, cannot establish causation because they measure exposure and outcome simultaneously. When Newsham et al. found that workers near windows reported higher satisfaction, this could reflect a causal effect of daylight, or it could reflect that senior employees (who differ in many ways) receive window seats.

A crucial point deserves emphasis: **sample size affects σ² but not γ**. A cross-sectional survey with 5,000 participants has the same causal identification strength as one with 50 participants. The larger study estimates the association more precisely, but precision about an association is not evidence for causation.

---

## Qualitative Research and Mechanism Demonstration

Qualitative studies contribute differently to our uncertainty framework. Rather than estimating effect sizes directly, they illuminate mechanisms—the processes by which effects occur.

| Type | Description | γ Contribution | Other Contributions |
|------|-------------|----------------|---------------------|
| Ethnography | Extended observation in context | Strong: temporal sequence + mechanism | π, ψ, moderators, τ² |
| Process Tracing | Systematic examination of causal chains | Very strong: tests observable implications | π, mechanism verification |
| Phenomenological | Deep exploration of lived experience | Moderate: post-hoc rationalisation risk | π, mechanism hypotheses |
| Case Study | In-depth single or multiple cases | Moderate–Strong: depends on process tracing | π, boundary conditions |

Consider Ulrich's hospital window study, which found that patients recovering from surgery healed faster when their window faced trees rather than a brick wall. Supplementary qualitative interviews might reveal *why*—perhaps patients reported feeling less confined, or found the view distracting from pain. Such mechanism evidence strengthens causal interpretation even when the quantitative design alone permits alternative explanations.

Qualitative evidence updates our probability that an edge exists (π) through Bayes factors. When a careful ethnography reveals plausible mechanisms, this constitutes evidence that the relationship is real:

- Strong mechanism demonstration: Bayes factor = 3–10
- Moderate process evidence: Bayes factor = 2–5
- Weak suggestive findings: Bayes factor = 1–2

---

## Triangulation

A powerful strategy for strengthening causal inference involves triangulation: combining evidence from multiple study types with different bias structures (Munafò & Davey Smith,). The logic is probabilistic. If a cross-sectional study could be biased by confounding, and a natural experiment could be biased by selection, but both find the same effect, the probability that both are biased in the same direction decreases multiplicatively.

Formally, if different studies provide independent information about causality with individual γ values, the triangulated estimate is:

γ_triangulated = 1 − ∏(1 − γᵢ)

Consider research on acoustic privacy and cognitive performance. A cross-sectional survey (γ = 0.30) finds that workers in acoustically private spaces report better concentration. A natural experiment exploiting a renovation (γ = 0.60) finds the same pattern. The triangulated γ = 1 − (0.70 × 0.40) = 0.72, substantially higher than either study alone.

This formula assumes the biases are independent—that the factors threatening validity in one study do not overlap with those in another. This assumption requires careful thought about each study's specific vulnerabilities.

---

## How We Assign Parameters to Edges

The statistical engine assigns parameters to each edge (relationship) in our causal diagram. The procedure depends on the quantity and quality of available evidence.

**Tier 1: Meta-Analytic + Experimental Evidence**

When five or more studies exist with at least one experimental design, we conduct formal meta-analysis. The effect size θ and heterogeneity τ² emerge from random-effects models. The causal identification γ begins with the value from the best available design and may be adjusted upward if multiple designs converge (triangulation) or if mechanisms are well-documented.

For example, the relationship between indoor plants and stress reduction has been examined in RCTs (Lohr et al.,), quasi-experiments, and surveys. Meta-analysis provides a pooled effect estimate, and the convergence across designs supports higher γ than any single study type would warrant.

**Tier 2: Limited Quantitative Studies**

With fewer than five studies, we supplement empirical estimates with informed prior distributions. Effect sizes in environmental psychology tend to be modest—Gignac and Szodorai found a median correlation of r = 0.19 across psychology. We use such base rates to construct reasonable priors that are then updated by the available data.

**Tier 3: Qualitative Evidence Only**

When only qualitative evidence exists, we can establish the likely direction of effects (ψ = +1 for positive, −1 for negative) but must use conservative effect size distributions. A series of ethnographies suggesting that high ceilings promote expansive thinking would set ψ = +1 with a modest prior on magnitude.

**Tier 4: Theoretical Only**

For theoretically plausible but empirically untested relationships, we include the edge with low π (probability < 0.50) and use Bayesian model averaging to account for structural uncertainty. The edge might be included in some model runs and excluded in others, weighted by our uncertainty about its existence.

---

## The Goldilocks Framework

The Goldilocks framework integrates with the uncertainty framework in several ways:

**Reducing φ through a priori specification.** 

For Tier 1 attributes, we can confidently specify curvilinear functional forms, setting φ ≈ 0.85–0.95. This eliminates the need to estimate functional form from data and prevents the systematic biases that arise from linear misspecification.

**Informative priors on optimal points.** 

The empirically-grounded optimal ranges provide prior distributions for the location and width of inverted-U curves. Rather than estimating these parameters de novo, we incorporate accumulated knowledge from environmental psychology.

**Structured heterogeneity in optima.** 

The framework acknowledges that optimal points may shift across contexts. Work environments may require lower visual information density (8–12 objects) than social spaces (12–15 objects) to support concentration. This context-dependency can be modelled as heterogeneity in the optimal point (τ²_optimal) rather than heterogeneity in the effect size at optimum.

---

## Propagating Uncertainty Through Predictions

To generate predictions, we use Monte Carlo simulation—running thousands of hypothetical scenarios that respect all four uncertainty dimensions.

For each iteration:
1. Sample whether the edge exists (Bernoulli draw with probability π)
2. If the edge exists, sample whether the relationship is causal (Bernoulli draw with probability γ)
3. If causal, sample the effect size from its distribution (accounting for both σ² and τ²)
4. If not causal, set the effective effect to zero
5. Propagate through the causal diagram using do-calculus
6. Record the predicted outcome

After 10,000 or more iterations, we obtain a distribution of predicted outcomes that properly reflects our uncertainty. The width of prediction intervals conveys not just sampling error but also our uncertainty about causal structure and contextual variation.

---

## Sensitivity Analysis and Research Prioritisation

Some predictions depend critically on assumptions we cannot verify. Sensitivity analysis identifies these dependencies.

**γ-Sensitivity Analysis** examines how predictions change if we assume different values for causal identification. For edges where γ < 0.70, we compute predictions under γ = 0.20, 0.50, and 0.80. Conclusions that reverse across this range are flagged as "causally sensitive"—they depend on assumptions about causation that current evidence cannot resolve.

**τ²-Sensitivity Analysis** examines context-dependency. We compute predictions under τ = 0 (no heterogeneity), 0.10 (moderate), and 0.20 (substantial). Predictions that change dramatically are flagged as "context-sensitive"—they may not generalise from studied contexts to the design context of interest.

**Variance Decomposition** reveals the sources of prediction uncertainty. Using methods such as Sobol indices, we partition prediction variance into contributions from:
- Structural uncertainty (π): not knowing whether relationships exist
- Causal identification (γ): not knowing whether relationships are causal
- Parametric uncertainty (σ²): imprecision in effect estimates
- Heterogeneity (τ²): variation across contexts

This decomposition guides research prioritisation. If uncertainty is dominated by low γ, we need experiments. If dominated by high τ², we need studies in more diverse contexts. If dominated by low π, we need more studies of any type.

**Expected Value of Perfect Information** quantifies the benefit of resolving specific uncertainties. If EVPI for γ is high, conducting an RCT would substantially improve predictions. If EVPI for τ² is high, we need studies in contexts similar to our design application.

---

## Key Metrics Summary

| Metric | Symbol | Definition | Interpretation |
|--------|--------|------------|----------------|
| Structural probability | π | P(edge exists) | Probability that any relationship connects X and Y |
| Causal identification | γ | P(X→Y \| edge exists) | Probability that the relationship is causal |
| Heterogeneity | τ² | Var(true effects) | How much true effects vary across contexts |
| Parametric uncertainty | σ² | Sampling variance | Precision of the effect estimate |
| Model Specification | φ | P(functional form correct) | Probability that we have assigned the appropriate mathematical form |
| Intervention probability | π × γ × φ | — | Probability that intervening on X will change Y |
| Expected effect | π × γ × φ × θ_correct + π × γ × (1 − φ) × θ_misspecified | — | Expected magnitude of causal effect |
| Context effect | N(μ, σ² + τ²) | — | Predicted effect in a specific context |

The compound metric π × γ × φ is particularly important for design decisions. It represents the probability that intervening on X (adding plants, changing lighting, modifying acoustics) will actually change outcome Y in the direction we expect. This is what designers ultimately need to know. The expected causal effect becomes: E[ΔY | do(X)] = π × γ × φ × θ(x)
where θ(x) is the effect at attribute level x, which may be constant (for monotonic relationships) or a function of deviation from optimum (for Goldilocks relationships).

---

## Conclusion

This framework treats uncertainty as multi-dimensional and informative rather than as a nuisance to minimise. By distinguishing structural, causal, heterogeneity, and parametric uncertainty, we can:

1. Appropriately weight different types of evidence
2. Generate predictions with honest uncertainty intervals
3. Identify which uncertainties most constrain design decisions
4. Prioritise future research to reduce the most consequential uncertainties

The Image Analyser's statistical engine implements these principles to bridge the gap between research literature and design practice. Rather than offering false precision, it makes uncertainty visible and actionable—transforming it from a liability into a signal for where additional evidence would be most valuable.

---

## References

Boubekri, M., Cheung, I. N., Reid, K. J., Wang, C. H., & Zee, P. C.. Impact of windows and daylight exposure on overall health and sleep quality of office workers: A case-control pilot study. *Journal of Clinical Sleep Medicine, 10*(6), 603–611. https://doi.org/10.5664/jcsm.3780

Evans, R. J., & Didelez, V.. Parameterizing and simulating from causal models. *Journal of the Royal Statistical Society Series B: Statistical Methodology, 86*(3), 535–568. https://doi.org/10.1093/jrsssb/qkad058

Ferguson, K. D., McCann, M., Katikireddi, S. V., Thomson, H., Green, M. J., Smith, D. J., & Lewsey, J. D.. Evidence synthesis for constructing directed acyclic graphs (ESC-DAGs): A novel and systematic method for building directed acyclic graphs. *International Journal of Epidemiology, 49*(1), 322–329. https://doi.org/10.1093/ije/dyz150

Gignac, G. E., & Szodorai, E. T.. Effect size guidelines for individual differences researchers. *Personality and Individual Differences, 102*, 74–78. https://doi.org/10.1016/j.paid..06.069

Kwallek, N., Soon, K., & Lewis, C. M.. Work week productivity, visual complexity, and individual environmental sensitivity in three offices of different color interiors. *Color Research & Application, 32*(2), 130–143. https://doi.org/10.1002/col.20298

Lawlor, D. A., Tilling, K., & Davey Smith, G.. Triangulation in aetiological epidemiology. *International Journal of Epidemiology, 45*(6), 1866–1886. https://doi.org/10.1093/ije/dyw314

Lewin, S., Booth, A., Glenton, C., Munthe-Kaas, H., Rashidian, A., Wainwright, M.,... & Noyes, J.. Applying GRADE-CERQual to qualitative evidence synthesis findings: Introduction to the series. *Implementation Science, 13*(Suppl 1), 2. https://doi.org/10.1186/s13012-017-0688-3

Lohr, V. I., Pearson-Mims, C. H., & Goodwin, G. K.. Interior plants may improve worker productivity and reduce stress in a windowless environment. *Journal of Environmental Horticulture, 14*(2), 97–100. https://doi.org/10.24266/0738-2898-14.2.97

Munafò, M. R., & Davey Smith, G.. Robust research needs many lines of evidence. *Nature, 553*(7689), 399–401. https://doi.org/10.1038/d41586-018-01023-3

Newsham, G. R., Veitch, J. A., Arsenault, C. D., & Duval, C. L.. Effect of dimming control on office worker satisfaction and performance. *Proceedings of the IESNA Annual Conference*, 1–13.

Pearl, J.. *Causality: Models, reasoning, and inference* (2nd ed.). Cambridge University Press.

Ulrich, R. S.. View through a window may influence recovery from surgery. *Science, 224*(4647), 420–421. https://doi.org/10.1126/science.6143402

Voils, C. I., Sandelowski, M., Barroso, J., & Hasselblad, V.. Making sense of qualitative and quantitative findings in mixed research synthesis studies. *Field Methods, 21*(1), 3–25. https://doi.org/10.1177/1525822X07307463

Zondervan-Zwijnenburg, M. A., Veldkamp, S. A., Nelemans, S. A., Bøe, T., & Beijers, R.. Introduction to Bayesian evidence synthesis. *Behavior Research Methods, 56*(3), 2176–2188. https://doi.org/10.3758/s13428-023-02257-0
