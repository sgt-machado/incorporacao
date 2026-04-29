from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Tabelas de apoio e choices
class Post_Grad(models.IntegerChoices):
    CORONEL = 1, 'Coronel'
    TENENTE_CORONEL = 2, 'Tenente-Coronel'
    MAJOR = 3, 'Major'
    CAPITAO = 4, 'Capitão'
    PRIMEIRO_TENENTE = 5, '1º Tenente'
    SEGUNDO_TENENTE = 6, '2º Tenente'
    ASPIRANTE = 7, 'Aspirante'
    SUBTENENTE = 8, 'Subtenente'
    PRIMEIRO_SARGENTO = 9, '1º Sargento'
    SEGUNDO_SARGENTO = 10, '2º Sargento'
    TERCEIRO_SARGENTO = 11, '3º Sargento'
    CABO = 12, 'Cabo'
    SOLDADO = 13, 'Soldado'

class Mencoes(models.IntegerChoices):
    INSUFICIENTE = 1, 'Insuficiente'
    REGULAR = 2, 'Regular'
    BOM = 3, 'Bom'
    MUITO_BOM = 4, 'Muito Bom'
    EXCELENTE = 5, 'Excelente'

class CNH_Categoria(models.IntegerChoices):
    NAO_POSSUO = 1, 'Não Possuo CNH'
    A = 2, 'Categoria A'
    B = 3, 'Categoria B'
    C = 4, 'Categoria C'
    D = 5, 'Categoria D'
    E = 6, 'Categoria E'
    AB = 7, 'Categorias A e B'
    AC = 8, 'Categorias A e C'
    AD = 9, 'Categorias A e D'
    AE = 10, 'Categorias A e E'

class Escolaridade(models.IntegerChoices):
    FUNDAMENTAL_INCOMPLETO = 1, 'Fundamental Incompleto'
    FUNDAMENTAL_COMPLETO = 2, 'Fundamental Completo'
    MEDIO_INCOMPLETO = 3, 'Médio Incompleto'
    MEDIO_COMPLETO = 4, 'Médio Completo'
    SUPERIOR_INCOMPLETO = 5, 'Superior Incompleto'
    SUPERIOR_COMPLETO = 6, 'Superior Completo'

class Moradia(models.IntegerChoices):
    IMOVEL_PROPRIO = 1, 'Imóvel Próprio'
    IMOVEL_ALUGADO = 2, 'Imóvel Alugado'
    OUTRO = 3, 'Outro'

class Arrimo(models.IntegerChoices):
    NAO = 1, 'Não se enquadra.'
    FILHO_UNICO = 2, 'Filho único de mulher viúva ou solteira, da abandonada pelo marido ou da desquitada, à qual sirva de único arrimo ou o que ela escolher quando tiver mais de um, sem direito a outra opção.'
    FILHO_PAI_INCAPAZ = 3, 'Filho que sirva de único arrimo ao pai fìsicamente incapaz para prover o seu sustento.'
    VIUVO_COM_DEPENDENTE = 4, 'Viúvo ou desquitado que tiver filho menor (legítimo ou legitimado) de que seja único arrimo.'
    CASADO_COM_DEPENDENTE = 5, 'Casado que sirva de único arrimo à esposa ou à esposa e filho menor (legítimo ou legitimado).'
    SOLTEIRO_COM_DEPENDENTE = 6, 'Solteiro que tiver filho menor (legalmente reconhecido) de que seja único arrimo.'
    ORFAO_COM_DEPENDENTE = 7, 'Órfão de pai e mãe que sustente irmão menor, ou maior inválido ou interdito, ou ainda irmã solteira ou viúva que viva em sua companhia.'
    ORFAO_COM_AVOS_DEPENDENTES = 8, 'Órfão de pai e mãe, que sirva de único arrimo a uma de suas avós ou avô decrépito ou valetudinário, incapaz de prover os meios de subsistência.'

class Parentesco(models.IntegerChoices):
    PAI = 1, 'Pai'
    MAE = 2, 'Mãe'
    IRMAO = 3, 'Irmão'
    IRMA = 4, 'Irmã'
    CUNHADO = 5, 'Cunhado'
    CUNHADA = 6, 'Cunhada'
    TIO = 7, 'Tio'
    TIA = 8, 'Tia'
    SOBRINHO = 9, 'Sobrinho'
    SOBRINHA = 10, 'Sobrinha'
    PRIMO = 11, 'Primo'
    PRIMA = 12, 'Prima'
    PADRASTO = 13, 'Padrasto'
    MADRASTA = 14, 'Madrasta'
    AVO = 15, 'Avô'
    AVOA = 16, 'Avó'
    BISAVO = 17, 'Bisavô'
    BISAVOA = 18, 'Bisavó'
    SOGRO = 19, 'Sogro'
    SOGRA = 20, 'Sogra'
    CONJUGE = 21, 'Cônjuge/Companheiro(a)'
    FILHO = 22, 'Filho'
    FILHA = 23, 'Filha'
    OUTRO = 24, 'Outro'

