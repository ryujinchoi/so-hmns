# Contributing to SO-HMNS
Thank you for contributing to the SO-HMNS Universal Infrastructure. To preserve the mathematical soundness of this engine, all contributions must strictly adhere to the zero-error hardware lattice principles.

## 📐 Invariant Development Rules
1. **Absolute Real Field ($\mathbb{R}$) Ban**: Never introduce floating-point numbers or continuum calculus approximations. All variables must utilize `fractions.Fraction` or Gaussian rational structures over $\mathbb{Q}(i)$.
2. **Determinant Unity Lock**: All new dynamic transformation matrices must be formally verified to satisfy $|det| = 1$ (for unitary mechanics) or $det = 0$ (for singular projection metrics).
3. **Syntax Guard Compliance**: Negative fractions must always be wrapped in protective parentheses, e.g., `(-num/den)`.

## 🚀 Pull Request Lifecycle
Before submitting a PR, you must run the local automated verifier:
```bash
./run_pipeline.sh
```
Any numeric leakage error greater than 0.0000% will result in automated system rejection.

## 💰 Capital Support Channels
Support our operational computing grid via:
- **PayPal.Me Capital Node**: https://paypal.me
- **GitHub Node**: https://github.com
