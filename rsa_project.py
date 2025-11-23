"""
RSA Cryptography Project
Implements RSA encryption/decryption and Quadratic Sieve factorization
"""

import math
import time
import random
from collections import defaultdict
from typing import Tuple, List, Dict
import numpy as np
import matplotlib.pyplot as plt

# Given RSA key pairs
RSA_KEYS = {
    'key1': {'p': 25117, 'q': 25601, 'N': 643020317, 'e': 65537},
    'key2': {'p': 131071, 'q': 131129, 'N': 17187209159, 'e': 65537},
    'key3': {'p': 262139, 'q': 262151, 'N': 68720000989, 'e': 65537}
}


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm
    Returns (gcd, x, y) such that ax + by = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
    """
    Calculate modular inverse of a mod m using extended Euclidean algorithm
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
    return (x % m + m) % m


def calculate_private_key(p: int, q: int, e: int) -> int:
    """
    Calculate RSA private key d from primes p, q and public exponent e
    d = e^(-1) mod phi(N) where phi(N) = (p-1)(q-1)
    """
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)
    return d


def fast_power(base: int, exp: int, mod: int) -> int:
    """
    Fast modular exponentiation: base^exp mod mod
    Uses binary exponentiation for efficiency
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result


def rsa_encrypt(message: int, e: int, N: int) -> int:
    """
    RSA encryption: ciphertext = message^e mod N
    """
    return fast_power(message, e, N)


def rsa_decrypt(ciphertext: int, d: int, N: int) -> int:
    """
    RSA decryption: message = ciphertext^d mod N
    """
    return fast_power(ciphertext, d, N)


def is_square(n: int) -> bool:
    """
    Check if n is a perfect square
    """
    root = int(math.isqrt(n))
    return root * root == n


