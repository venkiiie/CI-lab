import itertools

n = int(input("\nEnter the number of tosses: "))

sample_space = [''.join(toss) for toss in itertools.product('HT', repeat=n)]
total_outcomes = len(sample_space)

one_head_one_tail = [i for i in sample_space if i.count("H") == 1 and i.count("T") == 1]
prob_1H1T = len(one_head_one_tail) / total_outcomes

atleast_one_head = [i for i in sample_space if i.count("T") == 2]
prob_atleast_1H = len(atleast_one_head) / total_outcomes

atleast_one_tail = [i for i in sample_space if "T" in i]
prob_atleast_1T = len(atleast_one_tail) / total_outcomes

atmost_one_tail = [i for i in sample_space if i.count("T") <= 1]
prob_atmost_1T = len(atmost_one_tail) / total_outcomes

print(f"Sample Space ({total_outcomes} outcomes):", sample_space)
print(f"\nExactly 1 Head : {one_head_one_tail}")
print(f"Probability: {prob_1H1T}")
print(f"\nAt least 2 Tail: {atleast_one_head}")
print(f"Probability: {prob_atleast_1H}")
print(f"\nAt least 1 Tail: {atleast_one_tail}")
print(f"Probability: {prob_atleast_1T}")
print(f"\nAt most 1 Tail: {atmost_one_tail}")
print(f"Probability: {prob_atmost_1T}")
print()
