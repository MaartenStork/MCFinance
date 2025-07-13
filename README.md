# Monte Carlo Methods in Computational Finance

This repository contains implementations of Monte Carlo methods applied to quantitative finance, focusing on three key areas: variance swaps, Asian options, and weather derivatives. The project demonstrates how computational finance balances analytic tractability with simulation-based methods to price various derivatives.

## Overview

Monte Carlo methods have been a cornerstone of quantitative finance since Boyle's 1977 application to option pricing. This project explores advanced Monte Carlo techniques for pricing complex or path-dependent securities where closed-form solutions are unavailable. The implementation showcases:

- **Variance Swaps**: Closed-form treatment using log-contracts and dynamic hedging
- **Asian Options**: Monte Carlo simulation under the Heston stochastic volatility model with variance reduction techniques
- **Weather Derivatives**: Temperature-based derivatives using seasonal mean-reverting processes

## Repository Structure

```
MCFinance/
├── ex2.ipynb                    # Asian Options under Heston Model
├── ex3.ipynb                    # Weather Derivatives Analysis
├── download_weather_data.py     # Amsterdam temperature data fetcher
├── daily_data.csv              # Daily temperature data (cleaned)
├── hourly_data.csv             # Hourly temperature data (cleaned)
├── daily_data_with_missing.csv # Original daily data with missing values
├── hourly_data_with_missing.csv # Original hourly data with missing values
└── plots/                      # Generated visualizations
```

## Key Components

### 1. Variance Swaps

- **Analytic Solution**: Derives closed-form expressions for variance swap pricing
- **Heston Model**: Implements stochastic volatility framework
- **Replication Strategy**: Shows how variance can be replicated using log-contracts
- **Dynamic Hedging**: Demonstrates fair variance strike computation

### 2. Asian Options

- **Monte Carlo Simulation**: Implements both Euler and Milstein discretization schemes
- **Heston Model**: Stochastic volatility with correlated Brownian motions
- **Variance Reduction**: Uses control variates (geometric Asian options) to reduce simulation variance
- **Path-Dependent Pricing**: Handles arithmetic Asian options where no closed-form solution exists

### 3. Weather Derivatives

- **Temperature Modeling**: Seasonal mean-reverting process calibrated to Amsterdam weather data
- **Time Series Analysis**: Comprehensive analysis including:
  - Seasonal decomposition
  - Autoregressive model fitting (AR(7))
  - Residual analysis and model validation
- **Derivative Pricing**: Monte Carlo pricing of heating/cooling degree day contracts
- **Data Processing**: Handles missing values with interpolation techniques

## Technical Implementation

### Monte Carlo Framework

- **Correlated Random Variables**: Implements Cholesky decomposition for correlated Brownian motions
- **Discretization Schemes**: Both Euler and Milstein methods for SDE simulation
- **Variance Reduction**: Control variates and antithetic variables
- **Path Generation**: Efficient vectorized implementations using NumPy

### Stochastic Models

- **Heston Model**: Full implementation with mean-reverting variance process
- **Geometric Brownian Motion**: Benchmark Black-Scholes framework
- **Seasonal Mean-Reversion**: Custom temperature model with sinusoidal trends

### Data Analysis

- **Weather Data**: Real Amsterdam temperature data (2020-2024) from Open-Meteo API
- **Time Series**: Comprehensive analysis including stationarity tests, ACF/PACF analysis
- **Model Validation**: Residual analysis, Q-Q plots, and goodness-of-fit tests

## Installation and Usage

### Prerequisites

```bash
pip install numpy pandas matplotlib seaborn scipy statsmodels
pip install openmeteo-requests requests-cache retry-requests
pip install tqdm jupyter
```

### Running the Analysis

1. **Download Weather Data** (optional - data files are included):

   ```bash
   python download_weather_data.py
   ```
2. **Asian Options Analysis**:
   Open and run `ex2.ipynb` to explore:

   - Heston model calibration
   - Monte Carlo path generation
   - Asian option pricing with control variates
   - Variance reduction effectiveness
3. **Weather Derivatives Analysis**:
   Open and run `ex3.ipynb` to explore:

   - Temperature data analysis and modeling
   - Seasonal decomposition and trend analysis
   - AR model fitting and validation
   - Weather derivative pricing

## Key Results

### Variance Swaps

- Derives exact analytical formula for fair variance strike under Heston model
- Demonstrates replication using log-contracts and dynamic hedging
- Shows power of no-arbitrage arguments in complete markets

### Asian Options

- Implements efficient Monte Carlo pricing with variance reduction
- Achieves order-of-magnitude improvement in simulation efficiency using control variates
- Compares Euler vs. Milstein discretization schemes

### Weather Derivatives

- Develops bespoke seasonal mean-reverting model for Amsterdam temperatures
- Fits AR(7) model to deseasonalized residuals
- Demonstrates Monte Carlo pricing for heating/cooling degree day contracts
- Highlights importance of careful model calibration for non-financial underlyings

## References

The implementation builds upon foundational work in computational finance, particularly Boyle (1977) and extends to modern applications in stochastic volatility and weather derivatives. The project showcases how Monte Carlo methods bridge theoretical finance with practical implementation challenges.

---

*This project demonstrates the versatility of Monte Carlo methods in capturing uncertainty beyond traditional financial assets, emphasizing the importance of tailored calibration and validation for different underlying processes.*
