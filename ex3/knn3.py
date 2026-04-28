import math
import random

# ----------------- HELPER FUNCTIONS -----------------

def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[i])**2
    return math.sqrt(distance)

def manhattan_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += abs(row1[i] - row2[i])
    return distance

def get_neighbors(training_set, test_row, k, metric_type):
    distances = []
    for train_row in training_set:
        features = train_row[:-1] # Exclude label
        label = train_row[-1]
        
        if metric_type == 1:
            dist = euclidean_distance(test_row, features)
        else:
            dist = manhattan_distance(test_row, features)
            
        distances.append((train_row, dist))
        
    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[1])
    
    neighbors = []
    for i in range(k):
        neighbors.append(distances[i])
        
    return distances, neighbors # Return all distances for ranking display, and just k for voting

def predict_classification(neighbors, weighted):
    class_votes = {}
    weighted_votes = {}
    
    for neighbor, dist in neighbors:
        label = neighbor[-1]
        
        # Simple counting
        class_votes[label] = class_votes.get(label, 0) + 1
        
        # Weighted voting (1 / distance^2), avoid division by zero
        weight = 1.0 / (dist**2 + 0.000001)
        weighted_votes[label] = weighted_votes.get(label, 0) + weight

    if weighted:
        print("\n--- VOTING & PREDICTION ---")
        print("Weighted values:")
        for cls in weighted_votes:
            print(f" Class {cls}: {weighted_votes[cls]:.4f}")
        return max(weighted_votes, key=weighted_votes.get)
    else:
        print("\n--- VOTING & PREDICTION ---")
        print("Votes per class:", class_votes)
        return max(class_votes, key=class_votes.get)

def normalize_dataset(dataset):
    minmax = []
    for i in range(len(dataset[0])):
        col_values = [row[i] for row in dataset]
        value_min = min(col_values)
        value_max = max(col_values)
        minmax.append([value_min, value_max])
        
    normalized_data = []
    for row in dataset:
        norm_row = []
        for i in range(len(row)):
            numer = row[i] - minmax[i][0]
            denom = minmax[i][1] - minmax[i][0]
            if denom == 0:
                norm_row.append(0.0)
            else:
                norm_row.append(numer / denom)
        normalized_data.append(norm_row)
        
    return normalized_data, minmax

def normalize_point(point, minmax):
    norm_point = []
    for i in range(len(point)):
        numer = point[i] - minmax[i][0]
        denom = minmax[i][1] - minmax[i][0]
        if denom == 0:
            norm_point.append(0.0)
        else:
            norm_point.append(numer / denom)
    return norm_point

# ----------------- MAIN EXECUTION -----------------

