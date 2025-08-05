from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import prime256v1, secp256k1, secp384r1, secp521r1, sect233r1
from charm.core.math.elliptic_curve import ZR, G 
import time

# ECC curves:
# prime256v1  - 128-bit sec, prime field, general use (NIST P-256)
# secp256k1   - 128-bit sec, prime field, used in Bitcoin/Ethereum
# secp384r1   - 192-bit sec, prime field, stronger TLS/government use
# secp521r1   - 256-bit sec, prime field, high-security niche use
# sect233r1   - 112-bit sec, binary field, used in embedded/hardware

REPEAT = 10000
TO_MICRO = 1000000

def benchmark(curve):
    group = ECGroup(curve)

    tuples = [(group.random(G), group.random(G), group.random(G), group.random(ZR)) for _ in range(REPEAT)]
    a, b, x, y = zip(*tuples)
    add_times = []
    mul_times = []

    for i in range(REPEAT):
        start = time.process_time()
        _ = a[i] * b[i]
        add_times.append(time.process_time() - start)

    for i in range(REPEAT):
        start = time.process_time()
        _ = x[i] ** y[i]
        mul_times.append(time.process_time() - start)

    return {
        "curve" : curve,
        "add_min": min(add_times),
        "add_max": max(add_times),
        "add_avg": sum(add_times) / len(add_times),
        "mul_min": min(mul_times),
        "mul_max": max(mul_times),
        "mul_avg": sum(mul_times) / len(mul_times),
    }

def main():
    curves = [
        prime256v1, secp256k1, secp384r1, secp521r1, sect233r1
    ]

    curve_names = {
        prime256v1: "prime256v1",
        secp256k1:  "secp256k1",
        secp384r1:  "secp384r1",
        secp521r1:  "secp521r1",
        sect233r1:  "sect233r1"
    }

    
    results = []
    
    print(f"Starting benchmark of operations over elliptic curves {REPEAT} operations per test\n" + 100 * "-")

    for curve in curves:
        print(f"Benchmarking '{curve_names[curve]}'...")
        results.append(benchmark(curve))

    print("\n" + "="*85)
    print("Benchmarking cost of point addition")
    print("="*85)
    print(f"{'Curve Name':<15} | {'Min CPU (µs)':<15} | {'Max CPU (µs)':<15} | {'Average CPU (µs)':<15}")
    print("-" * 85)
    for res in results:
        print(f"{curve_names[res['curve']]:<15} | {(res['add_min'] * TO_MICRO):<15.2f} | {(res['add_max'] * TO_MICRO):<15.2f} | {(res['add_avg'] * TO_MICRO):<15.2f}")
    print("-" * 85)

    print("\n" + "="*85)
    print("Benchmarking cost of scalar multiplication")
    print("="*85)
    print(f"{'Curve Name':<15} | {'Min CPU (µs)':<15} | {'Max CPU (µs)':<15} | {'Average CPU (µs)':<15}")
    print("-" * 85)
    for res in results:
        print(f"{curve_names[res['curve']]:<15} | {(res['mul_min'] * TO_MICRO):<15.2f} | {(res['mul_max'] * TO_MICRO):<15.2f} | {(res['mul_avg'] * TO_MICRO):<15.2f}")
    print("-" * 85)


if __name__ == "__main__":
    main()


