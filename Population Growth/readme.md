# Population Growth with Carrying Capacity: Complete Mathematical Derivations
A comprehensive mathematical treatment of population dynamics with complete derivations from first principles. This repository presents step-by-step mathematical development of the logistic growth model, analytical solutions, and practical applications.

## Overview

Population growth in biological systems follows predictable mathematical patterns when environmental constraints are properly modeled. This work develops the complete mathematical framework for population dynamics, starting from fundamental biological assumptions and deriving all governing equations through rigorous mathematical analysis.

## Mathematical Development from First Principles

### Derivation of Basic Population Growth

Consider a population P(t) at time t. The fundamental assumption in population dynamics is that the rate of change depends on the current population size. Let β represent the per capita birth rate and δ represent the per capita death rate.

**Step 1: Rate of births and deaths**
```
Rate of births = β × P(t)
Rate of deaths = δ × P(t)
Net rate of change = β × P(t) - δ × P(t)
```

**Step 2: Differential equation formulation**
```
dP/dt = βP - δP = (β - δ)P
```

**Step 3: Define intrinsic growth rate**
Let r = β - δ (intrinsic growth rate), then:
```
dP/dt = rP
```

This is the fundamental exponential growth equation.

### Analytical Solution of Exponential Growth

**Step 1: Separate variables**
```
dP/P = r dt
```

**Step 2: Integrate both sides**
```
∫(1/P)dP = ∫r dt
ln|P| = rt + C₁
```

**Step 3: Solve for P(t)**
```
|P| = e^(rt + C₁) = e^(C₁) × e^(rt)
P(t) = C × e^(rt)
```

**Step 4: Apply initial condition P(0) = P₀**
```
P₀ = C × e^(r×0) = C × 1 = C
```

**Final exponential solution:**
```
P(t) = P₀e^(rt)
```

### Derivation of Carrying Capacity Concept

Exponential growth assumes unlimited resources, which is unrealistic. Real environments have finite carrying capacity K. As population approaches K, resources become scarce and effective growth rate decreases.

**Mathematical formulation of resource limitation:**

The fraction of available resources is (K - P)/K, which equals (1 - P/K). The effective growth rate becomes:
```
r_effective = r × (1 - P/K)
```

**Substituting into the fundamental equation:**
```
dP/dt = r_effective × P = rP(1 - P/K)
```

This is the **logistic differential equation**.

## Complete Analytical Solution of Logistic Equation

Starting with the logistic equation:
```
dP/dt = rP(1 - P/K)
```

**Step 1: Separate variables**
```
dP/[P(1 - P/K)] = r dt
```

**Step 2: Simplify the left side**
```
dP/[P(1 - P/K)] = dP/[P(K-P)/K] = K dP/[P(K-P)]
```

So our equation becomes:
```
K dP/[P(K-P)] = r dt
```

**Step 3: Partial fraction decomposition**

We need to decompose K/[P(K-P)]:
```
K/[P(K-P)] = A/P + B/(K-P)
```

Multiply both sides by P(K-P):
```
K = A(K-P) + BP
K = AK - AP + BP
K = AK + P(B-A)
```

Comparing coefficients:
- Constant term: K = AK → A = 1
- Coefficient of P: 0 = B - A → B = A = 1

Therefore:
```
K/[P(K-P)] = 1/P + 1/(K-P)
```

**Step 4: Substitute back and integrate**
```
∫[1/P + 1/(K-P)]dP = ∫r dt
∫(1/P)dP + ∫(1/(K-P))dP = ∫r dt
ln|P| - ln|K-P| = rt + C₂
ln|P/(K-P)| = rt + C₂
```

**Step 5: Solve for P(t)**
```
P/(K-P) = e^(rt + C₂) = e^(C₂) × e^(rt)
```

Let A = e^(C₂), then:
```
P/(K-P) = Ae^(rt)
P = (K-P)Ae^(rt)
P = KAe^(rt) - PAe^(rt)
P + PAe^(rt) = KAe^(rt)
P(1 + Ae^(rt)) = KAe^(rt)
P = KAe^(rt)/(1 + Ae^(rt))
```

**Step 6: Simplify by dividing numerator and denominator by Ae^(rt)**
```
P(t) = K/(A^(-1)e^(-rt) + 1)
P(t) = K/(1 + A^(-1)e^(-rt))
```

**Step 7: Determine integration constant using initial conditions**

At t = 0: P(0) = P₀
```
P₀ = K/(1 + A^(-1))
P₀(1 + A^(-1)) = K
P₀ + P₀A^(-1) = K
P₀A^(-1) = K - P₀
A^(-1) = (K - P₀)/P₀
A = P₀/(K - P₀)
```

**Final analytical solution:**
```
P(t) = K/(1 + ((K-P₀)/P₀)e^(-rt))
```

## Mathematical Properties and Characteristics

### Inflection Point Calculation

The inflection point occurs where d²P/dt² = 0. Taking the derivative of dP/dt = rP(1-P/K):

**Step 1: First derivative**
```
dP/dt = rP - rP²/K
```

**Step 2: Second derivative**
```
d²P/dt² = r(dP/dt) - (2rP/K)(dP/dt)
d²P/dt² = (dP/dt)[r - 2rP/K]
d²P/dt² = (dP/dt) × r(1 - 2P/K)
```

**Step 3: Set equal to zero**
Since dP/dt ≠ 0 for growing populations:
```
1 - 2P/K = 0
P = K/2
```

The inflection point occurs at exactly half the carrying capacity.

