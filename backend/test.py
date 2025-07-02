def matrix_chain_order(dims):
    n = len(dims) - 1

    dp = [None for _ in range(n)]
    for i in range(n):
        dp[i] = [0 for _ in range(n)]
    
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            dp[i][j] = float('inf')
            
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]

                if cost < dp[i][j]:
                    dp[i][j] = cost
                    
    return dp[0][n-1]

dims = [10, 6, 9, 8, 3, 4, 4, 8, 5, 4, 8]
result = matrix_chain_order(dims)

print("Min cost:", result)