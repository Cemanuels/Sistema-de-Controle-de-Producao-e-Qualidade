# 🏭 Protótipo de Controle de Qualidade Industrial

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)

Este projeto é um protótipo em Python que simula um sistema de controle de qualidade e automação para uma linha de montagem industrial. Ele permite o cadastro interativo de peças, realiza uma inspeção automática baseada em critérios pré-definidos (peso, cor, comprimento) e gerencia o armazenamento de peças aprovadas em caixas com capacidade limitada.

## ⚙️ Explicação do Funcionamento

A arquitetura da solução é baseada em **Programação Orientada a Objetos (POO)** para um gerenciamento de estado eficaz, permitindo que o sistema "lembre" das peças e caixas entre as interações do usuário.

* **Classe `LinhaDeMontagem`**: É o "cérebro" do sistema. Esta classe encapsula (armazena) todas as listas de dados (peças cadastradas, caixas de aprovadas, peças reprovadas) e o contador de IDs. Todos os métodos para manipular esses dados (inspecionar, adicionar, remover, gerar relatório) estão contidos nesta classe.

* **Loop Principal (`main()`)**: O script principal é responsável apenas por exibir o menu e capturar a entrada do usuário. Ele cria uma única instância da `LinhaDeMontagem` e chama os métodos apropriados dessa instância com base na escolha do usuário, sem nunca manipular os dados diretamente.

Essa separação de responsabilidades (Interface vs. Lógica de Negócio) torna o código limpo, organizado e fácil de manter.

### Critérios de Qualidade (Regras de Negócio)

Para ser **Aprovada**, a peça deve satisfazer TODAS as seguintes condições:
* **Peso:** Entre 95g e 105g (inclusive).
* **Cor:** "azul" ou "verde" (não sensível a maiúsculas).
* **Comprimento:** Entre 10cm e 20cm (inclusive).

Peças aprovadas são armazenadas em caixas com capacidade para **10 peças**.

## 🚀 Como Rodar o Programa

### Pré-requisitos

* Você precisa ter o **Python 3.7** (ou superior) instalado em sua máquina.

### Passo a Passo

1.  **Clone o repositório** (ou apenas salve o arquivo `.py` em um diretório):
    ```bash
    git clone [https://github.com/Cemanuels/Sistema-de-Controle-de-Producao-e-Qualidade.git](https://github.com/Cemanuels/Sistema-de-Controle-de-Producao-e-Qualidade.git)
    cd Sistema-de-Controle-de-Producao-e-Qualidade
    ```

2.  **Navegue até o diretório** que contém o script.

3.  **Execute o script** através do seu terminal:
    ```bash
    # No Windows
    python sistema.py
    
    # No macOS / Linux
    python3 sistema.py
    ```

4.  O menu interativo será iniciado e você poderá usar o sistema.

## 📊 Exemplos de Entradas e Saídas

Abaixo, um exemplo de fluxo de uso do sistema.

### 1. Cadastro de Peça Aprovada

```text
===========================================
   Sistema de Controle de Produção e Qualidade
===========================================
1. Cadastrar nova peça
...
0. Sair do Sistema
-------------------------------------------
Escolha uma opção: 1

--- [1] Cadastrar Nova Peça ---
Digite o peso (em gramas, ex: 101.5): 102
Digite a cor (azul/verde): azul
Digite o comprimento (em cm, ex: 15.0): 15

Inspecionando Peça ID: 1...
Status: APROVADA ✅
Peça adicionada à Caixa 1 (Ocupação: 1/10).

Peça ID 1 cadastrada e processada com sucesso.

Pressione [Enter] para continuar...