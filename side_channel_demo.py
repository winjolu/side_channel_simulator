import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# simulated AES encryption powewr traces
def simulate_traces(num_traces=50, key_byte=0x5a):
    traces = []
    plaintexts = []
    for _ in range(num_traces): 
        plaintext = np.random.randint(0, 256)  # random plaintext byte
        intermediate = plaintext ^ key_byte  #  XOR of random plaintext byte and key byte to simulate AES encryption
        hamming_weight = bin(intermediate).count("1")  # hamming weight of intermediate value (how many 1s in the binary representation)
        noise = np.random.normal(0, 0.5, 10) # gaussian noise
        trace = hamming_weight + noise  # simulate power trace
        traces.append(trace) # append power trace
        plaintexts.append(plaintext) # append plaintext byte
    return np.array(traces), np.array(plaintexts) # return power traces and plaintext bytes

# perform correlation power analysis (CPA)
def perform_cpa(traces, plaintexts):
    correlations = []
    for guess in range(256): # iterate over all possible key byte guesses
        hypothesis = [bin(pt ^ guess).count("1") for pt in plaintexts] # calculate hamming weight hypothesis for each plaintext byte
        correlation = pearsonr(hypothesis, traces.mean(axis=1))[0] # calculate correlation coefficient between hypothesis and power traces
        correlations.append(correlation) # append correlation coefficient
    return correlations

# spin up the simulation
def main():
    num_traces = 100 
    true_key_byte = 0x9f
    print(f"Simulating {num_traces} power traces for AES encryption...") 

    # simulate power traces and plaintexts
    traces, plaintexts = simulate_traces(num_traces, true_key_byte)

    # perform CPA attack
    correlations = perform_cpa(traces, plaintexts)
    recovered_key_byte = np.argmax(correlations) # find key byte with highest correlation coefficient
    
    # Print the exact values of points of interest with the guess number
    print(f"True Key Byte: Guess {true_key_byte}")
    print(f"Recovered Key Byte: Guess {recovered_key_byte}, Correlation (y): {correlations[recovered_key_byte]}\n")
    print(f"\nCorrelations for each key guess: {correlations}")
    assert recovered_key_byte == true_key_byte, "Recovered key does not match the true key!"

# print(plt.style.available)


    # plot the results
    plt.style.use('classic')
    plt.plot(correlations, label="Correlation per Key Guess", color='blue', linewidth=2)  
    plt.axvline(true_key_byte - 0.5, color="orange", linestyle="--", linewidth=2, label="True Key Byte")  
    plt.axvline(recovered_key_byte + 0.5, color="purple", linestyle="-.", linewidth=2, label="Recovered Key Byte")
    plt.xlabel("Key Guess")
    plt.ylabel("Correlation Coefficient")
    plt.legend()
    plt.title("Correlation Power Analysis (CPA) Attack Results")
    plt.show()

# run the simulation
if __name__ == "__main__":
    main() 



        