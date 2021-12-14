#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 18:33:54 2021

@author: Jonathan
"""
import numpy as np
import copy
import math


# Back substitution function #################################################


def BackSub(A, b):
    x = np.zeros_like(b, dtype=np.double)  # solution vector
    x[-1] = b[-1] / A[-1, -1]
    for i in range(n-2, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i:], x[i:])) / A[i, i]
    return x


# Modified Gram-Schmidt ######################################################

def MGS(A, b):
    """
    MGS - computes QR factorization of a square matrix A
    via modified gram schmidt and solves Ax = b

    Parameters
    ----------
    A : Matrix A
        array_type, size n x n.
    b : Solution vector b
        size n.

    Returns
    -------
    xc : Unknown vector x
        solution to Ax = b

    Q : Orthogonal Matrix
        Size m x n for reduced QR
        Size m x m for full QR
    R : Upper Triangular Matrix
        Size n x n for reduced QR
        Size m x n for full QR
    """
    V = copy.deepcopy(A)
    m, n = A.shape
    Q = np.zeros([m, n], dtype=A.dtype)
    R = np.zeros([n, n], dtype=A.dtype)

    for i in range(0, n):
        R[i, i] = np.linalg.norm(V[:, i])
        Q[:, i] = V[:, i] / R[i, i]
        for j in range(i + 1, n):
            R[i, j] = np.dot(np.transpose(Q[:, i]), V[:, j])
            V[:, j] = V[:, j] - np.dot(R[i, j], Q[:, i])

    xc = BackSub(R, np.dot(np.transpose(Q), b))

    return xc, Q, R


# HouseHolder QR Factorization ###############################################

def sign(x):
    if x >= 0:
        return 1
    else:
        return -1


def HouseholderQR(A, b):
    """
    MGS - computes QR factorization of a square matrix A
    via householder reflections and solves Ax = b

    Parameters
    ----------
    A : Matrix A
        array_type, size n x n.
    b : Solution vector b
        size n.

    Returns
    -------
    xc : Unknown vector x
        solution to Ax = b

    Q : Orthogonal Matrix
        Size m x n for reduced QR
        Size m x m for full QR
    R : Upper Triangular Matrix
        Size n x n for reduced QR
        Size m x n for full QR
    """
    m, n = A.shape
    R = copy.deepcopy(A)
    V = np.zeros((m, n))
    for k in range(n - 1):
        x = copy.deepcopy(R[k:m, k])
        e1 = np.identity(m-k)[0]
        V[0:m-k, k] = sign(x[0]) * (np.linalg.norm(x))*e1 + x
        V[0:m-k, k] = V[0:m-k, k] / np.linalg.norm(V[0:m-k, k])
        R[k:m, k:n] -= 2*np.outer(V[0:m-k, k],
                                  (np.matmul(np.transpose(V[0:m - k, k]),
                                             R[k:m, k:n])))

    Q = np.eye(m)
    for k in range(n - 1, -1, -1):
        Q[k:m, k:n] -= 2*np.outer(V[0:m-k, k],
                                  (np.matmul(np.transpose(V[0:m-k, k]),
                                             Q[k:m, k:n])))

    xc = BackSub(R, np.transpose(Q).dot(b))

    return xc, Q, R


# QR Factorization Via Givens Rotation #######################################

def givens(A, b):
    """
    MGS - computes QR factorization of a square matrix A
    via givens rotations and solves Ax = b

    Parameters
    ----------
    A : Matrix A
        array_type, size n x n.
    b : Solution vector b
        size n.

    Returns
    -------
    xc : Unknown vector x
        solution to Ax = b

    Q : Orthogonal Matrix
        Size m x n for reduced QR
        Size m x m for full QR
    R : Upper Triangular Matrix
        Size n x n for reduced QR
        Size m x n for full QR
    """
    m, n = A.shape
    R = copy.deepcopy(A)
    Q = np.identity(m)
    for j in range(n):
        for i in range(m - 1, j, -1):
            alpha, beta = R[i - 1, j], R[i, j]
            if abs(alpha) > abs(beta):
                t = beta / alpha
                c = 1 / (math.sqrt(1 + t**2))
                s = c*t
            else:
                tau = alpha / beta
                s = 1 / (math.sqrt(1 + tau**2))
                c = s*tau
            G = np.array([[c, s], [-s, c]])
            R[i - 1:i + 1, :] = G.dot(R[i - 1:i + 1, :])
            Q[:, i - 1:i + 1] = Q[:, i - 1:i + 1].dot(np.transpose(G))

    xc = BackSub(R, np.transpose(Q).dot(b))

    return xc, Q, R


# Orthogonal Matching Pursuit ################################################

def OMP(A, b, stop=np.inf, r_thresh=0.01):
    """
    Solving LASSO regression via Orthogonal Matching Pursuit (OMP)

    Parameters
    ----------
    A : array_type, size m x n
        Input matrix A
    b : array_type, shape n
        solution vector b

    Returns
    -------
    gamma: array_type
        sparse representation of matrix A, used to solve Ax = b.
    """
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


# Iterative Shrinkage Thresholding Algorithm #################################

def soft_threshold(x, tau, lmbda):
    return np.sign(x) * np.maximum(0, np.abs(x) - lmbda*tau)


def ista(A, b, lmbda, iter_max=3000):
    """
    Solve LASSO regression with Iterative Shrinkage Thresholding Algorithm
    (ISTA)

    Parameters
    ----------
    A : array_type, size m x n
        Input matrix A
    b : array_type, shape n
        solution vector b
    lmbda : float
        regularization parameter
    iter_max : int
        Set number of iterations. The default is 3000.

    Returns
    -------
    x : array_like
        unknown vector x, solution to Ax = b.

    """
    x = np.zeros(A.shape[1])
    tau = 0.75/np.linalg.norm(A) ** 2  # Lipschitz constant
    iters = 0
    while iters < iter_max:
        x = soft_threshold(x + np.dot(np.dot(tau, np.transpose(A)),
                                      b - A.dot(x)), tau, lmbda)
        iters += 1
    return x
