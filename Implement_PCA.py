import numpy as np
class PCA: 
    def __init__(self):
        self.eigenvectors = None
        self.prj_matrix= None
    
    def standardize(self, X):
        mu = np.mean(X, axis = 0) 
        X = X - mu  
        std = np.std(X, axis = 0)  
            # nếu các phần tử trong cùng 1 cột bằng nhau => std = 0
        std_filled = std.copy()
        std_filled[std == 0] = 1.0
        Xbar = (X-mu) / std_filled
        return Xbar, mu, std

    def find_eig_and_sort(self,cov_matrix):
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)  
        sorted_eig  = np.argsort(-eigenvalues)
        eigenvalues = eigenvalues[sorted_eig]
        eigenvectors = eigenvectors[:, sorted_eig]
        
        return (eigenvalues, eigenvectors)

    def projection_matrix(self,U):    
        P = U @ U.T 
        return P

    def fit(self, Xbar):
        S = np.cov(Xbar.T)  
        self.eigenvectors = self.find_eig_and_sort(S)[1]

    def reconstruct_img(self, Xbar, num_components):
        U = self.eigenvectors[:, range(num_components)]
        self.prj_matrix = self.projection_matrix(U)
        reconstructed_img =  Xbar @ self.prj_matrix
        return reconstructed_img
    
    