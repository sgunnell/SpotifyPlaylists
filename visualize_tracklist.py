import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
#plt.style.use("seaborn")
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA



df = pd.read_csv('data/tracklist.csv')

print(df.head())  
print(df.describe())   
print(df.info())

df.dropna(inplace=True)
#columns_to_use = added_at,id,name,popularity,uri,artist,album,release_date,duration_ms,length,danceability,acousticness,energy,instrumentalness,liveness,loudness,speechiness,tempo,time_signature,valence,mode,key
#columns_to_use = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'liveness', 'valence', 'tempo', 'duration_ms', 'release_date']
columns_to_use = ['danceability', 'energy', 'valence', 'tempo']
df['release_date']= df['release_date'].astype(str).str[:4]
df1 = df[columns_to_use]
col_features = df[columns_to_use]

fig,axes = plt.subplots(2,2,figsize=(15,8))

for i in range(0,2):
    for j in range(0,2):
        #print(columns_to_use[(i)*3+j])
        #if (i)*3+j < 5:
        axes[i,j].hist(df1[columns_to_use[(i)*2+j]])
        axes[i,j].set_title(columns_to_use[(i)*2+j],fontsize=15)
plt.show()
#for i,col in enumerate(columns_to_use):

#df1 = MinMaxScaler().fit_transform(df[columns_to_use])
df1 = (df1 - df1.mean()) / df1.std()
# Initialize an empty list to store the sum of squared distances for each number of clusters
sse = [] 

# Fit the KMeans model to the data with a range of different numbers of clusters
for k in range(1, 37):
    kmeans = KMeans(n_clusters = k,     
                    init = 'k-means++',                 # Initialization method for kmeans
                    max_iter = 300,                     # Maximum number of iterations 
                    n_init = 10,                        # Choose how often algorithm will run with different centroid 
                    random_state = 0)
    kmeans.fit(df1)
    sse.append(kmeans.inertia_)  # Add the sum of squared distances for the current number of clusters to the list


# Plot the sum squared distances for each number of clusters for elbow method

plt.plot(range(1, 37), sse)
plt.title('Elbow Method for Clustering')
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squared distances')
plt.show()

print("considering the elbow method and personal prefence enter number of playlists:")
user_clusters = int(input())
# Initialize the KMeans model with 8 clusters
kmeans = KMeans(n_clusters=user_clusters, random_state=1,n_init="auto")

# Fit the model to the data
kmeans.fit(df1)  

# Generate cluster assignments for each data point
clusters = kmeans.predict(df1)
df['kmeans']=kmeans.labels_
# Print the cluster assignments for the first few data points
print(clusters[:10])

# Calculate the silhouette score for the generated clusters
print(silhouette_score(df1, clusters))



# To visualize the generated clusters, we will first need to reduce the data to two dimensions
# so that we can plot it on a scatter plot

pca = PCA(n_components=2)  # Initialize a PCA model with 2 components
df_2d = pca.fit_transform(df1)  # Reduce the data to two dimensions using the PCA model

# Plot the data points on a scatter plot
# Coloring the data points according to their cluster assignment
plt.scatter(df_2d[:, 0], df_2d[:, 1], c=clusters)
plt.title('Clustering Of Spotify Songs')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.show()


# Get the unique cluster assignments
unique_clusters = np.unique(clusters)

# Create a grid of subplots
fig, axs = plt.subplots(nrows=6, ncols=6, figsize=(8, 8), sharex=True, sharey=True)

# Flatten the array of subplots to make it easier to iterate over
axs = axs.flatten()

# Iterate over the clusters
for i, cluster in enumerate(unique_clusters):
    # Select the data points belonging to the current cluster
    df_cluster = df_2d[clusters == cluster]
    
    # Select the data points belonging to other clusters
    df_other_clusters = df_2d[clusters != cluster]
    
    # Plot the data points belonging to other clusters in gray
    axs[i].scatter(df_other_clusters[:, 0], df_other_clusters[:, 1], c='gray', label='Other clusters', alpha=0.5)
    
    # Plot the data points belonging to the current cluster with a different color
    axs[i].scatter(df_cluster[:, 0], df_cluster[:, 1], c='red', label='Cluster {}'.format(cluster))
    
    # Set the x and y labels for the current subplot
    axs[i].set_xlabel('Component 1')
    axs[i].set_ylabel('Component 2')
    
    # Add a legend to the current subplot
    axs[i].legend()

plt.show()

# First, let's create a new dataframe with the cluster assignments as a column
clustered_df = df1.copy()
clustered_df['cluster'] = clusters

# Now, we can examine the characteristics of the individual clusters
# For example, we can group the data by cluster and compute the mean of each column
cluster_means = clustered_df.groupby('cluster').mean()
print(cluster_means)

# We can also compare the clusters to each other by creating a plot of the cluster means
# This can help us to see how the clusters differ from each other
cluster_means.plot(kind='bar')
plt.title('Cluster Characteristics')
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.show()

#print(df.groupby(['kmeans']).mean())

cluster_list = ["cluster"+str(user_clusters)+"_"+str(i) for i in range(user_clusters)]
print(cluster_list)
cluster_dict = {}
print(df.head())
df2 = df[['id','name','artist','kmeans']]
for i,cluster in enumerate(cluster_list):
    df2[df2['kmeans']==i].to_csv("data/"+cluster+".csv",index=False)

