from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from .choices import Tipo_Avaliacao, Tipo_Perfil, Post_Grad, Mencoes, CNH_Categoria, Escolaridade, Moradia, Arrimo, Parentesco, Tamanhos

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
    nome = models.IntegerField(choices=Tipo_Perfil.choices, blank=True, null=True, verbose_name='Perfil')

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
    jaqueta = models.IntegerField(choices=Tamanhos.choices, verbose_name='Tamanho da jaqueta')

class BDI(models.Model):
    # Relacionamento com o seu modelo de Conscrito
    conscrito = models.OneToOneField('Conscrito', on_delete=models.CASCADE, related_name='bdi')
    data_preenchimento = models.DateTimeField(auto_now_add=True)

    # Definição das opções para cada pergunta (Baseado no PDF)
    OPCOES_Q1 = [(0, "Não me sinto triste"), (1, "Eu me sinto triste"), (2, "Estou sempre triste e não consigo sair disto"), (3, "Estou tão triste ou infeliz que não consigo suportar")]
    OPCOES_Q2 = [(0, "Não estou desanimado quanto ao meu futuro"), (1, "Eu me sinto mais desanimado quanto ao meu futuro do que costumava estar"), (2, "Não espero que as coisas deem certo para mim"), (3, "Sinto que meu futuro é sem esperança e que só vai piorar")]
    OPCOES_Q3 = [(0, "Não me sinto um fracasso"), (1, "Fracassei mais do que deveria"), (2, "Ao olhar para trás, vejo muitos fracassos"), (3, "Sinto que sou um fracasso total como pessoa")]
    OPCOES_Q4 = [(0, "Tenho tanto prazer nas coisas como antes"), (1, "Não aproveito as coisas como costumava aproveitar"), (2, "Sinto muito pouco prazer com as coisas"), (3, "Estou completamente insatisfeito")]
    OPCOES_Q5 = [(0, "Não me sinto particularmente culpado"), (1, "Sinto-me culpado boa parte do tempo"), (2, "Sinto-me muito culpado na maior parte do tempo"), (3, "Sinto-me culpado o tempo todo")]
    OPCOES_Q6 = [(0, "Não sinto que estou sendo punido"), (1, "Sinto que posso ser punido"), (2, "Espero ser punido"), (3, "Sinto que estou sendo punido")]
    OPCOES_Q7 = [(0, "Não me sinto decepcionado comigo mesmo"), (1, "Estou decepcionado comigo mesmo"), (2, "Sinto nojo de mim mesmo"), (3, "Eu me odeio")]
    OPCOES_Q8 = [(0, "Não me sinto pior do que ninguém"), (1, "Sou crítico comigo mesmo por minhas fraquezas ou erros"), (2, "Culpo-me o tempo todo por minhas falhas"), (3, "Culpo-me por tudo de ruim que acontece")]
    OPCOES_Q9 = [(0, "Não tenho nenhum pensamento de me matar"), (1, "Tenho pensamentos de me matar, mas não os levaria adiante"), (2, "Gostaria de me matar"), (3, "Eu me mataria se tivesse oportunidade")]
    OPCOES_Q10 = [(0, "Não choro mais do que o habitual"), (1, "Choro mais do que costumava"), (2, "Choro o tempo todo agora"), (3, "Eu costumava ser capaz de chorar, mas agora não consigo nem que eu queira")]
    OPCOES_Q11 = [(0, "Não sou mais irritado do que antes"), (1, "Estou um pouco mais irritado do que o habitual"), (2, "Estou bastante irritado ou chateado boa parte do tempo"), (3, "Sinto-me irritado o tempo todo")]
    OPCOES_Q12 = [(0, "Não perdi o interesse nas outras pessoas"), (1, "Estou menos interessado nas outras pessoas do que costumava estar"), (2, "Perdi a maior parte do meu interesse nas outras pessoas"), (3, "Perdi todo o meu interesse nas outras pessoas")]
    OPCOES_Q13 = [(0, "Tomo decisões tão bem quanto antes"), (1, "Acho mais difícil tomar decisões do que o habitual"), (2, "Tenho muito mais dificuldade em tomar decisões do que costumava ter"), (3, "Tenho problemas para tomar qualquer decisão")]
    OPCOES_Q14 = [(0, "Não sinto que minha aparência esteja pior do que costumava ser"), (1, "Estou preocupado que pareço velho ou sem atrativos"), (2, "Sinto que há mudanças permanentes na minha aparência que me deixam sem atrativos"), (3, "Acredito que pareço feio")]
    OPCOES_Q15 = [(0, "Consigo trabalhar tão bem quanto antes"), (1, "É necessário um esforço extra para começar a fazer algo"), (2, "Tenho que me esforçar muito para fazer qualquer coisa"), (3, "Não consigo fazer trabalho algum")]
    OPCOES_Q16 = [(0, "Consigo dormir tão bem quanto o habitual"), (1, "Não durmo tão bem quanto costumava"), (2, "Acordo 1 ou 2 horas mais cedo que o habitual e acho difícil voltar a dormir"), (3, "Acordo várias horas mais cedo do que costumava e não consigo voltar a dormir")]
    OPCOES_Q17 = [(0, "Não me canso mais do que o habitual"), (1, "Canso-me mais facilmente do que costumava"), (2, "Canso-me fazendo quase qualquer coisa"), (3, "Estou cansado demais para fazer qualquer coisa")]
    OPCOES_Q18 = [(0, "Meu apetite não está pior do que o habitual"), (1, "Meu apetite não é tão bom quanto costumava ser"), (2, "Meu apetite está muito pior agora"), (3, "Não tenho mais nenhum apetite")]
    OPCOES_Q19 = [(0, "Não perdi muito peso ultimamente"), (1, "Perdi mais de 2 quilos"), (2, "Perdi mais de 4 quilos"), (3, "Perdi mais de 7 quilos")]
    OPCOES_Q20 = [(0, "Não estou mais preocupado com minha saúde do que o habitual"), (1, "Estou preocupado com problemas físicos como dores, mal-estar estomacal ou constipação"), (2, "Estou muito preocupado com meus problemas físicos e é difícil pensar em outra coisa"), (3, "Estou tão preocupado com meus problemas físicos que não consigo pensar em mais nada")]
    OPCOES_Q21 = [(0, "Não notei nenhuma mudança recente no meu interesse por sexo"), (1, "Estou menos interessado em sexo do que costumava estar"), (2, "Quase não tenho interesse em sexo"), (3, "Perdi o interesse por sexo completamente")]

    # Campos de Perguntas
    q1 = models.IntegerField(choices=OPCOES_Q1, verbose_name="1. Tristeza")
    q2 = models.IntegerField(choices=OPCOES_Q2, verbose_name="2. Pessimismo")
    q3 = models.IntegerField(choices=OPCOES_Q3, verbose_name="3. Sensação de Fracasso")
    q4 = models.IntegerField(choices=OPCOES_Q4, verbose_name="4. Falta de Satisfação")
    q5 = models.IntegerField(choices=OPCOES_Q5, verbose_name="5. Sentimentos de Culpa")
    q6 = models.IntegerField(choices=OPCOES_Q6, verbose_name="6. Sentimento de Punição")
    q7 = models.IntegerField(choices=OPCOES_Q7, verbose_name="7. Auto-decepção")
    q8 = models.IntegerField(choices=OPCOES_Q8, verbose_name="8. Auto-acusação")
    q9 = models.IntegerField(choices=OPCOES_Q9, verbose_name="9. Ideação Suicida")
    q10 = models.IntegerField(choices=OPCOES_Q10, verbose_name="10. Crises de Choro")
    q11 = models.IntegerField(choices=OPCOES_Q11, verbose_name="11. Irritabilidade")
    q12 = models.IntegerField(choices=OPCOES_Q12, verbose_name="12. Isolamento Social")
    q13 = models.IntegerField(choices=OPCOES_Q13, verbose_name="13. Indecisão")
    q14 = models.IntegerField(choices=OPCOES_Q14, verbose_name="14. Imagem Corporal")
    q15 = models.IntegerField(choices=OPCOES_Q15, verbose_name="15. Inibição para o Trabalho")
    q16 = models.IntegerField(choices=OPCOES_Q16, verbose_name="16. Distúrbio do Sono")
    q17 = models.IntegerField(choices=OPCOES_Q17, verbose_name="17. Fadiga")
    q18 = models.IntegerField(choices=OPCOES_Q18, verbose_name="18. Perda de Apetite")
    q19 = models.IntegerField(choices=OPCOES_Q19, verbose_name="19. Perda de Peso")
    q20 = models.IntegerField(choices=OPCOES_Q20, verbose_name="20. Preocupações Somáticas")
    q21 = models.IntegerField(choices=OPCOES_Q21, verbose_name="21. Perda de Libido")

    @property
    def pontuacao_total(self):
        return sum([getattr(self, f'q{i}') for i in range(1, 22)])

    @property
    def classificacao(self):
        p = self.pontuacao_total
        if p <= 13: return "Mínima"
        if p <= 19: return "Leve"
        if p <= 28: return "Moderada"
        return "Grave"

    class Meta:
        verbose_name = "Resultado BDI"
        verbose_name_plural = "Resultados BDI"
        
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