class ListaEsportes(models.IntegerChoices):
    FUTEBOL = 1, 'Futebol'
    FUTSAL = 2, 'Futsal'
    VOLEI = 3, 'Vôlei'
    BASQUETE = 4, 'Basquete'
    HANDEBOL = 5, 'Handebol'
    RUGBY = 6, 'Rugby'
    FUTEBOL_AMERICANO = 7, 'Futebol Americano'
    BEISEBOL = 8, 'Beisebol'
    TENIS = 9, 'Tênis'
    TENIS_DE_MESA = 10, 'Tênis de Mesa'
    BADMINTON = 11, 'Badminton'
    SQUASH = 12, 'Squash'
    BEACH_TENNIS = 13, 'Beach Tennis'
    VOLEI_DE_PRAIA = 14, 'Vôlei de Praia'
    JUDO = 15, 'Judô'
    KARATE = 16, 'Karatê'
    BOXE = 17, 'Boxe'
    JIU_JITSU = 18, 'Jiu-Jitsu'
    MUAY_THAI = 19, 'Muay Thai'
    MMA = 20, 'MMA'
    ESGRIMA = 21, 'Esgrima'
    TAEKWONDO = 22, 'Taekwondo'
    NATACAO = 23, 'Natação'
    SURFE = 24, 'Surfe'
    POLO_AQUATICO = 25, 'Polo Aquático'
    REMO = 26, 'Remo'
    VELA = 27, 'Vela'
    CANOAGEM = 28, 'Canoagem'
    ATLETISMO = 29, 'Atletismo'
    GINASTICA_ARTISTICA = 30, 'Ginástica Artística'
    GINASTICA_RITMICA = 31, 'Ginástica Rítmica'
    LEVANTAMENTO_DE_PESO = 32, 'Levantamento de Peso'
    TIRO_COM_ARCO = 33, 'Tiro com Arco'
    CICLISMO = 34, 'Ciclismo'
    SKATE = 35, 'Skate'
    GOLFE = 36, 'Golfe'

class ListaHabilidades(models.IntegerChoices):
    PROGRAMACAO = 1, 'Programação'
    DESENVOLVIMENTO_WEB = 2, 'Desenvolvimento Web'
    CIENCIA_DE_DADOS = 3, 'Ciência de Dados'
    SEGURANCA_CIBERNETICA = 4, 'Segurança Cibernética'
    INTELIGENCIA_ARTIFICIAL = 5, 'Inteligência Artificial'
    BANCO_DE_DADOS = 6, 'Banco de Dados'
    FERRAMENTAS_GOOGLE = 7, 'Ferramentas Google'
    PACOTE_OFFICE = 8, 'Pacote Office'
    EDICAO_DE_VIDEO = 9, 'Edição de Vídeo'
    DESIGN_GRAFICO = 10, 'Design Gráfico'
    MARKETING_DIGITAL = 11, 'Marketing Digital'
    GESTAO_DE_TRÁFEGO = 12, 'Gestão de Tráfego'
    MECANICA_AUTOMOTIVA = 13, 'Mecânica de Automóveis'
    MECANICA_MOTOCICLETAS = 14, 'Mecânica de Motocicletas'
    ELETRICA_AUTOMOTIVA = 15, 'Elétrica de Automóveis'
    ELETRONICA = 16, 'Eletrônica'
    ELETRICA_RESIDENCIAL = 17, 'Elétrica Residencial'
    CARPINTARIA = 18, 'Carpintaria'
    ENCANAMENTO = 19, 'Encanamento'
    SOLDA = 20, 'Solda'
    MARCENARIA = 21, 'Marcenaria'
    GESTAO_DE_PROJETOS = 22, 'Gestão de Projetos'
    LIDERANCA = 23, 'Liderança'
    VENDAS = 24, 'Vendas'
    NEGOCIACAO = 25, 'Negociação'
    FINANCAS_PESSOAIS = 26, 'Finanças Pessoais'
    RECURSOS_HUMANOS = 27, 'Recursos Humanos'
    ORATORIA = 28, 'Oratória'
    ESCRITA_CRIATIVA = 29, 'Escrita Criativa'
    INGLES = 30, 'Inglês'
    ESPANHOL = 31, 'Espanhol'
    TRADUCAO = 32, 'Tradução'
    PRIMEIROS_SOCORROS = 33, 'Primeiros Socorros'
    GASTRONOMIA = 34, 'Gastronomia'
    FOTOGRAFIA = 35, 'Fotografia'
    ADESTRAMENTO_DE_CAES = 36, 'Adestramento de Cães'

