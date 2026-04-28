import random
import csv

def generate_csv():
    header = ["CreditScore", "AnnualIncome", "LoanAmount", "YearsEmployed", "Defaulted"]
    rows = []

    for _ in range(250):
        rows.append([
            random.randint(300, 850),       
            random.randint(20000, 150000),  
            random.randint(5000, 50000),    
            random.randint(0, 40),          
            0           
        ])
    for _ in range(250):
        rows.append([
            random.randint(300, 850),
            random.randint(20000, 150000),
            random.randint(5000, 50000),
            random.randint(0, 40),
            1
        ])

    with open('loan_default.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    
    return rows

if __name__ == "__main__":
    generate_csv()
    print("loan_default.csv generated.")
