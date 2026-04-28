import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def print_class_distribution(y, target_names, title="Class Distribution:"):
    """Prints per-class distribution for the given dataset."""
    counts = y.value_counts().sort_index()
    perc = (counts / len(y) * 100).round(2)

    dist_df = pd.DataFrame({
        "Class": target_names,
        "Count": counts.values,
        "Percent (%)": perc.values
    })

    print(title)
    print("-" * 45)
    print(dist_df.to_string(index=False))
    print("-" * 45)

def main():
    # Generate synthetic binary classification data (1250 samples total)
    X_arr, y_arr = make_classification(
        n_samples=2000,
        n_features=10,
        n_informative=5,
        n_classes=2,
        random_state=42
    )

    feature_names = [f"Feature_{i+1}" for i in range(10)]
    X = pd.DataFrame(X_arr, columns=feature_names)
    y = pd.Series(y_arr, name="target")
    target_names = ["Class 0 (Negative)", "Class 1 (Positive)"]

    print("\n--- Synthetic Binary Classification Dataset ---")
    print(f"Total Samples: {len(X)}")
    print(f"Features: {len(X.columns)}")
    print(f"Classes: {', '.join(target_names)}\n")

    # Preview rows input
    try:
        n_preview = int(input("Enter number of rows to preview: "))
    except ValueError:
        n_preview = 5  # Fallback

    print(f"\nData Preview (First {n_preview} rows, showing first 4 features):")
    print("-" * 75)
    print(X.iloc[:, :4].head(n_preview).to_string())
    print("-" * 75)
    print()

    # Test size input
    try:
        test_size = float(input("Enter test size as a fraction (e.g., 0.2 for 20%): "))
        if not (0.0 < test_size < 1.0):
            raise ValueError
    except ValueError:
        test_size = 0.2  # Fallback

    n_estimators = 100
    criterion = "gini"
    k_folds = 5

    # Split the dataset WITHOUT stratify=y, so the class distribution in the test set is purely random
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    # Print how much data is used for training/testing
    print("\n--- Train/Test Split ---")
    print(f"Requested test_size: {test_size:.2f} ({test_size*100:.0f}%)")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples:  {len(X_test)}\n")

    # Print class distribution specifically for the test data
    print_class_distribution(y_test, target_names, title="Test Set Class Distribution:")
    print()

    # Initialize and train the Random Forest Classifier
    rf = RandomForestClassifier(
        n_estimators=n_estimators,
        criterion=criterion,
        random_state=42
    )
    rf.fit(X_train, y_train)

    # 5-Fold Cross Validation on training data
    cv = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision', 'recall', 'f1']
    cv_res = cross_validate(rf, X_train, y_train, cv=cv, scoring=scoring)

    # Predictions on the Test Set
    y_pred = rf.predict(X_test)

    print("Performance Metrics (Binary):")
    print("-" * 45)
    print(f"{'Metric':<15} | {'CV (5-Fold)':<12} | {'Test Set':<12}")
    print("-" * 45)

    # Explicit pos_label=1 ensures we get the metrics specifically for Class 1 (Positive)
    print(f"{'Accuracy':<15} | {cv_res['test_accuracy'].mean():<12.4f} | {accuracy_score(y_test, y_pred):<12.4f}")
    print(f"{'Precision':<15} | {cv_res['test_precision'].mean():<12.4f} | {precision_score(y_test, y_pred, pos_label=1):<12.4f}")
    print(f"{'Recall':<15} | {cv_res['test_recall'].mean():<12.4f} | {recall_score(y_test, y_pred, pos_label=1):<12.4f}")
    print(f"{'F1 Score':<15} | {cv_res['test_f1'].mean():<12.4f} | {f1_score(y_test, y_pred, pos_label=1):<12.4f}")
    print("-" * 45)

    print("\nConfusion Matrix (Test Set):")
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(
        cm,
        index=[f"Actual {cls}" for cls in target_names],
        columns=[f"Pred {cls}" for cls in target_names]
    )
    print(cm_df.to_string())
    print()

if __name__ == "__main__":
    main()