class ListaInstrumentos(models.IntegerChoices):
    VIOLAO = 1, 'Violão'
    GUITARRA = 2, 'Guitarra Elétrica'
    BAIXO = 3, 'Contrabaixo'
    VIOLINO = 4, 'Violino'
    VIOLONCELO = 5, 'Violoncelo'
    HARPA = 6, 'Harpa'
    UKELELE = 7, 'Ukulele'
    CAVAQUINHO = 8, 'Cavaquinho'
    BANJO = 9, 'Banjo'
    PIANO = 10, 'Piano'
    TECLADO = 11, 'Teclado Sintetizador'
    ORGAO = 12, 'Órgão'
    ACORDEON = 13, 'Acordeom (Sanfona)'
    FLAUTA_DOCE = 14, 'Flauta Doce'
    FLAUTA_TRANSVERSA = 15, 'Flauta Transversa'
    CLARINETE = 16, 'Clarinete'
    SAXOFONE = 17, 'Saxofone'
    OBUE = 18, 'Oboé'
    FAGOTE = 19, 'Fagote'
    TROMPETE = 20, 'Trompete'
    TROMBONE = 21, 'Trombone'
    TUBA = 22, 'Tuba'
    TROMPA = 23, 'Trompa'
    BATERIA = 24, 'Bateria'
    PANDEIRO = 25, 'Pandeiro'
    CAJON = 26, 'Cajón'
    ATABAQUE = 27, 'Atabaque'
    XILOFONE = 28, 'Xilofone'
    TRIANGULO = 29, 'Triângulo'
    CONGAS = 30, 'Congas'
    TIMPANO = 31, 'Tímpano'

class Estado(models.Model):
    id = models.IntegerField(primary_key=True) # Código IBGE (2 dígitos). Ex: 35 para SP
    uf = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} ({self.uf})' # Retorna o nome completo do estado com a UF

class Municipio(models.Model): 
    id = models.IntegerField(primary_key=True) # Código IBGE (7 dígitos). Ex: 3550308 para São Paulo
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='municipios')
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} ({self.estado.uf})' # Retorna o nome completo do município com a UF

# Entidade abstrata
class Usuario(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11, unique=True, verbose_name='CPF')
    nome = models.CharField(max_length=100, verbose_name='Nome Completo')
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name='E-mail')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

# Entidades concretas
class Avaliador(Usuario): # Herda os campos de Usuario
    post_grad = models.IntegerField(
        choices=Post_Grad.choices,
        default=Post_Grad.CORONEL,
        verbose_name='Posto/Graduação')
    nome_guerra = models.CharField(max_length=50, blank=False, null=False, verbose_name='Nome de Guerra')
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # Verifica se a senha já está com hash (se começa com algoritmos conhecidos)
        # Isso evita que o Django faça o hash de um hash já existente ao atualizar o objeto
        if self.senha and not self.senha.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Avaliador"
        verbose_name_plural = "Avaliadores"

class Conscrito(Usuario): # Herda os campos de Usuario
    ra = models.CharField(max_length=12, blank=True, null=True, verbose_name='RA')
    pai = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome do Pai')
    mae = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome da Mãe')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento', help_text='Formato: DD/MM/AAAA')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    rg = models.CharField(max_length=20, verbose_name='RG')
    rg_orgao_emissor = models.CharField(max_length=20, blank=True, null=True, verbose_name='Órgão Emissor do RG')
    titulo_eleitor = models.CharField(max_length=12, blank=True, null=True, verbose_name='Título de Eleitor')
    titulo_zona = models.CharField(max_length=3, blank=True, null=True, verbose_name='Zona Eleitoral')
    titulo_secao = models.CharField(max_length=4, blank=True, null=True, verbose_name='Seção Eleitoral')
    cnh = models.IntegerField(choices=CNH_Categoria.choices, default=CNH_Categoria.NAO_POSSUO, verbose_name='CNH / Categoria')
    escolaridade = models.IntegerField(choices=Escolaridade.choices, default=Escolaridade.MEDIO_COMPLETO)

