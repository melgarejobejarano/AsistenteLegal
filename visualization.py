import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the style
sns.set_theme(style="white")

# Generate random data
np.random.seed(42)  # For reproducibility
n_samples = 200

# Create random data similar to MPG dataset
data = {
    'horsepower': np.random.normal(100, 30, n_samples),  # Random horsepower values
    'mpg': np.random.normal(25, 8, n_samples),          # Random MPG values
    'weight': np.random.normal(3000, 500, n_samples),   # Random weight values
    'origin': np.random.choice(['USA', 'Europe', 'Asia'], n_samples)  # Random origins
}

# Create DataFrame
df = pd.DataFrame(data)

# Create the visualization
plt.figure(figsize=(10, 6))
sns.relplot(
    x="horsepower", 
    y="mpg", 
    hue="origin", 
    size="weight",
    sizes=(40, 400), 
    alpha=.5, 
    palette="muted",
    height=6, 
    data=df
)

# Add title and labels
plt.title('Relationship between Horsepower and MPG by Origin and Weight', pad=20)
plt.xlabel('Horsepower')
plt.ylabel('Miles per Gallon (MPG)')

# Show the plot
plt.show() 