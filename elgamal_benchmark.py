from charm.toolbox.eccurve import prime256v1, secp256k1, secp384r1, secp521r1, sect233r1
from charm.toolbox.eccurve import *
from charm.toolbox.ecgroup import ECGroup
from charm.schemes.pkenc.pkenc_elgamal85 import ElGamal
import time, os

REPEAT = 10000
TO_MICRO = 1000000

def random_message(curve_group) -> bytes:
    return b'\x00'+ os.urandom(curve_group.bitsize() - 1)
  
    
def benchmark(curve):
    group = ECGroup(curve)
    elgamal = ElGamal(group)
    public, private = elgamal.keygen()
    encryption_times = []
    decryption_times = []

    for i in range(REPEAT):
        message = random_message(group)
        start = time.process_time()
        cipher = elgamal.encrypt(public, message)
        encryption_times.append(time.process_time() - start)
        start = time.process_time()
        decrypted = elgamal.decrypt(public, private, cipher)
        decryption_times.append(time.process_time() - start)
   
    return {
        "curve" : curve,
        "enc_min": min(encryption_times),
        "enc_max": max(encryption_times),
        "enc_avg": sum(encryption_times) / len(encryption_times),
        "dec_min": min(decryption_times),
        "dec_max": max(decryption_times),
        "dec_avg": sum(decryption_times) / len(decryption_times),
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
        sect233r1:  "sect233r1",
    }

    results = []

    print(f"Starting benchmark of elgamal encryption and decryption scheme with {REPEAT} operations per test\n" + 100 * "-")
    
    for curve in curves:
        print(f"Benchmarking '{curve_names[curve]}'...")
        results.append(benchmark(curve))

    print("\n" + "="*85)
    print("Encryption cost benchmark")
    print("-" * 85)
    print(f"{'Curve Name':<15} | {'Min CPU (µs)':<15} | {'Max CPU (µs)':<15} | {'Average CPU (µs)':<15}")
    print("-" * 85)
    for res in results:
        print(f"{curve_names[res['curve']]:<15} | {(res['enc_min'] * TO_MICRO):<15.2f} | {(res['enc_max'] * TO_MICRO):<15.2f} | {(res['enc_avg'] * TO_MICRO):<15.2f}")
    print("-" * 85)

    print("\n" + "="*85)
    print("Decryption cost benchmark")
    print("-" * 85)
    print(f"{'Curve Name':<15} | {'Min CPU (µs)':<15} | {'Max CPU (µs)':<15} | {'Average CPU (µs)':<15}")
    for res in results:
        print(f"{curve_names[res['curve']]:<15} | {(res['dec_min'] * TO_MICRO):<15.2f} | {(res['dec_max'] * TO_MICRO):<15.2f} | {(res['dec_avg'] * TO_MICRO):<15.2f}")
    print("-" * 85)

if __name__ == '__main__':
    main()