# Informações complementares (1:1 com Conscrito)
class Contato(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    telefone_pessoal = models.CharField(max_length=15, verbose_name='Telefone')
    telefone_emergencia = models.CharField(max_length=15, blank=True, null=True, verbose_name='Contato de Emergência')
    instagram = models.CharField(max_length=50, blank=True, null=True)
    facebook = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    linkedin = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.conscrito.nome

class Endereco(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    logradouro = models.CharField(max_length=100)
    numero = models.IntegerField(verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=8, verbose_name='CEP')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    def __str__(self):
        return self.conscrito.nome

class Composicao_Familiar(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    moradia = models.IntegerField(choices=Moradia.choices, default=Moradia.IMOVEL_PROPRIO, verbose_name='Tipo de Moradia')
    sustento = models.BooleanField(default=False, verbose_name='Contribui para o sustento da família?')
    contribuicao = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, verbose_name='Contribuição mensal (R$)')
    arrimo = models.IntegerField(choices=Arrimo.choices, default=Arrimo.NAO, verbose_name='Situação de Arrimo')

    def __str__(self):
        return self.conscrito.nome

class Psicossocial(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    drogas = models.CharField(max_length=200, blank=True, null=True, verbose_name='Já consumiu ou consome drogas?')
    jogos = models.CharField(max_length=200, blank=True, null=True, verbose_name='Já participou ou participa de jogos de azar?')
    movimentos_sociais = models.CharField(max_length=200, blank=True, null=True, verbose_name='Já participou ou participa de movimentos sociais?')
    movimentos_politicos = models.CharField(max_length=200, blank=True, null=True, verbose_name='Já participou ou participa de movimentos políticos?')
    movimentos_religiosos = models.CharField(max_length=200, blank=True, null=True, verbose_name='Já participou ou participa de movimentos religiosos?')
    osp = models.CharField(max_length=200, blank=True, null=True, verbose_name='Você ou alguém da família já se envolveu com Órgãos de Segurança Pública, mesmo na condição de testemunha?')
    trafico_proximidades = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nas proximidades do local onde reside existem problemas com relação a tráfico ou consumo de drogas?')
    acao_justica = models.CharField(max_length=200, blank=True, null=True, verbose_name='Possui ações na justiça contra o estado ou a nível federal?')

    def __str__(self):
        return self.conscrito.nome

class Atividades(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    trabalha = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nome da empresa e função que exerce')
    estuda = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nome do estabelecimento de ensino e curso que frequenta')
    clubes_associacoes = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nome do clube ou associação que frequenta e atividade que realiza')

    def __str__(self):
        return self.conscrito.nome

class Particularidades(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    relacao_familiar = models.IntegerField(choices=Mencoes.choices, blank=True, null=True, verbose_name='Relacionamento familiar')
    relacao_social = models.IntegerField(choices=Mencoes.choices, blank=True, null=True, verbose_name='Relacionamento social')
    sv_militar = models.CharField(max_length=200, blank=True, null=True, verbose_name='Alguém da família já serviu às Forças Armadas ou trabalhou em Órgão de Segurança Pública? (Exército, Marinha, Força Aérea, Polícia Militar, Polícia Civil, GCM)')
    armas_fogo = models.CharField(max_length=200, blank=True, null=True, verbose_name='Já utilizou qualquer tipo de arma de fogo?')
    voluntario = models.BooleanField(default=False, verbose_name='Deseja servir voluntariamente?')
    voluntario_justificativa = models.CharField(max_length=200, blank=True, null=True, verbose_name='Justifique sua resposta anterior:')

    def __str__(self):
        return self.conscrito.nome

# Informações complementares (1:N com Conscrito)
class Residente(models.Model):
    conscrito = models.ForeignKey(Conscrito, on_delete=models.CASCADE, related_name='residentes') # Permite acessar os residentes de um conscrito via conscrito.residentes.all()
    parentesco = models.IntegerField(choices=Parentesco.choices, verbose_name='Parentesco')
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    idade = models.PositiveIntegerField(verbose_name="Idade")
    estudante = models.BooleanField(default=False, verbose_name="Estudante?")
    trabalha = models.BooleanField(default=False, verbose_name="Trabalha?")
    renda = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Renda Mensal")

    def __str__(self):
        return self.conscrito.nome

    class Meta:
        verbose_name = "Residente"
        verbose_name_plural = "Residentes"

class Esporte(models.Model):
    conscrito = models.ForeignKey(Conscrito, on_delete=models.CASCADE, related_name='esportes')
    esporte = models.IntegerField(choices=ListaEsportes.choices, blank=True, null=True, verbose_name='Esporte')

    def __str__(self):
        return self.conscrito.nome
    
    class Meta:
        verbose_name = "Esporte"
        verbose_name_plural = "Esportes"

class Habilidade(models.Model):
    conscrito = models.ForeignKey(Conscrito, on_delete=models.CASCADE, related_name='habilidades')
    habilidade = models.IntegerField(choices=ListaHabilidades.choices, blank=True, null=True, verbose_name='Habilidade')

    def __str__(self):
        return self.conscrito.nome
    
    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"

class Instrumento(models.Model):
    conscrito = models.ForeignKey(Conscrito, on_delete=models.CASCADE, related_name='instrumentos')
    instrumento = models.IntegerField(choices=ListaInstrumentos.choices, blank=True, null=True, verbose_name='Instrumento Musical')

    def __str__(self):
        return self.conscrito.nome
    
    class Meta:
        verbose_name = "Instrumento"
        verbose_name_plural = "Instrumentos"