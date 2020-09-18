import pandas as pd

from bokeh.io import show
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar
from bokeh.plotting import figure

# Load in the flights dataset
data = pd.read_csv('logoart.csv')
# Make sure the months column consists of just the unique months, not every instance, make it categorical
data["var2"] = pd.Categorical(data["var2"], data.var2.unique())

# We need to pivot the dataset in order to get the minimum and maximum values for the color mapper below
data_pivot = data.pivot("var2", "var1", "var3")

# Set the colors and get the min/max values for the LinearColorMapper
colors = ["#fff0c6", "#ffe080", "#ffd444", "#c5d8e8", "#79a2c5", "#3772a3"]
mapper = LinearColorMapper(palette=colors, low=data_pivot.min().min(), high=data_pivot.max().max())

# Preprocess data, ensure that years and months are lists and that all values are recognized as strings
years = list(data_pivot.columns.astype('str'))
months = list(data_pivot.index)
data['var1'] = data.var1.astype('str')

# Make the ColumnDataSource object
source = ColumnDataSource(data)

# Set up the heatmap figure, set tooltips
p = figure(title="Logo Heatmap", x_range=years, y_range=months)
# Use the rect plotting function
p.rect(x='var1', y='var2', width=1, height=1, source=source, fill_color={'field': 'var3', 'transform': mapper}, line_color='white')

# Create the color bar object and add it to the left of the figure with `add_layoout`
color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="10pt", border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'left')
p.plot_height = 250
p.plot_width = 350

show(p)