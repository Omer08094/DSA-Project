import tkinter as tk
import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation
import numpy as np
from tkinter import simpledialog
import tkinter.messagebox as messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



# file = open("dataset.csv")
# data = list(csv.reader(file, delimiter=","))
# file.close()
file = open("Bus_data.csv")
data = list(csv.reader(file, delimiter=","))
file.close()
def addNodes(G, Nodes):
    for x in Nodes:
        G[x] = []
    return G

def addEdges(G,edges,directed):
    if directed == True:
        for x in edges:
            G[x[0]].append((x[1],x[2]))
    else:
        for x in edges:
            G[x[0]].append((x[1],x[2]))
            G[x[1]].append((x[0],x[2]))
    return (G)
graph = {}
nodes = []
edgelist = []
guilist = []
for x in data:
    index = x[0].find('-')
    key = x[0][:index]
    key = key.strip(' ')
    if key not in nodes:
        nodes.append(key)
    equal = x[0].find('=')
    edge = x[0][index+4:equal]
    edge = edge.strip(' ')
    if edge not in nodes:
        nodes.append(edge)
    weight = x[0][equal+2:]
    weight =weight.strip(' ')
    weight = int(weight)
    tup = (key,edge,weight)
    tup1 = (key,edge)
    guilist.append(tup1)
    edgelist.append(tup)

addNodes(graph,nodes)
addEdges(graph,edgelist,False)

def hash_function(key,size): 
    if key.isnumeric() == True:
        return int(key) % size
    
    sum1 = 0 
    for i in range(len(key)):
        sum1 = sum1 + ord(key[i])
    return sum1 % size


def rehash(old_hash, size, iteration):
 return (old_hash + iteration) % size


def put(keys, values, key, size):
    slotindex = hash_function(key,size)
    if keys[slotindex] == None or keys[slotindex] == key:
        keys[slotindex] = key
        values[slotindex] = str(slotindex)
    else:
        iteration = 1
        for x in range(size):
            slotindex2 = rehash(slotindex,size,iteration)
            if keys[slotindex2] == None or keys[slotindex2] == key:
                keys[slotindex2] = key
                values[slotindex2] = str(slotindex2)
                break
            else:
                iteration+=1
 
def get(keys,values,key,size):
    slotindex = hash_function(key,size)
    data = None
    if keys[slotindex] == key:
        data = values[slotindex]
    else:
        iteration = 1
        for x in range(size):
            slotindex2 = rehash(slotindex,size,iteration)
            if keys[slotindex2] == None or keys[slotindex2] == key:
                data = values[slotindex2]
                break
            else:
                iteration+=1
    return data

def delitem(keys,values,key,size):
    slotindex = hash_function(key,size)
    if keys[slotindex] != None and keys[slotindex] == key:
        keys[slotindex] = None
        values[slotindex] = None
    else:
        iteration = 1
        for x in range(size):
            slotindex2 = rehash(slotindex,size,iteration)
            if keys[slotindex2] != None and keys[slotindex2] == key:
                keys[slotindex2] = None
                values[slotindex2] = None
                break
            else:
                iteration+=1


def enqueue(queue, item, priority):
    for i, (p, _) in enumerate(queue):
        if p > priority:
            queue.insert(i, (priority, item))
            return
    queue.append((priority, item))


def dequeue(queue):
    a =queue.pop(0)
    return a

def is_empty(queue):
    if len(queue) == 0:
        return True
    else:
        return False

def getNeighbors(g,n):
    lst=[]
    for i in g[n]:
        lst.append(i[0])
    return (lst)



# Use insertion sort here


def insertion_sort(lst):
    for i in range(1,len(lst)):
        to_sort = lst[i]
        to_sort_index = i
        index = i
        for j in range(i,-1,-1):
            if to_sort <= lst[j]:
                index = j
        lst.pop(to_sort_index)
        lst.insert(index,to_sort)
    return lst
nodes = insertion_sort(nodes)



# Define a function to calculate the bus stop path between two bus stops


