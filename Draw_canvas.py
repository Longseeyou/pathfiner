import tkinter as tk
import heapq
from tkinter import ttk
import copy
GRID_COLOR = "black"
PADDING = 2.5
SIZE = 32
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0
start = None
end = None
edges = []
poly = []
new_poly = []
K = 1
points_num = 0
g = {}

def gen_adj_list():
    global g, new_poly, edges
    g[len(new_poly)] = []
    g[len(new_poly) + 1] = []
    for edge in edges:
        u, v = edge
        g[u].append((v, distance(new_poly[u], new_poly[v])))
        g[v].append((u, distance(new_poly[v], new_poly[u])))
    for i in range(len(new_poly)):
        check = True
        for edge in edges:
            point1 = new_poly[edge[0]]
            point2 = new_poly[edge[1]]
            if cut(start, new_poly[i], point1, point2):
                if(start == point1 or start == point2 or new_poly[i] == point1 or new_poly[i] == point2):
                    pass
                else:
                    check = False
                    break
        if check:
            g[len(new_poly)].append((i, distance(new_poly[i], start)))
            g[i].append((len(new_poly), distance(new_poly[i], start)))
    for i in range(len(new_poly)):
        check = True
        for edge in edges:
            point1 = new_poly[edge[0]]
            point2 = new_poly[edge[1]]
            if cut(end, new_poly[i], point1, point2):
                if(end == point1 or end == point2 or new_poly[i] == point1 or new_poly[i] == point2):
                    pass
                else:
                    check = False
                    break
        if check:
            g[len(new_poly)+1].append((i, distance(new_poly[i], end)))
            g[i].append((len(new_poly)+1, distance(new_poly[i], end)))
    
def dijkstra():
    global g, new_poly
    gen_adj_list()
    distance = {node: float('inf') for node in g}
    parent = {node: None for node in g}
    print("g:", g[len(new_poly)])
    path = []
    distance[len(new_poly)] = 0
    pq = [[0, len(new_poly)]]
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if (current_dist != distance[current_node]):
            pass
        for v, w in g[current_node]:
            if current_dist + w < distance[v]:
                distance[v] = distance[current_node] + w
                parent[v] = current_node
                heapq.heappush(pq, [distance[v], v])
    u = len(new_poly)+1
    while u != len(new_poly):
        path.append(u)
        u = parent[u]
    path.append(len(new_poly))
    path.reverse()
    return path

def in_polygon(map, x, y):
    inside = False
    for u in range(len(map) - 1):
        xu, yv = map[u]
        xv, yu = map[u + 1]

        if yv > yu:
            xu, xv = xv, xu
            yv, yu = yu, yv

        if y > yv and y <= yu and x <= xu + (xv - xu) * (y - yv) / (yu - yv):
            inside = not inside

    return inside

def draw_point(x, y, status):
    # x, y = make_point(x, y)
    canvas.create_oval(x - PADDING, y - PADDING, x + PADDING, y + PADDING, fill="red", tags=status)

def make_point(x, y):
    orig_x = x/SIZE
    orig_y = y/SIZE
    orig_x = round(orig_x)
    orig_y = round(orig_y)
    return (orig_x*SIZE, orig_y*SIZE)

def on_click(event):
    global points_num, start, end, new_poly
    if(points_num < 2 and in_polygon(new_poly, event.x, event.y)):    
        points_num += 1
        if(points_num == 1):
            start = [event.x, event.y]
            draw_point(event.x, event.y, "start")
        else:
            end = [event.x, event.y]
            draw_point(event.x, event.y, "end")
            path = dijkstra()
            new_poly.append(start)
            new_poly.append(end)
            for i in range(1, len(path)):
                print(i)
                canvas.create_line(new_poly[path[i-1]], new_poly[path[i]], fill="green")
       
def gen_edges():
    global edges
    global new_poly
    edges.clear()
    for i in range(len(new_poly)-1):
        edges.append([i, i+1])
    edges.append([len(new_poly)-1, 0])

def read_map():
    f = open("Vert1.txt", "r")
    for i in range(28):
        poly.append(list(map((int), f.readline().split())))
        poly[i][0] = poly[i][0] * SIZE
        poly[i][1] = poly[i][1] * SIZE
    f.close()

def orientation(A, B, C):
    xA, yA = A
    xB, yB = B
    xC, yC = C
    area = (yB-yA)*(xC-xB) - (xB-xA)*(yC-yB)
    return 1 if area > 0 else -1 if area < 0 else 0

def on_segment(A, B, C):
    if min(A[0], B[0]) <= C[0] <= max(A[0], B[0]) and min(A[1], B[1]) <= C[1] <= max(A[1], B[1]):
        return True
    return False

def cut(A, B, C, D):
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(A, B, C):
        return True
    if o2 == 0 and on_segment(A, B, D):
        return True
    if o3 == 0 and on_segment(C, D, A):
        return True
    if o4 == 0 and on_segment(C, D, B):
        return True
    return False

def distance(A, B):
    return (A[0]-B[0])**2 + (A[1]-B[1])**2

