import numpy as np
class PCA: 
    def __init__(self):
        self.eigenvectors = None
        self.prj_matrix= None
        self.optimize = False

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
        eigenvalues = eigenvalues.astype(np.float64)
        eigenvectors = eigenvectors.astype(np.float64)
        sorted_eig  = np.argsort(-eigenvalues)
        eigenvalues = eigenvalues[sorted_eig]
        eigenvectors = eigenvectors[:, sorted_eig]
        
        return (eigenvalues, eigenvectors)

    def projection_matrix(self,U):    
        P = U @ U.T 
        return P

    def fit(self, Xbar):
        if self.optimize:
            S = np.cov(Xbar.T)  
        else:
            S = np.cov(Xbar)
            S = S.astype(np.float64)
        self.eigenvectors = self.find_eig_and_sort(S)[1]

    def reconstruct_img(self, Xbar, num_components):
        U = self.eigenvectors[:, range(num_components)]
        self.prj_matrix = self.projection_matrix(U)
        if self.optimize:
            reconstructed_img =  Xbar @ self.prj_matrix
        else:
            reconstructed_img = Xbar.T @self.prj_matrix
            reconstructed_img = reconstructed_img.T
        return reconstructed_img
    

    
    