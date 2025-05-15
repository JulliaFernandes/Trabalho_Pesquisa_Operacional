<h1 align="center"><b>ENUMERAÇÃO DE SOLUÇÕES DE PROBLEMAS DE PROGRAMAÇÃO LINEAR</b></h1>

<div align="center">
  <br>
  <a href="https://code.visualstudio.com/docs/?dv=linux64_deb">
    <img src="https://img.shields.io/badge/IDE-Visual%20Studio%20Code-informational" alt="VSCode">
  </a>
  <img src="https://img.shields.io/badge/Linguagem-Python-orange" alt="Python">
</div>

Este projeto realiza a resolução de sistemas lineares derivados de problemas de Programação Linear. A ideia central é encontrar todas as **soluções básicas possíveis**, identificar as **soluções viáveis** (com todas as variáveis não negativas), e determinar a **melhor solução**, com base na função objetivo.

## 🎯 Objetivo

Dado um sistema linear representando uma função objetivo e restrições, o programa busca todas as combinações possíveis de soluções básicas, resolve os sistemas lineares associados, e determina:

- Quais soluções são viáveis (todas as variáveis ≥ 0)
- O valor da função objetivo em cada uma
- Qual é a melhor solução viável

---

## 🧠 Como Funciona

1. **Leitura do arquivo** com a função objetivo e restrições
2. **Geração das combinações** de variáveis que serão zeradas
3. **Construção de sistemas reduzidos** para cada combinação
4. **Resolução dos sistemas** usando `np.linalg.solve`
5. **Filtragem das soluções viáveis**
6. **Cálculo do valor da função objetivo**
7. **Exibição da melhor solução viável**

---

## 📂 Estrutura dos Arquivos

- `main.py`: arquivo principal com toda a lógica do programa
- `exemplo.txt`: arquivo de entrada com a função objetivo e restrições
- `README.md`: este arquivo

---

## 📥 Formato do Arquivo de Entrada

O arquivo `.txt` deve conter:

1. Primeira linha: dois inteiros → número de variáveis e número de restrições  
2. Segunda linha: coeficientes da função objetivo  
3. Linhas seguintes: coeficientes das restrições seguidos do termo independente


---

## ▶️ Como Executar

Certifique-se de ter o Python e o NumPy instalados.

```bash
python main.py entrada/LP_XX.txt

