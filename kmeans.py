#!/usr/bin/python

import math
import random
import sys


def calculate_distance(p1, p2):
    # sqrt[(x2-x1)^2 + (y2-y1)^2]
    return math.sqrt((abs(p2[0] - p1[0]) ** 2) + (abs(p2[1] - p1[1]) ** 2))


def update_clusters(points, centroids, k):
    """ Calculates clusters of points"""
    # clusters = Dict[int k , list points]
    #       int = cluster number (k total clusters)
    #       list = list of points in that cluster
    clusters = {}
    #
    for i in range(k):
        clusters[i] = []
    for i in points:
        euclidean_distance = []
        for j in range(k):
            euclidean_distance.append(calculate_distance(i, centroids[j]))
        # Reports minimum distance from cluster 1 or 2 (if k=2)
        clusterID = euclidean_distance.index(min(euclidean_distance))
        # Whichever cluster the point is closer to, is the cluster the point belongs to
        clusters[clusterID].append(i)
    return clusters


def update_centroids(clusters, centroids, k):
    """ Updates centroids by taking average of all data points in a cluster """
    for i in range(k):
        centroids[i] = [float(sum(point)) / len(point) for point in zip(*clusters[i])]  # column averages
    return centroids


def initiate_centroids(points, k):
    """ Creates K centroids at random spots within our data set

    Parameters
    ----------
    points : List[List[int]]
        x,y coordinates of our data points
    k : int
        number of clusters

    Returns
    -------
    centroids : List[List[int]]
        An initial list of centers
    """
    # Get min and max for better random numbers
    x_min = min(point[0] for point in points)  # min of x-coords
    x_max = max(point[0] for point in points)  # max of x-coords
    y_min = min(point[1] for point in points)  # min of y-coords
    y_max = max(point[1] for point in points)  # max of y-coords

    # random.seed(0)  # delete later for more pseudorandom-ness
    centroids = []
    for cluster in range(k):
        rand_x = random.randint(x_min, x_max)
        rand_y = random.randint(y_min, y_max)
        newCentroid = [rand_x, rand_y]
        centroids.append(newCentroid)
    return centroids

def main():
    # Arbitrary number of iterations
    # If I wanted to improve time, I would find when my centroids
    # do not change anymore and then stop.
    global filename
    stopAt = 10

    # Sanity checks
    # Check arguments = 2
    if len(sys.argv) != 3:
        print("ERROR: Please enter two arguments. (kmeans.py <k> <textfile>")
        exit()
    # Check if k is integer and k>1
    else:
        try:
            k = int(sys.argv[1])
        except ValueError:
            print("ERROR: k entered is not an integer.")
            exit()
        if k < 2:
            print("ERROR: Enter a k value >1")
            exit()
        filename = sys.argv[2]
    # end sanity checks

    # Open file
    with open(filename) as f:
        points = [[int(x) for x in line.split()] for line in f]
        # points = [x + [-1] for x in points]   # add cluster column

    # Initializing centroids with random points
    centroids = initiate_centroids(points, k)

    # Running cluster and centroid recalculation for n-iterations
    for i in range(stopAt):
        clusters = update_clusters(points, centroids, k)
        centroids = update_centroids(clusters, centroids, k)

    #     DEBUG      #
    # print("points:")
    # print(points)
    #
    # print("clusters:")
    # print(clusters)
    #
    # print("centroids:")
    # print(centroids)
    #                #

    # Output to file
    o = open("output.txt", "w")
    # Prep data for expected output ex. [669, 214] -> 669 214 1
    for i in range(k):
        for j in range(len(clusters[i])):
            o.write(str(clusters[i][j]).strip('[]').replace(',', '') + " " + str(i + 1) + "\n")
    print("\nOutput written to output.txt")
    o.close()


if __name__ == "__main__":
    main()
