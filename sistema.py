import time

class LinhaDeMontagem:
    """
    Classe para gerenciar todo o processo da linha de montagem,
    incluindo cadastro, inspeção e armazenamento de peças.
    """

    def __init__(self, capacidade_caixa=10):
        # Constante
        self.CAPACIDADE_CAIXA = capacidade_caixa
        
        # --- Estruturas de Armazenamento Dinâmicas ---
        
        # Lista mestre de TODAS as peças já cadastradas
        self.pecas_cadastradas = [] 
        
        # Lista de listas (cada lista interna é uma caixa)
        self.caixas_de_aprovadas = [[]] 
        
        # Lista de peças reprovadas (com motivos)
        self.pecas_reprovadas = []
        
        # Contador para gerar IDs únicos para as peças
        self.peca_id_counter = 1

    # --- Lógica de Inspeção (Interna) ---
    
    def _inspecionar_peca(self, peca):
        """
        Avalia uma única peça com base nos critérios de qualidade.
        (Método privado, usado apenas pela classe)
        """
        peso = peca['peso']
        cor = peca['cor']
        comprimento = peca['comprimento']
        motivos_reprovacao = []

        if not (95 <= peso <= 105):
            motivos_reprovacao.append("Peso fora do padrão (95-105g)")
        if cor.lower() not in ['azul', 'verde']:
            motivos_reprovacao.append("Cor inválida ('azul' ou 'verde')")
        if not (10 <= comprimento <= 20):
            motivos_reprovacao.append("Comprimento fora do padrão (10-20cm)")

        if not motivos_reprovacao:
            return "Aprovada", None
        else:
            return "Reprovada", motivos_reprovacao

    # --- Lógica de Processamento (Interna) ---

    def _processar_peca_cadastrada(self, peca):
        """
        Após cadastrar, esta função decide o destino da peça.
        """
        status, motivos = self._inspecionar_peca(peca)
        
        print(f"\nInspecionando Peça ID: {peca['id']}...")
        time.sleep(0.5)

        if status == "Aprovada":
            print("Status: APROVADA ✅")
            
            caixa_atual = self.caixas_de_aprovadas[-1]

            if len(caixa_atual) < self.CAPACIDADE_CAIXA:
                caixa_atual.append(peca)
                print(f"Peça adicionada à Caixa {len(self.caixas_de_aprovadas)} (Ocupação: {len(caixa_atual)}/{self.CAPACIDADE_CAIXA}).")
            else:
                print(f"*** 📦 Caixa {len(self.caixas_de_aprovadas)} FECHADA (capacidade {self.CAPACIDADE_CAIXA} atingida). ***")
                nova_caixa = [peca] # A nova peça já vai para a nova caixa
                self.caixas_de_aprovadas.append(nova_caixa)
                print(f"*** 📦 Abrindo nova Caixa {len(self.caixas_de_aprovadas)}. ***")
                print(f"Peça adicionada à Caixa {len(self.caixas_de_aprovadas)} (Ocupação: 1/{self.CAPACIDADE_CAIXA}).")

        elif status == "Reprovada":
            print(f"Status: REPROVADA ❌ (Motivos: {', '.join(motivos)})")
            self.pecas_reprovadas.append({"id": peca['id'], "motivos": motivos, "dados": peca})


    # --- Funções do Menu ---

    def cadastrar_nova_peca(self):
        """
        Opção 1: Pede dados ao usuário e cadastra uma nova peça.
        """
        print("\n--- [1] Cadastrar Nova Peça ---")
        try:
            # Validação robusta da entrada do usuário
            while True:
                try:
                    peso = float(input("Digite o peso (em gramas, ex: 101.5): ").strip())
                    break
                except ValueError:
                    print("Erro: Peso deve ser um número.")
            
            cor = input("Digite a cor (azul/verde): ").strip().lower()

            while True:
                try:
                    comprimento = float(input("Digite o comprimento (em cm, ex: 15.0): ").strip())
                    break
                except ValueError:
                    print("Erro: Comprimento deve ser um número.")

            # Cria a peça
            nova_peca = {
                'id': self.peca_id_counter,
                'peso': peso,
                'cor': cor,
                'comprimento': comprimento
            }
            
            # Incrementa o ID para a próxima peça
            self.peca_id_counter += 1
            
            # Adiciona à lista mestre
            self.pecas_cadastradas.append(nova_peca)
            
            # Processa (inspeciona e armazena)
            self._processar_peca_cadastrada(nova_peca)
            
            print(f"\nPeça ID {nova_peca['id']} cadastrada e processada com sucesso.")

        except Exception as e:
            print(f"Ocorreu um erro inesperado no cadastro: {e}")

    def listar_pecas(self):
        """
        Opção 2: Lista todas as peças aprovadas e reprovadas.
        """
        print("\n--- [2] Listar Peças Aprovadas/Reprovadas ---")
        
        print("\n🟢 Peças APROVADAS (distribuídas nas caixas):")
        total_aprovadas = 0
        if not self.caixas_de_aprovadas[0]:
             print("Nenhuma peça aprovada ainda.")
        else:
            for i, caixa in enumerate(self.caixas_de_aprovadas):
                print(f"   Caixa {i+1} (Atual: {len(caixa)}/{self.CAPACIDADE_CAIXA}):")
                if not caixa:
                    print("     (Vazia)")
                for peca in caixa:
                    print(f"     - ID: {peca['id']} (Peso: {peca['peso']}g, Cor: {peca['cor']}, Comp: {peca['comprimento']}cm)")
                    total_aprovadas += 1
        print(f"   [Total Aprovadas: {total_aprovadas}]")

        print("\n🔴 Peças REPROVADAS:")
        if not self.pecas_reprovadas:
            print("Nenhuma peça reprovada.")
        else:
            for peca_info in self.pecas_reprovadas:
                peca = peca_info['dados']
                motivos = ", ".join(peca_info['motivos'])
                print(f"   - ID: {peca['id']} (Peso: {peca['peso']}g, Cor: {peca['cor']}, Comp: {peca['comprimento']}cm)")
                print(f"     Motivos: {motivos}")
        print(f"   [Total Reprovadas: {len(self.pecas_reprovadas)}]")

    def remover_peca_cadastrada(self):
        """
        Opção 3: Remove uma peça de todo o sistema (Mestre, Aprovadas, Reprovadas).
        """
        print("\n--- [3] Remover Peça Cadastrada ---")
        try:
            id_para_remover = int(input("Digite o ID da peça que deseja remover: ").strip())
        except ValueError:
            print("Erro: ID inválido. Deve ser um número.")
            return

        removido_mestre = False
        removido_aprovadas = False
        removido_reprovadas = False
        
        # 1. Tentar remover da lista mestre
        peca_encontrada = next((p for p in self.pecas_cadastradas if p['id'] == id_para_remover), None)
        if peca_encontrada:
            self.pecas_cadastradas.remove(peca_encontrada)
            removido_mestre = True

        # 2. Tentar remover das caixas de aprovadas
        for caixa in self.caixas_de_aprovadas:
            # Usamos [:] para modificar a lista 'in-place'
            pecas_na_caixa_antes = len(caixa)
            caixa[:] = [p for p in caixa if p['id'] != id_para_remover]
            if len(caixa) < pecas_na_caixa_antes:
                removido_aprovadas = True

        # 3. Tentar remover das reprovadas
        pecas_reprovadas_antes = len(self.pecas_reprovadas)
        self.pecas_reprovadas = [p for p in self.pecas_reprovadas if p['id'] != id_para_remover]
        if len(self.pecas_reprovadas) < pecas_reprovadas_antes:
            removido_reprovadas = True
            
        # Feedback ao usuário
        if not removido_mestre and not removido_aprovadas and not removido_reprovadas:
            print(f"Peça com ID {id_para_remover} não foi encontrada em nenhum local.")
        else:
            print(f"Peça ID {id_para_remover} removida com sucesso do sistema.")
            if removido_aprovadas:
                print("   (Removida da caixa de aprovadas)")
            if removido_reprovadas:
                print("   (Removida da lista de reprovadas)")
            
            # Opcional: Reorganizar caixas se a remoção esvaziar a última
            if self.caixas_de_aprovadas[-1] == [] and len(self.caixas_de_aprovadas) > 1:
                self.caixas_de_aprovadas.pop()
                print("   (A última caixa ficou vazia e foi removida.)")


    def listar_caixas_fechadas(self):
        """
        Opção 4: Mostra o conteúdo apenas das caixas cheias (fechadas).
        """
        print("\n--- [4] Listar Caixas Fechadas ---")
        
        # Caixas fechadas são todas as que atingiram a capacidade
        caixas_fechadas = [c for c in self.caixas_de_aprovadas if len(c) == self.CAPACIDADE_CAIXA]
        
        if not caixas_fechadas:
            print("Nenhuma caixa foi fechada (capacidade máxima) ainda.")
            return

        print(f"Exibindo {len(caixas_fechadas)} caixa(s) fechada(s) (com {self.CAPACIDADE_CAIXA} peças):")
        
        # Para fins de numeração correta, precisamos do índice original
        for i, caixa in enumerate(self.caixas_de_aprovadas):
            if len(caixa) == self.CAPACIDADE_CAIXA:
                print(f"\n   📦 Caixa {i+1} (FECHADA):")
                ids_na_caixa = [str(peca['id']) for peca in caixa]
                print(f"     IDs: [ {', '.join(ids_na_caixa)} ]")

    def gerar_relatorio_final(self):
        """
        Opção 5: Gera o relatório consolidado final.
        """
        print("\n" + "=" * 50)
        print("       [5] RELATÓRIO CONSOLIDADO DE PRODUÇÃO")
        print("=" * 50)

        # 1. Total de Peças Aprovadas
        total_aprovadas = sum(len(caixa) for caixa in self.caixas_de_aprovadas)

        # 2. Total de Peças Reprovadas
        total_reprovadas = len(self.pecas_reprovadas)
        
        # 3. Total Processado
        total_processado = total_aprovadas + total_reprovadas
        print(f"Total de Peças Processadas (na sessão): {total_processado}")
        print(f"Total de Peças Cadastradas (na lista mestre): {len(self.pecas_cadastradas)}")
        print("-" * 50)

        # 4. Quantidade de Caixas
        if total_aprovadas == 0:
            total_caixas = 0
        else:
            total_caixas = len(self.caixas_de_aprovadas)

        print(f"🟢 Total de Peças APROVADAS: {total_aprovadas}")
        print(f"📦 Total de Caixas Utilizadas: {total_caixas}")
        if total_caixas > 0:
            print("\n   Distribuição das Caixas:")
            for i, caixa in enumerate(self.caixas_de_aprovadas):
                status_caixa = "FECHADA" if len(caixa) == self.CAPACIDADE_CAIXA else "ABERTA"
                print(f"      - Caixa {i+1} [{status_caixa}]: {len(caixa)} / {self.CAPACIDADE_CAIXA} peças")

        print("-" * 50)

        # 5. Detalhes da Reprovação
        print(f"🔴 Total de Peças REPROVADAS: {total_reprovadas}")
        if total_reprovadas > 0:
            contagem_motivos = {}
            for item in self.pecas_reprovadas:
                for motivo in item['motivos']:
                    contagem_motivos[motivo] = contagem_motivos.get(motivo, 0) + 1
            
            print("\n   Detalhes da Reprovação (Contagem individual de falhas):")
            for motivo, contagem in sorted(contagem_motivos.items(), key=lambda item: item[1], reverse=True):
                print(f"      - {motivo}: {contagem} ocorrência(s)")
        print("=" * 50)