def gen_visibility():
    global edges, new_poly, g
    for i in range(len(new_poly)):
        for j in range(i+1, len(new_poly)):
            check = True
            for k in range(len(edges)):
                if (new_poly[i] == new_poly[edges[k][0]] or new_poly[i] == new_poly[edges[k][1]]) and (new_poly[j] == new_poly[edges[k][1]] or new_poly[j] == new_poly[edges[k][0]]):
                    check = False
                    break
            if(check):
                for k in range(len(edges)):
                    if cut(new_poly[i], new_poly[j], new_poly[edges[k][0]], new_poly[edges[k][1]]):
                        if new_poly[i] == new_poly[edges[k][0]] or new_poly[i] == new_poly[edges[k][1]] or new_poly[j] == new_poly[edges[k][1]] or new_poly[j] == new_poly[edges[k][0]]:
                            pass
                        else:
                            check = False
                            break
            if(check):
                mid = ((new_poly[i][0]+new_poly[j][0])//2, (new_poly[i][1]+new_poly[j][1])//2)
                if(in_polygon(new_poly, mid[0], mid[1])):
                    canvas.create_line(new_poly[i], new_poly[j], fill="red", tag="visibility")
                    if(i not in g):
                        g[i] = []
                    if(j not in g):
                        g[j] = []
                    g[i].append((j, distance(new_poly[i], new_poly[j])))
                    g[j].append((i, distance(new_poly[i], new_poly[j])))

def draw_grid():
    MAP_WIDTH = WINDOW_WIDTH // SIZE
    MAP_HEIGHT = WINDOW_HEIGHT // SIZE
    for i in range(int(MAP_WIDTH) + 1):
        canvas.create_line(i * SIZE, 0, i * SIZE, MAP_HEIGHT * SIZE, fill=GRID_COLOR, width=0.1)
    for i in range(int(MAP_HEIGHT) + 1):
        canvas.create_line(0, i * SIZE, MAP_WIDTH * SIZE, i * SIZE, fill=GRID_COLOR, width=0.1)

def updateK():
    global poly
    global new_poly
    canvas.delete("path", "visibility")
    if(not(K_val.get() == "")):
        K = int(K_val.get())
    if K > 0:
        new_poly = copy.deepcopy(poly) 
    for j in range(K-1):
        new_poly.pop(len(new_poly)-2*(j+1)-1)
        new_poly.pop(len(new_poly)-2*(j+1)-1)
        for k in range(2, len(poly), 1):
            new_poly.insert(len(new_poly)-2*(j+1), [poly[k][0]+(j+1)*9*SIZE, poly[k][1]+(j+1)*8*SIZE])
    canvas.create_polygon(new_poly, fill="", outline="black", width=3, tags = "path")
    gen_edges()
    gen_visibility()

def updateSIZE():
    canvas.delete("all")
    global SIZE
    global poly
    for i in range(len(poly)):
        poly[i][0] = poly[i][0] // SIZE
        poly[i][1] = poly[i][1] // SIZE
    SIZE = int(SIZE_val.get())
    draw_grid()
    for i in range(len(poly)):
        poly[i][0] = poly[i][0] * SIZE
        poly[i][1] = poly[i][1] * SIZE
    updateK()

def reset():
    global start, end, points_num, g, new_poly
    canvas.delete("start", "end")
    start, end = None, None
    points_num = 0
    g[len(new_poly)].clear()
    g[len(new_poly) + 1].clear()

def main():
    global window
    window = tk.Tk()
    window.title("DIJKSTRA")
    window.resizable(False, False)
    global WINDOW_HEIGHT
    global WINDOW_WIDTH
    global SIZE
    if WINDOW_HEIGHT == 0:
        WINDOW_HEIGHT = window.winfo_screenheight() * 3 / 4
    if WINDOW_WIDTH == 0:
        WINDOW_WIDTH = window.winfo_screenwidth() * 3 / 4
    window.geometry(
        "%dx%d+%d+%d"
        % (
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            window.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2,
            window.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2,
        )
    )

    global canvas
    global K
    global poly
    global K_val
    global SIZE_val
    global points_num
    global start
    global end
    global edges
    global g
    K_val = tk.StringVar()
    SIZE_val = tk.StringVar()
    root_frame = tk.Frame(window).pack(padx=PADDING, pady=PADDING)
    menu_frame = tk.Frame(root_frame)
    menu_frame.pack(side=tk.TOP, padx=PADDING, pady=PADDING, fill="x")
    K_entry = tk.Entry(menu_frame, textvariable=K_val).pack(side = tk.LEFT, padx=PADDING, pady=PADDING, anchor="nw")
    updateK_button = tk.Button(menu_frame, text="Update", command=updateK).pack(side = tk.LEFT, padx=PADDING, pady=PADDING, anchor="nw")
    SIZE_entry = tk.Entry(menu_frame, textvariable=SIZE_val).pack(side = tk.LEFT, padx=PADDING, pady=PADDING, anchor="ne")
    updateSIZE_button = tk.Button(menu_frame, text="Update", command=updateSIZE).pack(side = tk.LEFT, padx=PADDING, pady=PADDING, anchor="ne")
    reset_button = tk.Button(menu_frame, text="Reset", command=reset).pack(side = tk.RIGHT, padx=PADDING, pady=PADDING, anchor="ne")
    canvas = tk.Canvas(root_frame, bg="#ffffff")
    canvas.pack(side=tk.BOTTOM, padx=PADDING, pady=PADDING, expand=True, fill="both", anchor="sw")
    global CANVAS_WIDTH
    global CANVAS_HEIGHT
    canvas.update()
    CANVAS_WIDTH = canvas.winfo_width()
    CANVAS_HEIGHT = canvas.winfo_height()
    canvas.bind("<Button-1>", on_click)

    draw_grid()
    read_map()

    window.mainloop();


if __name__ == "__main__":
    main()