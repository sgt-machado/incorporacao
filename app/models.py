from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from .choices import Tipo_Avaliacao, Perfil, Post_Grad, Mencoes, CNH_Categoria, Escolaridade, Moradia, Arrimo, Parentesco, Tamanhos

class Estado(models.Model):
    id = models.IntegerField(primary_key=True) # Código IBGE (2 dígitos). Ex: 35 para SP
    uf = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ['uf']

    def __str__(self):
        return f'{self.nome} ({self.uf})' # Retorna o nome completo do estado com a UF

class Municipio(models.Model): 
    id = models.IntegerField(primary_key=True) # Código IBGE (7 dígitos). Ex: 3550308 para São Paulo
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='municipios')
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ['estado', 'nome']

    def __str__(self):
        return f'{self.nome} ({self.estado.uf})' # Retorna o nome completo do município com a UF

class Esporte(models.Model):
    nome = models.CharField(max_length=100)
    class Meta: ordering = ['nome']
    def __str__(self): return self.nome

class Habilidade(models.Model):
    nome = models.CharField(max_length=100)
    class Meta: ordering = ['nome']
    def __str__(self): return self.nome

class Instrumento(models.Model):
    nome = models.CharField(max_length=100)
    class Meta: ordering = ['nome']
    def __str__(self): return self.nome

# Entidades concretas
class Avaliador(AbstractUser):
    # Usamos o CPF como username (o campo username continua existindo internamente)
    username = models.CharField(max_length=11, unique=True, verbose_name='CPF')
    nome = models.CharField(max_length=100, verbose_name='Nome Completo')
    post_grad = models.IntegerField(
        choices=Post_Grad.choices,
        blank=False, null=True, 
        verbose_name='Posto/Graduação')
    nome_guerra = models.CharField(max_length=50, blank=False, null=False, verbose_name='Nome de Guerra')

    # Desativa os campos nativos do Django
    first_name = None
    last_name = None

    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['post_grad', 'nome_guerra']
        verbose_name = "Avaliador"
        verbose_name_plural = "Avaliadores"

    def __str__(self):
        return f'{self.get_post_grad_display()} {self.nome_guerra}'

class Perfil(models.Model):
    avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE, related_name='perfis')
    nome = models.IntegerField(choices=Perfil.choices, blank=True, null=True, verbose_name='Perfil')

    def __str__(self):
        return self.avaliador.nome
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

class Conscrito(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11, unique=True, verbose_name='CPF')
    nome = models.CharField(max_length=100, verbose_name='Nome Completo')
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

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    conscrito = models.ForeignKey(Conscrito, on_delete=models.CASCADE, related_name='avaliacoes')
    avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE, related_name='avaliacoes')
    tipo = models.IntegerField(choices=Tipo_Avaliacao.choices, verbose_name='Tipo de Avaliação')
    avaliacao_geral = models.IntegerField(choices=Mencoes.choices, verbose_name='Avaliação Geral')
    observacoes = models.TextField(verbose_name='Observações do Avaliador')
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conscrito.nome

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

# Informações complementares (1:1 com Conscrito)
class Contato(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    telefone_pessoal = models.CharField(max_length=15, verbose_name='Telefone')
    telefone_emergencia = models.CharField(max_length=15, blank=True, null=True, verbose_name='Contato de Emergência')
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name='E-mail')
    instagram = models.CharField(max_length=50, blank=True, null=True)
    facebook = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    linkedin = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.conscrito.nome

class Endereco(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    cep = models.CharField(max_length=8, verbose_name='CEP')
    municipio = models.ForeignKey(Municipio, null=True, blank=True, on_delete=models.CASCADE)
    logradouro = models.CharField(max_length=100)
    numero = models.IntegerField(blank=True, null=True, verbose_name='Número')
    bairro = models.CharField(max_length=50)
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')

    class Meta:
        ordering = ['conscrito']

    def __str__(self):
        return self.conscrito.nome

class Composicao_Familiar(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    moradia = models.IntegerField(choices=Moradia.choices, verbose_name='Tipo de Moradia')
    sustento = models.BooleanField(verbose_name='Contribui para o sustento da família?')
    contribuicao = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Contribuição mensal (R$)')
    arrimo = models.IntegerField(choices=Arrimo.choices, verbose_name='Situação de Arrimo')

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
    esportes = models.ManyToManyField(Esporte, blank=True, verbose_name='Esportes que pratica')
    habilidades = models.ManyToManyField(Habilidade, blank=True, verbose_name='Habilidades que possui')
    instrumentos = models.ManyToManyField(Instrumento, blank=True, verbose_name='Instrumentos que toca')

    def __str__(self):
        return self.conscrito.nome

class Particularidades(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    relacao_familiar = models.IntegerField(choices=Mencoes.choices, blank=True, null=True, verbose_name='Relacionamento familiar')
    relacao_social = models.IntegerField(choices=Mencoes.choices, blank=True, null=True, verbose_name='Relacionamento social')
    sv_militar = models.CharField(max_length=200, blank=True, null=True, verbose_name='Alguém da família já serviu às Forças Armadas ou trabalhou em Órgão de Segurança Pública? (EB, MB, FAB, PM, Polícia Civil, GCM)')
    armas_fogo = models.CharField(max_length=200, blank=True, null=True, verbose_name='Já utilizou qualquer tipo de arma de fogo?')
    voluntario = models.BooleanField(verbose_name='Deseja servir voluntariamente?')
    voluntario_justificativa = models.CharField(max_length=200, blank=True, null=True, verbose_name='Justifique sua resposta anterior:')

    def __str__(self):
        return self.conscrito.nome

class GradeFardamento(models.Model):
    conscrito = models.OneToOneField(Conscrito, on_delete=models.CASCADE, primary_key=True)
    calcado = models.PositiveIntegerField(verbose_name='Número do Calçado')
    gorro = models.PositiveIntegerField(verbose_name='Tamanho do Gorro')
    boina = models.PositiveIntegerField(verbose_name='Tamanho da Boina')
    tfm = models.IntegerField(choices=Tamanhos.choices, verbose_name='Tamanho do uniforme de TFM')
    camuflado = models.IntegerField(choices=Tamanhos.choices, verbose_name='Tamanho do uniforme camuflado')
    passeio = models.IntegerField(choices=Tamanhos.choices, verbose_name='Tamanho do uniforme de passeio')
    jaquela = models.IntegerField(choices=Tamanhos.choices, verbose_name='Tamanho da jaqueta')

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