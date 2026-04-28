import random
import csv

def generate_dataset(filename="loan_default.csv", n=200):
    
    headers = ["Age", "Income", "CreditScore", "Employment", "Loan_Default"]
    
    ages = ["Young", "Middle", "Senior"]
    incomes = ["Low", "Medium", "High"]
    credit_scores = ["Poor", "Average", "Good"]
    employment = ["Salaried", "Self-Employed"]
    
    data = []

    for _ in range(n):
        age = random.choice(ages)
        income = random.choice(incomes)
        credit = random.choice(credit_scores)
        job = random.choice(employment)
        
        # Simple rule to generate Loan_Default
        if income == "Low" and credit == "Poor":
            default = "Yes"
        elif credit == "Good" and income == "High":
            default = "No"
        else:
            default = random.choice(["Yes", "No"])
        
        data.append([age, income, credit, job, default])

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Dataset '{filename}' generated with {n} records.")

if __name__ == "__main__":
    generate_dataset()

