A = input("\nEnter eventA : ")
B = input("ENter eventB : ")
pA = float(input(f"P({A}) = "))
pB = float(input(f"P({B}) = "))
pBgA = float(input(f"P({B}|{A}) = "))

pAgB = (pBgA * pA) / pB
print("\nUsing Bayes Rule : ")
print(f"P({A}|{B}) = {pAgB:.2f}\n")
