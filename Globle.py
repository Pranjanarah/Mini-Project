# import tkinter as tk
# from tkinter import messagebox
# import random
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# import math
# import requests
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.colors as mcolors
# import numpy as np
# import geopandas as gpd

# # Fetch countries data from the API
# # def fetch_countries_from_api():
# #     url = "https://restcountries.com/v3.1/all"
# #     response = requests.get(url, verify=False)
# #     countries_data = response.json()
# #     countries = {}
# #     for country in countries_data:
# #         name = country['name']['common']
# #         lat, lon = country['latlng']
# #         countries[name] = (lat, lon)
# #     return countries

# # # Usage
# # countries = fetch_countries_from_api()

# countries = {
#     "India": (20.5937, 78.9629),
#     "Brazil": (-14.2350, -51.9253),
#     "Canada": (56.1304, -106.3468),
#     "France": (46.6034, 1.8883),
#     "Australia": (-25.2744, 133.7751),
#     "Japan": (36.2048, 138.2529)
# }

# # Haversine formula to calculate distance
# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371  # Radius of Earth in km
#     dlat = math.radians(lat2 - lat1)
#     dlon = math.radians(lon2 - lon1)
#     a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#     return R * c

# # Function to calculate bearing
# def calculate_bearing(lat1, lon1, lat2, lon2):
#     dlon = math.radians(lon2 - lon1)
#     lat1, lat2 = math.radians(lat1), math.radians(lat2)
    
#     x = math.sin(dlon) * math.cos(lat2)
#     y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
#     bearing = math.atan2(x, y)
    
#     # Convert bearing from radians to degrees
#     bearing = math.degrees(bearing)
#     bearing = (bearing + 360) % 360  # Normalize the bearing to a range between 0 and 360
#     return bearing

# # Function to convert bearing to cardinal direction
# def bearing_to_direction(bearing):
#     directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
#     index = int((bearing + 22.5) // 45)  # Normalize to nearest cardinal direction
#     index = index % 8  # Ensure the index is within the valid range [0, 7]
#     return directions[index]

# # Select a random target country
# def get_random_country():
#     return random.choice(list(countries.items()))

# # Create GUI
# class GlobleGame:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Globle")
        
#         # Initial game state
#         self.target_country, self.target_coords = get_random_country()
#         self.guessed_countries = {}

#         # Set maximum number of guesses
#         self.max_guesses = 1
#         self.guess_count = 0

#         # Input Field
#         self.main_frame = tk.Frame(root)
#         self.main_frame.pack(fill=tk.BOTH, expand=True)

#         self.map_frame = tk.Frame(self.main_frame, bg="white")
#         self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         self.ui_frame = tk.Frame(self.main_frame, width=400, height=800, bg="#D6EAF8")  # Light blue background
#         self.ui_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
#         self.label = tk.Label(self.ui_frame, text="Guess the mystery country:", font=("Roboto", 16, "bold"), bg="#D6EAF8")
#         self.label.pack(pady=10)
#         self.entry = tk.Entry(self.ui_frame, font=("Roboto", 14), width=30)
#         self.entry.pack(pady=5)
#         self.submit_button = tk.Button(self.ui_frame, text="Submit Guess", font=("Roboto", 14), command=self.check_guess, relief="flat", bg="#7D7DFF", fg="white")
#         self.submit_button.pack(pady=5)
#         self.hint_label = tk.Label(self.ui_frame, text="", font=("Roboto", 12), bg="#D6EAF8")
#         self.hint_label.pack(pady=10)
        
#         # Add space for the correct country name
#         self.correct_country_label = tk.Label(self.ui_frame, text="", font=("Roboto", 12), bg="#D6EAF8")
#         self.correct_country_label.pack(pady=10)

#         # Restart Button (hidden initially)
#         self.restart_button = tk.Button(self.ui_frame, text="Restart Game", font=("Roboto", 14), command=self.restart_game, relief="flat", bg="#FF7D7D", fg="white")
#         self.restart_button.pack(pady=10)
#         self.restart_button.pack_forget()  # Hide it initially

#         # Initialize Map
#         self.fig = plt.figure(figsize=(12, 9), dpi=100)  # Increase figure size and resolution
#         self.map_ax = self.fig.add_subplot(1, 1, 1)
#         self.map = Basemap(projection="mill", resolution="i", ax=self.map_ax)  # "i" for intermediate resolution
#         self.map.drawcoastlines()
#         self.map.fillcontinents(color="#C4E1FF", lake_color="#ADD8E6")  # Livelier colors for continents and lakes
#         self.map.drawcountries()

