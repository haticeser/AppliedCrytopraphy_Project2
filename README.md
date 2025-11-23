# RSA Cryptography Project

This project implements RSA encryption/decryption and Quadratic Sieve factorization algorithm.

## Requirements

Install the required packages:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install numpy matplotlib
```

## Usage

### Run the main project:
```bash
python rsa_project.py
```

This will:
1. Calculate secret keys for all three RSA key pairs
2. Measure RSA encryption/decryption performance
3. Factor each modulus using Quadratic Sieve
4. Display timing results and extrapolation to 2048-bit RSA

### Generate the report:
```bash
python generate_report.py
```

This will generate a comprehensive markdown report (`REPORT.md`) with all results, analysis, and code descriptions.

## Project Structure

- `rsa_project.py` - Main implementation with all algorithms
- `generate_report.py` - Report generator
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Key Features

1. **RSA Implementation**:
   - Extended Euclidean Algorithm for modular inverse
   - Fast modular exponentiation
   - Encryption and decryption with timing

2. **Quadratic Sieve Factorization**:
   - Factor base generation
   - Sieving for smooth numbers
   - Gaussian elimination over GF(2)
   - Factor recovery

3. **Performance Analysis**:
   - Timing measurements
   - Extrapolation to 2048-bit RSA
   - Growth analysis

## Notes

- The Quadratic Sieve implementation is simplified but functional for the given key sizes
- For larger keys, more sophisticated optimizations would be needed
- The code includes error handling and verification of results

