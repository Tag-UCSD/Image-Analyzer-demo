---
editor_options: 
 markdown: 
 wrap: 72
---

Image-to-Psychology System: Complete Statistical Specifications A
Practical, Scientifically Valid Architecture for Evidence-Based Design
Target Audience: Second-year undergraduates with basic statistics and
programming Version: 1.0 Date: 

Table of Contents

Executive Summary System Overview Statistical Foundations (From First
Principles) Data Collection Requirements Model Architecture
Implementation Roadmap Experimental Validation Program Limitations and
Assumptions Cost and Time Estimates Glossary

1. Executive Summary 1.1 What We're Building A system that:

Takes an image of an interior space (office, living room, hospital)
Extracts visual features (amount of wood, daylight level, spatial
complexity) Predicts psychological outcomes (stress, focus ability,
satisfaction) Explains why (which features drive which outcomes, through
what mechanisms) Suggests design changes ("Add plants to reduce stress
by 15%") Recommends experiments to test uncertain relationships

1.2 Why Current Approaches Fail Problem 1: Black Box AI

Most systems use deep learning: image → prediction No explanation of why
Can't design targeted interventions Not scientifically defensible

Problem 2: Literature Synthesis Without Data

Reviews say "wood reduces stress" but don't specify:

How much wood? Through what mechanism (color? acoustics? cultural
associations)? For which activities/people?

Conflicting studies with no way to reconcile

Problem 3: Overclaiming Precision

Systems that pretend to know more than science actually does Ignore
uncertainty Make causal claims without experimental evidence

1.3 Our Approach (In One Paragraph) We build a modular three-layer model
where:

Visual features are extracted from images (measurable, validated)
Psychological mediators (perceived warmth, cognitive load, acoustic
comfort) are measured through human ratings Outcomes (stress, focus,
satisfaction) are predicted from mediators using causal relationships
validated by experiments

We use Bayesian statistics to combine prior knowledge from literature
with new data, producing predictions with honest uncertainty. We use
do-calculus to answer "what if" questions. We run targeted experiments
to validate mechanisms. We track provenance so every claim traces back
to its evidence. 1.4 What Makes This Feasible Critical decisions that
make it buildable: ✓ We measure mediators, not infer them (solves
identifiability) ✓ We use interventional inference only, not
counterfactuals (simpler, sufficient) ✓ We start small (200 images, 4-6
mediators) and expand incrementally ✓ We use Goldilocks framework to
reduce functional complexity ✓ We run experiments first to validate
causal structure ✓ We're honest about uncertainty (no false precision)

2. System Overview 2.1 The Three-Layer Architecture
 ┌─────────────────────────────────────────────────────────┐ │ INPUT:
 IMAGE │ │ (photo of interior space) │
 └────────────────┬────────────────────────────────────────┘ │ ▼
 ┌─────────────────────────────────────────────────────────┐ │ LAYER
 1: ATTRIBUTES │ │ (Physical/visual features extracted from image) │
 │ │ │ Examples: │ │ • wood_coverage = 35% │ │ • daylight_lux = 450 │
 │ • plant_density = 8% │ │ • spatial_entropy = 2.1 bits │ │ •
 color_temperature = 4200K │ │ │ │ Status: OBSERVABLE via computer
 vision │ └────────────────┬────────────────────────────────────────┘
 │ ▼ ┌─────────────────────────────────────────────────────────┐ │
 LAYER 2: MEDIATORS │ │ (Psychological perceptions/experiences) │ │ │
 │ Examples: │ │ • perceived_warmth = 6.2/10 │ │ • cognitive_load =
 4.8/10 │ │ • acoustic_comfort = 5.5/10 │ │ • spatial_comfort =
 7.1/10 │ │ │ │ Status: MEASURED via human ratings │
 └────────────────┬────────────────────────────────────────┘ │ ▼
 ┌─────────────────────────────────────────────────────────┐ │ LAYER
 3: OUTCOMES │ │ (Psychological states we care about) │ │ │ │
 Examples: │ │ • stress_level = 4.2/10 │ │ • focus_ability = 6.8/10 │
 │ • satisfaction = 7.5/10 │ │ • social_comfort = 6.0/10 │ │ │ │
 Status: MEASURED via human ratings + experiments │
 └─────────────────────────────────────────────────────────┘ 2.2
 Information Flow Forward Prediction (Image → Outcomes): Image →
 [Computer Vision] → Attributes → [Model A] → Mediators → [Model B] →
 Outcomes Model A: Attributes → Mediators

Statistical model: Regression with Goldilocks functions Input: Image
attributes (continuous values) Output: Predicted mediator ratings with
uncertainty Estimated from: N=200 images × 30 human raters

Model B: Mediators → Outcomes

Statistical model: Bayesian causal graph Input: Mediator values
(measured or predicted) Output: Outcome predictions with uncertainty
Estimated from: Experiments + observational data with confound
adjustment

Intervention Queries (What-If Questions): "What if we increase
wood_coverage from 35% → 50%?" → Update attributes → Predict new
mediator values → Predict new outcomes → Report change with uncertainty
2.3 Why This Architecture? Design Principle 1: Modularity

Each layer can be validated independently If computer vision improves,
swap Layer 1 without changing Models A/B If new experiments update Model
B, Layer 1 stays the same

Design Principle 2: Measurability

Attributes: Verifiable via computer vision benchmarks Mediators:
Testable via inter-rater reliability Outcomes: Validatable via
experimental manipulation

Design Principle 3: Interpretability

Can trace any prediction: Outcome ← Mediator ← Attribute ← Image Can
answer: "Why does this image score high on stress?" Can explain: "Wood
matters because it affects perceived warmth (mediator), which reduces
stress (outcome)"

3. Statistical Foundations (From First Principles) This section builds
 up all the statistical concepts you need to understand the system.
 If you're already comfortable with regression, Bayesian inference,
 and causal graphs, you can skim this. If not, read carefully—this is
 your foundation. 3.1 Regression: Predicting One Variable From Others
 The Basic Idea: Suppose you want to predict a person's height (Y)
 from their age (X). You collect data from 100 people and plot it:
 Height \^ \| ● \| ● ● \| ● ● ● \| ● ● ● ● \|● ● ● ●
 +─────────────────\> Age A regression finds the best-fit line
 through these points: Y = β₀ + β₁ × X + ε

Where: - Y = height (what we want to predict) - X = age (what we know) -
β₀ = intercept (height when age = 0, usually meaningless) - β₁ = slope
(how much height changes per year of age) - ε = error (random variation
not explained by age) Example: If β₀ = 80 cm and β₁ = 8 cm/year, then a
10-year-old is predicted to be 80 + 8×10 = 160 cm tall. Multiple
Regression: In our system, mediators depend on many attributes:
perceived_warmth = β₀ + β₁×wood + β₂×daylight + β₃×plants +
β₄×color_temp + ε Each β tells you: "Holding all else constant, if
attribute X increases by 1 unit, mediator Y changes by β units." Key
Assumption: The relationship is linear (or we transform it to be
linear). For Goldilocks attributes, we use a nonlinear function but
still fit via regression: perceived_warmth = β₀ + β₁×goldilocks(wood,
optimal=40%, width=15%) +...

Where goldilocks(x, optimal, width) = exp(-(x - optimal)² / (2×width²))
This is a Gaussian curve centered at the optimal point. 3.2 Why We Need
Bayesian Statistics The Problem with Regular Regression: Regular
regression gives you one best estimate: "β₁ = 0.35" But what if:

Your dataset is small (N=200)? You want to combine results from multiple
studies? You have prior knowledge ("wood probably increases warmth,
based on 10 previous papers")?

Bayesian Solution: Treat Parameters as Random Variables Instead of β₁ =
0.35, we say: β₁ \~ Normal(mean=0.3, sd=0.1) This means: "β₁ is probably
around 0.3, with 95% confidence it's between 0.1 and 0.5." Bayes'
Theorem (The Core Formula): P(β \| Data) ∝ P(Data \| β) × P(β)

Where: - P(β \| Data) = POSTERIOR (what we want: parameters given
data) - P(Data \| β) = LIKELIHOOD (how well data fits for given β) -
P(β) = PRIOR (what we believe before seeing data) In words: Your updated
belief (posterior) is proportional to how well the data fits
(likelihood) times your prior belief. Example for Our System: Prior
(from literature):

"10 studies suggest wood increases perceived warmth, with average effect
of +0.3 ± 0.2" Express as: β_wood \~ Normal(0.3, 0.2)

Likelihood (from our data):

We rate 200 images and see β_wood ≈ 0.25 based on our data alone

Posterior (combined):

Bayesian inference produces: β_wood \~ Normal(0.28, 0.12) Mean shifted
slightly toward our data Uncertainty reduced (0.12 \< 0.2) because we
have more information

Why This Matters:

Honest uncertainty: We report "β = 0.28 ± 0.12", not false precision
Literature integration: We use prior knowledge without ignoring new data
Small sample sizes: Priors prevent overfitting when N is small
Prediction intervals: We can say "predicted warmth is 6.2 ± 0.8" (not
just 6.2)

3.3 Hierarchical Models: Sharing Information Across Groups The Problem:
Suppose you want to estimate the effect of wood on warmth for different
wood types:

Oak Pine Walnut Bamboo

If you have only 20 images with oak, your estimate will be noisy.
Hierarchical Solution: Assume all wood types have similar effects (they
share a common distribution): β_oak \~ Normal(μ_wood, τ²) β_pine \~
Normal(μ_wood, τ²) β_walnut \~ Normal(μ_wood, τ²) β_bamboo \~
Normal(μ_wood, τ²)

Where: - μ_wood = average effect across all wood types - τ² = variation
between wood types This pools information: If oak has little data, its
estimate borrows strength from pine/walnut/bamboo. In Our System: We
group Goldilocks attributes by type:

Cognitive Load Attributes (spatial_entropy, info_density, hierarchy)
Pattern Attributes (fractal_dimension, self_similarity, rhythm) Color
Attributes (saturation, palette_diversity, temperature)

Each group shares a common prior distribution, reducing the effective
number of parameters. 3.4 Causal Inference: Moving Beyond Correlation
The Fundamental Problem: Regression tells you correlation: "Images with
more wood have higher warmth ratings." But does wood cause warmth? Or do
both correlate with something else (e.g., expensive homes have both)?
Wealth /\
▼ ▼ Wood → Warmth? Maybe wealthy homeowners afford both wood and good
lighting, and lighting causes warmth, not wood. Causal Graphs (DAGs): A
Directed Acyclic Graph specifies causal relationships: Wood ────→
Perceived_Warmth ────→ Stress ↗ Lighting ─┘ Arrows mean "causes" (or
"directly affects"). Key Rules:

No cycles: Can't have A→B→C→A Arrows = causal direction: Wood→Warmth
means wood affects warmth, not vice versa Confounders: Variables that
affect both cause and effect (like Wealth above)

The Gold Standard: Randomized Experiments To prove Wood→Warmth causally:

Create two identical rooms Randomly assign one to have wood, one not
Measure warmth ratings If wood room rates higher → causal effect proven

Why? Randomization breaks all confounds. Wealth/lighting/etc. are
equally distributed across groups. Observational Data + Adjustment:
Without experiments, we can sometimes infer causality by:

Measuring confounders: Include lighting, wealth, etc. in the model
Blocking backdoor paths: Ensure all confounding variables are accounted
for Checking robustness: Test if results hold under different
adjustments

In Our System:

Model A (Attributes→Mediators): Observational, we adjust for confounds
where possible, but acknowledge limits Model B (Mediators→Outcomes): We
run experiments to validate causal edges

3.5 Interventional Inference (Do-Calculus) The Question We Want to
Answer: "What would happen if we changed wood coverage from 30% to 50%?"
Why Normal Regression Doesn't Answer This: Regression: P(Warmth \|
Wood=50%) — "Warmth in images that happen to have 50% wood"

This includes all confounds (maybe 50% wood correlates with expensive
homes)

Intervention: P(Warmth \| do(Wood=50%)) — "Warmth if we forced wood to
50%"

This is the causal effect, as if we did an experiment

Do-Calculus (Pearl,): A set of rules for computing interventional
probabilities from observational data + causal graph. Key Insight: If
you know the causal graph and measure enough variables, you can answer
intervention questions without experiments. Example: Graph: Lighting →
Wood → Warmth → Stress ↘ ↗ Wealth To compute P(Stress \| do(Wood=50%)):

"Cut" all arrows into Wood (remove confounds) Set Wood=50% Propagate
forward through Warmth→Stress

In Our System: We use do-calculus to answer designer questions:

"If I add 10% more plants, how does stress change?" "If I increase
daylight from 300 to 600 lux, what happens to focus?"

Implementation: pythondef intervention_query(graph, intervention,
outcome): \# Set intervention node to fixed value graph_do =
graph.copy graph_do.remove_incoming_edges(intervention)
graph_do.set_value(intervention, value)

``` 
# Propagate through model
predicted_outcome = graph_do.predict(outcome)
return predicted_outcome
```

``` 

### 3.6 Why We DON'T Do Counterfactuals

**Counterfactual Question:**

"This specific person rated this room as stress=7. What would *their* stress have been if the room had wood?"

**Why This Is Harder:**

Requires knowing:
1. All structural equations (exact functional forms)
2. Individual-level noise distributions
3. The person's unmeasured traits

**These are not identifiable from data** (Pearl's result).

**Why We Don't Need It:**

Designers care about **population averages**: "Adding wood typically reduces stress by 0.3 points."

They don't care about: "Alice's stress would have been 6.4 instead of 7.0."

**So we skip counterfactuals** and use interventions only (sufficient + identifiable).

### 3.7 Measurement Models and Latent Variables

**The Problem:**

"Perceived warmth" is not directly observable. It's a **psychological construct** inferred from:
- Self-report: "This space feels warm and inviting" (Likert scale 1-7)
- Behavior: Time spent in space
- Physiology: Skin temperature preference

**Measurement Model:**

Links observed indicators (Y) to latent construct (M):
```

Y₁ = λ₁×M + ε₁ (Item 1: "This space feels warm") Y₂ = λ₂×M + ε₂ (Item 2:
"This environment seems cozy") Y₃ = λ₃×M + ε₃ (Item 3: "I would feel
comfortable here")

Where: - M = true latent "perceived warmth" - λ = factor loading (how
strongly each item relates to M) - ε = measurement error

``` 

**Why This Matters:**

If items Y₁, Y₂, Y₃ all correlate (people who rate one high rate others high), this validates that M exists as a coherent construct.

**In Our System:**

We validate mediators via:
1. **Factor analysis:** Do items load on expected factors?
2. **Internal consistency:** Do items correlate (Cronbach's α > 0.7)?
3. **Test-retest reliability:** Do ratings stay consistent over time?

**Critical Decision:** We measure mediators via human ratings (3-5 items each), not try to infer them from attributes alone.

### 3.8 The Goldilocks Principle (Inverted-U Functions)

**The Pattern:**

Many environmental attributes affect outcomes via inverted-U:
```

Outcome \^ \| ●●● \| ● ● \| ● ● \| ● ● \|● ● +─────────────────────\>
Attribute low optimal high

``` 

**Examples:**
- **Visual complexity:** Too little = boring; too much = overwhelming; moderate = engaging
- **Plant density:** None = sterile; excessive = claustrophobic; some = biophilic
- **Spatial entropy:** Uniform = monotonous; chaotic = confusing; varied = interesting

**Mathematical Form:**

Instead of linear β×X, we use:
```

effect = β × exp(-(X - X_optimal)² / (2×σ²))

Where: - X_optimal = best value - σ = tolerance (how quickly it gets
worse away from optimum) Why This Helps:

Reduces parameters: 3 values (β, X_optimal, σ) instead of fitting
arbitrary curves Theory-informed: Goldilocks effects predicted by
arousal theory, cognitive load theory Interpretable: Can tell designers
"optimal wood coverage is 40% ± 15%"

In Our System: We identify \~15-20 Strong Goldilocks attributes and
model them with this functional form.

4. Data Collection Requirements 4.1 Image Corpus Purpose: Train
 computer vision models to extract attributes; provide stimuli for
 human rating. Specifications: Phase 1 (Minimum Viable):

N = 200 images Coverage: Diverse interior types

Offices (open plan, private, co-working) Living rooms (small apartment,
large house, various styles) Healthcare (patient rooms, waiting areas)
Educational (classrooms, libraries)

Quality standards:

Resolution ≥ 1024×768 Good lighting (not over/underexposed)
Representative viewpoint (human eye-level) Minimal post-processing (no
heavy filters)

Sampling strategy: Stratified by key attributes

Wood coverage: 0-10%, 10-30%, 30-50%, 50%+ Daylight: None, low (\<200
lux), medium (200-500), high (\>500) Plant density: None, sparse (\<5%),
moderate (5-15%), high (\>15%) Spatial complexity: Low, medium, high
(based on edge density)

Why 200?

Minimum for stable regression with \~15 predictors (10-15 obs per
predictor rule) Allows \~40 images per major space type Achievable on
realistic budget (\$20-30K for full rating)

Phase 2 (Scale-Up):

N = 1000 images Use active learning: initial model identifies which new
images are most informative Cost: \~\$80-100K

Sources:

Stock photography (Shutterstock, Getty) — \$1-5/image with license
Architectural databases (Architizer, ArchDaily) — free with attribution
Partnered firms — proprietary with permission Synthetic (rendered) —
control experimental variables exactly

4.2 Image Attribute Extraction Purpose: Convert images → numerical
features for modeling. Method 1: Computer Vision Models Use pretrained
networks fine-tuned on our taxonomy: Object Detection:

Model: YOLOv8 or Detectron2 Output: Bounding boxes for furniture,
plants, windows, fixtures Attributes derived: Object counts, coverage
ratios

Semantic Segmentation:

Model: DeepLabv3+ or Mask R-CNN Output: Pixel-level labels (wall, floor,
wood, fabric, glass) Attributes derived: Material coverage %, spatial
zones

Depth Estimation:

Model: MiDaS or DPT Output: Depth map Attributes derived: Spatial
entropy, ceiling height variation, occlusion complexity

Color/Light Analysis:

Direct computation: HSV statistics, illuminance estimation, contrast
ratios No ML needed: Standard image processing

Example attribute computations: python# Wood coverage wood_mask =
segmentation_model.predict(image, class='wood') wood_coverage =
wood_mask.sum / image.size \# → 0.35 (35%)

# Spatial entropy

depth_map = depth_model.predict(image) depth_discrete =
discretize(depth_map, bins=16) entropy = -sum(p \* log2(p) for p in
histogram(depth_discrete)) \# → 2.1 bits

# Fractal dimension

edges = canny_edges(image) fractal_dim = box_counting_dimension(edges)
\# → 1.45

``` 

**Validation:**
- **Ground truth:** Manually label 50 images with high precision
- **Metrics:** IoU >0.7 for segmentation, RMSE <10% for continuous attributes
- **Inter-annotator agreement:** Krippendorff's α >0.8

**Limitations:**
- Depth estimation from single images is approximate (error ~15-20%)
- Lighting estimation depends on camera settings (need calibration if available)
- Occluded features may be missed

**Time/Cost:**
- Model setup: 2-3 weeks, 1 FTE
- Running inference: ~1 second per image on GPU
- Validation annotation: 50 images × 30 min = 25 hours ($500 at $20/hr)

### 4.3 Mediator Ratings (Critical Data)

**Purpose:** Measure psychological perceptions that mediate attribute→outcome effects.

**Mediators to Measure (Phase 1: 4-6 mediators):**

1. **Affective Quality** (combines warmth, pleasantness, coziness)
2. **Cognitive Load** (visual complexity, information processing demand)
3. **Acoustic Comfort** (perceived quietness, speech privacy)
4. **Spatial Comfort** (enclosure, spaciousness, privacy balance)
5. **Restorativeness** (attention restoration, mental restoration)
6. *(Optional) Social Comfort* (appropriateness for social interaction)

**Measurement Instruments:**

**Example: Affective Quality Scale**
```

Instructions: Rate your immediate impression of this space.

1. This space feels warm and inviting. [1=Strongly Disagree] ───
 [7=Strongly Agree]

2. This environment seems cozy and comfortable. [1=Strongly Disagree]
 ─── [7=Strongly Agree]

3. I would feel at ease spending time here. [1=Strongly Disagree] ───
 [7=Strongly Agree]

``` 

**Example: Cognitive Load Scale**
```

1. This space feels visually complex. [1=Very Simple] ─── [7=Very
 Complex]

2. Processing the visual information in this space would be:
 [1=Effortless] ─── [7=Demanding]

3. This environment seems: [1=Clear and organized] ─── [7=Cluttered and
 chaotic]

``` 

**For restorativeness:** Use validated **Perceived Restorativeness Scale (PRS-11)** short form.

**Data Collection Protocol:**

**Platform:** Prolific or MTurk (crowdsourced)

**Per-image rating:**
- Show image for 15 seconds (forced viewing time)
- Present 4-6 mediators × 3 items = 12-18 items
- Add 2 attention checks ("Select 'Strongly Agree' for this item")
- Total time: ~3-4 minutes per image

**Quality control:**
- Require: English fluency, 95%+ approval rate, desktop (not mobile)
- Attention checks: Fail >1 → exclude
- Check response time: <90 seconds → exclude (too fast)
- Check variance: SD=0 for all items → exclude (straight-lining)

**Sample size per image:**
- **N = 30 raters per image** (target ICC > 0.7)
- Some images may need N=40 if ICC is low

**Cost calculation:**
- Base rate: $0.60-0.80 per image rating (4 min × $9/hour minimum)
- 200 images × 30 raters × $0.70 = **$4,200**
- Add 20% for failed attention checks → **$5,000**
- Plus platform fees (20-30%) → **$6,000-6,500 total**

**Timeline:**
- Setup survey (Qualtrics/Gorilla): 1 week
- Pilot test (20 images, 10 raters): 1 week, $150
- Full data collection (200 images, 30 raters): 2-4 weeks depending on recruitment
- **Total: 4-6 weeks**

**Data validation:**
- **Inter-rater reliability:** ICC(2,k) >0.7 for each mediator
- **Internal consistency:** Cronbach's α >0.75 for each scale
- **Exploratory factor analysis:** Confirm items load as expected

**Deliverable:** Dataset of 200 images × 6 mediators with mean ± SD

### 4.4 Outcome Ratings

**Purpose:** Measure target psychological states that designers want to affect.

**Outcomes to Measure (Phase 1: 3-4 outcomes):**

1. **Stress/Relaxation**
 - Single item: "This space would make me feel:" [1=Very Stressed ─── 7=Very Relaxed]
 - Or STAI-6 brief anxiety inventory

2. **Focus Ability**
 - "I could focus on complex work in this space:" [1=Not at all ─── 7=Very well]

3. **Satisfaction**
 - "Overall, I would be satisfied with this space:" [1=Very Dissatisfied ─── 7=Very Satisfied]

4. **Social Comfort** (if measuring social mediator)
 - "This space would be comfortable for social interaction:" [1=Very Uncomfortable ─── 7=Very Comfortable]

**Collection:** Same protocol as mediators (included in same survey).

**Cost:** Included in mediator rating ($6,000 above covers both).

---

## 5. Model Architecture

### 5.1 Model A: Attributes → Mediators

**Purpose:** Predict mediator ratings from image attributes.

**Statistical Form:**

For each mediator *j* (e.g., Affective Quality):
```

M_j = β₀ + Σᵢ βᵢ × f(Attribute_i) + ε

Where: - M_j = mediator rating (mean across raters) - Attribute_i = wood
coverage, daylight, plants, etc. - f(·) = functional form (linear or
Goldilocks) - ε \~ Normal(0, σ²) = residual error

``` 

**Goldilocks Attributes:**

For attributes with known inverted-U relationships:
```

f(X) = goldilocks(X, θ, τ) = exp(-(X - θ)² / (2τ²))

Where: - θ = optimal value (learned) - τ = tolerance width (learned)

``` 

**Linear Attributes:**

For monotonic relationships:
```

f(X) = X

``` 

**Example Model for Affective Quality:**
```

Affective_Quality = β₀ + β₁ × goldilocks(wood_coverage, θ_wood,
τ_wood) + β₂ × goldilocks(plant_density, θ_plant, τ_plant) + β₃ ×
goldilocks(color_saturation, θ_sat, τ_sat) + β₄ × daylight_lux (linear:
more is better) + β₅ × concrete_coverage (linear: more is worse) + ε

``` 

**Hierarchical Structure:**

Group similar attributes to pool information:
```

Goldilocks optimal points: θ_wood \~ Normal(μ_natural_materials,
σ²_natural) θ_plant \~ Normal(μ_natural_materials, σ²_natural)

Effect sizes: β_wood \~ Normal(μ_affective_effects, σ²_affective)
β_plant \~ Normal(μ_affective_effects, σ²_affective)

``` 

**Priors (from literature):**

For each parameter, set prior based on meta-analysis of existing studies:
```

β_wood \~ Normal(0.3, 0.2)\
\# "Wood likely increases warmth, but uncertain by how much"

θ_wood \~ Normal(40%, 10%) \# "Optimal wood coverage probably around
40%, but could be 30-50%"

τ_wood \~ HalfNormal(15%) \# "Tolerance width probably around 15%, not
too narrow or wide" Estimation Method: Option 1: Variational Inference
(fast, approximate)

Tool: PyMC with ADVI Time: Minutes for 200 images Use for: Interactive
UI, rapid iteration

Option 2: MCMC (Hamiltonian Monte Carlo/NUTS) (slow, accurate)

Tool: PyMC or Stan Time: Hours for 200 images Use for: Final estimates,
publication, validation

Validation: Out-of-sample R²:

Split data: 160 train, 40 test Fit on train, predict on test Report R²
(proportion variance explained) Target: R² \>0.4 (decent), \>0.5 (good)

Calibration:

Predicted ± uncertainty should cover true values Check: Do 95% intervals
contain truth 95% of time?

Residual analysis:

Plot predicted vs. actual Check for systematic patterns (suggests
missing features)

Deliverable: For each mediator:

Posterior distributions for all parameters: β_i \~ N(μ, σ²) Predictions:
M_j = μ_predicted ± σ_predicted for each image Model fit: R²,
calibration curves Feature importance: Which attributes matter most?

Implementation (Python pseudocode): pythonimport pymc as pm

with pm.Model as model_A: \# Priors β₀ = pm.Normal('intercept', mu=0,
sigma=1)

``` 
# Goldilocks parameters
θ_wood = pm.Normal('optimal_wood', mu=0.4, sigma=0.1)
τ_wood = pm.HalfNormal('tolerance_wood', sigma=0.15)
β_wood = pm.Normal('effect_wood', mu=0.3, sigma=0.2)

#... (repeat for other attributes)

# Goldilocks function
wood_effect = β_wood * pm.math.exp(-(attributes['wood'] - θ_wood)**2 / (2 * τ_wood**2))

# Linear function
daylight_effect = β_daylight * attributes['daylight']

# Combine
μ = β₀ + wood_effect + daylight_effect +...

# Likelihood
σ = pm.HalfNormal('error', sigma=1)
observed = pm.Normal('affective_quality', mu=μ, sigma=σ, 
 observed=mediator_ratings)

# Inference
trace = pm.sample(, tune=1000, return_inferencedata=True)
```

``` 

**Time/Cost:**

- Model specification: 1 week, 1 FTE
- Initial fitting/debugging: 1 week
- Validation: 1 week
- **Total: 3 weeks, 1 FTE** (~$6,000 in labor)

### 5.2 Model B: Mediators → Outcomes (Causal Graph)

**Purpose:** Estimate causal effects of mediators on outcomes, supporting intervention queries.

**Causal Graph Structure:**

Initial structure based on theory:
```

``` 
 ┌──→ Stress
 │
```

Affective ─┼──→ Satisfaction │ └──→ Social_Comfort

Cognitive ─┬──→ Focus_Ability │ └──→ Stress (cognitive overload)

Spatial ───┬──→ Satisfaction │ └──→ Social_Comfort

Acoustic ──┬──→ Focus_Ability │ └──→ Stress

Restorative→ Stress (via restoration)

``` 

**Statistical Form:**

For each outcome *k*:
```

Outcome_k = β₀ + Σⱼ βⱼ × Mediator_j + Confounds + ε

Where: - Mediator_j = affective quality, cognitive load, etc. -
Confounds = attributes not mediated (direct effects) - ε \~ Normal(0,
σ²)

``` 

**Example for Stress:**
```

Stress = β₀ + β_affective × Affective_Quality (negative: warmth reduces
stress) + β_cognitive × Cognitive_Load (positive: overload increases
stress) + β_acoustic × Acoustic_Comfort (negative: quiet reduces
stress) + β_restorative × Restorativeness (negative: restoration reduces
stress) + β_direct_glare × glare_risk (direct effect not via
mediators) + ε

``` 

**Handling Confounding:**

**In observational data,** mediators may correlate due to:
- Image-level confounds (expensive spaces have good everything)
- Rater effects (some raters rate everything high)

**Solutions:**

1. **Include direct effects:** Add key attributes as covariates
2. **Rater fixed effects:** Control for rater ID (if tracked)
3. **Residualization:** Use mediator residuals after regressing out confounds

**Better: Experimental Validation**

Run experiments to measure causal effects directly (see Section 7).

**Priors:**

From literature, set directional priors:
```

β_affective_on_stress \~ Normal(-0.3, 0.2) \# Negative effect
β_cognitive_on_stress \~ Normal(+0.2, 0.15) \# Positive effect
Estimation: Same Bayesian approach as Model A (PyMC/Stan).
Interventional Queries: To answer "What if Affective_Quality increased
by 1 point?": pythondef intervention_query(mediator, change, graph): \#
Set mediator to new value new_mediators = mediators.copy
new_mediators[mediator] += change

``` 
# Predict outcomes
new_outcomes = graph.predict(new_mediators)

# Compute difference
delta = new_outcomes - original_outcomes
return delta
```

``` 

**Validation:**

- **Cross-validation:** 5-fold, report out-of-sample R²
- **Experimental comparison:** Do predicted effects match experimental results?

**Deliverable:**

- Posterior distributions for all edges: `β_j ~ N(μ, σ²)`
- Intervention function: `predict_do(mediator, value) → outcomes`
- Causal graph visualization with effect sizes

**Time/Cost:**

- Graph specification: 1 week
- Model fitting: 1-2 weeks
- Validation: 1 week
- **Total: 3-4 weeks, 1 FTE** (~$6-8K in labor)

### 5.3 Uncertainty Quantification

**Why It Matters:**

We must distinguish:
- **Aleatory uncertainty:** Random variation (some people just differ)
- **Epistemic uncertainty:** Lack of knowledge (small sample, no experiments)

**Sources of Uncertainty:**

1. **Measurement error:** Raters disagree (ICC <1.0)
2. **Model uncertainty:** Don't know true functional form
3. **Parameter uncertainty:** β could be 0.2 or 0.4
4. **Structural uncertainty:** Is the causal graph correct?

**How We Quantify:**

**Posterior Predictive Distribution:**

Instead of point estimate "Stress = 4.5", report:
```

Stress \~ Normal(4.5, 0.8)

Interpretation: - Best guess: 4.5 - 95% interval: [3.1, 5.9] - Reflects
all sources of uncertainty

``` 

**Sensitivity Analysis:**

Test how predictions change if:
- Priors change (e.g., β_wood ~ N(0.2, 0.3) instead of N(0.3, 0.2))
- Graph structure changes (add/remove edges)
- Confounds are/aren't included

Report: "Stress prediction ranges from 4.2 to 4.8 across plausible models."

**UI Presentation:**
```

┌────────────────────────────────────────┐ │ Predicted Stress Level: 4.5
± 0.8 │ │ │ │ Confidence: MODERATE │ │ [████████░░] 80% certain │ │ │ │
This prediction relies on: │ │ ✓ Measured mediators (high confidence) │
│ ⚠ Observational Mediator→Stress link │ │ (no experiments yet) │ │ ⚠
Assumes causal graph structure │ │ │ │ Suggestion: Run stress validation
│ │ experiment to reduce uncertainty │
└────────────────────────────────────────┘ Implementation: python#
Generate posterior predictive samples samples =
model.posterior_predictive.sample(n=1000)

# Compute credible interval

lower = np.percentile(samples, 2.5) upper = np.percentile(samples, 97.5)
mean = np.mean(samples)

# Display

print(f"Stress: {mean:.1f} [95% CI: {lower:.1f}, {upper:.1f}]")

``` 

---

## 6. Implementation Roadmap

### 6.1 Phase 0: Setup (Months 0-1)

**Goals:**
- Assemble team
- Set up infrastructure
- Finalize specifications

**Tasks:**

1. **Team hiring:**
 - 1 FTE Data Scientist (modeling, statistics)
 - 0.5 FTE Computer Vision Engineer (part-time or contractor)
 - 0.25 FTE Psychometrician (consultant)
 - 1 FTE Research Coordinator (data collection, experiments)

2. **Infrastructure:**
 - Cloud compute (AWS/GCP): $200/month
 - Storage: S3/Cloud Storage for images
 - Software licenses: PyMC, Qualtrics, experiment platforms
 - IRB approval for human subjects research

3. **Documentation:**
 - Finalize attribute taxonomy (list of 50-100 attributes)
 - Finalize mediator scales (3-5 items each, validated)
 - Create annotation guidelines

**Deliverables:**
- Team in place
- Infrastructure running
- IRB approval obtained

**Cost:** ~$10K (hiring, setup, software)
**Timeline:** 1 month

### 6.2 Phase 1: Data Foundation (Months 1-4)

**Goals:**
- Collect image corpus
- Collect mediator + outcome ratings
- Validate psychometric properties

**Tasks:**

**Month 1:**
- Source 200 images (license/photograph)
- Run computer vision models to extract attributes
- Validate attributes on 50 images (manual check)

**Month 2:**
- Design rating survey (Qualtrics/Gorilla)
- Pilot with 20 images, 10 raters
- Analyze pilot: check ICC, internal consistency, completion time
- Revise survey based on pilot

**Months 3-4:**
- Full data collection: 200 images × 30 raters
- Ongoing quality control (check attention, variance)
- May need to collect additional ratings if ICC <0.7 for some images

**Psychometric validation:**
- Factor analysis (EFA): Do items load as expected?
- Reliability: Cronbach's α >0.75 for each scale?
- Inter-rater: ICC >0.7 for each mediator?
- Correlation structure: Are mediators distinct (not r>0.9)?

**Deliverables:**
- Dataset: 200 images × attributes × mediator ratings × outcome ratings
- Validation report: Factor structure, reliability, ICC
- Possibly revised mediator definitions (if some collapse)

**Cost:**
- Images: $1,000 (licenses)
- Computer vision setup: $2,000 (labor)
- Manual validation: $500
- Survey design: $1,000
- Pilot: $150
- Full ratings: $6,000
- Analysis: $2,000
- **Total: ~$12,500**

**Timeline:** 3-4 months (data collection is rate-limiting)

### 6.3 Phase 2: Model Development (Months 4-8)

**Goals:**
- Fit Model A (Attributes→Mediators)
- Fit Model B (Mediators→Outcomes)
- Validate out-of-sample

**Tasks:**

**Months 4-5: Model A**

- Specify model for each mediator (which attributes, which functional forms)
- Implement in PyMC
- Fit using MCMC (may take days for convergence)
- Check diagnostics: R-hat <1.01, ESS >1000
- Validate:
 - Out-of-sample R² (160 train, 40 test)
 - Calibration curves
 - Residual analysis

**Expected outcomes:**
- R² = 0.4-0.6 for most mediators (moderate prediction)
- Some mediators predict better (e.g., Affective Quality from visual features)
- Some worse (e.g., Acoustic Comfort hard to infer from images)

**Months 6-7: Model B**

- Specify causal graph (which mediators → which outcomes)
- Include confounders (direct attribute effects)
- Fit models for each outcome
- Validate:
 - Out-of-sample R²
 - Check if directionality makes sense (affective → stress negative? ✓)

**Month 8: Integration + Intervention Functions**

- Combine Models A and B into full pipeline
- Implement `intervention_query` function
- Test: "Increase wood by 10% → predict mediator changes → predict outcome changes"
- Build uncertainty propagation (sample from Model A posterior, feed to Model B)

**Deliverables:**
- Fitted models with all posteriors
- Validation report (R², calibration, diagnostics)
- Intervention query function

**Cost:**
- Model development: 4 months × 1 FTE = $24,000
- Compute: 4 months × $200/mo = $800
- **Total: ~$25,000**

**Timeline:** 4 months

### 6.4 Phase 3: Experimental Validation (Months 8-15)

**Purpose:** Run experiments to validate causal edges that Model B estimates observationally.

**Strategy:** Focus on highest-impact mediator→outcome links with highest uncertainty.

**Experiment 1: Affective Quality → Stress (Months 8-11)**

**Design:** Manipulate perceived warmth via matched stimuli

- Create photorealistic renders of same room with:
 - Condition A: Warm materials (wood, warm colors) — high affective quality
 - Condition B: Cool materials (metal, concrete, cool colors) — low affective quality
 - **Matched on:** Complexity, daylight, spatial layout, plants
 
**Manipulation check:** Measure affective quality ratings to confirm successful manipulation

**Outcomes:**
- Stress: STAI-6 brief anxiety inventory
- Physiological: Heart rate variability (optional, if budget allows)
- Preference: "How much would you like this space?"

**Sample:** N=200 participants, between-subjects

**Analysis:**
```

Stress = β₀ + β_condition × Condition + ε

Compare to Model B prediction: β_condition =? β_affective ×
(Affective_high - Affective_low) Timeline: 3 months (design, collect,
analyze) Cost: 200 × \$8 = \$1,600 (online study) Experiment 2:
Cognitive Load → Focus (Months 11-14) Design: Manipulate visual
information density

3 conditions (within-subjects):

Low density: Sparse (5 objects/quadrant) Optimal: Moderate (12
objects/quadrant) High density: Cluttered (25 objects/quadrant)

Task: Working memory task (n-back) while viewing space images Measures:

Task performance (accuracy, reaction time) Subjective cognitive load
(NASA-TLX scale) Preference

Sample: N=150 participants (within-subjects, counterbalanced) Analysis:
Test inverted-U for both performance and preference Timeline: 3 months
Cost: 150 × \$12 = \$1,800 Experiment 3: Acoustic Comfort → Focus
(Months 13-15) (if budget allows) Design: Manipulate perceived quietness
via acoustic simulation

Add background noise (office ambience, speech) at varying levels Measure
focus ability via sustained attention task (SART)

Sample: N=120 Timeline: 2-3 months Cost: \$1,000-1,500 Post-Experiment
Model Updates: After each experiment:

Update Model B priors with experimental effect sizes Tighten posteriors
(experiments reduce uncertainty) Mark edges as "experimentally
validated" (green in UI) Re-run predictions to see how they change

Deliverables:

2-3 published papers (experiments + model updates) Validated causal
graph Updated Model B with tighter uncertainty

Total Cost: \~\$5,000-6,000 (online experiments) Timeline: 7 months (can
overlap partially) 6.5 Phase 4: System Integration + UI (Months 12-18)
Goal: Build production system with user-facing interface. Components:
Backend API: pythonPOST /predict Input: {image_url: "..."} Output: {
attributes: {...}, mediators: {...}, outcomes: { stress: {mean: 4.5,
ci_lower: 3.8, ci_upper: 5.2}, focus: {mean: 6.2, ci_lower: 5.6,
ci_upper: 6.8},... }, provenance: [...] }

POST /intervene Input: { image_url: "...", intervention: {wood_coverage:
+0.10} } Output: { original_outcomes: {...}, new_outcomes: {...}, delta:
{...} } Frontend (Designer Interface): Mock-up:
┌─────────────────────────────────────────────────────┐ │ Image Analyzer
│ ├─────────────────────────────────────────────────────┤ │ │ │ [Upload
Image] or [Select from Library] │ │ │ │ ┌─────────────────────┐ │ │ │ │
│ │ │ [Image Preview] │ │ │ │ │ │ │ └─────────────────────┘ │ │ │ │
Detected Features: │ │ • Wood: 35% ████████░░ │ │ • Plants: 8%
██░░░░░░░░ │ │ • Daylight: 450 luxRetryTContinue🌤 │ │ │
├─────────────────────────────────────────────────────┤ │ Predicted
Outcomes: │ │ │ │ 😰 Stress: 4.5 ± 0.8 [Why?] │ │ 🎯 Focus: 6.2 ± 0.6
[Why?] │ │ 😊 Satisfaction: 7.1 ± 0.5 │ │ │ │ [Explore What-If
Scenarios] │ │ │ ├─────────────────────────────────────────────────────┤
│ Recommendations: │ │ │ │ ⚠ Stress is moderate-high. Consider: │ │ •
Increase wood coverage → -0.5 stress │ │ • Add plants (10%+) → -0.3
stress │ │ │ │ [View Experiments to Run] │
└─────────────────────────────────────────────────────┘

**Provenance Viewer:**

Click "Why?" next to any prediction:
┌─────────────────────────────────────────────────────┐ │ Why is Stress
= 4.5? │ ├─────────────────────────────────────────────────────┤ │ Path
Analysis: │ │ │ │ 35% Wood → Affective Quality (6.8) │ │ → Stress -0.4
[Literature: β=-0.3±0.2] │ │ │ │ High Complexity → Cognitive Load (5.2)
│ │ → Stress +0.6 [Experiment #2] │ │ │ │ Net effect: 4.5 (baseline
4.3 + contributions) │ │ │ │ Evidence Strength: │ │ • Wood effect: ⚠
Observational only │ │ • Complexity effect: ✓ Validated experimentally │
│ │ │ [Suggest experiment to validate wood→stress] │
└─────────────────────────────────────────────────────┘

**Experiment Proposer:**
┌─────────────────────────────────────────────────────┐ │ Recommended
Experiment │ ├─────────────────────────────────────────────────────┤ │
Goal: Validate wood → stress pathway │ │ │ │ Design: 2×2 factorial │ │ •
Wood coverage: 20% vs 50% │ │ • Acoustic absorption: Low vs High │ │
(Tests if wood effect is visual or acoustic) │ │ │ │ Sample size: N=180
(90 per cell) │ │ Estimated cost: \$1,440 (online) │ │ Expected
uncertainty reduction: 60% │ │ │ │ [Generate Protocol] [Export Stimuli]
│ └─────────────────────────────────────────────────────┘

**Implementation:**

- **Framework:** React (frontend), FastAPI (backend)
- **Deployment:** Docker containers, AWS/GCP
- **Inference:** Precomputed for fast queries (recompute when models
 update)

**Timeline:** - API: 2 months, 1 FTE - UI: 2-3 months, 1 FTE frontend
developer - Testing: 1 month - **Total: 6 months, 1-2 FTE**

**Cost:** \~\$30,000 (labor) + \$500/mo hosting

### 6.6 Phase 5: Scale-Up (Months 18-24)

**Goals:** - Expand image corpus to N=1000 - Add more
mediators/outcomes - Validate in new building types - Run community
experiments

**Tasks:**

- Active learning: Model identifies most informative images to rate
 next
- Expand to new contexts (healthcare, education, retail)
- Crowdsource experiments (partner with firms to run in real
 buildings)
- Add physiological outcomes (if feasible: HRV, cortisol)

**Cost:** \$50-100K **Timeline:** 6-12 months

------------------------------------------------------------------------

## 7. Experimental Validation Program

### 7.1 Why Experiments Are Essential

**The Problem:**

From observational data alone (ratings of existing images), we cannot
prove causality: Wood coverage correlates with Affective Quality
Affective Quality correlates with low Stress But is this causal? Or:

Do expensive spaces have both wood and good lighting? Do architects who
use wood also use other stress-reducing features? Do raters who like
wood also rate stress low for unrelated reasons?

**The Solution: Randomized Experiments**

By **randomly assigning** participants to see high-wood vs. low-wood
images (matched on all else), we break all confounds.

### 7.2 Experiment Types

**Type 1: Mediator Validation**

**Purpose:** Confirm that manipulating attributes changes mediators as
Model A predicts.

**Example:** Does increasing wood coverage from 20%→50% increase
Affective Quality by 1.2 points (as Model A predicts)?

**Design:** - Between-subjects: Group A sees 20% wood room, Group B sees
50% wood room - Rooms identical otherwise (layout, daylight, complexity,
plants) - Measure: Affective Quality rating

**Analysis:** ΔAffective = Mean(Group B) - Mean(Group A) Compare to
Model A prediction: ΔAffective_predicted = model_A.predict(wood=0.5) -
model_A.predict(wood=0.2) Test: \|ΔAffective - ΔAffective_predicted\| \<
threshold?

**Outcome:** Validate or recalibrate Model A

**Type 2: Causal Pathway Validation**

**Purpose:** Confirm mediator→outcome causal edges.

**Example:** Does increasing Affective Quality reduce Stress?

**Design:** - Manipulate features known to affect Affective (wood,
color, plants) - Measure Affective Quality (manipulation check) -
Measure Stress - Regress: Stress \~ Affective Quality

**Analysis:** β_observed =? β_modelB If close → Model B validated If
different → Update Model B

**Type 3: Mechanism Decomposition**

**Purpose:** Disambiguate which pathway drives an effect.

**Example:** Wood reduces stress via (a) visual warmth, (b) acoustic
absorption, or (c) cultural associations?

**Design: 2×2×2 factorial**

| Condition | Visual Wood | Acoustic Absorption | Label |
|-----------|-------------|---------------------|----------------|
| 1 | No | No | "Synthetic" |
| 2 | Yes | No | "Wood veneer" |
| 3 | No | Yes | "Fabric" |
| 4 | Yes | Yes | "Solid wood" |
| 5 | No | No | "Natural wood" |
| 6 | Yes | No | "Natural wood" |

(Simplified: may need fewer cells or within-subjects design)

**Measures:** - Affective Quality, Acoustic Comfort (mediators) - Stress
(outcome)

**Analysis:** Stress = β₀ + β_visual×Visual + β_acoustic×Acoustic +
β_label×Label + β_interaction×Visual×Acoustic + ε Which β is largest? →
Primary mechanism identified

**Outcome:** Update causal graph with validated pathways

### 7.3 Detailed Example: Experiment 1 (Affective → Stress)

**Hypothesis:** Spaces rated higher on Affective Quality produce lower
stress.

**Design:**

**Stimuli Creation:** 1. Generate photorealistic renders of the same
base room (Blender/Unreal) 2. Create 4 versions varying
materials/colors: - **Condition A (Low Affective):** Concrete, metal,
cool gray colors - **Condition B (Medium-Low Affective):** Painted
drywall, neutral colors - **Condition C (Medium-High Affective):** Light
wood, warm beige - **Condition D (High Affective):** Rich wood, warm
terracotta, textiles

3. **Hold constant:** Layout, furniture, daylight, plants, ceiling
 height

**Manipulation Check (Pilot, N=40):** - Rate all 4 conditions on
Affective Quality - Confirm: A \< B \< C \< D (statistically significant
differences)

**Main Study (N=200):**

**Recruitment:** Prolific, require 95%+ approval, desktop, English
fluency

**Procedure:** 1. Participants randomly assigned to one condition
(between-subjects) 2. View image for 30 seconds (forced viewing) 3.
Imagine spending 1 hour working in this space 4. Complete measures: -
**Affective Quality:** 3 items (manipulation check) - **STAI-6:** 6-item
brief anxiety scale (stress outcome) - **Satisfaction:** Single item -
**Preference:** "How much would you like this space?"

**Duration:** \~5 minutes

**Payment:** \$0.80 (=\$9.60/hour)

**Quality Control:** - 2 attention checks ("Select 'Strongly Agree'
here") - Response time: Exclude if \<2 minutes (too fast) - Check
variance: Exclude if all ratings identical

**Analysis Plan (Pre-Registered):**

**Primary analysis:** Model 1: Stress \~ Condition + ε Test: Linear
trend across conditions (A \> B \> C \> D)? Model 2: Stress \~
Affective_Quality + ε β_affective =? β_modelB (from Model B)

**Secondary:** - Mediation analysis: Condition → Affective → Stress -
Test if effect is fully mediated by Affective Quality

**Power Analysis:** - Assume effect size d=0.5 (medium) - N=50 per
condition → Power=0.80 to detect - Total N=200 allows detection of d=0.4

**Expected Results:**

**Scenario 1 (Model B correct):** - Observed β_affective ≈ -0.3 (as
predicted) - Model validated ✓

**Scenario 2 (Model B overestimated):** - Observed β_affective ≈ -0.15 -
Update Model B: Reduce β_affective posterior mean - Tighten uncertainty
(now we have experimental data)

**Scenario 3 (No effect):** - β_affective ≈ 0 - Model B was wrong -
Remove or weaken this edge in graph

**Cost Breakdown:** - Stimuli creation (rendering): \$500 (contractor, 5
hours × \$100/hr) - Prolific fees: 200 × \$0.80 = \$160 - Platform fees
(33%): \$53 - Pilot: 40 × \$0.80 = \$32 - **Total: \~\$750**

**Timeline:** - Stimuli creation: 1 week - Pilot: 1 week (recruit +
analyze) - Main study: 2 weeks (recruit + collect) - Analysis: 1 week -
Write-up: 2 weeks - **Total: 7 weeks**

**Deliverable:** - Experimental paper (submit to Journal of
Environmental Psychology) - Updated Model B with validated edge -
Provenance: Mark "Affective→Stress" edge as experimentally validated

### 7.4 Experiment Portfolio (Full Program)

**Phase 3 Experiments (Months 8-15):**

| \# | Experiment | Purpose | N | Cost | Timeline |
|----|----|----|----|----|----|
| 1 | Affective→Stress | Validate key mediator→outcome | 200 | \$750 | 7 weeks |
| 2 | Cognitive Load→Focus | Test inverted-U | 150 | \$900 | 7 weeks |
| 3 | Wood Mechanism | Decompose visual/acoustic/semantic | 240 | \$1,500 | 8 weeks |
| 4 | Plant Dose-Response | Find optimal plant density | 180 | \$800 | 7 weeks |
| 5 | Acoustic→Focus | Validate acoustic pathway | 120 | \$600 | 6 weeks |

**Total Phase 3 Cost:** \~\$4,500 **Total Phase 3 Time:** \~35 weeks
(some can overlap)

**Phase 5 Experiments (Months 18-24):**

After initial validation, run: - **Context moderators:** Do effects
differ by task type (focus work vs. social vs. restorative)? -
**Individual differences:** Personality (introversion), expertise
(architects vs. laypeople), culture - **Long-term exposure:** Do
preferences shift after repeated exposure (adaptation)? - **Real-world
validation:** Partner with firms to test in actual buildings (pre/post
redesign)

**Estimated Cost:** \$10-20K **Timeline:** 6-12 months

------------------------------------------------------------------------

## 8. Limitations and Assumptions

### 8.1 What This System CAN Do

✓ **Predict outcomes from images** with quantified uncertainty ✓
**Explain predictions** via mediators (warm space → low stress because
warmth is calming) ✓ **Answer "what if" questions** (what if we add
plants?) ✓ **Prioritize design changes** (which changes have biggest
impact?) ✓ **Recommend experiments** to reduce uncertainty ✓ **Integrate
literature** via Bayesian priors (without false precision) ✓ **Track
provenance** (which claim comes from which study/experiment?)

### 8.2 What This System CANNOT Do

✗ **Predict individual responses** (only population averages) ✗
**Measure unmeasured mediators** (if we skip data collection, model
fails) ✗ **Prove causality without experiments** (observational data has
limits) ✗ **Generalize beyond training distribution** (if you only rate
offices, predictions for hospitals are extrapolations) ✗ **Account for
all context** (activity, culture, time of day matter but aren't in
images) ✗ **Replace human judgment** (designers still make final calls)

### 8.3 Critical Assumptions

**Assumption 1: Image ratings generalize to real experience**

**Assumption:** People's ratings of images correlate with how they'd
feel in the actual space.

**Evidence for:** - Virtual reality studies show moderate correlation
(r=0.6-0.7) between VR and real-space ratings - Images capture most
visual information (which dominates environmental perception)

**Evidence against:** - Images miss: Sound, smell, temperature,
kinesthetic experience, temporal dynamics - Images are static (can't
explore)

**Mitigation:** - Validate on subset: Compare image ratings to
real-space ratings (when possible) - Acknowledge: Our system predicts
visual responses primarily - For acoustic/thermal outcomes, use image
cues as *proxies* (known to be noisy)

**Assumption 2: Mediators measured at group level apply to new images**

**Assumption:** The relationship "wood → affective quality" learned from
200 images generalizes to new images.

**Validity:** - Requires representative sampling of image space -
Requires stable relationships (not context-dependent)

**Mitigation:** - Diverse training set (many room types, styles) - Test
on out-of-distribution images (different eras, cultures) - Report when
extrapolating beyond training data

**Assumption 3: Causal graph structure is correct**

**Assumption:** Mediators → Outcomes follows the graph we specified.

**Validity:** - Theory-informed (based on environmental psychology) -
But theory could be wrong or incomplete

**Mitigation:** - **Test alternative graphs:** Fit competing models,
compare via cross-validation - **Sensitivity analysis:** How much do
predictions change if we add/remove edges? - **Experimental
validation:** Experiments can falsify edges

**Assumption 4: Literature priors are informative**

**Assumption:** Studies in the literature generalize to our context.

**Problems:** - Different populations (students vs. workers vs.
patients) - Different measures (cortisol vs. self-report stress) -
Different designs (lab vs. field)

**Mitigation:** - **Wide priors:** Don't trust literature too much
(large σ) - **Prior sensitivity:** Test how much priors affect
posteriors - **Prefer recent, high-quality studies** (RCTs \>
observational)

**Assumption 5: Static images capture temporal dynamics**

**Assumption:** A single snapshot represents the space adequately.

**Problems:** - Lighting changes throughout day - Spaces are experienced
over time (not one glance) - People move through spaces (not static
viewpoints)

**Mitigation:** - For dynamic spaces (e.g., daylight), collect multiple
images (morning/afternoon) - Acknowledge: System best for evaluating
static moments, not full temporal experience - Future: Add temporal
dimension (time-lapse, video)

### 8.4 Boundary Conditions (When System Fails)

**Scenario 1: Novel/Extreme Spaces**

If you upload an image very different from training data (e.g.,
futuristic spaceship interior), predictions will be unreliable (high
uncertainty).

**System should:** Detect out-of-distribution inputs, warn user, report
very wide uncertainty

**Scenario 2: Context-Specific Effects**

Some effects depend on activity (open office is bad for focus, good for
collaboration). If activity isn't specified, system gives average across
all activities.

**System should:** Ask for context ("What activity will occur here?")
and adjust predictions

**Scenario 3: Cultural Differences**

Preferences for wood, colors, spatial layout vary by culture. If
training data is Western-centric, predictions for non-Western spaces may
be biased.

**System should:** Either collect diverse training data OR restrict
claims ("validated for North American offices")

**Scenario 4: Long-Term vs. Short-Term**

Image ratings reflect immediate impressions. Some effects emerge over
time (e.g., adaptation, boredom).

**System should:** Clarify that predictions are for initial impressions,
not long-term satisfaction

------------------------------------------------------------------------

## 9. Cost and Time Estimates

### 9.1 Development Costs (Phase 1-4)

| Phase | Component | Duration | Labor Cost | Other Cost | Total |
|----|----|----|----|----|----|
| **0** | **Setup** | 1 mo | \$8K (team) | \$2K (infra) | **\$10K** |
| **1** | **Data Collection** | 3-4 mo | \$5K (coord) | \$7.5K (ratings) | **\$12.5K** |
| **2** | **Model Development** | 4 mo | \$24K (scientist) | \$1K (compute) | **\$25K** |
| **3** | **Experiments** | 7 mo | \$14K (coord) | \$5K (participants) | **\$19K** |
| **4** | **System/UI** | 6 mo | \$30K (dev) | \$3K (hosting) | **\$33K** |
| | **TOTAL** | **18 mo** | **\$81K** | **\$18.5K** | **\$99.5K** |

**Labor breakdown:** - Data Scientist: \$50K/year × 1.5 FTE-years =
\$75K - Research Coordinator: \$40K/year × 0.5 FTE-years = \$20K -
Developer: \$60K/year × 0.5 FTE-years = \$30K - Consultant
(psychometrician): \$5K - **Total labor: \~\$130K** (but not all FTE
throughout)

**Realistic budget: \$100-120K for MVP** (18 months, small team)

### 9.2 Per-Experiment Costs

**Online Experiments (Image-Based):**

| Type | Sample Size | Duration | Participant Cost | Stimuli | Total |
|----|----|----|----|----|----|
| Simple Between-Subjects | 200 | 6-7 weeks | \$750 | \$500 | **\$1,250** |
| Factorial (2×2×2) | 240 | 7-8 weeks | \$1,200 | \$800 | **\$2,000** |
| Within-Subjects | 150 | 6-7 weeks | \$900 | \$600 | **\$1,500** |
| Dose-Response (6 levels) | 180 | 7 weeks | \$800 | \$700 | **\$1,500** |

**Lab Experiments (with Physiology):**

| Type | Sample Size | Duration | Participant Cost | Equipment/Space | Total |
|----|----|----|----|----|----|
| Simple Between-Subjects | 100 | 8-10 weeks | \$2,000 | \$3,000 | **\$5,000** |
| Factorial | 120 | 10-12 weeks | \$2,500 | \$4,000 | **\$6,500** |

Lab costs 4-5× online but provides physiological validation (HRV,
cortisol, EEG).

**Field Experiments (Real Buildings):**

| Type | Sites | Duration | Cost Range |
|-----------------------|-------|-------------|------------|
| Pre/Post Redesign | 2-3 | 6-12 months | \$10-30K |
| Longitudinal Tracking | 5-10 | 12 months | \$30-60K |

Field studies expensive but provide ecological validity.

**Recommendation:** Start with online experiments (cheap, fast),
validate key findings in lab/field.

### 9.3 Ongoing Operational Costs

**After MVP Launch:**

| Component | Monthly Cost | Annual Cost |
|----------------------------------|-------------------|----------------|
| Hosting (AWS/GCP) | \$200-500 | \$2,400-6,000 |
| Maintenance (developer, 10% FTE) | \$500 | \$6,000 |
| Data collection (expand corpus) | \$500-1,000 | \$6,000-12,000 |
| Experiments (2-4 per year) | \$500-1,000 | \$6,000-12,000 |
| **TOTAL** | **\$1,700-3,000** | **\$20-36K** |

**Scalability:** - Cost grows sublinearly with user base (hosting scales
cheaply) - Main costs: Data collection, model updates, experiments

### 9.4 Return on Investment

**Use Case 1: Design Firm (100 projects/year)**

- Current: Ad-hoc literature review + designer intuition
- With system: Evidence-based predictions + experiments for key
 decisions
- **Value:**
 - Avoid 1 costly mistake per year (e.g., open office that kills
 productivity) = \$100K+ saved
 - Faster design iterations (don't need to build mockups to test) =
 10 hours/project × 100 = 1000 hours = \$100K
 - Differentiation (evidence-based design) = More clients, higher
 fees = \$50K+
- **ROI: \$250K value vs. \$30K system cost = 8× return**

**Use Case 2: Research Lab**

- Systematizes literature, accelerates research
- Publications (10+ papers from experiments) = Career advancement
- Grants enabled by tool = \$500K+ over 5 years

**Use Case 3: Policy/Standards Bodies**

- Evidence base for building codes (e.g., minimum daylight, max noise)
- Public health impact (better buildings → less stress) = Societal
 value in millions

------------------------------------------------------------------------

## 10. Glossary

**Attribute:** A measurable feature of an image (e.g., wood coverage,
daylight level, plant density). Extracted via computer vision.

**Bayesian Inference:** Statistical method that updates beliefs (priors)
based on data (likelihood) to produce updated beliefs (posteriors).
Quantifies uncertainty.

**Causal Graph (DAG):** A diagram showing which variables cause which
others, using arrows (A→B means A causes B). Must have no cycles.

**Confound/Confounder:** A variable that affects both a cause and an
effect, creating spurious correlation. Randomized experiments eliminate
confounds.

**Counterfactual:** A statement about what *would have happened* in an
alternate reality. Example: "If Alice had seen the wood room instead of
the concrete room, her stress would have been 5.2 instead of 6.0." Hard
to identify; not used in our system.

**Credible Interval:** Bayesian version of confidence interval. "95%
credible interval [3.1, 5.9]" means "95% probability the true value is
between 3.1 and 5.9."

**Do-Calculus:** Mathematical framework (Pearl) for answering "what if
we intervened?" questions using causal graphs + observational data.

**Effect Size:** Magnitude of a relationship. β=0.3 means "1-unit
increase in X causes 0.3-unit increase in Y." Cohen's d (for
experiments) measures difference in standard deviation units.

**Goldilocks Effect:** Inverted-U relationship where outcomes are best
at moderate levels (not too little, not too much). Example: Moderate
complexity is preferred over simple or chaotic.

**Hierarchical Model:** Statistical model where parameters themselves
have distributions, allowing information sharing across groups. Reduces
overfitting.

**ICC (Intraclass Correlation):** Measure of inter-rater reliability.
ICC=0.7 means 70% of variance is between images (consensus), 30% is
within images (disagreement). Target: ICC\>0.7.

**Identifiability:** Whether you can uniquely determine parameters from
data. Non-identifiable models have multiple parameter sets that fit data
equally well (bad).

**Intervention:** Setting a variable to a specific value (as if by
experiment). P(Y \| do(X=x)) is the interventional distribution.

**Latent Variable:** Unobserved variable inferred from observed
indicators. We avoid these by *measuring* mediators directly.

**Likelihood:** Probability of data given parameters: P(Data \| θ). How
well the model fits observations.

**MCMC (Markov Chain Monte Carlo):** Algorithm for sampling from complex
probability distributions (like Bayesian posteriors). Slow but accurate.

**Mediator:** Variable that explains *how* X affects Y. Example: Wood
(X) → Warmth (mediator) → Stress (Y). Warmth mediates the wood→stress
effect.

**Posterior:** Updated belief after seeing data. P(θ \| Data) in Bayes'
theorem.

**Prior:** Initial belief before seeing data. P(θ) in Bayes' theorem.
Can come from literature, expert judgment, or be "uninformative."

**Provenance:** Traceability of claims back to their evidence sources.
Every prediction links to the studies/experiments that support it.

**R² (R-squared):** Proportion of variance explained by a model. R²=0.5
means model explains 50% of outcome variation; 50% is unexplained.

**Regression:** Statistical method for predicting an outcome (Y) from
predictors (X). Linear regression fits Y = β₀ + β₁X + ε.

**Uncertainty Quantification:** Reporting not just predictions but also
how certain we are. "Stress = 4.5 ± 0.8" includes uncertainty (±0.8).

**Variational Inference:** Fast approximate Bayesian inference. Trades
accuracy for speed (used for interactive UI).

------------------------------------------------------------------------

## Appendices

### Appendix A: Mathematical Notation Guide

- **X** = Attribute (image feature)
- **M** = Mediator (psychological perception)
- **Y** = Outcome (psychological state)
- **β** = Effect size (regression coefficient)
- **θ** = Optimal point (for Goldilocks functions)
- **τ** = Tolerance width (for Goldilocks functions)
- **σ** = Standard deviation (uncertainty)
- **ε** = Error term (unexplained variance)
- **\~** = "Distributed as" (X \~ Normal means X follows a normal
 distribution)
- **\|** = "Given" or "conditional on" (P(Y\|X) = probability of Y
 given X)
- **Σ** = Sum (Σᵢ βᵢXᵢ = β₁X₁ + β₂X₂ +...)

### Appendix B: Software/Tools Required

**Data Collection:** - Qualtrics or Gorilla (survey platform):
\$1,500/year - Prolific (participant recruitment): Pay-per-use - AWS S3
(image storage): \$50/month

**Computer Vision:** - Python 3.9+ - PyTorch 2.0+ - Detectron2, YOLOv8
(object detection) - MiDaS (depth estimation) - OpenCV (image
processing)

**Statistical Modeling:** - PyMC 5.0+ (Bayesian inference) - ArviZ
(diagnostics, visualization) - scikit-learn (preprocessing,
validation) - pandas, numpy (data manipulation)

**Experiment Design:** - G\*Power (power analysis) - R/lavaan
(structural equation modeling, optional)

**Deployment:** - FastAPI (backend) - React (frontend) - Docker
(containerization) - AWS/GCP (hosting)

### Appendix C: Key Papers to Read

**Foundational Theory:** 1. Kaplan & Kaplan. *The Experience of
Nature*. (Complexity-coherence framework) 2. Ulrich. Aesthetic
and affective response to natural environment. *Human Behavior &
Environment*, 6. 3. Berlyne. *Aesthetics and Psychobiology*.
(Arousal theory)

**Causal Inference:** 4. Pearl. *Causality* (Chapters 1-3: Basics
of causal graphs) 5. Pearl & Mackenzie. *The Book of Why*
(Accessible introduction)

**Bayesian Statistics:** 6. McElreath. *Statistical Rethinking*
(Chapters 1-5: Bayesian basics, regression, causality) 7. Gelman et al.. *Bayesian Data Analysis* (Reference, more advanced)

**Environmental Psychology Methods:** 8. Stamps. Mystery,
complexity, legibility and coherence: A meta-analysis. *J Environ
Psychology*. 9. Vartanian et al.. Architectural design and the
brain. *J Environ Psychology*.

**Goldilocks Principle:** 10. Taylor et al.. Perceptual and
physiological responses to Jackson Pollock's fractals. *Front Human
Neurosci*.

### Appendix D: Example Code Snippet

**Fitting a Simple Goldilocks Model:**

``` python
import pymc as pm
import numpy as np

# Data: 200 images
wood_coverage = np.array([...]) # 200 values, 0-1 scale
affective_ratings = np.array([...]) # 200 mean ratings, 1-7 scale

with pm.Model as model:
 # Priors
 β₀ = pm.Normal('intercept', mu=4, sigma=1)
 β_wood = pm.Normal('effect_wood', mu=0.3, sigma=0.2)
 θ_wood = pm.Normal('optimal_wood', mu=0.4, sigma=0.1)
 τ_wood = pm.HalfNormal('tolerance_wood', sigma=0.15)
 
 # Goldilocks function
 wood_effect = β_wood * pm.math.exp(-(wood_coverage - θ_wood)**2 / (2 * τ_wood**2))
 
 # Linear predictor
 μ = β₀ + wood_effect
 
 # Likelihood
 σ = pm.HalfNormal('sigma', sigma=0.5)
 y_obs = pm.Normal('affective', mu=μ, sigma=σ, 
 observed=affective_ratings)
 
 # Sample posterior
 trace = pm.sample(, tune=1000, return_inferencedata=True)
 
# Inspect results
print(pm.summary(trace, var_names=['effect_wood', 'optimal_wood']))

# Posterior mean of optimal wood coverage
optimal = trace.posterior['optimal_wood'].mean.values
print(f"Optimal wood coverage: {optimal:.1%}")
```

------------------------------------------------------------------------

## Final Recommendations

### For Immediate Start (Month 1):

1. **Assemble team:**
 - Hire 1 FTE data scientist (Bayesian modeling, causal inference)
 - Hire 0.5 FTE computer vision engineer (contract OK)
 - Recruit psychometrician consultant (part-time)
2. **Finalize scope:**
 - Select 10-15 attributes (from Goldilocks framework, prioritize
 Strong tier)
 - Select 4-6 mediators (affective, cognitive, acoustic, spatial)
 - Select 3-4 outcomes (stress, focus, satisfaction)
3. **Begin data collection prep:**

Source 200 images (stratified sampling) Write IRB protocol Draft
mediator/outcome scales

4. **Budget approval:**

Phase 1-2: \$40K (data + models) Phase 3: \$20K (experiments) Phase 4:
\$35K (system) Total: \$95-100K, 18 months

### Critical Success Factors:

✓ Start small (200 images, not) ✓ Measure mediators (don't skip
this step) ✓ Run experiments early (don't wait until "model is perfect")
✓ Be honest about uncertainty (wide intervals, not false precision) ✓
Track provenance (every claim → evidence source) ✓ Iterate (update
models as experiments complete) Red Flags to Avoid: ✗ Trying to infer
latent mediators without measurement → Non-identifiable ✗ Claiming
causality without experiments → Unjustified ✗ Using literature effect
sizes directly → Wrong context ✗ Building full system before validating
models → Wasted effort ✗ Ignoring uncertainty → False confidence

This system is ambitious but feasible. The key insight is modular
validation: Each component (computer vision, Model A, Model B) can be
validated independently. Start with a solid foundation (measured
mediators, \~200 images), build incrementally, and let experiments guide
expansion. Questions? Decision points to revisit:

Month 3: After pilot data, decide whether to proceed with full
collection Month 6: After Model A fitting, assess if R² is adequate
(\>0.4) Month 12: After first experiments, decide whether to scale or
refine Month 18: After MVP, decide on commercial vs. research focus

# The question of mediators / latent constructs

### What are the benefits and downsides of including latent constructs like "perceived warmth" versus only including image attributes and outcomes of interest?

The Latent Construct Trade-off: A Complete Analysis This is one of the
most fundamental design decisions for your system. Let me break down
both approaches completely.

Approach A: With Mediators (Current Plan) Image Attributes → Mediators
(measured) → Outcomes (wood, plants) (warmth, complexity) (stress,
focus) Approach B: Without Mediators (Direct Model) Image Attributes →
Outcomes (wood, plants) (stress, focus)

Benefits of INCLUDING Mediators 1. Mechanistic Understanding (The Big
Win) With mediators: Wood (35%) → Perceived Warmth (6.8/10) → Stress
(4.2/10) ↓ Effect: -0.4 stress points via warmth pathway You can answer:
"Wood reduces stress because it increases perceived warmth." Without
mediators: Wood (35%) → Stress (4.2/10) ↓ Effect: -0.4 stress points You
only know: "Wood reduces stress" (but not why). Why this matters for
design:

Scenario: An architect asks: "We can't afford real wood. Will wood-look
laminate work?" With mediators: You can test whether laminate produces
similar perceived warmth. If yes → it should work. If no → it won't
work. Without mediators: You have no way to predict. You'd need to run a
whole new study on laminate. Scenario: "We want stress reduction but
have acoustic constraints (can't add wood panels for sound absorption)."
With mediators: "Wood works via perceived warmth (visual), not
acoustics. Use wood veneer on non-acoustic surfaces." Without mediators:
You don't know if acoustic properties matter.

Real example:

You find: Wood → Stress (β=-0.3) But WHY? Is it:

Visual warmth (color, texture)? Acoustic absorption (reduces noise)?
Biophilic association (naturalness)? Cultural meaning (wealth,
craftsmanship)? Olfactory (wood smell)?

With mediators, you can decompose: Wood → Perceived Warmth → Stress
(-0.2) Wood → Acoustic Comfort → Stress (-0.1) Total effect: -0.3 Now
you know: 67% of effect is visual, 33% is acoustic. You can design
targeted interventions.

2. Generalization to New Attributes With mediators: Once you validate
 "Perceived Warmth → Stress", you can predict effects of ANY
 attribute that affects warmth:

Wood? ✓ Tested Warm paint colors? New, but if it increases warmth, it
should reduce stress Textiles (rugs, curtains)? New, but same logic
Lighting color temperature? New, but same pathway

Without mediators: You must test EVERY attribute separately:

Wood → Stress? Need data Warm colors → Stress? Need new data Textiles →
Stress? Need new data Etc.

This is the scientific power of mediators: You learn generalizable
mechanisms, not just attribute-specific effects. Example:

With 50 experiments, you might validate 10 mediators → You can now
predict effects of 100+ attributes Without mediators, 50 experiments
give you 50 attribute-outcome pairs → No generalization

3. Efficiency in Experimentation Suppose you want to test 10 attributes
 on 5 outcomes = 50 relationships. Without mediators:

50 separate experiments (or 1 massive factorial with 10 variables) Cost:
\$50K+ Time: Years

With mediators (assuming 6 mediators):

10 attribute → mediator experiments (small) 6 mediator → outcome
experiments (well-powered) Total: 16 experiments Cost: \$15-20K Time:
1-2 years

Why fewer experiments?

Attributes → Mediators: Can test multiple attributes per experiment
(e.g., wood + plants + color in one study, all affecting warmth)
Mediators → Outcomes: Universal tests (once you validate "warmth →
stress", it applies to all sources of warmth)

4. Handles Complex Interactions Real design scenario:

Open office with high visual connectivity Could increase stress (lack of
privacy) OR decrease stress (social support) Which dominates?

With mediators: Visual Connectivity → Perceived Privacy (low) → Stress
(+0.3) Visual Connectivity → Social Comfort (high) → Stress (-0.2) Net
effect: +0.1 (slight stress increase) You understand the competing
mechanisms and can design to balance them (e.g., add visual screens for
privacy while maintaining some social connection). Without mediators:
Visual Connectivity → Stress (+0.1) You see a small positive effect but
don't understand why. You can't design interventions because you don't
know which mechanism to target.

5. Individual and Context Differences With mediators: You can model
 heterogeneity at the mediator level:

Introverts: Visual Connectivity → Privacy concerns (high sensitivity)
Extroverts: Visual Connectivity → Social comfort (high value)

Both see same image features, but perceive mediators differently,
leading to different outcomes. Implementation: python# Mediator depends
on person Perceived_Privacy = f(Visual_Connectivity, Introversion)
Stress = g(Perceived_Privacy) Without mediators: You must model
attribute × personality interactions directly: pythonStress =
f(Visual_Connectivity, Introversion, Visual_Connectivity × Introversion)

``` 

This requires **much more data** to identify (3-way interactions proliferate) and doesn't explain the mechanism.

---

### 6. **Design Communication**

**With mediators, you can create clear design cards:**
```

┌─────────────────────────────────────────┐ │ RECOMMENDATION: Add Wood
Elements │ ├─────────────────────────────────────────┤ │ WHY IT WORKS: │
│ Wood increases Perceived Warmth │ │ → Warmth reduces Stress │ │ │ │
ALTERNATIVES (same mechanism): │ │ • Warm paint colors (terra cotta) │ │
• Warm lighting (2700-3000K) │ │ • Textiles (rugs, curtains) │ │ │ │
WHAT WON'T WORK: │ │ • Cool-toned wood (gray stain) │ │ → Doesn't
increase warmth │ └─────────────────────────────────────────┘

``` 

**Without mediators:**
```

┌─────────────────────────────────────────┐ │ RECOMMENDATION: Add Wood
Elements │ ├─────────────────────────────────────────┤ │ WHY IT WORKS: │
│ Wood has been shown to reduce stress │ │ in 8 studies (see citations)
│ │ │ │ We don't know why, so we can't suggest │ │ alternatives. Try
wood and see. │ └─────────────────────────────────────────┘

``` 

Designers want **actionable principles** ("increase warmth"), not just attribute lists ("use wood").

---

### 7. **Scientific Progress and Accumulation**

**With mediators,** your system contributes to **theory building**:
- You're testing "Does Perceived Warmth reduce stress?" (a psychological theory)
- Other researchers can build on this
- Knowledge accumulates: Future researchers test new attributes → warmth, reusing your validated warmth → stress link

**Without mediators:**
- You contribute "Wood reduces stress in offices" (a specific finding)
- Less generalizable
- Each new finding is isolated

---

## Benefits of EXCLUDING Mediators (Direct Model)

### 1. **Simplicity (Major Practical Advantage)**

**Data collection:**
- Without mediators: 200 images × 30 raters × 4 outcomes × 1 item = 24,000 ratings
- With mediators: 200 images × 30 raters × (6 mediators × 3 items + 4 outcomes × 1 item) = 132,000 ratings

**Cost:**
- Without: $2,500
- With: $6,500

**Participant burden:**
- Without: 2 minutes per image
- With: 4 minutes per image

**Model complexity:**
- Without: 1 model (Attributes → Outcomes)
- With: 2 models (Attributes → Mediators, Mediators → Outcomes)

---

### 2. **Fewer Assumptions**

**With mediators, you assume:**
1. Mediators exist as coherent constructs (not always true—they might collapse in factor analysis)
2. Mediators fully mediate effects (but some effects might be direct, bypassing mediators)
3. Mediators are measured correctly (measurement error propagates)
4. Causal graph structure is correct (which mediators cause which outcomes)

**Without mediators:**
- Just one assumption: Attributes → Outcomes relationship exists
- No need to specify mechanism

**Example where mediation assumptions fail:**

You hypothesize:
```

Wood → Perceived Warmth → Stress

``` 

But in reality:
```

Wood → (Some unmeasured factor: nostalgia? status?) → Stress

``` 

Your measured "Perceived Warmth" doesn't capture the true mediator. Your model will:
- Underestimate the total effect of wood
- Misattribute the mechanism
- Fail to predict when you manipulate warmth via other means

**Direct model doesn't have this problem** (but loses mechanistic insight).

---

### 3. **Avoids Measurement Error Propagation**

**Statistical issue:** Error compounds across model stages.

**Model A:** Attributes → Mediators
- Has error: R² = 0.5 means 50% unexplained variance

**Model B:** Mediators → Outcomes
- Uses predicted mediators from Model A (which have error)
- Error from Model A propagates into Model B
- Final predictions have compounded error

**Example:**
- Model A predicts Warmth = 6.0 ± 1.0
- Model B: Stress = 4.0 - 0.3 × Warmth
- If true Warmth = 5.0, Model A is off by 1.0
- This causes Model B to be off by 0.3 × 1.0 = 0.3 stress points
- **Total prediction error from cascade**

**Direct model:**
- Attributes → Outcomes (one step)
- Error occurs once, not compounded

**Mitigation for mediated model:**
- Use measurement error models (explicitly model mediator uncertainty)
- Propagate uncertainty through both stages
- But this adds complexity

---

### 4. **Faster Iteration**

**Without mediators:**
- New dataset? Refit one model (Attributes → Outcomes)
- Takes hours-days

**With mediators:**
- New dataset? Refit Model A, then Model B
- If mediator scales change, may need to re-collect data
- Takes weeks

**For rapid prototyping,** direct models are faster.

---

### 5. **Prediction May Be All You Need (For Some Users)**

**User persona: Facilities manager**
- Question: "Will this office design lead to low stress?"
- Doesn't care WHY
- Just wants: Stress prediction ± uncertainty

**For pure prediction tasks** (not design exploration), direct models are sufficient.

**Analogy:**
- Weather forecasting: Don't need to understand atmospheric physics to predict rain tomorrow
- Just need good predictive model

**But:** Most design applications DO need mechanism understanding (see benefits above).

---

### 6. **No "Mediator Realism" Debate**

**Philosophical issue:** Are mediators "real" psychological constructs, or just convenient fictions?

Example: Is "Perceived Warmth" a distinct mental state? Or is it a label we apply to a pattern of neural activity that's actually multidimensional?

**With mediators,** you're committing to a psychological ontology (warmth exists, is measurable, causes outcomes).

**Without mediators,** you stay agnostic: "Wood affects stress, period. We don't theorize about internal mental states."

**For pragmatists,** direct models avoid this debate.

---

## Downsides of INCLUDING Mediators

### 1. **High Data Collection Cost**

Already covered: ~2.5× more expensive.

---

### 2. **Model Complexity and Failure Modes**

**More complex models have more ways to fail:**

**Failure Mode 1: Mediator doesn't exist**
- You hypothesize "Acoustic Comfort" as a mediator
- Factor analysis shows: Items don't cohere (α = 0.5)
- Turns out: "Acoustic comfort" is not a unitary construct
- **Solution:** Re-analyze, merge with another construct, or drop
- **Cost:** Wasted data collection on bad mediator

**Failure Mode 2: Wrong causal direction**
- You assume: Perceived Warmth → Stress
- Reality: Low stress → people perceive spaces as warmer (mood affects perception)
- Model is backwards
- **Solution:** Experiments to establish directionality
- **Cost:** Need experiments you thought you could skip

**Failure Mode 3: Complete mediation assumed, but isn't**
- You assume: All wood effects go through mediators
- Reality: Wood has direct effect on stress (e.g., via smell, not captured by mediators)
- Model underestimates total wood effect
- **Solution:** Add direct paths (but then why bother with mediators?)

---

### 3. **Identifiability Challenges (The Big One)**

**Even with measured mediators, identifying causal effects is hard.**

**Problem: Confounding between mediators**
```

Example: Wood → Perceived Warmth (6.8) Wood → Perceived Naturalness
(7.2)

Both correlate with low stress. But which causes it?

Possible structures: A) Warmth → Stress, Naturalness → Stress (both
causal) B) Warmth → Naturalness → Stress (chain) C) Naturalness → Warmth
→ Stress (reverse chain) D) Both caused by unmeasured "General
Pleasantness" → Stress

``` 

**From observational data alone, you cannot distinguish these.**

**You need experiments that manipulate mediators independently** (e.g., vary warmth while holding naturalness constant).

But if you're going to run those experiments anyway, **why not just test attributes directly?**

---

### 4. **Measurement Burden on Participants**

**Participant fatigue:**
- Rating 6 mediators × 3 items = 18 items per image
- Plus 4 outcomes = 22 items total
- Attention drops after ~10 items
- Quality degrades (straight-lining, random responses)

**Solutions:**
- Shorter scales (1-2 items per mediator) → But reduces reliability
- Fewer mediators (4 instead of 6) → But loses richness
- Between-subjects design (each rater does subset) → But need more raters per image

---

### 5. **Assumes Mediators Are Universal**

**Problem:** Mediators might be context-dependent.

**Example:**
- In offices: "Perceived Privacy" is a key mediator for stress
- In homes: "Perceived Privacy" barely matters (you're alone)
- In hospitals: "Perceived Safety" matters more

**With mediators,** you need different models for different contexts.

**Without mediators,** you can have context-dependent attribute effects without changing model structure:
```

Stress = β_wood × Wood + β_context × Context + β_interaction × Wood ×
Context

``` 

---

## Downsides of EXCLUDING Mediators

### 1. **No Mechanism Understanding (Critical Loss)**

Already covered extensively. This is **the biggest downside.**

You're stuck with:
- Attribute-specific effects that don't generalize
- No ability to design alternatives
- No ability to handle novel attributes
- Black-box predictions

**This severely limits the system's scientific and practical value.**

---

### 2. **Requires Massive Data for Each Attribute-Outcome Pair**

**Without mediators:**
- To test 50 attributes on 5 outcomes = 250 relationships
- Each needs adequate statistical power
- With interactions (attribute × context), the number explodes

**With mediators:**
- 50 attributes → 6 mediators (learn shared patterns via hierarchical grouping)
- 6 mediators → 5 outcomes (30 relationships, well-powered experiments)
- Much more tractable

---

### 3. **No Way to Handle Unseen Attributes**

**Scenario:** A new material is invented (e.g., smart glass that changes opacity).

**With mediators:**
- Collect ratings on how it affects perceived privacy, warmth, etc.
- Use existing mediator → outcome links to predict stress/focus
- **Works even though material is new**

**Without mediators:**
- No way to predict effects until you collect outcome data for this specific material
- **System is brittle to novelty**

---

### 4. **Literature Integration Is Harder**

**Most environmental psychology literature is about mediators:**
- "Perceived restorativeness reduces stress" (Ulrich, Kaplan)
- "Cognitive load impairs focus" (Sweller)
- "Privacy needs vary by personality" (Altman)

**With mediators,** you can directly incorporate this literature as priors.

**Without mediators,** you must translate to attribute level:
- "Wood reduces stress... but by how much, through what mechanism, in what contexts?"
- Much harder to extract usable priors

---

### 5. **Missed Scientific Contribution**

**With mediators,** you contribute to psychological theory:
- Test hypotheses about perception-affect-behavior links
- Publishable in *Journal of Environmental Psychology*, *Psychological Science*

**Without mediators,** you contribute only to design heuristics:
- "Wood reduces stress in offices"
- Less generalizable, lower-tier journals

**If you care about academic impact,** mediators are essential.

---

## The Hybrid Approach (Best of Both Worlds?)

### Option 1: Include Mediators BUT Model Direct Effects Too
```

Attributes → Mediators → Outcomes ↘ ↗ (direct paths) Model: pythonStress
= β₀ + β_affective × Affective_Quality \# Mediated + β_cognitive ×
Cognitive_Load \# Mediated + β_direct_wood × Wood \# Direct
(non-mediated) + β_direct_glare × Glare \# Direct + ε Benefits:

Captures mediated AND non-mediated effects If mediators miss something,
direct paths pick it up Total effect = mediated + direct

Downsides:

More complex Risk of "double counting" if mediators aren't perfectly
measured

When to use:

If you suspect some effects bypass your measured mediators Glare →
discomfort (probably direct, not via warmth/complexity) Threatening
imagery → stress (direct emotional response)

Option 2: Start Without Mediators, Add Later Phase 1 (MVP):

Direct model: Attributes → Outcomes Fast, simple, cheap Get system
working, demonstrate value

Phase 2 (Scale-Up):

Add mediator measurement Refit as mediated model Gain mechanistic
understanding

Benefits:

De-risks: Proves prediction is possible before investing in mediators
Incremental cost

Downsides:

Phase 1 system has limited value (prediction only) Need to re-collect
data for Phase 2 (or collect both from start)

Option 3: Mediators for Subset of Attributes Identify key attributes
where mechanism matters:

Wood, plants, daylight, spatial complexity, color (10-15 core
attributes) Measure mediators for these

For other attributes (less central):

Direct effects only E.g., "Presence of signage → wayfinding clarity"
(don't need mediators)

Benefits:

Focused data collection (less burden) Mechanism understanding where it's
most valuable

Downsides:

Mixed model (some paths mediated, some direct) Complexity in
implementation

Decision Framework: When to Include Mediators Include Mediators If: ✓
Your users need mechanistic understanding (architects, researchers) ✓
You want to generalize to new attributes (predict effects of novel
materials) ✓ You have budget for data collection (\$6K vs. \$2.5K) ✓ You
plan to run experiments anyway (mediators enable efficient experiment
design) ✓ Scientific contribution is a goal (publishable theory testing)
✓ Multiple outcomes of interest (mediators share effects across
outcomes) Exclude Mediators If: ✓ Pure prediction is sufficient
(facilities managers: "just tell me if it's good") ✓ Budget is very
tight (\<\$3K for data collection) ✓ Rapid prototyping is priority
(prove concept quickly) ✓ Attributes are highly specific (e.g., "Does
this exact paint color work?" No generalization needed) ✓ Skeptical of
psychological constructs (pragmatist stance)

My Recommendation for Your System Include Mediators (Current Plan Is
Correct) Why:

Your stated use cases require mechanism understanding:

Use Case A (critique): "Why is this stressful?" needs mediators Use Case
C (experiments): "Which pathway matters?" requires mediators Designers
need actionable principles, not just attribute checklists

Generalization is critical:

You can't test every attribute exhaustively Mediators enable: Learn 50
attributes → 6 mediators, then predict 1000 attributes

Literature integration:

Most existing theory is at mediator level Priors from Ulrich
(restorativeness), Kaplan (complexity), etc. map naturally to mediators

Scientific credibility:

Mediated models are testable theories Direct models are "black boxes
with extra steps"

The cost is manageable:

\$6.5K vs. \$2.5K is only \$4K difference The value from mechanistic
insight far exceeds \$4K

BUT: Start focused (4-6 mediators, not 10) Priority Tier 1 Mediators
(Must Have):

Affective Quality (warmth, pleasantness) — Most universal Cognitive Load
(complexity, information density) — Key for focus/stress Spatial Comfort
(enclosure, privacy) — Core to satisfaction Acoustic Comfort (quietness)
— Distinct mechanism

Priority Tier 2 (Add if budget allows): 5. Restorativeness (attention
restoration) — Theoretically important (Kaplan) 6. Social Comfort
(appropriateness for interaction) — Context-dependent Rationale:

4 mediators × 3 items = 12 items per image (manageable) Covers main
pathways from literature Distinct constructs (likely won't collapse in
factor analysis) If you need to cut costs, drop #5-6

Implementation Strategy Phase 1: Validate That Mediators Exist Before
committing to full data collection:

Pilot (50 images, 30 raters, 4 mediators × 3 items)

Cost: \$750 Factor analysis: Do items load as expected? ICC: Do raters
agree (\>0.7)? Discriminant validity: Are mediators distinct
(correlations \<0.8)?

Decision point:

If mediators are valid → Proceed with full 200 images If some collapse →
Revise and re-pilot If all collapse to "general pleasantness" → Consider
direct model

Phase 2: Full Data Collection with Fallback Collect BOTH mediators and
outcomes in same survey This allows you to:

Fit mediated model (preferred) If mediated model fails, fall back to
direct model (same data) Compare predictive accuracy of both

You don't lose anything by collecting mediator data—you just gain
optionality.

Summary Table CriterionWith MediatorsWithout MediatorsMechanistic
insight✓✓✓ Deep understanding✗ Black boxGeneralization✓✓✓ To new
attributes✗ Only tested attributesDesign alternatives✓✓✓ Can suggest✗
Can't suggestExperiment efficiency✓✓ 16 experiments✗ 50+ experimentsData
collection cost✗ \$6.5K✓ \$2.5KModel complexity✗✗ Two stages✓ One
stageIdentifiability⚠ Needs experiments✓ SimplerParticipant burden✗ 4
min/image✓ 2 min/imageLiterature integration✓✓✓ Natural fit⚠
AwkwardScientific contribution✓✓✓ Theory testing✓ Applied onlyHandles
novelty✓✓✓ New attributes✗ Needs new dataFailure modes✗✗ Many
assumptions✓ Fewer assumptions Overall: Mediators win on almost every
criterion except cost and complexity. The scientific and practical
benefits far outweigh the extra \$4K and modeling complexity.

Final Answer Include mediators. The \$4,000 extra cost buys you:

Mechanistic understanding (invaluable for design) Generalization (10×
efficiency in long run) Scientific credibility (publishable, fundable)
Design flexibility (can suggest alternatives)

But validate them first (pilot with 50 images) to confirm they're
coherent constructs. If you must cut costs: Start with 4 mediators
instead of 6, but don't eliminate mediators entirely. The system loses
most of its value without them.

### article extraction details to support mediator identification

1.1 Extract Pathway Information from Literature What to code from each
paper: Paper: Smith et al. Attribute: Wood exposure Mediator:
[Explicitly mentioned? Y/N] - If yes: Which? "Perceived naturalness" -
If no: Is mechanism discussed? "Authors speculate acoustic properties"
Outcome: Stress reduction Study design: RCT with manipulation check on
naturalness Result: Wood → Naturalness confirmed (d=0.8); Naturalness →
Stress (β=-0.3) Mediation tested?: Yes, 65% of effect mediatedCreate
structured database:pythonliterature_db = [ { 'paper_id': 'Smith2018',
'attribute': 'wood_coverage', 'mediator_measured':
['perceived_naturalness', 'acoustic_comfort'], 'mediator_confirmed':
['perceived_naturalness'], 'outcome': 'stress', 'mediation_proportion':
0.65, \# 65% mediated 'direct_effect': 0.35, \# 35% direct
'study_quality': 'high', \# RCT with manipulation check }, { 'paper_id':
'Jones2020', 'attribute': 'wood_coverage', 'mediator_measured': None, \#
Direct effect only 'mediator_speculated': ['visual_warmth'], \# Authors
guess 'outcome': 'stress', 'mediation_proportion': None,
'study_quality': 'medium', \# Observational }, \#... more papers]

Algorithm: Score each candidate mediator pythondef
score_mediator_importance(mediator_name, literature_db): """ Score a
mediator on how often it appears and is validated in literature """
score = 0

``` 
# 1. Frequency: How many papers mention it?
mentions = sum(1 for p in literature_db 
 if mediator_name in p.get('mediator_measured', [])
 or mediator_name in p.get('mediator_speculated', []))
score += mentions * 1.0

# 2. Validation: How many actually test and confirm it?
confirmations = sum(1 for p in literature_db 
 if mediator_name in p.get('mediator_confirmed', []))
score += confirmations * 3.0 # Weight confirmed 3x higher

# 3. Study quality: Weight by design quality
quality_weights = {'high': 3, 'medium': 2, 'low': 1}
quality_score = sum(quality_weights[p['study_quality']] 
 for p in literature_db 
 if mediator_name in p.get('mediator_confirmed', []))
score += quality_score * 2.0

# 4. Breadth: How many different attributes does it mediate?
unique_attributes = len(set(p['attribute'] for p in literature_db
 if mediator_name in p.get('mediator_confirmed', [])))
score += unique_attributes * 2.0 # Reward generality

# 5. Proportion mediated: When tested, how much does it explain?
mediation_props = [p['mediation_proportion'] 
 for p in literature_db 
 if mediator_name in p.get('mediator_confirmed', [])
 and p['mediation_proportion'] is not None]
if mediation_props:
 avg_mediation = np.mean(mediation_props)
 score += avg_mediation * 5.0 # Strong mediators get bonus

return score
```

Score all candidate mediators mediators = ['perceived_warmth',
'perceived_naturalness', 'cognitive_load', 'acoustic_comfort',
'spatial_comfort', 'restorativeness', 'visual_interest', 'legibility',
'privacy', 'social_affordance']

scores = {m: score_mediator_importance(m, literature_db) for m in
mediators} ranked = sorted(scores.items, key=lambda x: x[1],
reverse=True)

print("Mediator Priority Ranking:") for mediator, score in ranked[:6]:
print(f"{mediator}: {score:.1f}")

``` 

**Expected output:**
```

Mediator Priority Ranking: perceived_naturalness: 45.2 (mentioned 12
papers, confirmed 8, high quality) cognitive_load: 38.7 (mentioned 10
papers, confirmed 7, medium quality) acoustic_comfort: 32.1 (mentioned 8
papers, confirmed 5, high quality) restorativeness: 28.4 (mentioned 9
papers, confirmed 4, medium quality) perceived_warmth: 22.3 (mentioned 7
papers, confirmed 3, speculated 8) spatial_comfort: 18.1 (mentioned 6
papers, confirmed 2) Decision: Focus data collection on top 4-6
mediators.

## Hierarchical/causal attributes

How do we deal with cases such as the following: natural textures and
medium statistical fractals are both physical attributes which are
associated with restoration & preference. It turns out natural textures
tend to contain medium statistical fractals. How do we account for this
hierarchy/complexity in the attributes layer? fractal dimension is not a
psychological mediator, but it may very well partially mediate
naturalness -\> preference, even though few papers as yet report on this
(most papers report on either fractals -\> perceptual fluency/cognitive
load -\> preference, or natural textures/plants -\> naturalness -\>
preference). how do we account for this?

The Hierarchical Attribute Problem: A Complete Solution This is an
excellent, subtle question that gets at a deep modeling challenge.
You've identified a case where the clean three-layer architecture
(Attributes → Mediators → Outcomes) breaks down because attributes
themselves have causal structure.

Let me work through this systematically.

The Problem Illustrated Your observation:

Natural Textures (wood, plants) → Restoration & Preference Fractal
Dimension (1.3-1.7) → Restoration & Preference

BUT: Natural textures contain medium fractals!

So is it: A) Natural Textures → Restoration (fractals are just a
property) B) Fractal Dimension → Restoration (naturalness is just a
proxy) C) Natural Textures → Fractal Dimension → Restoration (fractals
mediate) D) Both have independent effects that happen to co-occur Why
this matters:

If you model both natural_textures and fractal_dimension as independent
attributes, you have:

Multicollinearity: They're correlated (r ≈ 0.7-0.8) Misattribution:
Effect might be credited to wrong attribute Poor predictions: When you
intervene on one, model doesn't know the other changes Example failure
mode:

Your model learns: natural_textures → restoration (β = 0.3)
fractal_dimension → restoration (β = 0.2)

Designer asks: "I want to add restoration. Should I use wood or
fractals?"

System says: "Add both! They're independent, so β_total = 0.5"

Reality: Wood IS fractals. Adding wood gives β = 0.3, not 0.5. Solution
1: Explicit Hierarchical Attributes (Causal DAG in Attribute Layer) 1.1
Model Attributes as a Causal Graph Don't treat attributes as
independent. Build a DAG among attributes that captures their
relationships:

``` 
 Natural Textures (wood, plants)
 ↓
 Fractal Dimension (1.3-1.7)
 ↓
 Mediators
 (Naturalness, Perceptual Fluency)
 ↓
 Outcomes
 (Restoration, Preference)
```

Formal specification:

python \# Attribute Layer (with internal structure) fractal_dimension =
f(natural_textures, other_factors, ε_fractal) \# Example: D = 1.1 + 0.4
× natural_coverage + noise

# Mediator Layer

naturalness = g1(natural_textures, ε_nat) perceptual_fluency =
g2(fractal_dimension, ε_fluency)

# Outcome Layer

restoration = h(naturalness, perceptual_fluency, ε_restoration)

``` 

**Key insight:** Fractal dimension is **caused by** natural textures, not independent of them.

---

### 1.2 Decompose Total Effects

With this structure, you can answer:

**Question: "Does wood work via fractals or something else?"**
```

Total effect of wood on restoration: Direct: Wood → Naturalness →
Restoration Indirect: Wood → Fractal Dim → Perceptual Fluency →
Restoration

Decomposition: Total = Direct + Indirect β_total =
β_wood→nat×β_nat→rest + β_wood→frac×β_frac→fluency×β_fluency→rest
Implementation:

python import pymc as pm

with pm.Model as hierarchical_model: \# Exogenous attributes (directly
measurable) natural_textures = data['natural_coverage'] \# 0-1 scale

