#!/usr/bin/python3


from bs4 import BeautifulSoup
import webcolors
from collections import Counter
from statistics import median
import numpy as np
import psycopg2


def color_name_to_rgb_webcolors(color_name):
    try:
        rgb_tuple = webcolors.name_to_rgb(color_name)
        return rgb_tuple
    except ValueError:
        print(f"Color '{color_name}' not found or not a valid color name.")
        return None

def calculate_mean_color_webcolors(colors):
    total_red = 0
    total_green = 0
    total_blue = 0

    for color in colors:
        rgb_tuple = color_name_to_rgb_webcolors(color)
        if rgb_tuple:
            total_red += rgb_tuple[0]
            total_green += rgb_tuple[1]
            total_blue += rgb_tuple[2]

    mean_red = total_red / len(colors)
    mean_green = total_green / len(colors)
    mean_blue = total_blue / len(colors)

    mean_color = (int(mean_red), int(mean_green), int(mean_blue))
    return mean_color

# HTML content for color extraction
html_content = """
...  # Your HTML content here
"""

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract color data for each day
color_data = {}
days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']
for day in days:
    color_td = soup.find('td', text=day).find_next('td').text
    color_data[day] = color_td.strip().split(', ')

# Convert color names to RGB values using webcolors library
color_data_rgb_webcolors = [[color_name_to_rgb_webcolors(color) for color in day_colors] for day_colors in color_data.values()]

# Calculate the mean color using webcolors library
all_colors_webcolors = [color for day_colors in color_data_rgb_webcolors for color in day_colors if color is not None]
mean_color_webcolors = calculate_mean_color_webcolors(all_colors_webcolors)

print("Color Data:")
print(color_data)
print("Mean Color (RGB) using webcolors library:", mean_color_webcolors)

# flatten the list of colors for all days
all_colors_flat = [color for day_colors in color_data.values() for color in day_colors]

# Count the occurrences of each color
color_counts = Counter(all_colors_flat)

# Find the most worn color
most_worn_color = max(color_counts, key=color_counts.get)

print("Most Worn Color:", most_worn_color)


# Find the median color
all_colors_rgb = [color_to_rgb[color] for color in all_colors_flat if color in color_to_rgb]
median_color_rgb = (
    int(median([color[0] for color in all_colors_rgb])),
    int(median([color[1] for color in all_colors_rgb])),
    int(median([color[2] for color in all_colors_rgb]))
)

print("Median Color (RGB):", median_color_rgb)

# Calculate variance of red component
red_components = [color[0] for color in all_colors_rgb]
variance_red = np.var(red_components)

# Calculate the probability of the color being red
total_colors = len(all_colors_flat)
red_count = all_colors_flat.count('RED')  # Assuming 'RED' is a color
probability_red = red_count / total_colors

print("Variance of Red Component:", variance_red)
print("Probability of the color being red:", probability_red)


# connect to PostgreSQL database
conn = psycopg2.connect(database="postgres", user="admin", password="admin_pass"