def main():
    filename = "loan_default.csv"
    
    try:
        with open(filename, 'r') as f:
            lines = f.read().strip().split('\n')
    except:
        print("File not found. Please ensure 'sample.txt' exists.")
        return

    headers = lines[0].split(',')
    raw_data = []
    for line in lines[1:]:
        parts = line.split(',')
        # Convert features to float, keep label as string/int
        # Assuming last column is Class (0 or 1)
        row = [float(x) for x in parts]
        # Convert label to int explicitly for cleaner output
        row[-1] = int(row[-1]) 
        raw_data.append(row)

    print(f"Total features detected: {len(headers)-1}")
    
    # User inputs for Feature Selection
    try:
        num_features = int(input(f"Enter number of features to use (Default {len(headers)-1}): ") or (len(headers)-1))
    except:
        num_features = len(headers)-1

    # ---------------- BALANCED SAMPLING LOGIC ----------------
    # Separate data by class
    class_0 = [row for row in raw_data if row[-1] == 0]
    class_1 = [row for row in raw_data if row[-1] == 1]
    
    total_records = len(raw_data)
    # Default sample size or user input
    sample_size = 15 
    
    if total_records > sample_size:
        # Determine split to ensure representation
        half_n = sample_size // 2
        
        # Sample safely (if one class is smaller than half_n, take all of it)
        sample_0 = random.sample(class_0, min(len(class_0), half_n))
        sample_1 = random.sample(class_1, min(len(class_1), sample_size - len(sample_0)))
        
        dataset = sample_0 + sample_1
        random.shuffle(dataset) # Shuffle to mix them up
        print(f"Dataset sampled to {len(dataset)} records (Balanced selection).")
    else:
        dataset = raw_data
        print(f"Dataset using full {len(dataset)} records.")

    # Split features and labels for processing
    feature_data = [row[:-1] for row in dataset]
    labels = [row[-1] for row in dataset]
    
    feature_names = headers[:num_features]

    print(f"\n================================================================================")
    print(f"Features: {feature_names}")

    while True:
        try:
            user_in = input(f"Enter unknown point ({num_features} values separated by space): ")
            unknown_point = [float(x) for x in user_in.split()]
            if len(unknown_point) != num_features:
                raise ValueError
        except:
            print("Invalid input.")
            continue

        try:
            metric_choice = int(input("Select Distance Metric (1: Euclidean, 2: Manhattan): "))
        except:
            metric_choice = 1
            
        try:
            norm_choice = int(input("Select Normalization (1: Min-Max, 2: Z-Score, 3: None) [Default 1]: ") or 1)
        except:
            norm_choice = 1

        # Prepare data for calculation
        processed_features = feature_data
        processed_point = unknown_point
        minmax_vals = []

        if norm_choice == 1:
            processed_features, minmax_vals = normalize_dataset(feature_data)
            processed_point = normalize_point(unknown_point, minmax_vals)

        # Recombine with labels for Neighbor search
        training_set = [f + [l] for f, l in zip(processed_features, labels)]
        
        # ---------------- PRINT DATASET DETAILS ----------------
        print("\n--- DATASET DETAILS ---")
        print(f"Features: {feature_names}")
        print(f"{'Original Values':<50} | {'Normalized':<50} | {'Distance'}")
        print("-" * 120)
        
        # Calculate all distances for display purposes
        all_dists_for_display = []
        for i in range(len(dataset)):
            orig_row = feature_data[i]
            norm_row = processed_features[i]
            label = labels[i]
            
            if metric_choice == 1:
                d = euclidean_distance(processed_point, norm_row)
            else:
                d = manhattan_distance(processed_point, norm_row)
            
            all_dists_for_display.append((orig_row, norm_row, d, label))
            
            # Print first 100 rows or all to match trace style
            if i < 100: 
                # Format formatting
                orig_str = str(orig_row)
                norm_str = "[" + ", ".join([f"{x:.4f}" for x in norm_row]) + "]"
                print(f"{orig_str:<50} | {norm_str:<50} | {d:.4f}")

        # ---------------- GET K ----------------
        try:
            k = int(input("\nEnter value of k: "))
        except:
            k = 3

        # Count votes in total dataset
        counts = {}
        for l in labels:
            counts[str(l)] = counts.get(str(l), 0) + 1
        print(f"Total Positive and Negative votes in DataSet: {counts}")

        # Sort all distances to rank them
        all_dists_for_display.sort(key=lambda x: x[2]) # Sort by distance
        
        # ---------------- RANKING TABLE ----------------
        print("\n--- RANKING & K-NEIGHBOR CHECK ---")
        print(f"Features: {feature_names}")
        print(f"{'Original Values':<50} | {'Distance':<10} | {'Rank':<6} | {'Class':<15} | {'Is Near K?'}")
        print("-" * 100)
        
        top_k_neighbors = [] # format for prediction function
        
        for i, (orig, norm, dist, lbl) in enumerate(all_dists_for_display):
            rank = i + 1
            is_near = "YES" if rank <= k else "NO"
            
            # Store top k for prediction
            if rank <= k:
                # Reconstruct row structure expected by predict function: [norm_features..., label]
                neighbor_row = norm + [lbl] 
                top_k_neighbors.append((neighbor_row, dist))
            
            # Print limited rows to match trace (e.g., k + some extra)
            if i < k + 5:
                print(f"{str(orig):<50} | {dist:.4f}     | {rank:<6} | {lbl:<15} | {is_near}")
            elif i == k + 5:
                print("...")

        # ---------------- PREDICTION ----------------
        weight_input = input("\nWeighted or Unweighted (W/U): ").lower()
        is_weighted = weight_input == 'w'
        
        prediction = predict_classification(top_k_neighbors, is_weighted)
        
        print(f"\nFINAL PREDICTED CLASS FOR {unknown_point}: {prediction}")
        
        cont = input("\nProcess another point? (Y/N): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
