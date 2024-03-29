import math
import numba as nb
import numpy as np



@nb.njit()
def kernel_linear(
    global_mean: float,
    user_bias: float,
    item_bias: float,
    user_feature_vec: np.ndarray,
    item_feature_vec: np.ndarray,
) -> float:
    """
    Calculates result with a linear kernel which is essentially just the dot product

    Args:
        global_mean (float): Global mean
        user_bias (float): User bias
        item_bias (float): Item bias
        user_feature_vec (np.ndarray): Vector of user latent features 
        item_feature_vec (np.ndarray): Vector of item latent features

    Returns:
        [float]: Linear kernel result
    """
    result = (
        global_mean + item_bias + user_bias + np.dot(user_feature_vec, item_feature_vec)
    )
    return result




@nb.njit()
def kernel_linear_sgd_update(
    user_id: int,
    item_id: int,
    rating: float,
    global_mean: float,
    user_biases: np.ndarray,
    item_biases: np.ndarray,
    user_features: np.ndarray,
    item_features: np.ndarray,
    lr: float,
    reg: float,
    update_user_params: bool = True,
    update_item_params: bool = True,
):
    """
    Performs a single update using stochastic gradient descent for a linear kernel given a user and item. 
    Similar to https://github.com/gbolmier/funk-svd and https://github.com/NicolasHug/Surprise we iterate over each factor manually for a given 
    user/item instead of indexing by a row such as user_feature[user] since it has shown to be much faster. We have also tested with representing
    user_features and item_features as 1D arrays but that also is much slower. Using parallel turned on in numba gives much worse performance as well.

    Args:
        user_id (int): User id 
        item_id (int): Item id
        rating (float): Rating for user and item
        global_mean {float} -- Global mean of all ratings
        user_biases {numpy array} -- User biases vector of shape (n_users, 1)
        item_biases {numpy array} -- Item biases vector of shape (n_items, 1)
        user_features {numpy array} -- Matrix P of user features of shape (n_users, n_factors)
        item_features {numpy array} -- Matrix Q of item features of shape (n_items, n_factors)
        lr (float): Learning rate alpha
        reg {float} -- Regularization parameter lambda for Frobenius norm
        update_user_params {bool} -- Whether to update user parameters or not. Default is True.
        update_item_params {bool} -- Whether to update item parameters or not. Default is True.
    """
    n_factors = user_features.shape[1]
    user_bias = user_biases[user_id]
    item_bias = item_biases[item_id]

    # Compute predicted rating
    rating_pred = (
        global_mean
        + item_bias
        + user_bias
        + np.dot(user_features[user_id, :], item_features[item_id, :])
    )

    # Compute error
    error = rating_pred - rating

    # Update bias parameters
    if update_user_params:
        user_biases[user_id] -= lr * (error + reg * user_bias)

    if update_item_params:
        item_biases[item_id] -= lr * (error + reg * item_bias)

    # Update user and item features
    for f in range(n_factors):
        user_feature_f = user_features[user_id, f]
        item_feature_f = item_features[item_id, f]

        if update_user_params:
            user_features[user_id, f] -= lr * (
                error * item_feature_f + reg * user_feature_f
            )

        if update_item_params:
            item_features[item_id, f] -= lr * (
                error * user_feature_f + reg * item_feature_f
            )

    return



