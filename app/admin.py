from django import forms
from django.contrib import admin
from .models import Estado, Municipio, Avaliador, Conscrito, Contato, Endereco, Composicao_Familiar, Residente, Psicossocial, Atividades, Particularidades, Esporte, Habilidade, Instrumento

class AvaliadorAdminForm(forms.ModelForm):
    class Meta:
        model = Avaliador
        fields = '__all__'
        widgets = {
            # Define o widget de senha para ocultar o que é digitado
            'senha': forms.PasswordInput(render_value=True),
        }

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
    extra = 1
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
    extra = 1
    verbose_name = 'Esporte'
    verbose_name_plural = 'ESPORTES'

class HabilidadeInline(admin.TabularInline):
    model = Habilidade
    extra = 1
    verbose_name = 'Habilidade'
    verbose_name_plural = 'HABILIDADES'

class InstrumentoInline(admin.TabularInline):
    model = Instrumento
    extra = 1
    verbose_name = 'Instrumento'
    verbose_name_plural = 'INSTRUMENTOS'

class ParticularidadesInline(admin.StackedInline):
    model = Particularidades
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Particularidades'
    verbose_name_plural = 'PARTICULARIDADES'

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('uf', 'nome')
    search_fields = ('nome', 'uf')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    list_filter = ('estado',)
    search_fields = ('nome',)
    autocomplete_fields = ['estado'] # Útil se tiver muitos estados

@admin.register(Avaliador)
class AvaliadorAdmin(admin.ModelAdmin):
    form = AvaliadorAdminForm
    list_display = ('post_grad', 'nome', 'nome_guerra', 'cpf')
    list_display_links = ('nome',)
    search_fields = ('nome', 'cpf')
    fields = ('post_grad', 'nome', 'nome_guerra', 'cpf', 'email', 'senha')

@admin.register(Conscrito)
class ConscritoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ra', 'cpf')
    search_fields = ('nome', 'ra', 'cpf')
    autocomplete_fields = ['municipio'] # Transforma o select comum em um campo de busca digitável
    inlines = [ContatoInline, EnderecoInline, ComposicaoFamiliarInline, ResidenteInline, PsicossocialInline, AtividadesInline, EsporteInline, HabilidadeInline, InstrumentoInline, ParticularidadesInline] # Exibe os inlines de contato, endereço, composição familiar, residentes, psicossocial, atividades, particularidades, esportes, habilidades e instrumentos na mesma página do conscrito

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone_pessoal')
    search_fields = ('nome', 'cpf')

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

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'bairro')
    search_fields = ('nome', 'cpf')

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

@admin.register(Composicao_Familiar)
class ComposicaoFamiliarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'sustento', 'arrimo')
    search_fields = ('nome', 'cpf')

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

@admin.register(Residente)
class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'parentesco', 'idade')
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

@admin.register(Psicossocial)
class PsicossocialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf')
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

@admin.register(Atividades)
class AtividadesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf')
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

@admin.register(Esporte)
class EsporteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'esporte')
    search_fields = ('conscrito__nome', 'conscrito__cpf', 'esporte')

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

@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'habilidade')
    search_fields = ('conscrito__nome', 'conscrito__cpf', 'habilidade')

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

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'instrumento')
    search_fields = ('conscrito__nome', 'conscrito__cpf', 'instrumento')

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

@admin.register(Particularidades)
class ParticularidadesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf')
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