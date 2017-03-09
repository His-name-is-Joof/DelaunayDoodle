import cv2
import numpy as np
import random

def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True

def centroid(cartesion_points):
    val = np.sum(cartesion_points, axis=0)
    val = val / cartesion_points.shape[0]
    return val
    

def draw_delaunay(img, subdiv, delaunay_color):
    triangleList = subdiv.getTriangleList()
    size = img.shape
    print(size)
    r = (0, 0, size[1], size[0])

    for t in triangleList:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        arr = [pt1, pt2, pt3]
        triangle = np.array(arr, 'int32')
        center = centroid(triangle)
        color = int(255 - 130 * (center[1] / size[0])) - random.randint(0, 10)

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            cv2.fillConvexPoly(img, triangle, color)

if __name__ == '__main__':
    win_delaunay = "Delaunay Triangulation"
    animate = True
    delaunay_color = (255, 255, 255)
    width = 1500
    height = 1500

    #img = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
    img = np.zeros((width, height), np.uint8)
    img_orig = img.copy();

    size = img.shape
    rect = (0, 0, size[1], size[0])

    subdiv = cv2.Subdiv2D(rect);

    points = []
    points.append((0, 0))
    x = width - 1
    y = height - 1
    iters = 20
    points.append((x, y))
    for i in range(0, iters):
        points.append((0, i * (y / iters)))
        points.append((x, i * (y / iters)))
        points.append((i * (x / iters), 0))
        points.append((i * (x / iters), y))
    for i in range(0, 300):
        points.append((random.randint(0, y), random.randint(0, y)))

    #with open("points.txt") as file:
    #    for line in file:
    #        x, y = line.split()
    #        points.append((int(x), int(y)))

    for p in points:
        subdiv.insert(p)

    draw_delaunay(img, subdiv, (255, 255, 255) )
    img = cv2.applyColorMap(img, cv2.COLORMAP_WINTER)
    cv2.imwrite("delaunay.jpg", img)
