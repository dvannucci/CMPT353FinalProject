import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from sklearn.cluster import KMeans

def main():

    print("List of values in neighbourhood: \n(nightlife, fitness, activities, leisure, family, pets, safety)")
    listofvalues = ['nightlife','fitness','activities', 'leisure', 'family', 'pets', 'safety']

    value1 = input("Enter first value: ")
    value2 = input("Enter second value: ")
    value3 = input("Enter third value: ")

    # included error messages in case typo in input

    if(value1 not in listofvalues or value2 not in listofvalues or value3 not in listofvalues):
        print("ERROR not a value")
        return

    print("List of transportation: \n(car, bike, public)")
    listoftransport = ['car','bike','public']
    transportation = input("Enter main mode of transportation: ")

    if(transportation not in listoftransport):
        print("ERROR incorrect transportation")
        return

    firstdf = pd.read_json(value1 + '_data.json')
    seconddf = pd.read_json(value2 + '_data.json')
    thirddf = pd.read_json(value3 + '_data.json')
    transportdf = pd.read_json(transportation + '_data.json')

    # merged the 3 dataframes of the 3 values chosen by user

    group = pd.concat([firstdf,seconddf,thirddf,transportdf])

    # filtered data to just Vancouver, not including Burnaby, Richmond, etc ..
    group = group[(group['lat']>= 49.2 )&(group['lat'] <= 49.3) & (group['lon'] >= -123.225 )&(group['lon'] <= -123.025)]

    # adapted from https://medium.com/python-in-plain-english/mapping-with-pythons-geopandas-2869bb758b08
    # data from https://opendata.vancouver.ca/pages/home/
    bnd_gdf = gpd.read_file('boundary/local-area-boundary.shp')
    ps_gdf = gpd.read_file('public-streets/public-streets.shp')

    fig, ax = plt.subplots(1, figsize = (16,8))

    bnd_gdf.plot(ax = ax, color = 'black')
    ps_gdf.plot(ax = ax, color = 'white', alpha = 0.4)
    plt.scatter(group['lon'],group['lat'], color = 'red')

    plt.title('Amenities of\n Vancouver, BC', loc = 'left', fontsize = 20)

    ax.axis('off')

    plt.show()

    # clustering https://datascience.stackexchange.com/questions/761/clustering-geo-location-coordinates-lat-long-pairs

    arr = [[x,y] for x,y in zip(group['lon'],group['lat'])]
    X = np.reshape(arr,(int(len(arr)),2))
    model = KMeans(n_clusters=10)
    y = model.fit_predict(X)

    fig, ax = plt.subplots(1, figsize = (16,8))

    bnd_gdf.plot(ax = ax, color = 'black')
    ps_gdf.plot(ax = ax, color = 'white', alpha = 0.4)

    # adapted from https://medium.com/pursuitnotes/k-means-clustering-model-in-6-steps-with-python-35b532cfa8ad

    plt.scatter(X[y==0, 0], X[y == 0, 1], s=100, c='red', label ='Cluster 1')
    plt.scatter(X[y==1, 0], X[y ==1, 1], s=100, c='blue', label ='Cluster 2')
    plt.scatter(X[y==2, 0], X[y ==2, 1], s=100, c='green', label ='Cluster 3')
    plt.scatter(X[y==3, 0], X[y ==3, 1], s=100, c='yellow', label ='Cluster 4')
    plt.scatter(X[y==4, 0], X[y ==4, 1], s=100, c='orange', label ='Cluster 5')
    plt.scatter(X[y==5, 0], X[y ==5, 1], s=100, c='cyan', label ='Cluster 6')
    plt.scatter(X[y==6, 0], X[y ==6, 1], s=100, c='purple', label ='Cluster 7')
    plt.scatter(X[y==7, 0], X[y ==7, 1], s=100, c='magenta', label ='Cluster 8')
    plt.scatter(X[y==8, 0], X[y ==8, 1], s=100, c='pink', label ='Cluster 9')
    plt.scatter(X[y==9, 0], X[y ==9, 1], s=100, c='crimson', label ='Cluster 10')
    ax.axis('off')
    plt.show()

if __name__=='__main__':
    main()
