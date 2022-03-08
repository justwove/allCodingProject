import numpy as np 
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.linear_model import LinearRegression 

### First we will generate the non - linear cooking data 
m = 100 
X = 6 * np.random.rand(m,1) - 3 
y = 0.5 * X**2 + X + 2 + np.random.randn(m, 1) 

### Set the Polynomial regression
polynomial_regression = PolynomialFeatures(degree=2, include_bias=False) 
X_poly = polynomial_regression.fit_transform(X) 

### Use the LinearRegression with our X_poly who has been transformed with y
lr = LinearRegression() 
lr.fit(X_poly, y) 

class Ridge():

    def __init__(self, alpha, iterations, l2_penalty):
        """
        Initialize the Ridge Regression with the given alpha and iterations
        l2_penalty is also known as ridge regression
        """
        self.alpha = alpha
        self.iterations = iterations
        self.l2_penalty = l2_penalty

    def fit(self, X, y):
        """
        Get the shape of X as m & n
        and update the parameters 
        """
        self.m, self.n = X.shape

        self.feature_weights = np.zeros(self.n)
        self.bias = 0

        self.X = X
        self.y = y

        [self.update_params() for i in range(self.iterations)]
        return self

    def update_params(self):
        Y_pred = self.predict(X)
        dW = ( - ( 2 * ( self.X.T ).dot( self.Y - Y_pred ) ) +               
               ( 2 * self.l2_penality * self.W ) ) / self.m 
        
        db = 2 * np.sum(self.Y - Y_pred) / self.m

        self.W = self.W - self.learning_rate * dW
        self.b = self.b - self.learning_rate * db
        return self

    def predict(self, X):
        """Predict X with the feature_weights and the bias"""
        return X.dot(self.feature_weights) + self.bias

