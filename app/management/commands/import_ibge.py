import requests
from django.core.management.base import BaseCommand
from app.models import Estado, Municipio

class Command(BaseCommand):
    help = 'Importa estados e municípios do IBGE para o banco de dados'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando importação...')
        self.importar_estados()
        self.importar_municipios()
        self.stdout.write(self.style.SUCCESS('Processo concluído com sucesso!'))

    def importar_estados(self):
        url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
        response = requests.get(url)
        
        if response.status_code == 200:
            self.stdout.write('Processando estados...')
            estados_data = response.json()
            for estado in estados_data:
                # update_or_create é seguro para estados (são apenas 27)
                Estado.objects.update_or_create(
                    id=estado['id'],
                    defaults={'uf': estado['sigla'], 'nome': estado['nome']}
                )
        else:
            self.stderr.write('Erro ao acessar API de Estados')

    def importar_municipios(self):
        url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
        response = requests.get(url)
        
        if response.status_code == 200:
            self.stdout.write('Preparando lista de municípios...')
            municipios_data = response.json()
            municipios_objs = []

            for municipio in municipios_data:
                # Navegação segura usando .get() para evitar o erro NoneType
                micro = municipio.get('microrregiao') or {}
                meso = micro.get('mesorregiao') or {}
                uf = meso.get('UF') or {}
                id_estado = uf.get('id')

                if id_estado:
                    municipios_objs.append(
                        Municipio(
                            id=municipio['id'],
                            nome=municipio['nome'],
                            estado_id=id_estado
                        )
                    )

            self.stdout.write(f'Salvando {len(municipios_objs)} municípios no banco...')
            Municipio.objects.bulk_create(municipios_objs, ignore_conflicts=True)
        else:
            self.stderr.write('Erro ao acessar API de Municípios')
