# 🔐 Cryptographic Benchmarking Project

This repository contains benchmarking code for measuring the computational cost of asymmetric cryptographic operations. The project focuses on three areas:

- **ElGamal encryption scheme** using Charm-Crypto (Python)
- **Elliptic curve operations** using Charm-Crypto (Python)
- **Prime-ordered group operations** using NTL and GMP (C++)

The purpose is to evaluate the performance across different security levels.

---
## ⚙️ Requirements

### For C++ Benchmarks (NTL + GMP)

Install dependencies:

```bash
sudo apt install libntl-dev libgmp-dev g++
```

### For Python Benchmarks (Charm-Crypto)

Set up a virtual environment and install Charm:

```bash
python3 -m venv venv
source venv/bin/activate
pip install charm-crypto
```
---

## 🚀 How to Run

### Prime-Ordered Group Benchmark (C++)

```bash
g++ -o benchmark benchmark.cpp -lntl -lgmp
./benchmark
```
---

### Elliptic Curve Benchmark (Python)

```bash
python curve_benchmark.py
```

This script benchmarks EC group addition and scalar multiplication on several standard curves:
- `secp256k1`
- `prime256v1`
- `secp384r1`
- `secp521r1`
- `sect233r1`

---

### ElGamal Scheme Benchmark (Python)

```bash
python elgamal_benchmark.py
```

This script tests the performance of ElGamal encryption and decryption over elliptic curve groups using Charm.

---

## 📊 Results

Each benchmark returns minimum, maximum, and average CPU times for the tested operations. These results are printed to the terminal.

To save the results:

```bash
python elgamal_benchmark.py > elgamal_results.txt
python curve_benchmark.py > curve_results.txt
./benchmark > benchmark_results.txt
```

All benchmark outputs are stored in:
- `benchmark_results.txt`
- `curve_results.txt`
- `elgamal_results.txt`

---

## 📝 Report
Full report is available for download in report.pdf file.

---

## 🔗 References

- [GMP – GNU Multiple Precision Arithmetic Library](https://gmplib.org/)
- [NTL – A Library for doing Number Theory](https://libntl.org/)
- [Charm-Crypto Framework](https://github.com/JHUISI/charm)

---

## 👤 Author

Andrej Hadži-Đorđević  
August 2025
