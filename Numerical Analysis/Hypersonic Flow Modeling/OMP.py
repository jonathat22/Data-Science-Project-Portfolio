#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 02:02:27 2021

@author: Jonathan
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt


def Poly(X_train, p):
    """
    Generates a matrix of all polynomial combinations of the features
    with degree less than or equal to the specified degree p.

    Parameters
    ----------
    X_train : array_type, shape(m, n)
        Feature matrix whose feaures are to be combined.
    p : int
        Specifies the maximum degree of the polynomial features.

    Returns
    -------
    D : array_type, D(X_train, P)
        Matrix of polynomial combinations of features of degree p.
    """
    poly = PolynomialFeatures(p)
    D = poly.fit_transform(np.transpose(X_train))
    return D


def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '-')


def OMP(A, b, stop=np.infty, r_thresh=0.01):
    r = b
    gamma = np.zeros(A.shape[1])
    ls = []
    i = 0
    while np.sqrt(np.sum([i**2 for i in r])) > r_thresh and i < stop:
        Lambda = np.argmax(abs(np.dot(np.transpose(A), r)))
        ls.append(Lambda)
        gamma[ls] = np.linalg.inv(np.dot(np.transpose(A[:, ls]), A[:, ls])) \
            .dot(np.transpose(A[:, ls]).dot(b))
        r = b - np.dot(A, gamma)
        i += 1
    return np.transpose(gamma)


M = np.loadtxt('HyShotII30.txt', delimiter=",", dtype="double")
M = np.transpose(M)
M.shape
X = M[:7, :]
y = M[-1]


mean_errors = []
sd_errors = []
rel_error = []
n = 20
for i in range(n):
    X_train, X_test, y_train, y_test = train_test_split(np.transpose(X), y,
                                                        test_size=0.50)
    X_train = np.transpose(X_train)
    X_test = np.transpose(X_test)
    A = Poly(X_train, 5)
    b = y_train
    x = OMP(A, b)
    y_pred = Poly(X_test, 5).dot(x)

    rel_error.append(np.linalg.norm(y_pred-y_test)/np.linalg.norm(y_test)
                     * 100)

mean_error = np.mean(rel_error)
sd_error = np.std(rel_error)

print("Mean Relative Error after 20 Trials:", mean_error, "%")
print("Standard Deviation after 20 Trials", sd_error)

plt.scatter(y_test, y_pred, color="black")
plt.xlabel("Actual Y")
plt.ylabel("Predicted Y")
plt.title("Actual Vs. Predicted Y Using Orthogonal Matching Pursuit (OMP)")
abline(1, 0)
plt.show()
