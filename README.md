# Option-Pricing-Analytics-Lab
**Quantitative Finance library for Multi-Model Option Pricing and Risk Analytics.**

## 1. Presentation
This project was developed during my second year at **Télécom SudParis**. It marks a significant evolution from linear derivatives to non-linear instruments. This library implements a high-performance engine capable of valuing both **European Vanilla** and **Path-Dependent Exotic** options using two distinct methodologies:
*   **Numerical Methods**: Monte-Carlo simulation based on Geometric Brownian Motion (GBM).
*   **Analytical Methods**: Black-Scholes closed-form solutions for model validation.

## 2. Pricing Methodologies

### A. Numerical: Monte-Carlo Engine
To value complex Path-Dependent options (Asian, Barrier, Lookback), the engine simulates thousands of possible market scenarios using the **Geometric Brownian Motion (GBM)** stochastic process:

$$ dS_t = r S_t dt + \sigma S_t dW_t $$

The fair value is obtained by computing the discounted expected payoff under the risk-neutral measure:

$$
Price = e^{-rT} E [ Payoff(S_t) ]
$$

### B. Analytical: Black-Scholes Benchmark
For Vanilla options, the engine implements the closed-form Black-Scholes formula to serve as a precision benchmark (Gold Standard) to validate the convergence of the Monte-Carlo paths.

## 3. Supported Instruments
*   **Vanilla**: European Calls & Puts.
*   **Asians**: Arithmetic and Geometric averages (mitigating spot volatility).
*   **Barriers**: Knock-in and Knock-out logic (Up/Down directions).
*   **Lookback**: Fixed and Floating strikes (capturing historical extrema).
*   **Chooser**: Dynamic switching between Call/Put at intermediate dates.
*   **Forward Start**: Strike determination at future fixing dates.

## 4. Technical Implementation & Numerical Stability
*   **Vectorized Computation**: Full use of **NumPy** to process 100,000+ paths simultaneously, avoiding Python overhead and ensuring industrial-grade performance.
*   **Numerical Stability**: Implementation of the **Log-mean-exp trick** for Geometric Asian options to prevent floating-point overflow during large-scale simulations.
*   **Abstract Architecture**: Use of Abstract Base Classes (ABC) and Polymorphism, allowing the `MonteCarloPricer` to value any instrument via a unified interface.

## 5. Sample Output & Convergence Validation
The engine provides a comparative report to verify model accuracy:

| PRODUCT NAME                        | MC FAIR VALUE | ANALYTICAL (BS) | DIFF    |
|-------------------------------------|---------------|-----------------|---------|
| Vanilla Call                        | 10.4521       | 10.4503         | 0.0018  |
| Asian Call (Geo)                    | 5.2104        | N/A             | N/A     |
| Lookback Call (Fixed)               | 18.3241       | N/A             | N/A     |

## 6. Project Structure
```text
core/
├── base.py       # Abstract interface & Common Analytics (PNL)
├── vanilla.py    # European standard pricing (MC + Black-Scholes)
├── exotic.py     # Path-Dependent logic for 6 exotic families
├── simulator.py  # GBM Stochastic trajectory engine
└── pricer.py     # Monte-Carlo valuation hub
```

## Career Objective
Aspiring **Quantitative Researcher / Developer**. Currently seeking an internship in Quantitative Finance starting in **Fall 2026**. I am focused on bridging the gap between advanced mathematical models and high-performance software implementation.

---
**Contact**: Maéva Cavaleri - [cavalerimaeva@gmail.com](mailto:cavalerimaeva@gmail.com)
