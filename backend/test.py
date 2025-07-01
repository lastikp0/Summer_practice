def matrix_chain_order(dims):
    n = len(dims) - 1  # Количество матриц
    # Создаем таблицу для хранения минимального количества операций
    dp = [[0] * n for _ in range(n)]
    
    # Заполняем таблицу для цепочек разной длины L
    for L in range(2, n + 1):  # L - длина цепочки (от 2 до n)
        for i in range(n - L + 1):  # Начало цепочки
            j = i + L - 1           # Конец цепочки
            dp[i][j] = float('inf') # Инициализируем бесконечностью
            
            # Перебираем все возможные точки разбиения
            for k in range(i, j):
                # Считаем стоимость текущего разбиения
                cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    
    return dp[0][n-1]

dims = [6, 4, 7, 8, 4, 7, 6, 9, 8, 7, 10]
result = matrix_chain_order(dims)
print("Минимальное количество операций:", result)