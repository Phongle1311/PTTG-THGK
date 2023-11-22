import numpy as np


class PCA:
    def __init__(self):
        self.eigenvalues = None
        self.eigenvectors = None
        self.prj_matrix = None
        self.optimize = False
        self.sum_of_var_explained = None

    def standardize(self, X):
        mu = np.mean(X, axis=0)
        X = X - mu
        std = np.std(X, axis=0)
        # nếu các phần tử trong cùng 1 cột bằng nhau => std = 0
        std_filled = std.copy()
        std_filled[std == 0] = 1.0
        Xbar = (X - mu) / std_filled
        return Xbar, mu, std

    def find_eig_and_sort(self, cov_matrix):
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        eigenvalues = eigenvalues.astype(np.float64)
        eigenvectors = eigenvectors.astype(np.float64)
        sorted_eig = np.argsort(-eigenvalues)
        eigenvalues = eigenvalues[sorted_eig]
        eigenvectors = eigenvectors[:, sorted_eig]

        return (eigenvalues, eigenvectors)

    def projection_matrix(self, U):
        P = U @ U.T
        return P

    def get_sum_of_variance_explained(self):
        sum_of_var_explained = np.sum(self.eigenvalues)
        return sum_of_var_explained

    def fit(self, Xbar):
        if self.optimize:
            S = np.cov(Xbar.T)
        else:
            S = np.cov(Xbar)
            S = S.astype(np.float64)
        # print(S)
        # print(S.shape)
        self.eigenvalues, self.eigenvectors = self.find_eig_and_sort(S)
        self.sum_of_var_explained = self.get_sum_of_variance_explained()

    def preserved_var_explained(self, ratio):
        var_required = ratio * self.sum_of_var_explained
        sum = 0
        num_components = 0
        for value in self.eigenvalues:
            num_components += 1
            sum = sum + value
            if sum > var_required:
                break

        return num_components

    def need_to_refit(self, num_components, num_of_images):
        delta = num_components - num_of_images
        if delta > 0 and self.optimize == True:
            self.optimize = False
            return True
        if delta <= 0 and self.optimize == False:
            self.optimize = True
            return True
        return False

    def reconstruct_img(self, Xbar, mu_Xbar, num_components=None, preserved=None):
        if preserved is not None:
            num_components = self.preserved_var_explained(preserved)

        if self.need_to_refit(num_components, Xbar.shape[1]):
            self.fit(Xbar)

        U = self.eigenvectors[:, range(num_components)]
        self.prj_matrix = self.projection_matrix(U)
        if self.optimize:
            reconstructed_img = Xbar @ self.prj_matrix + mu_Xbar
        else:
            reconstructed_img = Xbar.T @ self.prj_matrix
            reconstructed_img = reconstructed_img.T + mu_Xbar
        return reconstructed_img
