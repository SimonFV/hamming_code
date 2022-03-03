def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)


# Agrega las casillas de los bits de paridad
def add_places(data):
    extended_data = []
    i = 1
    digit = 0
    while digit < len(data):
        if is_power_of_two(i):
            extended_data.append(-1)
        else:
            extended_data.append(data[digit])
            digit += 1
        i += 1
    return extended_data


# Retorna 0 si la cantidad de 1 en la lista es par, 1 si es impar
def is_even(data):
    total = 0
    for i in data:
        if i == 1:
            total += 1
    return total % 2


# Revisa la paridad de los datos para un valor Pn y retorna dicha lista con el
# bit de paridad modificado y con -1 en las casillas vacias
def check_parity(n, data):
    data_to_check = []
    m = pow(2, n - 1)
    i = m - 1
    for x in range(i):
        data_to_check.append(-1)
    while i < len(data):
        j = 0
        while i < len(data) and j < m:
            data_to_check.append(data[i])
            i += 1
            j += 1
        j = 0
        while i < len(data) and j < m:
            data_to_check.append(-1)
            i += 1
            j += 1
    data_to_check[m - 1] = is_even(data_to_check)
    return data_to_check


# Construye la matriz de paridad segun el codigo hamming
def get_parity_table(extended_data):
    matrix = []
    n = 1
    while pow(2, n - 1) < len(extended_data):
        matrix.append(check_parity(n, extended_data))
        n += 1
    return matrix


def final_message(matrix):
    message = []
    for n in range(len(matrix)):
        for i in range(pow(2, n) - 1, len(matrix[n])):
            if matrix[n][i] != -1:
                message.append(matrix[n][i])
            else:
                break
    return message

