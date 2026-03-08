# app/clustering.py
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

class FuzzyClusterer:
    def __init__(self, n_components=15): # Justify this number via BIC in your notebook/README
        self.pca = PCA(n_components=50) # Reduce dims for GMM
        self.gmm = GaussianMixture(n_components=n_components, covariance_type='full')

    def fit(self, embeddings):
        reduced_embs = self.pca.fit_transform(embeddings)
        self.gmm.fit(reduced_embs)

    def get_cluster_distribution(self, query_embedding):
        reduced = self.pca.transform(query_embedding.reshape(1, -1))
        # predict_proba returns the fuzzy distribution
        distribution = self.gmm.predict_proba(reduced)[0] 
        return distribution