``` 
# Fractal dimension is CAUSED by natural textures
β_nat_to_frac = pm.Normal('nat_to_frac', mu=0.4, sigma=0.1)
fractal_baseline = pm.Normal('frac_baseline', mu=1.3, sigma=0.1)

fractal_dim = pm.Deterministic('fractal_dim',
 fractal_baseline + β_nat_to_frac * natural_textures)
# Note: This is deterministic (no error term) if fractals are 
# perfectly determined by naturalness, or add noise if not

# Mediators (psychological)
# Naturalness depends on natural textures (direct perception)
β_nat_textures = pm.Normal('beta_nat_textures', mu=0.5, sigma=0.1)
naturalness = pm.Normal('naturalness',
 mu=β_nat_textures * natural_textures,
 sigma=0.5)

# Perceptual fluency depends on fractal dimension (processing ease)
β_fractal = pm.Normal('beta_fractal', mu=0.3, sigma=0.1)
optimal_fractal = 1.5 # Peak of Goldilocks curve
fluency = pm.Normal('fluency',
 mu=β_fractal * pm.math.exp(-(fractal_dim - optimal_fractal)**2 / 0.2),
 sigma=0.5)

# Outcome: Restoration depends on both mediators
β_nat_to_rest = pm.Normal('beta_nat_to_rest', mu=0.3, sigma=0.1)
β_fluency_to_rest = pm.Normal('beta_fluency_to_rest', mu=0.2, sigma=0.1)

restoration = pm.Normal('restoration',
 mu=β_nat_to_rest * naturalness + β_fluency_to_rest * fluency,
 sigma=0.3,
 observed=data['restoration'])
```