#         # Embed Map in Tkinter
#         self.canvas = tk.Canvas(root, bg="white", width=1000, height=800)  # Match map size
#         self.canvas.pack(fill=tk.BOTH, expand=True)
#         self.map_fig = None
#         self.update_map()

#         # Load shapefile for countries
#         self.world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#     def update_map(self):
#         """Update map with guessed countries and color gradient."""
#         # Create a colormap for smoother gradient
#         cmap = plt.get_cmap("RdYlGn_r")  # Red to Green (reverse for hot-to-cold)

#         # Plot each guessed country
#         for country, distance in self.guessed_countries.items():
#             # Find the country polygon by its name
#             country_data = self.world[self.world['name'] == country]
#             if not country_data.empty:
#                 # Normalize distance for colormap
#                 norm = plt.Normalize(vmin=0, vmax=3000)  # Normalize the distance for the colormap
#                 color = cmap(norm(distance))  # Get the color from colormap
                
#                 # Plot the country polygon and fill it with the appropriate color
#                 country_data.plot(ax=self.map_ax, color=color, edgecolor='black', linewidth=0.5)

#         if self.map_fig:
#             self.map_fig.draw()  # Redraw the canvas
#         else:
#             self.map_fig = FigureCanvasTkAgg(self.fig, master=self.map_frame)
#             self.map_fig.draw()
#             self.map_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#     def check_guess(self):
#         """Check the user's guess and provide feedback."""
#         guess = self.entry.get().strip()
        
#         if guess not in countries:
#             messagebox.showerror("Invalid Country", "Please enter a valid country.")
#             return
        
#         if guess in self.guessed_countries:
#             messagebox.showinfo("Already Guessed", "You already guessed this country.")
#             return
        
#         guessed_coords = countries[guess]
#         distance = haversine(self.target_coords[0], self.target_coords[1], guessed_coords[0], guessed_coords[1])
        
#         # Add the guess and its distance to the dictionary
#         self.guessed_countries[guess] = distance
        
#         # Calculate bearing and direction
#         bearing = calculate_bearing(self.target_coords[0], self.target_coords[1], guessed_coords[0], guessed_coords[1])
#         direction = bearing_to_direction(bearing)
        
#         # Feedback based on proximity
#         if distance == 0:
#             messagebox.showinfo("Congratulations!", f"You found the mystery country: {self.target_country}!")
#             self.root.destroy()
#         else:
#             self.hint_label.config(text=f"{guess}: {distance:.1f} km to the {direction}.")
        
#         self.guess_count += 1
        
#         # Check if the player has reached the maximum guesses
#         if self.guess_count >= self.max_guesses:
#             self.correct_country_label.config(text=f"The correct country was: {self.target_country}")
#             self.restart_button.pack()  # Show the restart button
        
#         self.update_map()

#     def restart_game(self):
#         """Restart the game with a new random country."""
#         self.target_country, self.target_coords = get_random_country()
#         self.guessed_countries = {}

#         self.guess_count = 0
#         self.hint_label.config(text="")
#         self.correct_country_label.config(text="")
#         self.restart_button.pack_forget()  # Hide the restart button
#         self.update_map()

# # Run Game
# root = tk.Tk()
# game = GlobleGame(root)
# root.mainloop()


import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
import numpy as np
import json

# Load the country data from a local JSON file
with open('countries.json', 'r') as file:
    countries = json.load(file)

# Print out the name of each country (to see what data we have)
for country in countries:
    print(country['name']['common'])

# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Function to calculate bearing
def calculate_bearing(lat1, lon1, lat2, lon2):
    dlon = math.radians(lon2 - lon1)
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.atan2(x, y)
    
    # Convert bearing from radians to degrees
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360  # Normalize the bearing to a range between 0 and 360
    return bearing

