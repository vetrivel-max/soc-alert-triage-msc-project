import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

def evaluate(model_path, x_path, y_path, title, filename):
    print(f"\n{'='*60}")
    print(f"EVALUATION: {title}")
    print(f"{'='*60}")
    model = joblib.load(model_path)
    X = pd.read_csv(x_path)
    y = pd.read_csv(y_path).squeeze()
    y_pred = model.predict(X)
    print(classification_report(y, y_pred, zero_division=0))

    labels = sorted(y.unique())
    cm = confusion_matrix(y, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    fig, ax = plt.subplots(figsize=(8, 8))
    disp.plot(ax=ax, cmap='Blues', xticks_rotation=45, colorbar=False)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved confusion matrix image: {filename}")

# Stage 1: Normal vs Attack (Static/CICIDS2017 model)
evaluate('stage1_model.pkl', 'data/X_test.csv', 'data/y_test.csv',
         'Stage 1 - Normal vs Attack (Static Model)', 'confusion_stage1.png')

# Stage 2: Attack type classification (Static/CICIDS2017 model)
evaluate('stage2_model.pkl', 'data/X_test_stage2.csv', 'data/y_test_stage2.csv',
         'Stage 2 - Attack Type (Static Model)', 'confusion_stage2.png')

# Own Model (self-generated lab traffic)
evaluate('own_model.pkl', 'data/X_test_own.csv', 'data/y_test_own.csv',
         'Own Model - Lab Traffic', 'confusion_own.png')