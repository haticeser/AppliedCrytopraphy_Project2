"""
Create visualization plots for the RSA project
"""
import matplotlib.pyplot as plt
import math
from rsa_project import RSA_KEYS, measure_rsa_performance, measure_factorization_performance

# Run experiments
message = 12345
rsa_results = measure_rsa_performance(RSA_KEYS, message, repetitions=1000)
factor_results = measure_factorization_performance(RSA_KEYS)

# Extract data
keys = list(RSA_KEYS.keys())
bits = [rsa_results[k]['N_bits'] for k in keys]
encrypt_times = [rsa_results[k]['encrypt_time'] * 1e6 for k in keys]  # Convert to μs
decrypt_times = [rsa_results[k]['decrypt_time'] * 1e6 for k in keys]  # Convert to μs
factor_times = [factor_results[k]['factor_time'] for k in keys]  # Keep in seconds

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('RSA Performance Analysis', fontsize=16, fontweight='bold')

# Plot 1: Encryption vs Decryption Time
ax1 = axes[0, 0]
x_pos = range(len(keys))
width = 0.35
ax1.bar([x - width/2 for x in x_pos], encrypt_times, width, label='Encryption', alpha=0.8)
ax1.bar([x + width/2 for x in x_pos], decrypt_times, width, label='Decryption', alpha=0.8)
ax1.set_xlabel('RSA Key')
ax1.set_ylabel('Time (μs)')
ax1.set_title('Encryption vs Decryption Performance')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(keys)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Factorization Time vs Bit Size
ax2 = axes[0, 1]
ax2.plot(bits, factor_times, 'o-', linewidth=2, markersize=8, color='red')
ax2.set_xlabel('N (bits)')
ax2.set_ylabel('Factorization Time (seconds)')
ax2.set_title('Quadratic Sieve Factorization Time')
ax2.grid(True, alpha=0.3)
for i, key in enumerate(keys):
    ax2.annotate(key, (bits[i], factor_times[i]), 
                textcoords="offset points", xytext=(0,10), ha='center')

# Plot 3: Log-scale Factorization Time
ax3 = axes[1, 0]
log_times = [math.log(t) for t in factor_times]
ax3.plot(bits, log_times, 's-', linewidth=2, markersize=8, color='green')
ax3.set_xlabel('N (bits)')
ax3.set_ylabel('log(Factorization Time)')
ax3.set_title('Exponential Growth of Factorization Time (log scale)')
ax3.grid(True, alpha=0.3)

# Fit line for extrapolation
import numpy as np
coeffs = np.polyfit(bits, log_times, 1)
fit_line = np.polyval(coeffs, bits)
ax3.plot(bits, fit_line, '--', alpha=0.7, label=f'Fit: log(t) = {coeffs[0]:.4f}*bits + {coeffs[1]:.4f}')
ax3.legend()

# Extrapolate to 2048 bits
bits_extended = bits + [2048]
estimated_log_time = coeffs[0] * 2048 + coeffs[1]
estimated_time = math.exp(estimated_log_time)
log_times_extended = log_times + [estimated_log_time]
ax3.plot([bits[-1], 2048], [log_times[-1], estimated_log_time], 'r--', alpha=0.5, linewidth=2)
ax3.plot(2048, estimated_log_time, 'ro', markersize=10, label='2048-bit estimate')
ax3.legend()

# Plot 4: Comparison Table (text)
ax4 = axes[1, 1]
ax4.axis('off')
table_data = []
for i, key in enumerate(keys):
    table_data.append([
        key,
        f"{bits[i]}",
        f"{encrypt_times[i]:.2f} μs",
        f"{decrypt_times[i]:.2f} μs",
        f"{factor_times[i]:.4f} s"
    ])

table = ax4.table(cellText=table_data,
                  colLabels=['Key', 'Bits', 'Encrypt', 'Decrypt', 'Factor'],
                  cellLoc='center',
                  loc='center',
                  bbox=[0, 0, 1, 1])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)
ax4.set_title('Summary Table', pad=20)

plt.tight_layout()
plt.savefig('C:\\Users\\eserh\\rsa_performance_plots.png', dpi=300, bbox_inches='tight')
print("Plots saved to rsa_performance_plots.png")
plt.show()

