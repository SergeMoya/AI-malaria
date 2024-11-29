# Malaria Prevention Analysis in Africa

This project analyzes the effectiveness of preventive measures against malaria in African countries using machine learning techniques.

## Project Structure

```
malaria/
├── malaria_analysis.py    # Main analysis script
├── requirements.txt       # Python dependencies
├── DatasetAfricaMalaria.csv  # Input dataset (not included)
└── output/               # Generated visualizations
    ├── prevention_effectiveness_heatmap.png
    └── prediction_accuracy_plot.png
```

## Setup and Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your `DatasetAfricaMalaria.csv` file in the project root directory
2. Run the analysis script:
   ```bash
   python malaria_analysis.py
   ```

3. Check the `output` directory for generated visualizations:
   - `prevention_effectiveness_heatmap.png`: Shows correlation between preventive measures and malaria incidence
   - `prediction_accuracy_plot.png`: Displays model prediction accuracy with R² and RMSE metrics

## Dataset Format

The input CSV file should contain the following columns:
- country: Name of the African country
- bed_nets: Data about bed net usage
- antimalarial_medication: Data about antimalarial medication usage
- malaria_incidence: Target variable showing malaria cases

## Output

The script generates:
1. A heatmap showing the effectiveness of different prevention methods across countries
2. A prediction accuracy plot comparing actual vs. predicted malaria incidence
3. Printed performance metrics (R² and RMSE)

## Error Handling

The script includes error handling for:
- Missing input file
- Data loading issues
- Visualization creation errors
- Model training problems