def legendre_symbol(a: int, p: int) -> int:
    """
    Calculate Legendre symbol (a/p)
    Returns 1 if a is a quadratic residue mod p, -1 if not, 0 if p divides a
    """
    return pow(a, (p - 1) // 2, p)


def factor_base(n: int, bound: int) -> List[int]:
    """
    Generate factor base: primes p such that (n/p) = 1 (n is quadratic residue mod p)
    """
    def sieve_of_eratosthenes(limit: int) -> List[int]:
        if limit < 2:
            return []
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(math.sqrt(limit)) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        return [i for i in range(2, limit + 1) if sieve[i]]
    
    primes = sieve_of_eratosthenes(bound)
    factor_base_list = []
    
    for p in primes:
        if legendre_symbol(n, p) == 1:
            factor_base_list.append(p)
    
    return factor_base_list


def quadratic_sieve(n: int, smooth_bound: int = None, M: int = None) -> Tuple[int, int]:
    """
    Quadratic Sieve Algorithm to factor n = p * q
    
    Parameters:
    - n: number to factor
    - smooth_bound: bound for smoothness (default: sqrt(n))
    - M: sieving interval size (default: 2 * smooth_bound)
    
    Returns:
    - (p, q): prime factors of n
    """
    if smooth_bound is None:
        smooth_bound = max(50, int(math.sqrt(math.sqrt(n))) + 50)
    
    if M is None:
        M = max(100, 2 * smooth_bound)
    
    # Generate factor base
    fb = factor_base(n, smooth_bound)
    print(f"  Factor base size: {len(fb)} primes (bound: {smooth_bound})")
    
    # Sieving
    sqrt_n = int(math.isqrt(n))
    relations = []
    smooth_numbers = []
    
    # Try different x values
    # Use q(x) = (sqrt_n + x)^2 - n for small values
    x_start = 0
    x_end = M
    
    print(f"  Sieving from x = {x_start} to {x_end}...")
    
    for x_offset in range(x_start, x_end):
        x = sqrt_n + x_offset
        q_x = x * x - n
        
        # Trial division to check if q(x) is smooth
        factors = {}
        temp = abs(q_x)
        
        for p in fb:
            count = 0
            while temp % p == 0:
                temp //= p
                count += 1
            if count > 0:
                factors[p] = count
        
        # Handle sign
        if q_x < 0:
            factors[-1] = 1
        
        # If q(x) is smooth (factors completely over factor base)
        if temp == 1:
            smooth_numbers.append(x)
            relations.append(factors)
            
            if len(relations) >= len(fb) + 5:  # Need more relations than primes
                break
    
    print(f"  Found {len(relations)} smooth relations")
    
    if len(relations) < len(fb):
        # Increase bounds and try again
        print(f"  Not enough relations, increasing bounds...")
        return quadratic_sieve(n, smooth_bound * 2, M * 2)
    
    # Linear algebra: find linear dependencies over GF(2)
    # Build matrix for exponent parity
    has_negative = any(-1 in r for r in relations)
    matrix_size = len(fb) + (1 if has_negative else 0)
    
    # Build matrix
    matrix = []
    for rel in relations:
        row = [0] * matrix_size
        for p, exp in rel.items():
            if p == -1:
                if has_negative:
                    row[-1] = exp % 2
            else:
                idx = fb.index(p)
                row[idx] = exp % 2
        matrix.append(row)
    
    # Gaussian elimination over GF(2) to find dependencies
    dependencies = gaussian_elimination_gf2(matrix)
    
    # Try each dependency to find factors
    for dep in dependencies:
        if not dep or not any(dep):
            continue
            
        x_prod = 1
        y_prod = 1
        
        for i, use in enumerate(dep):
            if use and i < len(smooth_numbers):
                x = smooth_numbers[i]
                x_prod = (x_prod * x) % n
                
                # Reconstruct y from factors (square root of product)
                y = 1
                for p, exp in relations[i].items():
                    if p == -1:
                        continue
                    y = (y * pow(p, exp // 2, n)) % n
                y_prod = (y_prod * y) % n
        
        # Check if we found a non-trivial factor
        diff = (x_prod - y_prod) % n
        gcd_val = math.gcd(diff, n)
        
        if 1 < gcd_val < n:
            p = gcd_val
            q = n // p
            return (p, q) if p < q else (q, p)
        
        # Also try x_prod + y_prod
        diff2 = (x_prod + y_prod) % n
        gcd_val2 = math.gcd(diff2, n)
        
        if 1 < gcd_val2 < n:
            p = gcd_val2
            q = n // p
            return (p, q) if p < q else (q, p)
    
    # If no factor found, try with larger bounds
    print(f"  No factor found, increasing bounds...")
    return quadratic_sieve(n, smooth_bound * 2, M * 2)


def gaussian_elimination_gf2(matrix: List[List[int]]) -> List[List[bool]]:
    """
    Gaussian elimination over GF(2) to find linear dependencies
    Returns list of dependency vectors indicating which original rows sum to zero
    """
    if not matrix:
        return []
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Create augmented matrix with identity to track row operations
    # Each row tracks which original rows contribute to it
    augmented = []
    for i in range(rows):
        row = [x % 2 for x in matrix[i]]
        # Add identity part to track dependencies
        identity_row = [0] * rows
        identity_row[i] = 1
        augmented.append(row + identity_row)
    
    # Forward elimination
    pivot_row = 0
    
    for col in range(cols):
        # Find pivot
        pivot = -1
        for row in range(pivot_row, rows):
            if augmented[row][col] == 1:
                pivot = row
                break
        
        if pivot == -1:
            continue
        
        # Swap rows
        if pivot != pivot_row:
            augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        
        # Eliminate
        for row in range(rows):
            if row != pivot_row and augmented[row][col] == 1:
                for c in range(len(augmented[0])):
                    augmented[row][c] = (augmented[row][c] + augmented[pivot_row][c]) % 2
        
        pivot_row += 1
        if pivot_row >= rows:
            break
    
    # Find dependencies: rows that are all zeros in the matrix part
    dependencies = []
    for row in range(rows):
        # Check if matrix part (first cols elements) is all zeros
        is_zero = True
        for col in range(cols):
            if augmented[row][col] != 0:
                is_zero = False
                break
        
        if is_zero:
            # The identity part (last rows elements) shows the dependency
            dep = [augmented[row][cols + i] == 1 for i in range(rows)]
            if any(dep):  # Only add non-trivial dependencies
                dependencies.append(dep)
    
    return dependencies


def measure_rsa_performance(keys: Dict, message: int, repetitions: int = 1000) -> Dict:
    """
    Measure RSA encryption and decryption performance
    """
    results = {}
    
    for key_name, key_data in keys.items():
        p = key_data['p']
        q = key_data['q']
        N = key_data['N']
        e = key_data['e']
        
        # Calculate private key
        d = calculate_private_key(p, q, e)
        
        # Ensure message is valid (less than N)
        msg = message % N
        
        # Measure encryption
        start = time.perf_counter()
        for _ in range(repetitions):
            cipher = rsa_encrypt(msg, e, N)
        encrypt_time = (time.perf_counter() - start) / repetitions
        
        # Measure decryption
        start = time.perf_counter()
        for _ in range(repetitions):
            decrypted = rsa_decrypt(cipher, d, N)
        decrypt_time = (time.perf_counter() - start) / repetitions
        
        # Verify correctness
        assert decrypted == msg, f"Decryption failed for {key_name}"
        
        results[key_name] = {
            'd': d,
            'encrypt_time': encrypt_time,
            'decrypt_time': decrypt_time,
            'N_bits': N.bit_length()
        }
        
        print(f"{key_name}: d = {d}")
        print(f"  Encryption: {encrypt_time*1e6:.4f} us")
        print(f"  Decryption: {decrypt_time*1e6:.4f} us")
    
    return results


def measure_factorization_performance(keys: Dict) -> Dict:
    """
    Measure Quadratic Sieve factorization performance
    """
    results = {}
    
    for key_name, key_data in keys.items():
        N = key_data['N']
        p_expected = key_data['p']
        q_expected = key_data['q']
        
        print(f"\nFactoring {key_name} (N = {N})...")
        start = time.perf_counter()
        
        p_found, q_found = quadratic_sieve(N)
        
        factor_time = time.perf_counter() - start
        
        # Verify
        assert p_found * q_found == N, "Factorization verification failed"
        assert {p_found, q_found} == {p_expected, q_expected}, f"Recovered primes don't match: got {p_found}, {q_found}, expected {p_expected}, {q_expected}"
        
        results[key_name] = {
            'p': p_found,
            'q': q_found,
            'factor_time': factor_time,
            'N_bits': N.bit_length()
        }
        
        print(f"  [OK] Found factors: p = {p_found}, q = {q_found}")
        print(f"  [OK] Time: {factor_time:.4f} seconds")
    
    return results


def main():
    """
    Main function to run all experiments
    """
    print("=" * 60)
    print("RSA Cryptography Project")
    print("=" * 60)
    
    # Use a fixed message for all keys (must be less than smallest N)
    message = 12345
    
    print("\n" + "=" * 60)
    print("PART 1: RSA Encryption/Decryption Performance")
    print("=" * 60)
    
    rsa_results = measure_rsa_performance(RSA_KEYS, message, repetitions=1000)
    
    print("\n" + "=" * 60)
    print("PART 2: Quadratic Sieve Factorization")
    print("=" * 60)
    
    factor_results = measure_factorization_performance(RSA_KEYS)
    
    # Print summary table
    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print(f"{'Key':<8} {'N (bits)':<12} {'Encrypt (μs)':<15} {'Decrypt (μs)':<15} {'Factor (s)':<15}")
    print("-" * 60)
    for key_name in RSA_KEYS.keys():
        rsa = rsa_results[key_name]
        fact = factor_results[key_name]
        print(f"{key_name:<8} {rsa['N_bits']:<12} {rsa['encrypt_time']*1e6:<15.4f} "
              f"{rsa['decrypt_time']*1e6:<15.4f} {fact['factor_time']:<15.4f}")
    
    # Extrapolation to 2048-bit
    print("\n" + "=" * 60)
    print("EXTRAPOLATION TO 2048-BIT RSA")
    print("=" * 60)
    
    # Collect data points
    bits = [rsa_results[k]['N_bits'] for k in RSA_KEYS.keys()]
    times = [factor_results[k]['factor_time'] for k in RSA_KEYS.keys()]
    
    # Fit exponential curve (factorization time grows exponentially with bit size)
    # Using least squares fit: log(time) = a * bits + b
    try:
        log_times = [math.log(t) for t in times]
        coeffs = np.polyfit(bits, log_times, 1)
        a, b = coeffs
        
        # Estimate for 2048 bits
        estimated_log_time = a * 2048 + b
        estimated_time_seconds = math.exp(estimated_log_time)
        estimated_time_years = estimated_time_seconds / (365.25 * 24 * 3600)
        
        print(f"Fitted curve: log(time) = {a:.6f} * bits + {b:.6f}")
        print(f"Estimated factorization time for 2048-bit RSA:")
        print(f"  {estimated_time_seconds:.2e} seconds")
        print(f"  {estimated_time_years:.2e} years")
    except:
        # Fallback calculation without numpy
        print("Note: numpy required for curve fitting. Install with: pip install numpy")
    
    return rsa_results, factor_results


if __name__ == "__main__":
    rsa_results, factor_results = main()

