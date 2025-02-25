import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns


class LinearRegressor:
    """
    Extended Linear Regression model with support for categorical variables and gradient descent fitting.
    """

    def __init__(self):
        self.coefficients = None
        self.intercept = None

    """
    This next "fit" function is a general function that either calls the *fit_multiple* code that
    you wrote last week, or calls a new method, called *fit_gradient_descent*, not implemented (yet)
    """

    def fit(self, X, y, method="least_squares", learning_rate=0.01, iterations=1000):
        """
        Fit the model using either normal equation or gradient descent.

        Args:
            X (np.ndarray): Independent variable data (2D array).
            y (np.ndarray): Dependent variable data (1D array).
            method (str): method to train linear regression coefficients.
                          It may be "least_squares" or "gradient_descent".
            learning_rate (float): Learning rate for gradient descent.
            iterations (int): Number of iterations for gradient descent.

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """
        if method not in ["least_squares", "gradient_descent"]:
            raise ValueError(
                f"Method {method} not available for training linear regression."
            )
        if np.ndim(X) == 1:
            X = X.reshape(-1, 1)

        X_with_bias = np.insert(
            X, 0, 1, axis=1
        )  # Adding a column of ones for intercept

        if method == "least_squares":
            self.fit_multiple(X_with_bias, y)
        elif method == "gradient_descent":
            self.fit_gradient_descent(X_with_bias, y, learning_rate, iterations)

    def fit_multiple(self, X, y):
        """
        Fit the model using multiple linear regression (more than one independent variable).

        This method applies the matrix approach to calculate the coefficients for
        multiple linear regression.

        Args:
            X (np.ndarray): Independent variable data (2D array), with bias.
            y (np.ndarray): Dependent variable data (1D array).

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """
        # Replace this code with the code you did in the previous laboratory session

        # Calculamos w
        x_traspuesta = np.transpose(X)
        mult = np.dot(x_traspuesta, X)
        inv = np.linalg.pinv(mult)
        mult2 = np.dot(inv, x_traspuesta)
        w = np.dot(mult2, y)
        w = np.transpose(w)

        # Store the intercept and the coefficients of the model
        self.coefficients = w[1:]
        self.intercept = w[0]

    def fit_gradient_descent(self, X, y, learning_rate=0.01, iterations=1000):
        """
        Fit the model using either normal equation or gradient descent.

        Args:
            X (np.ndarray): Independent variable data (2D array), with bias.
            y (np.ndarray): Dependent variable data (1D array).
            learning_rate (float): Learning rate for gradient descent.
            iterations (int): Number of iterations for gradient descent.

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """

        # Initialize the parameters to very small values (close to 0)
        m = len(y)
        self.coefficients = (np.random.rand(X.shape[1] - 1) * 0.01)  # Small random numbers
        self.intercept = np.random.rand() * 0.01

        mse_values = []
        w_values = []
        b_values = []

        # Implement gradient descent (TODO)
        for epoch in range(iterations):
            predictions = np.dot(X[:, 1:], self.coefficients) + self.intercept
            error = predictions - y

            # TODO: Write the gradient values and the updates for the paramenters
            gradient_w = (1/m) * np.dot(X[:, 1:].T, error)
            gradient_b = (1/m) * np.sum(error)
            self.intercept -= learning_rate * gradient_b
            self.coefficients -= learning_rate * gradient_w
            
            # TODO: Calculate and print the loss every 100 epochs
            if epoch % 100 == 0:
                mse = np.mean(error**2)
                mse_values.append(mse)
                print(f"Epoch {epoch}: MSE = {mse}")

                # Además de medir el error, mediremos también los valros de los coeficientes y del interecept
                w_values.append(self.coefficients.copy())  
                b_values.append(self.intercept)

        w_values = np.array(w_values)
        b_values = np.array(b_values)

        # Importamos scikit learn para comparar resultados
        from sklearn.linear_model import LinearRegression

        # Calculamos la solución óptima usando Scikit-learn para comparar
        model = LinearRegression()
        model.fit(X[:, 1:], y)
        optimal_w = model.coef_  
        optimal_b = model.intercept_

        # Seleccionar solo el primer coeficiente w para la visualización
        w_values_plot = w_values[:, 0]  # Tomamos el primer coeficiente de cada iteración
        optimal_w_plot = optimal_w[0]  # Tomamos solo el primer coeficiente de Scikit-Learn

        # Imprimimos cuáles son los valores de w y b que hemos obtenido, con mi función y con scikit learn para comparar
        print(f"Valores de w y b según Scikit-learn: ({optimal_w_plot}, {optimal_b}")
        print(f"Valores de w y b calculados con mi descenso de gradiente: ({w_values_plot[-1]}, {b_values[-1]})")

        # Graficamos dos gráficos, la evolución del mse y la evolución de los coeficientes e intercept
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Evolución del MSE
        axes[0].plot(range(0, iterations, 100), mse_values, linestyle='-', color='b', label="MSE over iterations")
        axes[0].set_xlabel("Epochs")
        axes[0].set_ylabel("Mean Squared Error (MSE)")
        axes[0].set_title("Progreso del descenso de gradiente")
        axes[0].legend()

        # Evolución de w y b
        axes[1].plot(w_values_plot, b_values, linestyle='-', marker='o', color='b', label="Gradient Descent Path")
        # Marcamos la solución de scikit learn con una cruz roja para comparar
        axes[1].scatter(optimal_w_plot, optimal_b, color='r', marker='x', s=100, label="Optimal Solution (Scikit-Learn)")
        axes[1].set_xlabel("First w value")
        axes[1].set_ylabel("b values")
        axes[1].set_title("Gradient Descent Steps Towards Optimum")
        axes[1].legend()

        plt.tight_layout()
        plt.show()
        
        


    def predict(self, X):
        """
        Predict the dependent variable values using the fitted model.

        Args:
            X (np.ndarray): Independent variable data (1D or 2D array).
            fit (bool): Flag to indicate if fit was done.

        Returns:
            np.ndarray: Predicted values of the dependent variable.

        Raises:
            ValueError: If the model is not yet fitted.
        """

        # Paste your code from last week

        if self.coefficients is None or self.intercept is None:
            raise ValueError("Model is not yet fitted")

        if np.ndim(X) == 1:
            # TODO: Predict when X is only one variable
            predictions = self.intercept + X * self.coefficients

        else:
            # TODO: Predict when X is more than one variable
            predictions = self.intercept + np.dot(X, self.coefficients)

        return predictions


