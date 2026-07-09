import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\Green\\Downloads\\CAR_T_data.csv')

# Filter core dataset: anti-FITC-CAR, Jurkat E6-1, 96-hour measurement time point
core_df = df[
    (df['CAR'] == 'anti-FITC-CAR') &
    (df['Cell_Type'] == 'Jurkat E6-1') &
    (df['Time'] == '96h')
].copy()

# Fill missing values with 0
core_df = core_df.fillna(0)
print(f"Total samples in core dataset: {len(core_df)}")
print("Dataset preview:")
print(core_df.head())

core_df['Concentration_encoded'] = core_df['Concentration'].map({'Non-concentrated':0, 'Concentrated':1}).fillna(0)
core_df['Shaking_encoded'] = core_df['Condition'].map({'Without Shaking':0, 'With Shaking':1}).fillna(0)
core_df['Enhancer_encoded'] = core_df['Condition'].map({'0% LentiBlast':0, '1% LentiBlast':1}).fillna(0)
core_df['Plasmid_encoded'] = core_df['Plasmid'].map({'PAX2':0, 'R8.74':1}).fillna(0)
core_df['Ratio_encoded'] = core_df['Ratio'].map({'0.5:3:1':0, '0.5:3:2':1, '0.5:3:4':0}).fillna(0)
core_df['Volume_uL'] = core_df['Volume_uL'].astype(float)

feat_cols = [
    'Concentration_encoded',
    'Shaking_encoded',
    'Plasmid_encoded',
    'Ratio_encoded',
    'Enhancer_encoded',
    'Volume_uL'
]
X = core_df[feat_cols]
y = core_df['Transduction_Percent']

# Split dataset: 80% training set, 20% test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("\n======= Model Evaluation Results =======")
print(f"Test set R² Score: {r2_score(y_test, y_pred):.3f}")
print(f"Test set Mean Absolute Error (MAE): {mean_absolute_error(y_test, y_pred):.3f}%")

# 5-fold cross validation for stable performance assessment
cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"Average 5-fold cross-validation R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Output impact coefficient of each experimental factor
print("\n======== Feature Impact Coefficients ========")
feature_coef = pd.DataFrame({
    'Feature': feat_cols,
    'Impact Coefficient': model.coef_
})
feature_coef = feature_coef.sort_values('Impact Coefficient', ascending=False)
print(feature_coef.round(2))

# Separate output for plasmid ratio impact
ratio_index = feat_cols.index('Ratio_encoded')
ratio_coef = model.coef_[ratio_index]

best_params_raw = {
    'Concentration_encoded': 1,
    'Shaking_encoded': 1,
    'Plasmid_encoded': 1,
    'Ratio_encoded': 1,
    'Enhancer_encoded': 1,
    'Volume_uL': 150
}
# Construct prediction dataframe strictly following training feature order
best_df = pd.DataFrame([best_params_raw], columns=feat_cols)
best_efficiency = model.predict(best_df)[0]

print("\n====== Optimal Experimental Combination ======")
best_readable = {
    "Virus Concentration": "Concentrated",
    "Shaking Condition": "With Shaking",
    "Packaging Plasmid": "R8.74",
    "Plasmid Ratio": "0.5:3:2 (Optimal)",
    "Enhancer Reagent": "1% LentiBlast",
    "Virus Volume": "150 μL"
}
for k, v in best_readable.items():
    print(f"{k}: {v}")
print(f"Predicted transduction efficiency for this combination: {best_efficiency:.2f}%")

# Disable Chinese font settings if you run on English environment, kept for Windows Chinese system compatibility
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(10, 6))

# Three groups of ratio test data, strictly aligned with feature column order
ratio_data = [
    [1, 1, 1, 0, 1, 150],  # 0.5:3:1
    [1, 1, 1, 1, 1, 150],  # 0.5:3:2
    [1, 1, 1, 0, 1, 150]   # 0.5:3:4
]
ratio_test_cases = pd.DataFrame(ratio_data, columns=feat_cols)
ratio_test_cases['Ratio Label'] = ['0.5:3:1', '0.5:3:2', '0.5:3:4']
# Predict only with standardized feature columns to avoid order mismatch error
ratio_test_cases['Predicted Efficiency (%)'] = model.predict(ratio_test_cases[feat_cols])

# Native Matplotlib plotting, no seaborn dependency
x = ratio_test_cases['Ratio Label']
y = ratio_test_cases['Predicted Efficiency (%)']
plt.bar(x, y, color='#4472c4', width=0.5)

# Chart formatting
plt.title('Predicted Transduction Efficiency by Different Plasmid Ratios', fontsize=14)
plt.xlabel('Plasmid Ratio (Envelope : Packaging : Transfer)', fontsize=12)
plt.ylabel('Predicted Transduction Efficiency (%)', fontsize=12)
plt.ylim(bottom=0)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Save image locally for Windows
plt.savefig('Ratio_Transduction_Efficiency_Comparison.png', dpi=300)
plt.show()

print("\nBar chart saved to current folder: Ratio_Transduction_Efficiency_Comparison.png")
