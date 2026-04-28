import csv
import math
import random
from collections import Counter

def euclidean(p1, p2):
    return math.sqrt(sum((p1[i] - p2[i])**2 for i in range(len(p1))))

def manhattan(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))

def get_min_max(data, n):
    if not data: return [], []
    mins = [min(row[i] for row in data) for i in range(n)]
    maxs = [max(row[i] for row in data) for i in range(n)]
    return mins, maxs

def get_zscore_params(data, n):
    if not data: return [], []
    means = [sum(row[i] for row in data)/len(data) for i in range(n)]
    stds = [math.sqrt(sum((row[i]-means[i])**2 for row in data)/len(data)) for i in range(n)]
    return means, stds

def read_csv(file):
    data = []
    header = []
    try:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            try:
                header = next(reader) # Capture header
            except StopIteration:
                pass

            for r in reader:
                if not r: continue
                try:
                    # Convert features to float, keep class as string/int
                    # Assuming last column is class
                    row = [float(x) for x in r[:-1]] + [int(float(r[-1]))] 
                    data.append(row)
                except ValueError:
                    continue
        return data, header
    except FileNotFoundError:
        print(f"File '{file}' not found.")
        return [], []

def balance_and_sample(data, sample_size):
    # Separate data by class
    class_0 = [row for row in data if row[-1] == 0]
    class_1 = [row for row in data if row[-1] == 1]
    
    print(f"\nTotal available records -> Class 0: {len(class_0)}, Class 1: {len(class_1)}")
    
    # Calculate target per class
    target_per_class = sample_size // 2
    
    # valid_sample_size ensures we don't ask for more than we have
    max_possible = min(len(class_0), len(class_1)) * 2
    
    if sample_size > max_possible:
        print(f"Warning: Not enough data to balance {sample_size} records.")
        print(f"Reducing sample size to max possible balanced dataset: {max_possible}")
        target_per_class = max_possible // 2
        
    sampled_0 = random.sample(class_0, target_per_class)
    sampled_1 = random.sample(class_1, target_per_class)
    
    balanced_data = sampled_0 + sampled_1
    random.shuffle(balanced_data)
    
    return balanced_data

def main():
    file = "loan_default.csv"
    raw_data, header = read_csv(file)

    if not raw_data:
        print("No data loaded. Exiting.")
        return

    # Assuming last column is class, previous are features
    total_features = len(raw_data[0]) - 1
    
    # Handle headers
    if not header:
        feature_names = [f"Feat{i+1}" for i in range(total_features)]
    else:
        feature_names = header[:-1]

    print(f"Total features detected: {total_features}")
    
    # --- 1. Ask for features to use ---
    try:
        n_input = input(f"Enter number of features to use (Default {total_features}): ")
        n = int(n_input) if n_input.strip() else total_features
    except ValueError:
        n = total_features

    current_feature_names = feature_names[:n]

    # --- 2. Dynamic Balanced Sampling ---
    try:
        sample_input = input(f"Enter total sample size to load (e.g. 150): ")
        sample_size = int(sample_input) if sample_input.strip() else 150
    except ValueError:
        sample_size = 150

    raw_data = balance_and_sample(raw_data, sample_size)
    
    # Check if we actually have data after sampling
    if not raw_data:
        print("Error: Dataset empty after sampling.")
        return

    # Verify split
    counts = Counter(row[-1] for row in raw_data)
    print(f"Final Balanced Dataset: {len(raw_data)} records (Class 0: {counts[0]}, Class 1: {counts[1]})")

    # Calculate stats on the balanced dataset
    mins, maxs = get_min_max(raw_data, n)
    means, stds = get_zscore_params(raw_data, n)

    while True:
        print("\n" + "="*80)
        print(f"Features: {current_feature_names}")
        print(f"Enter unknown point ({n} values separated by space):")

        try:
            user_in = input()
            if not user_in.strip(): break 
            unknown_raw = list(map(float, user_in.split()))
            if len(unknown_raw) != n:
                print(f"Error: Expected {n} values.")
                continue
        except ValueError:
            print("Invalid input.")
            continue

        dist_choice = input("Select Distance Metric (1: Euclidean, 2: Manhattan) [Default 1]: ")
        dist_func = manhattan if dist_choice == '2' else euclidean

        norm_input = input("Select Normalization (1: Min-Max, 2: Z-Score, 3: None) [Default 1]: ")
        norm_type = norm_input if norm_input in ['1', '2', '3'] else '1'

        processed_table = []
        
        # --- Normalization Logic ---
        
        # 1. Normalize Unknown Point
        norm_unknown = []
        if norm_type == '1':
            norm_unknown = [(unknown_raw[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i in range(n)]
        elif norm_type == '2':
            norm_unknown = [(unknown_raw[i] - means[i]) / (stds[i] + 1e-9) for i in range(n)]
        else:
            norm_unknown = list(unknown_raw)

        # 2. Normalize Dataset and Calculate Distance
        for row in raw_data:
            orig_feat = row[:n] # Slice to used features
            row_class = row[-1]
            
            norm_feat = []
            if norm_type == '1':
                norm_feat = [(row[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i in range(n)]
            elif norm_type == '2':
                norm_feat = [(row[i] - means[i]) / (stds[i] + 1e-9) for i in range(n)]
            else:
                norm_feat = orig_feat

            distance = dist_func(norm_feat, norm_unknown)

            processed_table.append({
                'orig': [round(x, 2) for x in orig_feat],
                'norm': [round(x, 4) for x in norm_feat],
                'dist': distance,
                'class': row_class
            })

        # --- Sort by Distance ---
        processed_table.sort(key=lambda x: x['dist'])

        try:
            k_input = input(f"\nEnter value of k (Total records {len(processed_table)}): ")
            k = int(k_input)
        except ValueError:
            print("Invalid k, defaulting to 3")
            k = 3

        print("\n--- NEAREST NEIGHBORS ---")
        print(f"{'Rank':<5} | {'Class':<6} | {'Distance':<10} | {'Original Values'}")
        print("-" * 60)

        for i in range(min(k, len(processed_table))):
            item = processed_table[i]
            print(f"{i+1:<5} | {item['class']:<6} | {item['dist']:.4f}     | {item['orig']}")

        neighbors = processed_table[:k]

        # --- Prediction ---
        mode = input("\nWeighted or Unweighted (W/U) [Default U]: ").upper()
        
        prediction = None
        if mode == 'W':
            weights = {0: 0.0, 1: 0.0}
            for nbr in neighbors:
                # Add small epsilon to avoid division by zero
                w = 1 / (nbr['dist'] + 1e-5) 
                c = nbr['class']
                if c in weights:
                    weights[c] += w
                else:
                    weights[c] = w # Handle if class isn't 0/1 exactly
            
            print("Weighted scores:", {k: round(v, 4) for k,v in weights.items()})
            prediction = max(weights, key=weights.get)
        else:
            # Unweighted
            votes = Counter([nbr['class'] for nbr in neighbors])
            print("Votes:", dict(votes))
            prediction = votes.most_common(1)[0][0]

        print(f"\n>>> FINAL PREDICTION: Class {prediction}")

        if input("\nProcess another point? (Y/N): ").upper() != 'Y':
            break

if __name__ == "__main__":
    main()