def calculate_path(graph, start_stop, end_stop):
    # Use Dijkstra's algorithm to find the shortest and cheapest path
    D = {node: [float("inf"), ()] for node in graph}
    D[start_stop] = [0, ()]
    Q = [(0, start_stop)]
    visited = []

    while Q:
        _, v = dequeue(Q)
        if v not in visited:
            visited.append(v)
            connections = getNeighbors(graph, v)
            for neighbor in connections:
                for edge in graph[v]:
                    if edge[0] == neighbor:
                        weight = edge[1]
                if D[v][0] + weight < D[neighbor][0]:
                    D[neighbor][0] = D[v][0] + weight
                    D[neighbor][1] = (v, neighbor)
                    enqueue(Q, neighbor, D[neighbor][0])

    path1 = []
    v = end_stop
    while v != start_stop:
        if D[v][1] != ():
            path1.append(D[v][1])
            v = D[v][1][0]
        else:
            path1 = None
            break

    if path1 is not None:
        path1.reverse()
        path = [start_stop] + [x[1] for x in path1]
        distance = D[end_stop][0]
        fare = distance * 10
    else:
        path = None
        distance = 0
        fare = 0
    path2 = []
    path3 = []
    if path != None:
        for x in range(1,len(path)):
            for node in graph[path[x-1]]:
                if node[0] == path[x]:
                    weight = node[1]
                    time = float(weight)*1.2
                    tup = (path[x-1],path[x],weight)
                    tup2 = (path[x-1],path[x],(str(weight)+'km',str(time)+'mins'))
                    if tup not in path2:
                        path2.append(tup)
                    if tup2 not in path3:
                        path3.append(tup2)
                        break
        time = int(time)
    else:
        time = None
        path2 = None
        path3 = None                
    # Return the results
    return {'path': path, 'distance': distance, 'fare': fare, 'path1': path1, 'path2': path2, 'path3': path3, 'time': time}


# Create the GUI
root = tk.Tk()
root.config(bg='#708090')
root.geometry('500x250')
root.title("Karachi Bus Stop Calculator")



# Create the start stop selector
start_label = tk.Label(root, text="Select Your Start Stop:",bg='#708090')
start_label.pack()
start_stop_var = tk.StringVar()
start_stop_dropdown = tk.OptionMenu(root, start_stop_var, *nodes)
start_stop_dropdown.pack()

# Create the end stop selector
end_label = tk.Label(root, text="Select Your End Stop:",bg='#708090')
end_label.pack()
end_stop_var = tk.StringVar()
end_stop_dropdown = tk.OptionMenu(root, end_stop_var, *nodes)
end_stop_dropdown.pack()



# Create the calculate button
def calculate():
    start_stop = start_stop_var.get()
    end_stop = end_stop_var.get()
    result = calculate_path(graph,start_stop, end_stop)
    root.geometry('500x350')
    if result['path'] != None:
        path_label.configure(text=f"Path: {' -> '.join(result['path'])}")
        distance_label.configure(text=f"Total distance: {result['distance']} km")
        fare_label.configure(text=f"Total fare: Rs. {result['fare']}")
        key_label.configure(text=f'All labels on the map are in km')
    else:
        path_label.configure(text=f"No paths available")
        distance_label.configure(text=f"Total distance: {result['distance']} km")
        fare_label.configure(text=f"Total fare: Rs. {result['fare']}")
    G = nx.Graph()
    if result['path1'] != None:
        # Create the seat booking label
        seat_booking_label = tk.Label(root, text="Seat Booking & Cancellation:",bg='#708090')
        seat_booking_label.pack()
        # Create the Book Seat button
        book_seat_button = tk.Button(root, text="Book Seat",bg="darkorange", fg="whitesmoke",command=book_seat)
        book_seat_button.pack()

        # Create the cancel booking button
        cancel_booking_button = tk.Button(root, text="Cancel Booking",bg="darkorange",fg="whitesmoke", command=cancel_booking)
        cancel_booking_button.pack()

        

        # define a function to update the bus position
        path=result["path"]
        G.add_nodes_from(result["path"])
        path1=result["path1"]
        G.add_weighted_edges_from(result['path2'])
        labels = nx.get_edge_attributes(G,'weight')

        # create a figure and axis
        fig, ax = plt.subplots(figsize=(12, 10))
        fig.set_facecolor('slategrey')

        # set the node positions
        pos = nx.spring_layout(G)

        # draw the graph
        nx.draw_networkx_nodes(G, pos, node_color='darkorange', node_size=1000, ax=ax)
        nx.draw_networkx_labels(G, pos, font_color="whitesmoke",font_size=7, font_weight='bold', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path1, edge_color='darkgrey',width=2, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)

        # add a bus image to the plot
        bus_image = plt.imread('bus.png')
        bus_offset = 0.0001
        busbox = OffsetImage(bus_image, zoom=0.07)
        busbox.image.axes = ax
        bus = AnnotationBbox(busbox, (0, 0), xycoords='data', frameon=False)
        ax.add_artist(bus)

        # calculate the positions along each edge
        edge_positions = {}
        for edge in path1:
            u, v = edge
            points = np.linspace(pos[u], pos[v], num=50, endpoint=True)
            edge_positions[edge] = points

        # define a function to update the bus position
        def update_bus(i):
            # calculate the current position of the bus
            path_idx = i // 50
            edge = path1[path_idx]
            points = edge_positions[edge]
            point_idx = i % 50
            point = points[point_idx]
            x, y = point[0] - bus_offset, point[1] - bus_offset
            bus.xyann = (x, y)
            return bus,

        # create the animation
        ani = FuncAnimation(fig, update_bus, frames=len(path1)*50, interval=5, blit=True)

        # for printing in the same window

        # show the plot
        # plt.axis('off')
        # plt.title('BUS ROUTE',color='whitesmoke',weight='bold')
        # canvas = FigureCanvasTkAgg(fig, root)
        # canvas.draw()
        # canvas.get_tk_widget().pack()
        # toolbar = NavigationToolbar2Tk(canvas,root)

        # show the plot
        plt.axis('off')
        plt.title('BUS ROUTE',color='whitesmoke',weight='bold')
        plt.show()

    # placing the toolbar on the Tkinter window
    # canvas.get_tk_widget().pack()
        
        