### Maximum Growth Rate

At the inflection point P = K/2:
```
(dP/dt)_max = rP(1 - P/K)
(dP/dt)_max = r(K/2)(1 - (K/2)/K)
(dP/dt)_max = r(K/2)(1 - 1/2)
(dP/dt)_max = r(K/2)(1/2)
(dP/dt)_max = rK/4
```

### Time to Inflection Point

To find when P = K/2, solve:
```
K/2 = K/(1 + Ae^(-rt))
1/2 = 1/(1 + Ae^(-rt))
1 + Ae^(-rt) = 2
Ae^(-rt) = 1
e^(-rt) = 1/A
-rt = ln(1/A) = -ln(A)
t = ln(A)/r
```

Since A = (K-P₀)/P₀:
```
t_inflection = ln((K-P₀)/P₀)/r
```

## Example: Forest Ecosystem Recovery

Consider a reforestation project where tree seedlings are planted in a degraded forest area. Based on ecological studies, we have the following parameters:

### Problem Setup
- **Initial population**: P₀ = 200 seedlings per hectare
- **Intrinsic growth rate**: r = 0.08 year⁻¹ (8% annual growth under ideal conditions)
- **Carrying capacity**: K = 1500 trees per hectare (mature forest density)

### Complete Mathematical Analysis

**Step 1: Calculate integration constant**
```
A = (K - P₀)/P₀ = (1500 - 200)/200 = 1300/200 = 6.5
```

**Step 2: A Complete analytical solution**
```
P(t) = 1500/(1 + 6.5e^(-0.08t))
```

**Step 3: Calculate key characteristics**

*Maximum growth rate:*
```
(dP/dt)_max = rK/4 = 0.08 × 1500/4 = 30 trees per hectare per year
```

*Time to inflection point:*
```
t_inflection = ln(A)/r = ln(6.5)/0.08 = 1.872/0.08 = 23.4 years
```

*Population at inflection:*
```
P_inflection = K/2 = 1500/2 = 750 trees per hectare
```

### Specific Calculations

**Question 1: Population after 10 years**
```
P(10) = 1500/(1 + 6.5e^(-0.08×10))
P(10) = 1500/(1 + 6.5e^(-0.8))
P(10) = 1500/(1 + 6.5 × 0.4493)
P(10) = 1500/(1 + 2.920)
P(10) = 1500/3.920 = 383 trees per hectare
```

**Question 2: Time to reach 90% of carrying capacity**

Target: 0.9 × 1500 = 1350 trees per hectare

```
1350 = 1500/(1 + 6.5e^(-0.08t))
1350(1 + 6.5e^(-0.08t)) = 1500
1 + 6.5e^(-0.08t) = 1500/1350 = 1.111
6.5e^(-0.08t) = 0.111
e^(-0.08t) = 0.111/6.5 = 0.0171
-0.08t = ln(0.0171) = -4.068
t = 4.068/0.08 = 50.85 years
```

**Question 3: Growth rate after 25 years**

First, find the population at t = 25:
```
P(25) = 1500/(1 + 6.5e^(-0.08×25))
P(25) = 1500/(1 + 6.5e^(-2))
P(25) = 1500/(1 + 6.5 × 0.1353)
P(25) = 1500/(1 + 0.879)
P(25) = 1500/1.879 = 799 trees per hectare
```

Growth rate at t = 25:
```
dP/dt = rP(1 - P/K) = 0.08 × 799 × (1 - 799/1500)
dP/dt = 63.92 × (1 - 0.533)
dP/dt = 63.92 × 0.467 = 29.9 trees per hectare per year
```

**Question 4: Population after 50 years**
```
P(50) = 1500/(1 + 6.5e^(-0.08×50))
P(50) = 1500/(1 + 6.5e^(-4))
P(50) = 1500/(1 + 6.5 × 0.0183)
P(50) = 1500/(1 + 0.119)
P(50) = 1500/1.119 = 1341 trees per hectare
```

### Summary of Results

| Time (years) | Population (trees/ha) | Growth Rate (trees/ha/year) | % of Carrying Capacity |
|--------------|----------------------|------------------------------|------------------------|
| 0            | 200                  | 12.8                         | 13.3%                  |
| 10           | 383                  | 22.9                         | 25.5%                  |
| 23.4         | 750                  | 30.0 (maximum)               | 50.0%                  |
| 25           | 799                  | 29.9                         | 53.3%                  |
| 50           | 1341                 | 11.4                         | 89.4%                  |
| 50.85        | 1350                 | 10.8                         | 90.0%                  |

### Biological Interpretation

The forest recovery follows the characteristic S-shaped logistic curve. During the first decade, growth remains relatively slow as young trees establish root systems and canopy coverage remains sparse. The exponential-like phase occurs between years 10-30, with maximum growth rate achieved around year 23 when tree density reaches half the mature forest level.

After year 25, intraspecific competition becomes significant as trees compete for sunlight, nutrients, and space. Growth rate begins declining despite continued population increase. By year 50, the forest approaches mature density with minimal net growth as mortality roughly balances recruitment.

The 51-year timeline to reach 90% of carrying capacity demonstrates the extended time scales required for forest ecosystem recovery, reflecting the complex ecological processes governing tree growth, survival, and competition in natural systems.

## Applications and Extensions

This mathematical framework applies broadly across biological systems, including bacterial growth, wildlife population management, epidemic modeling, and conservation biology. The analytical solution provides exact predictions without numerical approximation, making it valuable for both theoretical analysis and practical applications.

