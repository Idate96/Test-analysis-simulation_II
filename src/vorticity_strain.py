def central_diff_1o2(func_pts, x):
    df = np.zeros((np.size(x)))
    for i in range(1, len(x) - 1):
        df[i] = (func_pts[i + 1] - func_pts[i - 1]) / (x[i + 1] - x[i - 1])
    return df
