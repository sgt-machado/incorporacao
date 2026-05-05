from django.db import models

class Tipo_Avaliacao(models.IntegerChoices):
    ENTREVISTA = 1, 'Entrevista'
    MEDICA = 2, 'Avaliação Médica'
    ODONTOLOGICA = 3, 'Avaliação Odontológica'
    ENC_MAT = 4, 'Avaliação do Material'
    SOCIAL = 5, 'Avaliação Social'

class Perfil(models.IntegerChoices):
    ENTREVISTADOR = 1, 'Entrevistador(a)'
    MEDICO = 2, 'Médico(a)'
    DENTISTA = 3, 'Dentista'
    ENC_MAT = 4, 'Encarregado de Material'
    SOCIAL = 5, 'Investigador(a) Social'

class Post_Grad(models.IntegerChoices):
    CORONEL = 1, 'Cel'
    TENENTE_CORONEL = 2, 'Ten Cel'
    MAJOR = 3, 'Maj'
    CAPITAO = 4, 'Cap'
    PRIMEIRO_TENENTE = 5, '1º Ten'
    SEGUNDO_TENENTE = 6, '2º Ten'
    ASPIRANTE = 7, 'Asp Of'
    SUBTENENTE = 8, 'STen'
    PRIMEIRO_SARGENTO = 9, '1º Sgt'
    SEGUNDO_SARGENTO = 10, '2º Sgt'
    TERCEIRO_SARGENTO = 11, '3º Sgt'
    CABO = 12, 'Cb'
    SOLDADO = 13, 'Sd'

class Mencoes(models.IntegerChoices):
    RUIM = 1, 'Ruim'
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

class Tamanhos(models.IntegerChoices):
    P = 1, 'P'
    M = 2, 'M'
    G = 3, 'G'
    GG = 4, 'GG'