# Create the seat booking label
seat_booking_label = tk.Label(root, text="")
seat_booking_label.pack()

keys = [None]*30
values = [None]*30
booked_seats = []
# Create the book seat button
def book_seat():
    start_stop = start_stop_var.get()
    end_stop = end_stop_var.get()
    if start_stop != None and end_stop != None:
        result = calculate_path(graph, start_stop, end_stop)
        if result['path'] is not None:
            # Prompt the user to enter their name
            name = tk.simpledialog.askstring("Enter Name", "Please enter your full name:")
            if name:
                # Use your custom hashing algorithm to generate the seat number
                if None in keys:
                    put(keys,values,name,30)
                    seat_number = get(keys,values,name,30)
                    booked_seats.append(name)
                else:
                    seat_number = 'Sorry, no seats available'
                # Display the ticket details in a separate window
                ticket_details = f"Name: {name}\nSeat Number: {seat_number}\nStart Stop: {start_stop}\nDestination: {end_stop}\nDistance: {result['distance']} km\nFare: Rs. {result['fare']} \nEstimated Time: {result['time']} mins \nPlease take a screenshot of this. \nThankyou and Safe travles :)"
                messagebox.showinfo("Ticket Details", ticket_details)
                # show_dark_message_box("Ticket Details", ticket_details)
                seat_booking_label.configure(text=f"Seat booked successfully! Seat Number: {seat_number}",bg='#708090')
            else:
                seat_booking_label.configure(text="Invalid name. Please try again.",bg='#708090')
        else:
            seat_booking_label.configure(text="No paths available for booking",bg='#708090')
    

    
def cancel_booking():
        # Prompt the user to enter their name
        name = simpledialog.askstring("Enter Name", "Please enter your name:")
        if name:
            # Check if the name exists in the booked seats list
            if name in booked_seats:
                # Remove the seat booking for the given name
                delitem(keys,values,name,30)
                messagebox.showinfo("Cancellation", f"Booking for {name} has been canceled.")
                seat_booking_label.configure(text=f"Booking canceled for {name}")
            else:
                messagebox.showinfo("Cancellation", f"No booking found for {name}.")
                seat_booking_label.configure(text=f"No booking found for {name}.")
        else:
            seat_booking_label.configure(text="Invalid name. Please try again.")



calculate_button = tk.Button(root, text="Calculate", bg="darkorange",fg="whitesmoke" ,command=calculate)
calculate_button.pack()

# Create the result labels
path_label = tk.Label(root, text="",bg='#708090')
path_label.pack()
distance_label = tk.Label(root, text="",bg='#708090')
distance_label.pack()
fare_label = tk.Label(root, text="",bg='#708090')
fare_label.pack()
key_label = tk.Label(root, text="", bg = '#708090')
key_label.pack()

root.mainloop()