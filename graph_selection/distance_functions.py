import numpy as np


def dist(A, B, mode):
    if mode is 'fro':
        return frobenius_norm(A, B)
    elif mode is 'abs':
        return abs_sum(A,B)
    elif mode is 'cos':
        return cosine_similarity_matrices(A, B)
    else:
        raise Exception("Incorrect distance mode")


def frobenius_norm(A, B):
    return np.linalg.norm(np.subtract(A, B), 'fro')

def abs_sum(A, B):
    val = np.subtract(A, B)
    abs_val = np.absolute(val)
    return abs_val.sum()

def cosine_similarity_matrices(matrix1, matrix2):
    def cosine_similarity(vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2) if norm1*norm2 != 0 else dot_product

    # Ensure both matrices have the same shape
    if matrix1.shape != matrix2.shape:
        raise ValueError("Matrices must have the same shape")

    # Compute cosine similarity between corresponding rows
    row_similarities = []
    for row1, row2 in zip(matrix1, matrix2):
        row_similarities.append(cosine_similarity(row1, row2))
    average_row_similarity = np.mean(row_similarities)

    # Compute cosine similarity between corresponding columns
    column_similarities = []
    for col1, col2 in zip(matrix1.T, matrix2.T):
        column_similarities.append(cosine_similarity(col1, col2))
    average_column_similarity = np.mean(column_similarities)

    return 1 - np.average([average_row_similarity, average_column_similarity])