Now you can compute path-specific effects:

python \# Direct path: Natural → Naturalness → Restoration direct_effect
= β_nat_textures \* β_nat_to_rest \# → 0.5 × 0.3 = 0.15

# Indirect path: Natural → Fractal → Fluency → Restoration

indirect_effect = β_nat_to_frac \* β_fractal \* β_fluency_to_rest \# →
0.4 × 0.3 × 0.2 = 0.024

# Total effect

total_effect = direct_effect + indirect_effect \# → 0.15 + 0.024 = 0.174

print(f"Wood effect on restoration: {total_effect:.3f}") print(f" 86%
via naturalness pathway") print(f" 14% via fractal/fluency pathway")

``` 

---

### 1.3 Benefits of Hierarchical Attributes

✓ **Correct multicollinearity handling:** Model knows fractals are caused by naturalness
✓ **Accurate interventions:** "Add wood" correctly updates both natural_textures AND fractal_dim
✓ **Mechanism clarity:** Can quantify "How much of naturalness effect is via fractals?"
✓ **Testable:** Can run experiments manipulating fractals independently of naturalness

---

### 1.4 How to Build the Attribute DAG

**Method 1: Physical/Computational Causality**

Some attribute relationships are **definitional** or **computational**:
```

Material Type (wood) → Fractal Dimension (computed from texture) Glazing
Ratio → Daylight Illuminance (physics) Object Count → Visual Information
Density (count = density) Seating Arrangement → Visual Connectivity
(geometric calculation) These are not statistical—they're deterministic
or near-deterministic.

Method 2: Statistical Mediation Analysis

For other cases, test empirically:

python from scipy import stats

# Test: Does natural_coverage predict fractal_dimension?

natural_coverage = data['natural_coverage'] fractal_dim =
data['fractal_dimension']

# Regression

β, *, r_value, p_value,* = stats.linregress(natural_coverage,
fractal_dim)

print(f"Natural coverage → Fractal dimension:") print(f" β = {β:.3f}, R²
= {r_value\*\*2:.3f}, p = {p_value:.4f}")

# If R² \> 0.5 and p \< 0.001, there's a strong relationship

# → Model fractal as caused by naturalness

Method 3: Literature + Theory

Taylor et al.: Natural objects have D=1.3-1.7 Mandelbrot:
Fractals are characteristic of natural forms (trees, coastlines, clouds)
Theory: Fractals are a property of natural textures, not independent
Method 4: Intervention Logic

Ask: "Can I change X without changing Y?"

Can you change natural_coverage without changing fractal_dim? No (adding
wood adds fractals) Can you change fractal_dim without changing
natural_coverage? Yes (artificial fractals: Pollock paintings,
computer-generated) If X always changes Y, but Y can change
independently, then X → Y causally.

Solution 2: Composite Attributes (Feature Engineering) 2.1 Create
Higher-Level Attributes That Bundle Related Features Instead of modeling
natural_textures and fractal_dimension separately, create:

python \# Composite attribute: "Biophilic Visual Properties"
biophilic_properties = { 'natural_material_coverage': 0.35, \# 35%
wood/plants 'fractal_dimension': 1.45, 'organic_forms': 0.6, \# Curves
vs. straight lines 'color_naturalness': 0.7, \# Earth tones }

# Aggregate into single score

biophilic_score = aggregate(biophilic_properties,
method='weighted_mean') \# Or use PCA/factor analysis on these
correlated features

``` 

**Then model:**
```

Biophilic Score → Naturalness → Restoration ↘ Perceptual Fluency →
Restoration

``` 

**Benefits:**
- Simpler model (one attribute instead of many correlated ones)
- Captures "bundle" that co-occurs in nature

**Downsides:**
- Less granular (can't separate wood from plants from fractals)
- Harder to give specific design guidance ("increase biophilic score" is vague)

---

### 2.2 Hierarchical Feature Groups (Goldilocks Framework Helps Here)

**Use the Goldilocks framework's clustering:**
```

Tier 1: High-Level Design Dimensions - Biophilic Character - Spatial
Complexity - Color Warmth - Acoustic Comfort

Tier 2: Component Attributes Biophilic Character: - Natural material
coverage - Fractal dimension - Organic forms - Green coverage (plants)

Spatial Complexity: - Spatial entropy - Visual information density -
Functional zones Model at Tier 1 for simplicity, decompose to Tier 2 for
detailed guidance.

Solution 3: Residualization (Statistical Control) 3.1 Separate
"Naturalness-Driven Fractals" from "Pure Fractal Effects" The idea:
Fractals have two components:

The part explained by natural textures The residual part (fractals
independent of naturalness) python from sklearn.linear_model import
LinearRegression

# Step 1: Regress fractal_dim on natural_textures

model = LinearRegression model.fit(data[['natural_coverage']],
data['fractal_dimension'])

fractal_predicted = model.predict(data[['natural_coverage']])
fractal_residual = data['fractal_dimension'] - fractal_predicted

# Step 2: Use residuals in outcome model

# fractal_residual captures "pure fractal effect" beyond naturalness

outcome_model = LinearRegression X = data[['natural_coverage',
'fractal_residual']] y = data['restoration'] outcome_model.fit(X, y)

print(f"Natural coverage effect: {outcome_model.coef\_[0]:.3f}")
print(f"Pure fractal effect (residual): {outcome_model.coef\_[1]:.3f}")

``` 

**Interpretation:**
- `β_natural`: Effect of naturalness (includes its typical fractals)
- `β_fractal_residual`: Effect of fractals **beyond** what naturalness provides

**Example result:**
```

Natural coverage effect: 0.28 (strong) Pure fractal effect: 0.05 (weak)

Interpretation: Most of fractal benefit comes via natural textures.
Adding artificial fractals (Pollock painting) would only add 0.05.

``` 

---

### 3.2 When to Use Residualization

**Use when:**
- You want to include both features in a regression
- You want to know "unique contribution" of each
- Attributes are strongly correlated (r > 0.6)

**Don't use when:**
- You want causal interpretation (residuals lose causal meaning)
- You want to predict interventions (residuals change when you intervene)

---

## Solution 4: Experimental Disambiguation

### 4.1 Manipulate Fractals Independently of Naturalness

**The gold standard:** Run experiments that break the natural correlation.

**Experiment: Fractal Dimension × Material Type (2×2)**

| Condition | Material | Fractal Dimension | Notes |
|-----------|----------|-------------------|-------|
| A | Synthetic (plastic) | Low (D=1.1) | Smooth plastic, no texture |
| B | Synthetic (plastic) | Medium (D=1.5) | Fractal-textured plastic surface |
| C | Natural (wood) | Medium (D=1.5) | Real wood (natural fractals) |
| D | Natural (wood) | Low (D=1.1) | Polished wood (fractals removed) |

**Measures:**
- Naturalness (perceived)
- Perceptual Fluency
- Restoration

**Analysis:**
```

Restoration = β₀ + β_material × Material + β_fractal × Fractal_Dim +
β_interaction × Material × Fractal_Dim + ε

If β_interaction ≈ 0: → Fractal and naturalness have independent effects

If β_interaction \> 0: → Fractals work BETTER in natural materials
(synergy)

If β_material \>\> β_fractal: → Naturalness dominates, fractals are
secondary

``` 

**This definitively answers:** "Can fractals work without naturalness?"

---

### 4.2 Practical Implementation

**Stimuli creation:**
```

Condition A: Render room with smooth gray plastic panels Condition B:
Apply fractal texture pattern to plastic (Perlin noise, D=1.5) Condition
C: Real wood photograph (D=1.5 measured) Condition D: Polished wood
(high gloss, removes texture)

``` 

**Cost:** $1,500-2,000 (N=240, between-subjects)

**Timeline:** 8 weeks

**Result example:**
```

Main effect of Material: β = 0.25 (naturalness matters) Main effect of
Fractal: β = 0.08 (fractals help slightly) Interaction: β = 0.12
(fractals help MORE in natural materials)

Interpretation: - Natural material provides restoration via
"naturalness" perception - Fractals add perceptual fluency benefit - But
fractals in natural materials have SYNERGY (0.12 extra) → Wood with
fractals: 0.25 + 0.08 + 0.12 = 0.45 total effect

``` 

---

## Solution 5: Latent Variable Model (Structural Equation Modeling)

### 5.1 Treat "Biophilic Character" as a Latent Construct

**Hypothesis:** Natural textures and fractals are both **indicators** of an underlying construct.
```

``` 
 Latent: Biophilic Character
 / | \
 / | \
```

Natural Fractal Organic (Observed attributes) Textures Dimension Forms
Structural Equation Model (SEM):

python from semopy import Model

# Define model

model_spec = """ \# Measurement model (latent → observed attributes)
BiophilicCharacter =\~ natural_textures + fractal_dimension +
organic_forms

# Structural model (latent → mediators → outcomes)

Naturalness \~ BiophilicCharacter PerceptualFluency \~
BiophilicCharacter Restoration \~ Naturalness + PerceptualFluency """

model = Model(model_spec) model.fit(data) print(model.inspect)

``` 

**Interpretation:**
- If loadings are high (>0.7), natural_textures and fractals both measure "biophilic character"
- Then use **latent score** as the predictor, not individual attributes

**Benefits:**
- Handles measurement error (fractals are noisy measure of biophilia)
- Reduces multicollinearity (one latent instead of correlated attributes)

**Downsides:**
- Requires theory (what is the latent construct?)
- Harder to interpret for designers ("increase biophilic character" less actionable than "add wood")

---

## Solution 6: Hybrid Model (Recommended)

### 6.1 Combine Hierarchical Structure + Residuals + Experiments

**Final architecture:**
```

Tier 1: Exogenous Attributes - Natural Material Coverage (wood, stone,
plants) - Color Palette - Spatial Configuration

Tier 2: Computed Attributes (caused by Tier 1) - Fractal Dimension =
f(Natural Materials, Texture Processing) - Visual Information Density =
f(Object Count, Spatial Layout) - Illuminance = f(Glazing Ratio,
External Conditions)

Tier 3: Mediators (psychological) - Perceived Naturalness \~ Natural
Materials + Color - Perceptual Fluency \~ Fractal Dimension - Cognitive
Load \~ Visual Information Density

Tier 4: Outcomes - Restoration \~ Naturalness + Perceptual Fluency +...
Model specification:

python with pm.Model as hybrid_model: \# Tier 1: Exogenous
natural_materials = data['natural_coverage']

``` 
# Tier 2: Computed (deterministic or near-deterministic)
fractal_dim = pm.Deterministic('fractal_dim',
 1.1 + 0.4 * natural_materials # Wood → fractals)

# Tier 3: Mediators
# Naturalness from direct perception of materials
naturalness = pm.Normal('naturalness',
 mu=β_natural * natural_materials,
 sigma=σ_natural)

# Fluency from fractal processing (with residual)
# Option A: Use fractal_dim directly (includes naturalness effect)
fluency_A = pm.Normal('fluency',
 mu=β_fractal * goldilocks(fractal_dim, optimal=1.5, width=0.2),
 sigma=σ_fluency)

# Option B: Use fractal_residual (pure fractal effect)
fractal_residual = data['fractal_dim'] - (1.1 + 0.4 * natural_materials)
fluency_B = pm.Normal('fluency',
 mu=β_fractal_resid * goldilocks(fractal_residual, optimal=0, width=0.2),
 sigma=σ_fluency)

# Tier 4: Outcome
restoration = pm.Normal('restoration',
 mu=β_nat * naturalness + β_flu * fluency,
 sigma=σ_rest,
 observed=data['restoration'])
```

Decision: Option A vs. B

Use Option A (fractal_dim directly) if:

Literature shows fractals matter regardless of source You want to
capture total fractal effect (natural + artificial) Use Option B
(fractal_residual) if:

You want to separate naturalness effect from pure fractal effect You've
run experiments showing fractals work independently 6.2 Practical
Workflow Phase 1: Identify Hierarchical Relationships (Month 1)

For each attribute pair, test: Correlation (r) Predictive relationship
(R²) Causal logic ("Can I change X without Y?") Build attribute DAG:
python attribute_dag = { 'natural_materials': { 'causes':
['fractal_dimension', 'color_naturalness'], 'deterministic': False, \#
Natural materials → fractals (not perfect) 'r_squared': 0.62 },
'glazing_ratio': { 'causes': ['daylight_illuminance'], 'deterministic':
True, \# Physics-based 'r_squared': 0.95 }, \#... etc }

``` 

**Phase 2: Decide on Model Structure (Month 2)**

For each hierarchical relationship, choose:

- **Fully hierarchical** (X causes Y, model Y as function of X)
 - Use when: R² >0.7, strong theory, deterministic relationship
 - Example: Glazing → Daylight
 
- **Residual approach** (X and Y residual both included)
 - Use when: R² =0.4-0.7, want to separate effects
 - Example: Natural materials and fractal residual
 
- **Composite** (Bundle X and Y into single score)
 - Use when: R² >0.8, no need to separate
 - Example: Merge all biophilic features

**Phase 3: Validate with Experiments (Months 8-12)**

Run 2-3 key experiments:

1. **Fractal × Naturalness experiment** (as described in Solution 4)
2. **Daylight × Color Temperature** (to test if warm light can substitute daylight)
3. **Spatial Complexity × Coherence** (test if they interact)

**Phase 4: Update Model (Month 13+)**

Based on experiments:
- If fractals work independently → Keep fractal_dimension as separate attribute
- If fractals only work in natural materials → Model as hierarchical (Natural → Fractal)
- If interaction is strong → Add interaction term

---

## Addressing Your Specific Case

### Natural Textures → Fractal Dimension → Restoration

**Current literature state:**
- Most papers test either (Natural → Naturalness → Restoration) OR (Fractals → Fluency → Restoration)
- Few test both simultaneously
- You hypothesize fractals partially mediate naturalness effect

**Recommended approach:**

**Step 1: Model hierarchically initially**
```

Natural Textures → Fractal Dimension → Perceptual Fluency → Restoration
↘ Naturalness → Restoration Step 2: Estimate from observational data

python \# Fit hierarchical model natural_coverage =
data['natural_coverage']

# Fractal is caused by natural coverage

fractal_dim = 1.1 + 0.4 \* natural_coverage + noise

# Two mediator pathways

naturalness = f(natural_coverage) fluency = g(fractal_dim)

# Restoration from both

restoration = β_nat \* naturalness + β_flu \* fluency Step 3: Compute
mediation

python \# Total effect of natural textures on restoration total =
indirect_via_naturalness + indirect_via_fractals + direct

# Decomposition

prop_via_naturalness = (β_nat_textures \* β_nat_to_rest) / total
prop_via_fractals = (β_nat_to_frac \* β_frac_to_flu \* β_flu_to_rest) /
total

print(f"Natural textures → Restoration:") print(f"
{prop_via_naturalness*100:.0f}% via naturalness perception") print(f"
{prop_via_fractals*100:.0f}% via fractal fluency")

``` 

**Expected result:**
```

Natural textures → Restoration: 75% via naturalness perception 25% via
fractal fluency

Interpretation: Naturalness dominates, but fractals contribute. Step 4:
Run disambiguation experiment (Year 2)

Test artificial fractals (Pollock painting) vs. natural wood vs. smooth
wood vs. smooth plastic.

If experiment shows:

Artificial fractals work → Fractals are independent mechanism Artificial
fractals don't work → Fractals only matter IN natural materials Step 5:
Update model structure

Based on experiments, either:

Keep hierarchical (current model is correct) Add interaction (Natural ×
Fractal synergy) Simplify to naturalness only (fractals don't add beyond
naturalness) Decision Framework: When to Model Hierarchically Model A →
B hierarchically if: ✓ Strong correlation (r \> 0.6) ✓ Predictable
relationship (R² \> 0.5 when regressing B on A) ✓ Causal logic
("Changing A always changes B") ✓ Literature consensus ("B is a property
of A")

Keep A and B separate if: ✓ Weak correlation (r \< 0.4) ✓ Independent
manipulation possible ("I can change B without A") ✓ Both have unique
effects (experiments show both matter independently)

Use residuals if: ✓ Moderate correlation (0.4 \< r \< 0.7) ✓ Want to
test unique effects beyond their shared variance ✓ Both plausibly causal
(unclear which causes which)

Implementation Roadmap Month 1-2: Build Attribute DAG python \# 1.
Compute all pairwise correlations corr_matrix = data[attributes].corr

# 2. For highly correlated pairs (r \> 0.6), test causality

hierarchical_pairs = [] for i, attr1 in enumerate(attributes): for j,
attr2 in enumerate(attributes[i+1:]): if corr_matrix.loc[attr1, attr2]
\> 0.6: \# Test: Does attr1 predict attr2? r2 =
test_predictive_relationship(attr1, attr2, data) \# Test: Causal logic
causal = expert_rating(f"Does {attr1} cause {attr2}?")

``` 
 if r2 > 0.5 and causal > 0.7:
 hierarchical_pairs.append((attr1, attr2, r2))
```

# 3. Build DAG

attribute_dag = build_dag(hierarchical_pairs) plot_dag(attribute_dag)
Month 3-6: Fit Hierarchical Model python \# Implement full hierarchical
Bayesian model \# with computed attributes as functions of exogenous
attributes

with pm.Model as model: \# Exogenous attributes (Tier 1) exogenous =
{name: data[name] for name in tier1_attributes}

``` 
# Computed attributes (Tier 2)
for attr, parents in attribute_dag.items:
 if parents:
 # This attribute is caused by others
 pred = sum(β[p] * exogenous[p] for p in parents)
 computed[attr] = pm.Deterministic(attr, pred)
 else:
 # This is exogenous
 exogenous[attr] = data[attr]

# Mediators (Tier 3) - as before
# Outcomes (Tier 4) - as before
```

Month 8-12: Validate Key Hierarchies Experimentally Run 2-3 experiments
on most important/uncertain hierarchies:

Fractal × Naturalness Daylight × Glazing Complexity × Coherence Month
13+: Refine Based on Experiments Update model structure based on
experimental results.

Final Recommendation For your specific case (Natural Textures /
Fractals):

Start with hierarchical model: Natural Materials → Fractal Dimension →
Fluency Also include direct path: Natural Materials → Naturalness →
Restoration Estimate mediation proportions from observational data Run
experiment in Year 2 to validate Update model based on experimental
findings General principle:

Model physical/computational hierarchies explicitly (glazing → daylight)
Model statistical hierarchies where R² \>0.6 and theory supports Use
residuals when unsure about direction Validate with experiments wherever
possible This gives you:

Correct handling of multicollinearity NOW Flexibility to refine later
Testable hypotheses for experiments Interpretable decomposition of
effects
