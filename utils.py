import numpy as np

class SupportResistance():
    
    def set_histogram(self, data):
        histogram = np.histogram(data, bins=self.nb_bins)
        return histogram[0], [[histogram[1][i], histogram[1][i+1]] for i in range(len(histogram[1])-1)]
    
    def denoise(self, hist_count):
        noise = self.divider // 10
        return np.array([0 if value <= noise else value for value in hist_count])
    
    def set_clusters_edge(self):
        self.hist_count_denoise[0] = 0
        clusters_index = []
        for i in range(1, len(self.hist_count_denoise)):
            if self.hist_count_denoise[i]:
                if not self.hist_count_denoise[i-1]:
                    clusters_index.append([])
                clusters_index[-1].append(i)
        clusters_edge_index = [[clusters_index[i][0], clusters_index[i][-1]] for i in range(len(clusters_index)) if len(clusters_index[i]) > self.nb_bins // 20]
        return np.array([[self.hist_edge[i[0]][0], self.hist_edge[i[1]][1]] for i in clusters_edge_index])
    
    def set_centroids(self):
        return np.array([arr.mean() for arr in self.clusters_edge])
    
    def kmeans_algorithm(self, data, centroids):
        clusters_variance = np.array([np.abs(data - value) for value in centroids])
        return np.array([value.argmin() for value in clusters_variance.T])
    
    def set_support_resistance(self, data):
        return np.array([[data[np.where(self.clusters_labels == c_l)].min(), data[np.where(self.clusters_labels == c_l)].max()] for c_l in np.unique(self.clusters_labels)])
    
    def get_limits(self, last_data):
        for s_r in self.support_resistance:
            if s_r[0] <= last_data <= s_r[1]:
                return s_r
    
    def __init__(self, data):
        self.divider = 1000
        self.nb_bins = data.size // self.divider
        
        self.hist_count, self.hist_edge = self.set_histogram(data)
        self.hist_count_denoise = self.denoise(self.hist_count)
        
        self.clusters_edge = self.set_clusters_edge()
        self.centroids = self.set_centroids()
        self.clusters_labels = self.kmeans_algorithm(data, self.centroids)
        
        self.support_resistance = self.set_support_resistance(data)