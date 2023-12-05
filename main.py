import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tkinter import Tk, Label, Entry, Button, Menu

# Loading world map data using GeoPandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
print(sorted(world['name'].unique()))

# Function to create GeoPandas animation
def create_animation():
    grandparents_countries = entry_grandparents.get().split(',')
    parents_countries = entry_parents.get().split(',')
    yourself_countries = entry_yourself.get().split(',')

    all_countries = list(set(grandparents_countries + parents_countries + yourself_countries))

    fig, ax = plt.subplots(figsize=(20, 10))
    world.plot(ax=ax, color='lightgrey', edgecolor='black')

    def update(frame):
        ax.clear()
        world.plot(ax=ax, color='lightgrey', edgecolor='black')

        grandparents_to_show = grandparents_countries[:]
        parents_to_show = parents_countries[:]
        yourself_to_show = yourself_countries[:]
        print('gradnparents to show', grandparents_to_show)

        print('parents to show', parents_to_show)

        mask_grandparents = world['name'].isin(grandparents_to_show)
        mask_parents = world['name'].isin(parents_to_show)
        mask_yourself = world['name'].isin(yourself_to_show)

        grandparents_data = world[mask_grandparents]
        parents_data = world[mask_parents]
        yourself_data = world[mask_yourself]

        if not grandparents_data.empty:  # Check if grandparents_data is not empty
            grandparents_data.plot(ax=ax, color='red', edgecolor='black')
            if frame == 0:
                for idx, row in grandparents_data.iterrows():
                    ax.annotate('', xy=(row.geometry.centroid.x, row.geometry.centroid.y), xytext=(0, 50), textcoords='offset points', arrowprops=dict(facecolor='black', arrowstyle='->'))
        if frame > 0:
            if not parents_data.empty:  # Check if parents_data is not empty
                parents_data.plot(ax=ax, color='red', edgecolor='black')
                if frame == 1:
                    for idx, row in parents_data.iterrows():
                        ax.annotate('', xy=(row.geometry.centroid.x, row.geometry.centroid.y), xytext=(0, 50), textcoords='offset points', arrowprops=dict(facecolor='black', arrowstyle='->'))
        if frame == 2:
            if not yourself_data.empty:  # Check if yourself_data is not empty
                yourself_data.plot(ax=ax, color='red', edgecolor='black')
                if frame == 2:
                    for idx, row in yourself_data.iterrows():
                        ax.annotate('', xy=(row.geometry.centroid.x, row.geometry.centroid.y), xytext=(0, 50), textcoords='offset points', arrowprops=dict(facecolor='black', arrowstyle='->'))

        # if frame == 0:
        #     ax.set_title(f'Grandparents')
        # if frame == 1:
        #     ax.set_title(f'Parents')
        # if frame == 2:
        #     ax.set_title(f'Me')
        ax.set_title(f'Frame {frame + 1}/3')
        ax.set_xticks([])
        ax.set_yticks([])

        # Set aspect ratio manually
        ax.set_aspect('equal')

    ani = FuncAnimation(fig, update, frames=3, repeat=True, interval=1000)
    plt.show()

# Function to set default countries in the text boxes
def set_default_countries():
    entry_grandparents.delete(0, 'end')
    entry_parents.delete(0, 'end')
    entry_yourself.delete(0, 'end')

    entry_grandparents.insert(0, "France,Spain,Germany")
    entry_parents.insert(0, "Cuba,Canada")
    entry_yourself.insert(0, "United States of America")

# GUI setup using Tkinter
root = Tk()
root.title("Progressive Countries Animation")

label_grandparents = Label(root, text="Grandparents' Countries (comma-separated):")
label_grandparents.pack()
entry_grandparents = Entry(root)
entry_grandparents.pack()

label_parents = Label(root, text="Parents' Countries (comma-separated):")
label_parents.pack()
entry_parents = Entry(root)
entry_parents.pack()

label_yourself = Label(root, text="Your Countries (comma-separated):")
label_yourself.pack()
entry_yourself = Entry(root)
entry_yourself.pack()

btn_animate = Button(root, text="Create Animation", command=create_animation)
btn_animate.pack()

# Creating a menu
menu = Menu(root)
root.config(menu=menu)

submenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Set Defaults", menu=submenu)
submenu.add_command(label="Default Countries", command=set_default_countries)

root.mainloop()