def evaluate_regression(y_true, y_pred):
    """
    Evaluates the performance of a regression model by calculating R^2, RMSE, and MAE.

    Args:
        y_true (np.ndarray): True values of the dependent variable.
        y_pred (np.ndarray): Predicted values by the regression model.

    Returns:
        dict: A dictionary containing the R^2, RMSE, and MAE values.
    """

    # R^2 Score
    # TODO
    rss = np.sum((y_true - y_pred)**2)
    tss = np.sum((y_true - np.mean(y_true))**2)
    r_squared = 1 - rss/tss

    # Root Mean Squared Error
    # TODO
    n = len(y_true)
    rmse = np.sqrt((1/n)*np.sum((y_true - y_pred)**2))

    # Mean Absolute Error
    # TODO
    mae = (1/n)*np.sum(abs(y_true - y_pred))

    return {"R2": r_squared, "RMSE": rmse, "MAE": mae}


def one_hot_encode(X, categorical_indices, drop_first=False):
    """
    One-hot encode the categorical columns specified in categorical_indices. This function
    shall support string variables.

    Args:
        X (np.ndarray): 2D data array.
        categorical_indices (list of int): Indices of columns to be one-hot encoded.
        drop_first (bool): Whether to drop the first level of one-hot encoding to avoid multicollinearity.

    Returns:
        np.ndarray: Transformed array with one-hot encoded columns.
    """
    X_transformed = X.copy()
    for index in sorted(categorical_indices, reverse=True):
        # TODO: Extract the categorical column
        categorical_column = X_transformed[:, index]

        # TODO: Find the unique categories (works with strings)
        unique_values = np.unique(categorical_column)

        # TODO: Create a one-hot encoded matrix (np.array) for the current categorical column
        one_hot = np.array([unique_values == val for val in categorical_column], dtype=int)

        # Optionally drop the first level of one-hot encoding
        if drop_first:
            one_hot = one_hot[:, 1:]

        # TODO: Delete the original categorical column from X_transformed and insert new one-hot encoded columns
        X_transformed = np.delete(X_transformed, index, axis=1)
        X_transformed = np.insert(X_transformed, index, one_hot.T, axis=1)

    return X_transformed
