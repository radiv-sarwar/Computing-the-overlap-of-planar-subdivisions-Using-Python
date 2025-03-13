#  A Python Script to measure the overlap between Planar Subdivisions

For my university project, I developed a Python script designed to measure the overlap between planar subdivisions. A planar subdivision is a division of a plane into distinct regions, formed by a collection of non-intersecting curves, such as edges of polygons. The objective of the project was to create a tool that could accurately analyze the degree of intersection between different subdivisions, helping to quantify how much they share common space.

-   Planar subdivisions divide a plane into distinct regions using non-intersecting curves.
-   The script calculates overlap metrics to quantify shared space between subdivisions.
-   Utilizes computational geometry techniques for accurate analysis.
-   Applicable in fields like GIS, CAD, and graph theory for spatial relationship analysis.


# Files
-   The Python source code is provided as "Python_Compuation_Script.py".
-   The University Final Report is provided as "Final_Project_Report_Radiv_Sarwar.pdf"
-   An compiled executable file is also included for running the program. 
- [Here](https://youtu.be/TA_5xiOI2fA) is a video demonstrating a working example of the python script. 

## Brief run through of the script:

This script contains the following dependencies:

1.  **Matplotlib**: This package will be primarily used for plotting points on the graph. Here we will be specifying two imports from this library:
	- `matplotlib.pyplot as plt`
	- `from matplotlib.widgets import Button`
2.  **Mplcursors**: This package facilitates interaction with the graph, enabling users to place points with a simple click.
	- `import mplcursors`
3.  **Shapely**: This package will be utilized to perform geometric operations on the entities (in this case any polygons) within the program.
	- `from shapely import polygon`

These packages can be installed using the pip package manager. 

I created a scatter plot to draw and showcase the polygons: 
```
fig, ax = plt.subplots()
scatter = ax.scatter([],  [])
ax.set_xlim(left  =  0,  right  =  100)
ax.set_ylim(bottom  =  0,  top  =  100)
```
Buttons were added to act as input from the user and we finally have our canvas to draw polygons on.


![image](https://github.com/user-attachments/assets/6a5b63e1-0759-4e18-9015-27f8dbdede19)

To take mouse clicks as input for different points I
defined the following function:
```
def  update_plot(x,  y):
	scatter.set_offsets([[x, y]])
	poly.append((x,y))
	plt.draw()
```
This function draws the points when we click on the canvas. The function that handles the clicking
event is done by the following function:
```
def  on_click(event):
	if event.inaxes:
	x, y =  round(event.xdata,1),round(event.ydata,1)
	update_plot(x, y)
	annotate_text =  f'({x:.2f}, {y:.2f})'
	ax.annotate(annotate_text,  (x, y),  textcoords="offset points",  xytext=(0,10),  ha='center')
	plt.draw()
```
When we run the program we will receive an interactive matplotlib scatter plot on the
screen as shown before. We can then start providing inputs by clicking on the canvas. We can then place more points around to make a polygon. When we are done placing all the desired points on the plot we click on the draw button. 


![image](https://github.com/user-attachments/assets/3462453d-ccc0-44b7-bfae-b2f848d67109)


Afterwards we will be able to add more points for the second polygon on the graph.
Clicking the draw button will also then complete the second polygon as such

![image](https://github.com/user-attachments/assets/6f4839ee-9167-44dc-b809-aceb299726e2)


We can keep adding more polygons. The final image will look like this with all the shapes that we entered:
![image](https://github.com/user-attachments/assets/10720782-15fe-4010-bf7c-04c04749a916)


We then take the x,y values from the polygon and plot it on the graph. Thus creating the polygon from the input points on the graph. Lastly we add a copy of the list poly to the all_polygons list that collects all the values of the polygons that are being input.
When we are happy with the input we will press the calculate button. This will call on
the function calculate_clicked().
We make all the lists in all polygons into shapely polygons
```
shapely_polys=  []
for p in all_polygons:
shapely_polys.append(Polygon(p))
```
The script now produces all intersection polygons and put them in intersection_polys[] array.
```
intersections =  []

for i in  range(len(shapely_polys)):
		for j in  range(i +  1,  len(shapely_polys)):
				intersection =  shapely_polys[i].intersection(shapely_polys[j])
				if  not intersection.is_empty:
						intersections.append(intersection)
for i in intersections:
		inter_draw = i.exterior.coords
		patch = plt.Polygon(inter_draw,  alpha=0.8)
		ax.add_patch(patch)
		plt.draw()
```
The script finally exports the result into a DCEL format:
```
filename =  "output_in_DCEL.txt"
with  open(filename,  "w")  as file:
		vertex_id =  0
		for polygon_id, intersections in  enumerate(intersections):
# Write the vertices

vertices = intersections.exterior.coords
for i,  (x, y)  in  enumerate(vertices):
		file.write(f"v {vertex_id}  {round(x,2)}  {round(y,2)}\n")
		vertex_id +=  1

# Write the half-edges
num_edges =  len(vertices)
for i in  range(num_edges):
		file.write(f"e {polygon_id*num_edges + i}  {polygon_id*num_edges + i}  {polygon_id*num_edges +  (i+1)  % num_edges}\n")

# Write the face
file.write(f"f {polygon_id*num_edges}\n")
```

The script will output the following overlapped region on the scatter plot as: 

![image](https://github.com/user-attachments/assets/f3c713ad-fec0-4947-b0d8-ef573dfe6775)


Here is a DCEL formatted text file with all the final results:
![image](https://github.com/user-attachments/assets/30416376-59f2-4733-94bc-7a094262253a)


