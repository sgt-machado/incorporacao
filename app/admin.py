from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Estado, Municipio, Esporte, Habilidade, Instrumento, Perfil, Avaliador, Conscrito, Avaliacao, Contato, Endereco, Composicao_Familiar, Residente, Psicossocial, Atividades, Particularidades, BDI

class ContatoInline(admin.StackedInline):
    model = Contato
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Contato'
    verbose_name_plural = 'CONTATOS'

class EnderecoInline(admin.StackedInline):
    model = Endereco
    autocomplete_fields = ['municipio'] # Transforma o select comum em um campo de busca digitável
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Endereço'
    verbose_name_plural = 'ENDEREÇOS'

class ComposicaoFamiliarInline(admin.StackedInline):
    model = Composicao_Familiar
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Composição Familiar'
    verbose_name_plural = 'COMPOSIÇÃO FAMILIAR'

class ResidenteInline(admin.TabularInline):
    model = Residente
    extra = 0
    verbose_name = 'Residente'
    verbose_name_plural = 'RESIDENTES'

class PsicossocialInline(admin.StackedInline):
    model = Psicossocial
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Psicossocial'
    verbose_name_plural = 'PSICOSSOCIAL'

class AtividadesInline(admin.StackedInline):
    model = Atividades
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Atividades'
    verbose_name_plural = 'ATIVIDADES'

class ParticularidadesInline(admin.StackedInline):
    model = Particularidades
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Particularidades'
    verbose_name_plural = 'PARTICULARIDADES'

class AvaliacaoInline(admin.StackedInline):
    model = Avaliacao
    extra = 0
    max_num = 4
    verbose_name = 'Avaliação'
    verbose_name_plural = 'AVALIAÇÕES'

# Cria um filtro personalizado para ser utilizado na nos Avaliadores
class PerfilFilter(admin.SimpleListFilter):
    title = 'Perfil' # Título que aparece no filtro lateral
    parameter_name = 'perfil_tipo'

    def lookups(self, request, model_admin):
        # Aqui pegamos as opções diretamente do Tipo_Perfil que você definiu no models
        from .models import Tipo_Perfil
        return Tipo_Perfil.choices

    def queryset(self, request, queryset):
        # Filtra os Avaliadores que possuem o perfil selecionado
        if self.value():
            return queryset.filter(perfis__nome=self.value()).distinct()
        return queryset

class PerfilInline(admin.StackedInline):
    model = Perfil
    extra = 0
    max_num = 5
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfis'

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('uf', 'nome')
    search_fields = ('nome', 'uf')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    search_fields = ('nome',)
    list_filter = ('estado',)
    autocomplete_fields = ['estado'] # Útil se tiver muitos estados

