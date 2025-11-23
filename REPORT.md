# RSA Cryptography Project Report
## Overview
This report presents the results of RSA encryption/decryption performance analysis and Quadratic Sieve factorization for three different RSA key sizes.

## Part 1: Secret Key Calculation

For each RSA key pair, the private key d is calculated using the formula:
d = e^(-1) mod phi(N), where phi(N) = (p-1)(q-1)

| Key | p | q | N | e | d |
|-----|---|---|---|-----|----------|
| key1 | 25117 | 25601 | 643020317 | 65537 | 489705473 |
| key2 | 131071 | 131129 | 17187209159 | 65537 | 15834271793 |
| key3 | 262139 | 262151 | 68720000989 | 65537 | 24051869273 |

## Part 2: RSA Encryption/Decryption Performance

Performance measurements were conducted using a fixed message (12345) with 1000 repetitions for each key pair.

### Timing Results

| Key | N (bits) | Encryption Time (us) | Decryption Time (us) |
|-----|----------|---------------------|---------------------|
| key1 | 30 | 3.4778 | 11.9242 |
| key2 | 35 | 8.6272 | 21.1857 |
| key3 | 37 | 8.6532 | 22.0566 |

### Analysis

The encryption and decryption times show that:
- Encryption is faster than decryption (since e=65537 is smaller than d)
- Performance scales with the size of the modulus N
- The modular exponentiation algorithm efficiently handles large numbers

## Part 3: Quadratic Sieve Factorization

### Algorithm Description

The Quadratic Sieve algorithm works as follows:

1. **Factor Base Generation**: Generate a set of small primes p such that    the Legendre symbol (N/p) = 1, meaning N is a quadratic residue mod p.

2. **Sieving**: For values x near sqrt(N), compute q(x) = x^2 mod N.    Find values where q(x) factors completely over the factor base (smooth numbers).

3. **Linear Algebra**: Build a matrix over GF(2) where each row represents    the parity of exponents in the factorization of a smooth number.    Find linear dependencies using Gaussian elimination.

4. **Factor Recovery**: For each dependency, compute X = product(x_i) and    Y = product(sqrt(q(x_i))) mod N. If X^2 = Y^2 (mod N) and X != +/-Y (mod N),    then gcd(X - Y, N) or gcd(X + Y, N) gives a non-trivial factor.

### Factorization Results

| Key | N | Recovered p | Recovered q | Factorization Time (s) |
|-----|---|-------------|-------------|----------------------|
| key1 | 643020317 | 25117 | 25601 | 0.0194 |
| key2 | 17187209159 | 131071 | 131129 | 0.0210 |
| key3 | 68720000989 | 262139 | 262151 | 0.0495 |

### Verification

All recovered prime factors were verified:
- **key1**: p * q = 25117 * 25601 = 643020317 = N [OK]
  - Expected private key d = 489705473
  - Recovered private key d = 489705473
  - Keys match: True [OK]

- **key2**: p * q = 131071 * 131129 = 17187209159 = N [OK]
  - Expected private key d = 15834271793
  - Recovered private key d = 15834271793
  - Keys match: True [OK]

- **key3**: p * q = 262139 * 262151 = 68720000989 = N [OK]
  - Expected private key d = 24051869273
  - Recovered private key d = 24051869273
  - Keys match: True [OK]

## Part 4: Extrapolation to 2048-bit RSA

### Growth Analysis

The factorization time grows exponentially with the bit size of N. Fitting an exponential curve to the data points:

- Fitted curve: log(time) = 0.111456 × bits + -7.394096

### Estimated Time for 2048-bit RSA

- **Seconds**: 8.35e+95
- **Years**: 2.65e+88

### Discussion

The extrapolation shows that factoring a 2048-bit RSA modulus using this basic Quadratic Sieve implementation would take an astronomical amount of time. However, this is a simplified implementation. Real-world factorization uses more sophisticated techniques like:

- Number Field Sieve (NFS), which is asymptotically faster
- Parallel processing and distributed computing
- Optimized sieving algorithms
- Better smoothness bounds and factor base selection

Even with these improvements, 2048-bit RSA remains secure against classical computers for the foreseeable future.

## Code Listings

All code is provided in `rsa_project.py`. Key functions include:

- `calculate_private_key()`: Computes RSA private key using extended Euclidean algorithm
- `rsa_encrypt()` / `rsa_decrypt()`: RSA encryption and decryption using fast exponentiation
- `quadratic_sieve()`: Main Quadratic Sieve factorization algorithm
- `factor_base()`: Generates factor base of quadratic residues
- `gaussian_elimination_gf2()`: Linear algebra over GF(2) to find dependencies

## Difficulties and Observations

### Challenges Encountered:

1. **Smoothness Bound Selection**: Choosing appropriate bounds for the factor base    and sieving interval required tuning. Too small bounds yield insufficient    smooth relations, while too large bounds increase computation time.

2. **Linear Algebra**: Implementing Gaussian elimination over GF(2) correctly    to find linear dependencies was crucial for factor recovery.

3. **Sign Handling**: Negative smooth numbers (when x² < N) required special    handling in the factor base and linear algebra steps.

### Interesting Observations:

1. The Quadratic Sieve performs well for the given key sizes, but the    exponential growth in complexity becomes apparent even for modest increases    in bit size.

2. RSA decryption is slower than encryption because the private exponent d    is typically much larger than the public exponent e (65537).

3. The number of smooth relations needed is approximately equal to the size    of the factor base, but having a few extra relations helps find dependencies.

