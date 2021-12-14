#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 02:59:21 2021

@author: Jonathan
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt


def Poly(X_train, p):
    poly = PolynomialFeatures(p)
    D = poly.fit_transform(np.transpose(X_train))
    return D


def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '-')


M = np.loadtxt('HyShotII30.txt', delimiter=",", dtype="double")
M = np.transpose(M)
M.shape

X = M[:7, :]
y = M[-1]


rel_error = []
mean_errors = []
sd_errors = []
p = [1, 2, 3, 4, 5, 6, 7]
n = 10
for k in p:
    for m in range(n):
        X_train, X_test, y_train, y_test = train_test_split(np.transpose(X),
                                                            y, test_size=0.19)
        X_train = np.transpose(X_train)
        X_test = np.transpose(X_test)

        D = Poly(X_train, k)
        u, s, v = np.linalg.svd(D, full_matrices=False)

        a = s.shape[0]
        s_inv = np.zeros((a, a))
        for i in range(a):
            if s[i] != 0:
                s_inv[i, i] = 1 / s[i]

        u_inv = np.transpose(u)
        v_inv = np.transpose(v)

        Ap = v_inv.dot(s_inv).dot(u_inv)
        c = Ap.dot(y_train)
        y_pred = Poly(X_test, k).dot(c)

        rel_error.append(np.linalg.norm(y_pred-y_test)/np.linalg.norm(y_test)
                         * 100)

    mean_error = np.mean(rel_error)
    sd_error = np.std(rel_error)
    mean_errors.append(mean_error)
    sd_errors.append(sd_error)

fig, ax = plt.subplots()
ax.errorbar(p, mean_errors, yerr=sd_errors, marker="o",
            color="blue", ecolor="black", capsize=4)
plt.xlabel("P")
plt.ylabel("Mean Relative Error (%)")
plt.title("Mean Relative Error for each Polynomial Degree P")
plt.show()


p = 1

mean_errors = []
sd_errors = []
rel_error = []

for i in range(100):
    X_train, X_test, y_train, y_test = train_test_split(np.transpose(X), y,
                                                        test_size=0.19)
    X_train = np.transpose(X_train)
    X_test = np.transpose(X_test)

    D = Poly(X_train, p)
    u, s, v = np.linalg.svd(D, full_matrices=False)

    a = s.shape[0]
    s_inv = np.zeros((a, a))
    for i in range(a):
        if s[i] != 0:
            s_inv[i, i] = 1 / s[i]

    u_inv = np.transpose(u)
    v_inv = np.transpose(v)

    Ap = v_inv.dot(s_inv).dot(u_inv)
    c = Ap.dot(y_train)
    y_pred = Poly(X_test, p).dot(c)

    rel_error.append(np.linalg.norm(y_pred-y_test)/np.linalg.norm(y_test)
                     * 100)

mean_error = np.mean(rel_error)
sd_error = np.std(rel_error)

print("Mean Relative Error after 100 Trials:", mean_error, "%")
print("Standard Deviation after 100 Trials", sd_error)


plt.scatter(y_pred, y_test, color="black")
plt.xlabel("Actual Y")
plt.ylabel("Predicted Y")
plt.title("Actual Vs. Predicted Y Using the SVD")
abline(1, 0)
plt.show()
