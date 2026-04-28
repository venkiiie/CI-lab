import csv
import math
import random
from collections import Counter

def euclidean(p1, p2):
    return math.sqrt(sum((p1[i] - p2[i])**2 for i in range(len(p1))))

def manhattan(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))

def get_min_max(data, n):
    mins = [min(row[i] for row in data) for i in range(n)]
    maxs = [max(row[i] for row in data) for i in range(n)]
    return mins, maxs

def get_zscore_params(data, n):
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
                # Capture the header row
                header = next(reader)
            except StopIteration:
                pass

            for r in reader:
                if not r: continue
                try:
                    # Convert features to float, keep class as is
                    row = [float(x) for x in r[:-1]] + [r[-1]]
                    data.append(row)
                except ValueError:
                    continue
                    
        return data, header
    except FileNotFoundError:
        print("File not found.")
        exit()

def main():
    file = "loan_default.csv"
    raw_data, header = read_csv(file)

    if not raw_data:
        print("No data found.")
        return

    total_features = len(raw_data[0]) - 1
    # If header exists, use it. Otherwise create generic names.
    if not header:
        feature_names = [f"Feat{i+1}" for i in range(total_features)]
    else:
        feature_names = header[:-1] # Exclude class label column

    print(f"Total features detected: {total_features}")
    
    try:
        n_input = input(f"Enter number of features to use (Default {total_features}): ")
        n = int(n_input) if n_input else total_features
    except ValueError:
        n = total_features

    # Truncate feature names list to matches selected number of features
    current_feature_names = feature_names[:n]

    if len(raw_data) >= 250:
        raw_data = random.sample(raw_data, 150)
        print("Dataset sampled to 150 records.")

    mins, maxs = get_min_max(raw_data, n)
    means, stds = get_zscore_params(raw_data, n)

    while True:
        print("\n" + "="*80)
        # --- PRINT FEATURES NAME BEFORE ASKING ---
        print(f"Features: {current_feature_names}")
        print(f"Enter unknown point ({n} values separated by space):")
        
        try:
            unknown_raw = list(map(float, input().split()))
            if len(unknown_raw) != n:
                print(f"Error: Expected {n} values.")
                continue
        except ValueError:
            print("Invalid input.")
            continue

        dist_choice = input("Select Distance Metric (1: Euclidean, 2: Manhattan): ")
        dist_func = euclidean if dist_choice == '2' else euclidean

        norm_input = input("Select Normalization (1: Min-Max, 2: Z-Score, 3: None) [Default 1]: ")
        norm_type = norm_input if norm_input in ['1', '2', '3'] else '1'

        processed_table = []
        norm_unknown = []

        # Normalize Unknown Point
        if norm_type == '1':
            norm_unknown = [(unknown_raw[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9) for i in range(n)]
        elif norm_type == '2':
            norm_unknown = [(unknown_raw[i] - means[i]) / (stds[i] + 1e-9) for i in range(n)]
        else:
            norm_unknown = unknown_raw

        # Normalize Dataset
        for row in raw_data:
            orig_feat = row[:n]
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
                'class': row[-1]
            })

        print("\n--- DATASET DETAILS ---")
        # Print feature names above table
        print(f"Features: {current_feature_names}")
        print(f"{'Original Values':<50} | {'Normalized':<50} | {'Distance'}")
        print("-" * 120)
        
        for item in processed_table:
            orig_str = str(item['orig'])
            norm_str = str(item['norm'])
            print(f"{orig_str:<50} | {norm_str:<50} | {item['dist']:.4f}")

        try:
            k = int(input("\nEnter value of k: "))
        except ValueError:
            print("Invalid k")
            continue

        v = Counter([i['class'] for i in processed_table])
        print("Total Positive and Negative votes in DataSet:", dict(v))
        
        processed_table.sort(key=lambda x: x['dist'])

        print("\n--- RANKING & K-NEIGHBOR CHECK ---")
        print(f"Features: {current_feature_names}")
        print(f"{'Original Values':<50} | {'Distance':<10} | {'Rank':<6} | {'Class':<15} | {'Is Near K?'}")
        print("-" * 100)
        
        for i, item in enumerate(processed_table, 1):
            is_near = "YES" if i <= k else "NO"
            print(f"{str(item['orig']):<50} | {item['dist']:.4f}     | {i:<6} | {item['class']:<15} | {is_near}")
            if i == k: 
                print("...")
                break

        mode = input("\nWeighted or Unweighted (W/U): ").upper()
        neighbors = processed_table[:k]

        print("\n--- VOTING & PREDICTION ---")
        prediction = None
        if mode == 'U':
            votes = Counter([nbr['class'] for nbr in neighbors])
            print("Unweighted votes:", dict(votes))
            prediction = votes.most_common(1)[0][0]
        else:
            weights = {}
            for nbr in neighbors:
                w = 1 / (nbr['dist'] + 1e-5)
                cls_key = str(nbr['class'])
                weights[cls_key] = weights.get(cls_key, 0) + w
            
            print("Weighted values:")
            for c, val in weights.items(): 
                print(f" Class {c}: {val:.4f}")
            prediction = max(weights, key=weights.get)

        print(f"\nFINAL PREDICTED CLASS FOR {unknown_raw}: {prediction}")

        if input("\nProcess another point? (Y/N): ").upper() != 'Y': 
            break

if __name__ == "__main__":
    main()