# --- ------------------------------------------------- ---
# --- LOOP PRINCIPAL DO MENU ---
# --- ------------------------------------------------- ---

def exibir_menu():
    """Imprime o menu de opções na tela."""
    print("\n" + "=" * 45)
    print("   Sistema de Controle de Produção e Qualidade")
    print("=" * 45)
    print("1. Cadastrar nova peça")
    print("2. Listar peças aprovadas/reprovadas")
    print("3. Remover peça cadastrada")
    print("4. Listar caixas fechadas")
    print("5. Gerar relatório final")
    print("0. Sair do Sistema")
    print("-" * 45)

def main():
    # Cria a instância da linha de montagem.
    # Todo o estado (peças, caixas) será mantido aqui.
    linha = LinhaDeMontagem(capacidade_caixa=10) # Você pode mudar a capacidade aqui (ex: 3)
    
    while True:
        exibir_menu()
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            linha.cadastrar_nova_peca()
            
        elif opcao == '2':
            linha.listar_pecas()
            
        elif opcao == '3':
            linha.remover_peca_cadastrada()
            
        elif opcao == '4':
            linha.listar_caixas_fechadas()
            
        elif opcao == '5':
            linha.gerar_relatorio_final()
            
        elif opcao == '0':
            print("\nGerando relatório final antes de sair...")
            linha.gerar_relatorio_final()
            print("\nSistema encerrado.")
            break
            
        else:
            print("\nErro: Opção inválida. Por favor, escolha de 0 a 5.")
        
        # Pausa para o usuário ler a saída
        input("\nPressione [Enter] para continuar...")


# --- Executar o Sistema Interativo ---
if __name__ == "__main__":
    main()