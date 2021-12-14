import numpy as np
import copy
import math

# Back substitution function:


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
        array_like, size n x n.
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


n = 100
QE = 0
AE = 0
xE = 0
for i in range(n):
    A = np.random.random((n, n))
    x = np.random.random(n)
    b = np.dot(A, x)
    xc, Q0, R0 = MGS(A, b)
    xE = np.linalg.norm(x - xc) / np.linalg.norm(xc)
    AE += np.linalg.norm(np.dot(Q0, R0)-A, np.inf)
    QE += np.linalg.norm(np.dot(np.transpose(Q0), Q0)-np.eye(n, n), np.inf)

AE = AE / n
QE = QE / n
print("Testing Modified Gram Schmidt:")
print("A = QR Error, MGS:", AE)
print("Orthogonality Error, MGS:", QE)
print("Solution to Ax = b Error:", xE)


# HouseHolder QR Factorization ###############################################


def sign(x):
    if x >= 0:
        return 1
    else:
        return -1


def HouseholderQR(A, b):
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


n = 100
orthog = 0
HAE = 0
for i in range(n):
    A = np.random.random((n, n))
    x = np.random.random(n)
    Q, R = np.linalg.qr(A)
    b = np.dot(A, x)
    xc, QH, RH = HouseholderQR(A, b)
    HxE = np.linalg.norm(x - xc) / np.linalg.norm(xc)
    HAE += np.linalg.norm(np.dot(QH, RH) - A, np.inf)
    orthog += np.linalg.norm(np.dot(np.transpose(QH), QH)-np.eye(n, n), np.inf)

HAE = HAE / n
orthog = orthog / n
print("Testing HouseholderQR:")
print("A = QR Error, Householder:", HAE)
print("Orthogonality Error, Householder:", orthog)
print("Solution to Ax = b Error:", HxE)


# QR Factorization Via Givens Rotation #######################################

def givens(A, b):
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


n = 100
ortho = 0
GAE = 0
for i in range(n):
    A = np.random.random((n, n))
    x = np.random.random(n)
    Q, R = np.linalg.qr(A)
    b = np.dot(A, x)
    xc, QG, RG = givens(A, b)
    GxE = np.linalg.norm(x-xc) / np.linalg.norm(xc)
    GAE += np.linalg.norm(np.dot(QG, RG)-A, np.inf)
    ortho += np.linalg.norm(np.dot(np.transpose(QG), QG) - np.eye(n, n),
                            np.inf)

GAE = GAE / n
ortho = ortho / n
print("Testing Givens Rotation:")
print("A = QR Error, Givens:", GAE)
print("Orthogonality Error, Givens:", ortho)
print("Solution to Ax = b Error:", GxE)
