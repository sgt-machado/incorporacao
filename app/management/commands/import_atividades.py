import csv
import os
from django.core.management.base import BaseCommand
from app.models import Esporte, Habilidade, Instrumento

class Command(BaseCommand):
    help = 'Importa listas de esportes, habilidades e instrumentos de arquivos CSV'

    def handle(self, *args, **options):
        # Mapeamento de Arquivo -> Modelo
        arquivos = {
            'esportes.csv': Esporte,
            'habilidades.csv': Habilidade,
            'instrumentos.csv': Instrumento,
        }

        for nome_arquivo, modelo in arquivos.items():
            if not os.path.exists(nome_arquivo):
                self.stderr.write(f'Arquivo {nome_arquivo} não encontrado. Pulando...')
                continue

            self.stdout.write(f'Processando {nome_arquivo}...')
            self.importar_csv(nome_arquivo, modelo)

        self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))

    def importar_csv(self, caminho_arquivo, model_classe):
        objetos_para_criar = []
        
        with open(caminho_arquivo, mode='r', encoding='utf-8') as csv_file:
            # Lendo sem cabeçalho, conforme seu formato: ID,Nome
            leitor = csv.reader(csv_file)
            
            for linha in leitor:
                if not linha: continue  # Pula linhas vazias
                
                id_obj, nome_obj = linha
                objetos_para_criar.append(
                    model_classe(id=int(id_obj), nome=nome_obj.strip())
                )

        # bulk_create é muito mais rápido para listas grandes
        # update_conflicts garante que se o nome mudar no CSV, ele atualiza no banco
        model_classe.objects.bulk_create(
            objetos_para_criar,
            update_conflicts=True,
            unique_fields=['id'],
            update_fields=['nome']
        )
        self.stdout.write(f' -> {len(objetos_para_criar)} itens processados em {model_classe.__name__}.')