from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Estado, Municipio, Perfil, Avaliador, Conscrito, Avaliacao, Contato, Endereco, Composicao_Familiar, Residente, Psicossocial, Atividades, Particularidades, Esporte, Habilidade, Instrumento

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

class EsporteInline(admin.TabularInline):
    model = Esporte
    extra = 0
    verbose_name = 'Esporte'
    verbose_name_plural = 'ESPORTES'

class HabilidadeInline(admin.TabularInline):
    model = Habilidade
    extra = 0
    verbose_name = 'Habilidade'
    verbose_name_plural = 'HABILIDADES'

class InstrumentoInline(admin.TabularInline):
    model = Instrumento
    extra = 0
    verbose_name = 'Instrumento'
    verbose_name_plural = 'INSTRUMENTOS'

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

@admin.register(Avaliador)
class AvaliadorAdmin(UserAdmin):
    list_display = ('post_grad', 'nome', 'nome_guerra', 'username', 'is_superuser')
    list_display_links = ('post_grad', 'nome', 'nome_guerra', 'username')
    search_fields = ('nome', 'username')
    inlines = [PerfilInline]
    ordering = ('post_grad', 'nome')

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
    inlines = [ContatoInline, EnderecoInline, ComposicaoFamiliarInline, ResidenteInline, PsicossocialInline, AtividadesInline, EsporteInline, HabilidadeInline, InstrumentoInline, ParticularidadesInline, AvaliacaoInline]

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