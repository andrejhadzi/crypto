#include <NTL/ZZ.h>
#include <NTL/ZZ_p.h>
#include <stdio.h>
#include <vector>
#include <chrono>
#include <algorithm>  
#include <numeric>    
#include <vector>    

#define REPEAT_TIMES 10000
using namespace NTL;
using namespace std;

bool find_generator(const ZZ& p, const ZZ& q, ZZ& g, long max_attempts = 1000) {
    ZZ exponent = (p - 1) / q;

    for (long attempt = 0; attempt < max_attempts; ++attempt) {
        ZZ h = RandomBnd(p);  
        if (h == 1 || h==0) continue;       
        PowerMod(g, h, exponent, p);
        if (g != 1) {
            return true;               
        }
    }
    return false;                  
}

bool generate_prime_order_group(ZZ& p, ZZ& q, ZZ& g, unsigned int modulus_bits, unsigned int order_bits, unsigned int max_attempts = 10000) {
    q = GenPrime_ZZ(order_bits);
    for (int attempt = 0; attempt < max_attempts; attempt++) {

        ZZ lower_bound = ZZ(1) << (modulus_bits - 1);
        ZZ rem;
        DivRem(lower_bound, rem, lower_bound, q);
        if (rem != 0) lower_bound++;

        unsigned int k_bits = modulus_bits - NumBits(q);
        if (k_bits <= 0) return false; 
        ZZ k = RandomLen_ZZ(k_bits);

        if (k < lower_bound)
            k = lower_bound + RandomLen_ZZ(k_bits / 2);

        p = k * q + 1;

        if (NumBits(p) != modulus_bits)
            continue;

        if (ProbPrime(p, 25)){
            if (find_generator(p, q, g)) return true;
            else return false;
        }
    }
    return false;
}

void generate_operands(ZZ& g, ZZ& p, ZZ& a, ZZ& b){
    PowerMod(a, g, RandomBnd(p-1)+1, p);
    PowerMod(b, g, RandomBnd(p-1)+1, p);
}

void benchmark_group(unsigned int order_bits, unsigned int modulus_bits){
    ZZ p, q, g, a, b, result;
    vector<double> mul_times, exp_times;

    if (generate_prime_order_group(p, q, g, modulus_bits, order_bits)) {
        cout << "Prime group generated order-" << order_bits << " modulus-" << modulus_bits << "\n";
        cout << "p (" << modulus_bits << " bits) = " << p << "\n";
        cout << "q (" << order_bits << " bits) = " << q << "\n";
        cout << "g = " << g << "\n\n";
        cout << "Benchmarking.....\n";
        for(int i = 0; i < REPEAT_TIMES; i++){
            generate_operands(g, p, a, b);
            auto start = chrono::high_resolution_clock::now();
            MulMod(result, a, b, p);    
            mul_times.push_back(chrono::duration<double, micro>(chrono::high_resolution_clock::now() - start).count());
            
            start = chrono::high_resolution_clock::now();
            PowerMod(result, a, b, p);    
            exp_times.push_back(chrono::duration<double, micro>(chrono::high_resolution_clock::now() - start).count());
        }

        double min_time = *min_element(mul_times.begin(), mul_times.end());
        double max_time = *max_element(mul_times.begin(), mul_times.end());
        double mean_time = accumulate(mul_times.begin(), mul_times.end(), 0.0) / mul_times.size();

        cout << "Min mul time:\t" << min_time << " us\n";
        cout << "Mean mul time:\t" << mean_time << " us\n";
        cout << "Max mul time:\t" << max_time << " us\n";

        min_time = *min_element(exp_times.begin(), exp_times.end());
        max_time = *max_element(exp_times.begin(), exp_times.end());
        mean_time = accumulate(exp_times.begin(), exp_times.end(), 0.0) / exp_times.size();

        cout << "Min exp time:\t" << min_time << " us\n";
        cout << "Mean exp time\t: " << mean_time << " us\n";
        cout << "Max exp time\t: " << max_time << " us\n";
        cout << "-----------------------------------------------------------------------------------------------------------\n";
    
    } else {
        cout << "Failed to generate prime p after max attempts\n";
    }
}

int main() {
    benchmark_group(160, 1024);
    benchmark_group(192, 2048);
    benchmark_group(256, 2048);
    benchmark_group(256, 4096);
    return 0;
}
