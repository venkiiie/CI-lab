import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def main():
    X_arr, y_arr = make_classification(
        n_samples=1000, 
        n_features=10, 
        n_informative=5, 
        n_classes=2, 
        random_state=42
    )
    
    feature_names = [f"Feature_{i+1}" for i in range(10)]
    X = pd.DataFrame(X_arr, columns=feature_names)
    y = pd.Series(y_arr)
    target_names = ["Class 0 (Negative)", "Class 1 (Positive)"]
    
    print("\n--- Synthetic Binary Classification Dataset ---")
    print(f"Total Samples: {len(X)}")
    print(f"Features: {len(X.columns)}")
    print(f"Classes: {', '.join(target_names)}\n")

    try:
        n = int(input("Enter number of rows to preview: "))
    except ValueError:
        n = 5  # Fallback
        
    print(f"\nData Preview (First {n} rows, showing first 6 features):")
    print("-" * 75)
    print(X.iloc[:, :6].head(n).to_string())
    print("-" * 75)
    print()

    test_size = 0.2
    n_estimators = 100
    criterion = "gini"
    k_folds = 5

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=42
    )

    rf = RandomForestClassifier(
        n_estimators=n_estimators,
        criterion=criterion,
        random_state=42
    )
    rf.fit(X_train, y_train)

    cv = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)
    
    scoring = ['accuracy', 'precision', 'recall', 'f1']
    cv_res = cross_validate(rf, X_train, y_train, cv=cv, scoring=scoring)
    
    y_pred = rf.predict(X_test)
    
    print("Performance Metrics (Binary):")
    print("-" * 45)
    print(f"{'Metric':<15} | {'CV (5-Fold)':<12} | {'Test Set':<12}")
    print("-" * 45)
    
    print(f"{'Accuracy':<15} | {cv_res['test_accuracy'].mean():<12.4f} | {accuracy_score(y_test, y_pred):<12.4f}")
    print(f"{'Precision':<15} | {cv_res['test_precision'].mean():<12.4f} | {precision_score(y_test, y_pred):<12.4f}")
    print(f"{'Recall':<15} | {cv_res['test_recall'].mean():<12.4f} | {recall_score(y_test, y_pred):<12.4f}")
    print(f"{'F1 Score':<15} | {cv_res['test_f1'].mean():<12.4f} | {f1_score(y_test, y_pred):<12.4f}")
    print("-" * 45)
    
    print("\nConfusion Matrix (Test Set):")
    cm = confusion_matrix(y_test, y_pred)
    
    cm_df = pd.DataFrame(
        cm, 
        index=[f"Actual {cls[:7]}" for cls in target_names], 
        columns=[f"Pred {cls[:7]}" for cls in target_names]
    )
    print(cm_df.to_string())
    print()

if __name__ == "__main__":
    main()