# Function to convert bearing to cardinal direction
def bearing_to_direction(bearing):
    directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
    index = int((bearing + 22.5) // 45)  # Normalize to nearest cardinal direction
    index = index % 8  # Ensure the index is within the valid range [0, 7]
    return directions[index]

# Select a random target country
def get_random_country():
    country = random.choice(countries)
    country_name = country['name']['common']
    latlng = country.get('latlng', [None, None])
    return country_name, latlng

# Create GUI
class GlobleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Globle")
        
        # Initial game state
        self.target_country, self.target_coords = get_random_country()
        self.guessed_countries = {}

        # Set maximum number of guesses
        self.max_guesses = 10
        self.guess_count = 0

        # Input Field
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.map_frame = tk.Frame(self.main_frame, bg="white")
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.ui_frame = tk.Frame(self.main_frame, width=400, height=800, bg="#D6EAF8")  # Light blue background
        self.ui_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.label = tk.Label(self.ui_frame, text="Guess the mystery country:", font=("Roboto", 16, "bold"), bg="#D6EAF8")
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.ui_frame, font=("Roboto", 14), width=30)
        self.entry.pack(pady=5)
        self.submit_button = tk.Button(self.ui_frame, text="Submit Guess", font=("Roboto", 14), command=self.check_guess, relief="flat", bg="#7D7DFF", fg="white")
        self.submit_button.pack(pady=5)
        self.hint_label = tk.Label(self.ui_frame, text="", font=("Roboto", 12), bg="#D6EAF8")
        self.hint_label.pack(pady=10)
        
        # Add space for the correct country name
        self.correct_country_label = tk.Label(self.ui_frame, text="", font=("Roboto", 12), bg="#D6EAF8")
        self.correct_country_label.pack(pady=10)

        # Restart Button (hidden initially)
        self.restart_button = tk.Button(self.ui_frame, text="Restart Game", font=("Roboto", 14), command=self.restart_game, relief="flat", bg="#FF7D7D", fg="white")
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide it initially

        # Initialize Map
        self.fig = plt.figure(figsize=(12, 9), dpi=100)  # Increase figure size and resolution
        self.map_ax = self.fig.add_subplot(1, 1, 1)
        self.map = Basemap(projection="mill", resolution="i", ax=self.map_ax)  # "i" for intermediate resolution
        self.map.drawcoastlines()
        self.map.fillcontinents(color="#C4E1FF", lake_color="#ADD8E6")  # Livelier colors for continents and lakes
        self.map.drawcountries()

        # Embed Map in Tkinter
        self.canvas = tk.Canvas(root, bg="white", width=1000, height=800)  # Match map size
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.map_fig = None
        self.update_map()

    def update_map(self):
        """Update map with guessed countries and color gradient."""
        # Create a colormap for smoother gradient
        cmap = plt.get_cmap("RdYlGn_r")  # Red to Green (reverse for hot-to-cold)
        
        for country, distance in self.guessed_countries.items():
            country_data = next(c for c in countries if c['name']['common'] == country)
            lat, lon = country_data.get('latlng', [None, None])
            if lat and lon:
                x, y = self.map(lon, lat)
                
                # Normalize distance for colormap
                norm = plt.Normalize(vmin=0, vmax=3000)  # Normalize the distance for the colormap
                color = cmap(norm(distance))  # Get the color from colormap
                
                self.map.scatter(x, y, color=color, s=100, zorder=5)  # Mark guessed countries
        
        if self.map_fig:
            self.map_fig.draw()  # Redraw the canvas
        else:
            self.map_fig = FigureCanvasTkAgg(self.fig, master=self.map_frame)
            self.map_fig.draw()
            self.map_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def check_guess(self):
        """Check the user's guess and provide feedback."""
        guess = self.entry.get().strip()
        
        if not any(c['name']['common'] == guess for c in countries):
            messagebox.showerror("Invalid Country", "Please enter a valid country.")
            return
        
        if guess in self.guessed_countries:
            messagebox.showinfo("Already Guessed", "You already guessed this country.")
            return
        
        guessed_country_data = next(c for c in countries if c['name']['common'] == guess)
        guessed_coords = guessed_country_data.get('latlng', [None, None])
        
        if not guessed_coords or None in guessed_coords:
            messagebox.showerror("Invalid Coordinates", "Country coordinates not found.")
            return
        
        distance = haversine(self.target_coords[0], self.target_coords[1], guessed_coords[0], guessed_coords[1])
        
        # Add the guess and its distance to the dictionary
        self.guessed_countries[guess] = distance
        
        # Calculate bearing and direction
        bearing = calculate_bearing(self.target_coords[0], self.target_coords[1], guessed_coords[0], guessed_coords[1])
        direction = bearing_to_direction(bearing)
        
        # Feedback based on proximity
        if distance == 0:
            messagebox.showinfo("Congratulations!", f"You found the mystery country: {self.target_country}!")
            self.root.destroy()
        else:
            self.hint_label.config(text=f"{guess}: {distance:.1f} km to the {direction}.")
        
        self.guess_count += 1
        
        # Check if the player has reached the maximum guesses
        if self.guess_count >= self.max_guesses:
            self.correct_country_label.config(text=f"The correct country was: {self.target_country}")
            self.restart_button.pack()  # Show the restart button
        
        self.update_map()

    def restart_game(self):
        self.target_country, self.target_coords = get_random_country()
        self.guessed_countries = {}
        self.guess_count = 0
        self.hint_label.config(text="")
        self.correct_country_label.config(text="")
        self.restart_button.pack_forget()  # Hide the restart button
        self.update_map()

# Run Game
root = tk.Tk()
game = GlobleGame(root)
root.mainloop()
