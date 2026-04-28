from itertools import product

def parse_condition(cond):
    cond = cond.strip().lower()
    if cond.startswith('~'):
        return cond[1:], False
    return cond, True

def check_conditions(row, conditions, logic='and'):
    if not conditions:
        return True

    results = []
    for var, val in conditions:
        if var in row:
            results.append(row[var] == val)

    if logic == 'or':
        return any(results)
    return all(results)

def compute_probability(kb, query_info, given_info=None):
    numerator = 0
    denominator = 0

    q_conds, q_logic = query_info

    if given_info is None:
        for row in kb:
            if check_conditions(row, q_conds, q_logic):
                numerator += row['prob']
        return round(numerator, 4)
    else:
        g_conds, g_logic = given_info
        for row in kb:
            if check_conditions(row, g_conds, g_logic):
                denominator += row['prob']
                if check_conditions(row, q_conds, q_logic):
                    numerator += row['prob']
        return round(numerator / denominator, 4) if denominator != 0 else 0

def parse_query_part(part):
    if 'v' in part:
        conds = [parse_condition(c) for c in part.split('v') if c.strip()]
        return (conds, 'or')
    else:
        # Standardize AND logic for ^ or comma
        part = part.replace('^', ',')
        conds = [parse_condition(c) for c in part.split(',') if c.strip()]
        return (conds, 'and')

def main():
    num_vars = int(input("\nEnter number of variables: ").strip())
    variables = []
    print("Enter variable names:")
    for _ in range(num_vars):
        variables.append(input().strip().lower())

    combinations = list(product([True, False], repeat=num_vars))
    kb = []

    print("\nEnter values for each combination:")
    for comb in combinations:
        row = {}
        display_parts = []
        for i, val in enumerate(comb):
            row[variables[i]] = val
            display_parts.append(f"{variables[i]}={'T' if val else 'F'}")
        print(", ".join(display_parts))
        row['prob'] = float(input("Value: "))
        kb.append(row)

    print("\nKnowledge Base Table:")
    header = " | ".join([v.upper() for v in variables]) + " | Value"
    print(header)
    print("-" * len(header))
    for row in kb:
        vals = " | ".join(["T" if row[v] else "F" for v in variables])
        print(f"{vals} | {row['prob']}")

    while True:
        raw_query = input("\nEnter query or '0' to exit: ").strip().lower()
        if raw_query == '0': break
        try:
            clean = raw_query.replace("p(", "").replace(")", "")
            if '|' in clean:
                left, right = clean.split('|')
                result = compute_probability(kb, parse_query_part(left), parse_query_part(right))
            else:
                result = compute_probability(kb, parse_query_part(clean))
            print(f"Result = {result}")
        except Exception as e:
            print(f"Error: {e}")
    print()

if __name__ == "__main__":
    main()