@admin.register(Esporte)
class EsporteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Avaliador)
class AvaliadorAdmin(UserAdmin):
    list_display = ('post_grad', 'nome_guerra', 'nome', 'username', 'is_superuser')
    list_display_links = ('post_grad', 'nome', 'nome_guerra', 'username')
    list_filter = list_filter = (PerfilFilter,)
    search_fields = ('nome', 'username')
    inlines = [PerfilInline]
    ordering = ('post_grad', 'nome_guerra')

    # Removemos 'first_name' e 'last_name' dos fieldsets
    fieldsets = (
        ('Informações Pessoais', {'fields': ('post_grad', 'nome', 'nome_guerra', 'email')}),
        ('Dados de login', {'fields': ('username', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('last_login', 'date_joined')

@admin.register(Conscrito)
class ConscritoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ra', 'cpf')
    search_fields = ('nome', 'ra', 'cpf')
    autocomplete_fields = ['municipio'] # Transforma o select comum em um campo de busca digitável
    inlines = [ContatoInline, EnderecoInline, ComposicaoFamiliarInline, ResidenteInline, PsicossocialInline, AtividadesInline, ParticularidadesInline, AvaliacaoInline]

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('conscrito', 'avaliador', 'tipo', 'data_avaliacao')
    list_filter = ('tipo', 'avaliacao_geral', 'avaliador')
    search_fields = ('tipo', 'conscrito__nome', 'avaliador__nome_guerra')
    autocomplete_fields = ['conscrito', 'avaliador'] # Transforma os selects comuns em campos de busca digitáveis

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj: # Se estiver editando um registro existente
            # Remove 'conscrito' da lista de campos exibidos
            return [f for f in fields if f != 'conscrito']
        return fields # Se for um novo registro, mostra todos os campos

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'bairro')
    search_fields = ('nome', 'cpf', 'bairro')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj: # Se estiver editando um registro existente
            # Remove 'conscrito' da lista de campos exibidos
            return [f for f in fields if f != 'conscrito']
        return fields # Se for um novo registro, mostra todos os campos

    def nome(self, obj):
        return obj.conscrito.nome
    nome.admin_order_field = 'conscrito__nome' # Permite ordenar por nome do conscrito

    def cpf(self, obj):
        return obj.conscrito.cpf
    cpf.admin_order_field = 'conscrito__cpf' # Permite ordenar por CPF do conscrito

    def bairro(self, obj):
        return obj.bairro
    bairro.admin_order_field = 'bairro' # Permite ordenar por bairro

@admin.register(Particularidades)
class ParticularidadesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'voluntario')
    search_fields = ('conscrito__nome', 'conscrito__cpf')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj: # Se estiver editando um registro existente
            # Remove 'conscrito' da lista de campos exibidos
            return [f for f in fields if f != 'conscrito']
        return fields # Se for um novo registro, mostra todos os campos

    def nome(self, obj):
        return obj.conscrito.nome

    def cpf(self, obj):
        return obj.conscrito.cpf

class ClassificacaoBDIFilter(admin.SimpleListFilter):
    title = 'Classificação'
    parameter_name = 'classificacao'

    def lookups(self, request, model_admin):
        return (
            ('minima', 'Mínima'),
            ('leve', 'Leve'),
            ('moderada', 'Moderada'),
            ('grave', 'Grave'),
        )

    def queryset(self, request, queryset):
        # Como a classificação depende da soma, filtramos pela pontuação_total
        if self.value() == 'minima':
            return queryset.filter(id__in=[o.id for o in queryset if o.pontuacao_total <= 13])
        if self.value() == 'leve':
            return queryset.filter(id__in=[o.id for o in queryset if 13 < o.pontuacao_total <= 19])
        if self.value() == 'moderada':
            return queryset.filter(id__in=[o.id for o in queryset if 19 < o.pontuacao_total <= 28])
        if self.value() == 'grave':
            return queryset.filter(id__in=[o.id for o in queryset if o.pontuacao_total > 28])
        return queryset

@admin.register(BDI)
class BDIAdmin(admin.ModelAdmin):
    list_display = ('conscrito', 'get_pontuacao', 'get_classificacao', 'data_preenchimento')
    list_filter = (ClassificacaoBDIFilter,)
    search_fields = ('conscrito__nome', 'conscrito__cpf')
    readonly_fields = ('data_preenchimento', 'get_pontuacao', 'get_classificacao')
    ordering = ('conscrito',)

    fieldsets = (
        ('Identificação', {
            'fields': ('conscrito', 'data_preenchimento')
        }),
        ('Resultado da Avaliação', {
            'fields': ('get_pontuacao', 'get_classificacao'),
        }),
        ('Respostas Individuais', {
            'classes': ('collapse',), # Deixa as 21 perguntas recolhidas por padrão
            'fields': [f'q{i}' for i in range(1, 22)],
        }),
    )

    # Métodos para exibir as @properties do Model na lista do Admin
    def get_pontuacao(self, obj):
        return obj.pontuacao_total
    get_pontuacao.short_description = 'Pontuação Total'
    get_pontuacao.admin_order_field = 'q1' # Permite ordenação básica

    def get_classificacao(self, obj):
        return obj.classificacao
    get_classificacao.short_description = 'Classificação'