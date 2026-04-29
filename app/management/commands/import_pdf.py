import tabula as tb
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from unidecode import unidecode  # Adicione esta importação
from app.models import Conscrito, Municipio, Contato, Endereco

class Command(BaseCommand):
    help = 'Importa dados do PDF e faz o preenchimento inicial do banco de dados'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando processamento...")
        
        # 1. Leitura do PDF
        lista_pdf = tb.read_pdf('db.pdf', pages='all', lattice=True, 
                                pandas_options={'header': None}, 
                                java_options=["-Xmx2g"], 
                                encoding='latin1')

        valores_fichas = [
            [str(val).strip() for val in df.iloc[:, 1]] 
            for df in lista_pdf if not df.empty
        ]

        colunas_pdf = ['Nome', 'Pai', 'Mãe', 'Nascimento', 'Mun Nasc', 'RG', 'Logradouro', 'Bairro', 'CEP', 'Telefone', 'CPF', 'E-mail']
        df = pd.DataFrame(valores_fichas, columns=colunas_pdf)

        # 2. Tratamento de Dados
        df['Nascimento'] = pd.to_datetime(df['Nascimento'], format='%d/%m/%Y', errors='coerce')
        
        # 2.1 Separa Município e UF para buscar no banco
        df[['Mun_Nome', 'UF_Sigla']] = df['Mun Nasc'].str.split('-', n=1, expand=True)
        df['Mun_Nome'] = df['Mun_Nome'].str.strip()
        df['UF_Sigla'] = df['UF_Sigla'].str.strip()

        # 3. Importação com Lógica de Relacionamento
        count = 0
        with transaction.atomic():
            # Pré-carregar municípios para performance (opcional, mas evita milhares de queries)
            todos_municipios = Municipio.objects.select_related('estado').all()
            
            # Itera sobre cada linha do DataFrame e importa os dados
            for _, row in df.iterrows():
                try:
                    # NORMALIZAÇÃO: Remove acentos e deixa em maiúsculo para comparar
                    mun_pdf = unidecode(str(row['Mun_Nome'])).upper()
                    uf_pdf = str(row['UF_Sigla']).upper()

                    # Busca o município ignorando acentos
                    municipio_obj = None
                    for m in todos_municipios:
                        if unidecode(m.nome).upper() == mun_pdf and m.estado.uf == uf_pdf:
                            municipio_obj = m
                            break

                    if not municipio_obj:
                        self.stdout.write(self.style.WARNING(f"Não encontrado: {row['Mun_Nome']}-{row['UF_Sigla']}"))
                        continue

                    # Cria o Conscrito
                    conscrito, created = Conscrito.objects.update_or_create(
                        # Busca pelo CPF, que é único. Se já existir, atualiza os outros campos. Se não existir, cria um novo registro.
                        cpf=row['CPF'],
                        defaults={
                            'nome': row['Nome'],
                            'pai': row['Pai'],
                            'mae': row['Mãe'],
                            'data_nascimento': row['Nascimento'],
                            'rg': row['RG'],
                            'municipio': municipio_obj,
                            'email': row['E-mail'],
                            'ra': "",
                            'escolaridade': 4 # Médio Completo (default)
                        }
                    )

                    # Contato e Endereço
                    Contato.objects.update_or_create(
                        conscrito=conscrito,
                        defaults={'telefone_pessoal': row['Telefone'], 'email': row['E-mail']}
                    )

                    Endereco.objects.update_or_create(
                        conscrito=conscrito,
                        defaults={
                            'logradouro': row['Logradouro'],
                            'bairro': row['Bairro'],
                            'cep': row['CEP'].replace('-', '').strip()[:8],
                            'numero': 0 
                        }
                    )
                    count += 1

                # Captura qualquer erro específico para cada linha e continua o processo, evitando que um erro pare toda a importação
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro no CPF {row['CPF']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Sucesso! {count} registros importados."))