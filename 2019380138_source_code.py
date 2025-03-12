import matplotlib.pyplot as plt
import mplcursors
from matplotlib.widgets import Button
from shapely import Polygon

# creating a scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter([], [])
ax.set_xlim(left = 0, right = 100)
ax.set_ylim(bottom = 0, top = 100)

#creating polygon variables
poly= []
all_polygons= []
all_intersections= []

#creating the buttons 
button1_ax = plt.axes([0.1, 0.005, 0.1, 0.05])
done = Button(button1_ax,"Draw")
button2_ax = plt.axes([0.25,0.005, 0.1, 0.05])
calculate = Button(button2_ax, "Calculate")

#defining what happens when we click the done button
def done_clicked(event):
    poly.pop()
    poly_drawn = Polygon(poly)
    x,y = poly_drawn.exterior.xy
    ax.plot(x,y)
    plt.draw()
    all_polygons.append(poly.copy())
    poly.clear()
    
    
def calculate_clicked(event):
    #we stop drawing polygons
    fig.canvas.mpl_disconnect(start_graph)
    #we make all the lists in all polygons into shapely polygons
    shapely_polys= []
    for p in all_polygons: 
        shapely_polys.append(Polygon(p))
    
    #we now need to produce all intersection polys and put them in intersection_polys[]
    intersections = []
    for i in range(len(shapely_polys)):
        for j in range(i + 1, len(shapely_polys)):
            intersection = shapely_polys[i].intersection(shapely_polys[j])
            if not intersection.is_empty:
                intersections.append(intersection)

    
    for i in intersections:
        inter_draw = i.exterior.coords
        patch = plt.Polygon(inter_draw, alpha=0.8)
        ax.add_patch(patch)
        plt.draw()

    #making the output in DCEL format in a txt file
    filename = "output_in_DCEL.txt"
    with open(filename, "w") as file:
        vertex_id = 0
        for polygon_id, intersections in enumerate(intersections):
            # Write the vertices
            vertices = intersections.exterior.coords
            for i, (x, y) in enumerate(vertices):
                file.write(f"v {vertex_id} {round(x,2)} {round(y,2)}\n")
                vertex_id += 1

            # Write the half-edges
            num_edges = len(vertices)
            for i in range(num_edges):
                file.write(f"e {polygon_id*num_edges + i} {polygon_id*num_edges + i} {polygon_id*num_edges + (i+1) % num_edges}\n")

            # Write the face
            file.write(f"f {polygon_id*num_edges}\n")

 
#function to update the scatter plot with a new point
def update_plot(x, y):
    scatter.set_offsets([[x, y]])
    poly.append((x,y))
    
    plt.draw()

#function to handle mouse click events
def on_click(event):
    if event.inaxes:
        x, y = round(event.xdata,1), round(event.ydata,1)
        update_plot(x, y)
        annotate_text = f'({x:.2f}, {y:.2f})'
        ax.annotate(annotate_text, (x, y), textcoords="offset points", xytext=(0,10), ha='center')
        plt.draw()
    
        


#connect the mouse click event to the function
start_graph = fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('button_press_event', on_click)
done.on_clicked(done_clicked)
calculate.on_clicked(calculate_clicked)
#enabling interactive cursor annotations
mplcursors.cursor(hover=True)

#set axis labels
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

plt.show()