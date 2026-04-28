import math
import random

def calculate_entropy(target_list):
    total = len(target_list)
    if total == 0:
        return 0

    counts = {}
    for item in target_list:
        counts[item] = counts.get(item, 0) + 1

    entropy = 0
    for key in counts:
        p = counts[key] / total
        entropy -= p * math.log2(p)

    return entropy

def build_tree(dataset, headers, attributes_indices, target_index):
    """Recursively builds the decision tree as a nested dictionary."""
    target_column = [row[target_index] for row in dataset]
    
    # Base Case 1: If all records have the same target value (Leaf Node)
    if len(set(target_column)) == 1:
        return target_column[0]
        
    # Base Case 2: If no attributes are left, return the majority target value
    if not attributes_indices:
        return max(set(target_column), key=target_column.count)
        
    total_entropy = calculate_entropy(target_column)
    
    best_gain = -1
    best_attr_index = -1
    
    # Find the attribute with the highest Information Gain
    for i in attributes_indices:
        unique_vals = set(row[i] for row in dataset)
        weighted_entropy = 0
        
        for val in unique_vals:
            subset_targets = [row[target_index] for row in dataset if row[i] == val]
            weight = len(subset_targets) / len(dataset)
            weighted_entropy += weight * calculate_entropy(subset_targets)
            
        gain = total_entropy - weighted_entropy
        
        if gain > best_gain:
            best_gain = gain
            best_attr_index = i
            
    # Base Case 3: If no info is gained, return majority target
    if best_gain <= 0:
         return max(set(target_column), key=target_column.count)
         
    best_attr_name = headers[best_attr_index]
    
    # Initialize the tree node
    tree = {best_attr_name: {}}
    
    # Remove chosen attribute for next recursive calls
    remaining_attributes = [i for i in attributes_indices if i != best_attr_index]
    
    # Split dataset and recurse
    unique_vals = set(row[best_attr_index] for row in dataset)
    for val in unique_vals:
        subset = [row for row in dataset if row[best_attr_index] == val]
        
        if not subset:
            tree[best_attr_name][val] = max(set(target_column), key=target_column.count)
        else:
            tree[best_attr_name][val] = build_tree(subset, headers, remaining_attributes, target_index)
            
    return tree

def print_tree_pictographical(tree, prefix=""):
    """Recursively prints the decision tree using plain ASCII characters."""
    if not isinstance(tree, dict):
        print(f" --> [Class: {tree}]")
        return

    # Extract the root attribute of this subtree
    attr_name = list(tree.keys())[0]
    branches = tree[attr_name]
    print(f"[{attr_name}]")

    # Iterate through branches
    items = list(branches.items())
    for i, (branch_val, subtree) in enumerate(items):
        is_last = (i == len(items) - 1)
        
        # Using standard ASCII characters to avoid UnicodeEncodeError
        connector = "\\-- " if is_last else "+-- "
        
        # Print the branch line and the value condition
        print(f"{prefix}{connector}{branch_val}", end="")
        
        # Extend the prefix for child nodes depending on whether this is the last branch
        extension = "    " if is_last else "|   "
        print_tree_pictographical(subtree, prefix + extension)

def main():
    filename = "loan_default.csv"

    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]
    except:
        print("File not found.")
        return

    headers = lines[0].split(',')
    dataset = [line.split(',') for line in lines[1:]]

    print(f"\nDataset loaded with {len(dataset)} records.")

    # ---------------- RANDOM SAMPLING ----------------
    try:
        n = int(input("Enter number of records for random sampling: "))
        if n < len(dataset):
            dataset = random.sample(dataset, n)
            print(f"Randomly selected {len(dataset)} records.")
    except:
        print("Using full dataset.")

    # ---------------- PRINT SAMPLED DATA ----------------
    print("\n================ SAMPLED DATA FOR CALCULATION ================")
    print(f"Features: {headers}")
    print("-" * 60)
    for i, row in enumerate(dataset):
        print(f"Record {i+1}: {row}")
    print("==============================================================")


    target_index = len(headers) - 1
    target_column = [row[target_index] for row in dataset]

    total_entropy = calculate_entropy(target_column)

    print("\n=================================================")
    print(f"Target Attribute: {headers[target_index]}")
    print(f"Total Entropy = {total_entropy:.4f}")
    print("=================================================")

    gains = {}

    # ----------- Calculate Information Gain (Original Output) -----------
    for i in range(len(headers) - 1):
        attr_name = headers[i]
        print(f"\nAttribute: {attr_name}")
        print("-" * 40)

        unique_vals = set(row[i] for row in dataset)

        weighted_entropy = 0

        for val in unique_vals:
            subset = [row[target_index] for row in dataset if row[i] == val]
            ent = calculate_entropy(subset)

            weight = len(subset) / len(dataset)
            weighted_entropy += weight * ent

            yes = subset.count("Yes")
            no = subset.count("No")

            print(f"Value = {val:15} | Yes={yes} No={no} | Entropy={ent:.4f}")

        gain = total_entropy - weighted_entropy
        gains[attr_name] = gain

        print(f"Entropy after split = {weighted_entropy:.4f}")
        print(f"Information Gain ({attr_name}) = {gain:.4f}")

    # ---------------- FINAL TABLE ----------------
    print("\n============== INFORMATION GAIN TABLE ==============")

    if gains:
        best_attr = max(gains, key=gains.get)

        for key in gains:
            print(f"{key:20} : {gains[key]:.4f}")

        print("\nRoot Node (Maximum Information Gain):", best_attr)
        print("Gain =", round(gains[best_attr], 4))
    else:
        print("No attributes processed.")
        return

    # ---------------- PICTOGRAPHICAL TREE ----------------
    print("\n\n================ DECISION TREE ================\n")
    feature_indices = list(range(len(headers) - 1))
    
    # Build the full decision tree mapping
    decision_tree = build_tree(dataset, headers, feature_indices, target_index)
    
    # Render it visually
    print_tree_pictographical(decision_tree)
    print("\n==============================================================")

if __name__ == "__main__":
    main()
