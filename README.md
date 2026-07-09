# Lentiviral CAR Transduction Efficiency Linear Regression Analysis
This repository contains Python code to analyze how experimental factors affect lentiviral anti-FITC-CAR transduction efficiency in Jurkat E6-1 cells, using linear regression modeling, cross-validation, feature importance evaluation and visualization of plasmid ratio performance.

## Project Background
Lentiviral CAR production efficiency is highly sensitive to multiple experimental variables: virus concentration, shaking culture condition, packaging plasmid type, DNA ratio, transfection enhancer dosage, and transfection volume.
This script builds a linear regression predictive model to:
1. Quantify the impact weight of each experimental variable on final transduction percentage
2. Evaluate model stability via 5-fold cross validation
3. Calculate the theoretically optimal experimental parameter combination for maximum transduction efficiency
4. Generate high-resolution bar chart comparing transduction performance across 3 common plasmid DNA ratios

## File Structure
├── CAR_T_data.csv                          # Raw experimental dataset of lentiviral CAR transfection
├── lenti_car_transduction_optimization.py  # Main linear regression analysis script
├── README.md                               # Project documentation
├── LICENSE                                 # MIT open-source license
└── .gitignore                              # Git ignore configuration for cache/env files

## How to Run
1. Modify the CSV file path inside the script to match your local `CAR_T_data.csv` location
2. Install required dependencies
pip install pandas numpy scikit-learn matplotlib
3. Execute main script via terminal/cmd
python lenti_car_transduction_optimization.py
4. Output: Console print all model metrics & generate comparison figure: Ratio_Transduction_Efficiency_Comparison.png

## Environment & Dependencies
### Required Python Libraries
```bash
pip install pandas numpy scikit-learn matplotlib
