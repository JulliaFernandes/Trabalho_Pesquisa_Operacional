from itertools import combinations
import numpy as np
import math
import os
import sys

# Cores ANSI
CYAN = "\033[1;36m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

def readFile(filename):
    with open(filename, 'r') as file:
        matrix = []
        firstLine = True

        for line in file:
            if firstLine:
                num_variables, num_restriction = map(int, line.split())
                firstLine = False
            else:
                row = list(map(float, line.split()))
                matrix.append(row)
    return num_variables, num_restriction, matrix


def numberOfSolutions(num_restriction, num_variables):
    fat_variables = math.factorial(num_variables)
    fat_restriction = math.factorial(num_restriction)
    fat_difference = math.factorial(num_variables - num_restriction)
    return fat_variables // (fat_restriction * fat_difference)


def generate_zero_combinations(num_variables, num_to_zero):
    return list(combinations(range(num_variables), num_to_zero))


def matrixFromCombination(list, matrix):
    newMatrix = []
    for i in range(1, len(matrix)):  
        newRow = []
        for j in range(len(matrix[1])): 
            if j not in list:  
                newRow.append(matrix[i][j]) 
        newMatrix.append(newRow)
    return newMatrix

def solveSystem(matrix):
    B = [row[-1] for row in matrix]
    A = [row[:-1] for row in matrix]
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    if A.shape[0] != A.shape[1]:
        print(f"{RED}  - Erro: sistema não quadrado. A matriz dos coeficientes deve ser m x m.{RESET}")
        return None

    try:
        # Tenta resolver o sistema Ax = B usando numpy (internamente faz eliminação com pivoteamento)
        x = np.linalg.solve(A, B)
        return [round(val, 2) for val in x]
    except np.linalg.LinAlgError:
        print(f"{RED}  - Aviso: Sistema singular (sem solução única).{RESET}")
        return None

def findIfSystemIsInfeasible(solutions):
    for i in range(len(solutions)):
        if solutions[i]< 0:
            return True
    return False



def findValueOfSolution(objective_function, solutions):
    result = 0
    for i in range(len(objective_function)-1):
        result += objective_function[i] * solutions[i]
    return result

def solutionOrganizer(matrix, combinations, i, solutions):
    new_solutions = []
    num_solutions = 0
    for j in range(len(matrix[1])-1):
        if j not in combinations[i]:
            new_solutions.append(solutions[num_solutions])
            num_solutions += 1
        else:
            new_solutions.append(0)
    return new_solutions


def bestSolution(solution_hash, num_basic, num_viable, num_infeasible):
    if solution_hash:
        best = min(solution_hash, key=solution_hash.get)
        best_val = solution_hash[best]
        print(f"{CYAN}===== Resumo Final ====={RESET}")
        print(f"  - Número total de soluções básicas: {num_basic}")
        print(f"  - Número de soluções básicas viáveis: {num_viable}")
        print(f"  - Número de soluções inviáveis: {num_infeasible}")
        print(f"{GREEN}  -> Melhor solução: {best}  \n \t\t (Z = {best_val}){RESET}")


def systemForEachCombination(combinations, matrix):
    num_viable = 0
    num_infeasible = 0
    solution_hash = {}

    for i, comb in enumerate(combinations):
        print(f"{CYAN}\n--- Combinação {i+1}: Zerando variáveis {tuple(c+1 for c in comb)}{RESET}")
        newMatrix = matrixFromCombination(comb, matrix)

        print("  Matriz reduzida:")
        for row in newMatrix:
            print("   ", row)

        solutions = solveSystem(newMatrix)

        if solutions is None:
            print(f"  {RED}Sistema não resolvido.{RESET}\n")
            continue

        solutions = solutionOrganizer(matrix, combinations, i, solutions)
        print("  Soluções:")
        for j, val in enumerate(solutions):
            print(f"    x{j+1} = {val}")
        z = findValueOfSolution(matrix[0], solutions)
        print(f"  {GREEN}Valor da função objetivo: {z}{RESET}")

        if findIfSystemIsInfeasible(solutions):
            print(f"  {ORANGE}Solução inviável: valores negativos.{RESET}\n")
            num_infeasible += 1
        else:
            # z = findValueOfSolution(matrix[0], solutions)
            solution_hash[tuple(solutions)] = z
            # print(f"  {GREEN}Valor da função objetivo: {z}{RESET}\n")
            num_viable += 1

    num_basic = num_viable + num_infeasible
    bestSolution(solution_hash, num_basic, num_viable, num_infeasible)


def main():
    if len(sys.argv) < 2:
        print("Erro: Forneça o caminho do arquivo como argumento.")
        print("Uso: python main.py <caminho_do_arquivo>")
        return

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"Erro: Caminho '{file_path}' inválido.")
        return

    num_vars, num_rest, matrix = readFile(file_path)
    print(f"{CYAN}=== Análise do Arquivo: {os.path.basename(file_path)} ==={RESET}")
    print(f"  - Variáveis: {num_vars}")
    print(f"  - Restrições: {num_rest}")
    print(f"  - Matriz:")
    for row in matrix:
        print("   ", row)

    max_solutions = numberOfSolutions(num_rest, num_vars)
    print(f"  - Máximo de soluções básicas: {max_solutions}\n")

    zero_combinations = generate_zero_combinations(num_vars, num_vars - num_rest)
    print(f"{CYAN}=== Começando resolução de sistemas ==={RESET}")
    systemForEachCombination(zero_combinations, matrix)
    print(f"{CYAN}=== Fim do processamento ==={RESET}")


if __name__ == "__main__":
    main()