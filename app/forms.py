from django import forms
from .models import Estado, Municipio, Conscrito, Avaliacao, Contato, Endereco, Composicao_Familiar, Residente, Psicossocial, Atividades, Particularidades, Esporte, Habilidade, Instrumento

# Classe Base para reaproveitar a lógica de Estado/Município
class Localidade:
    def configurar_localidade(self):
        # Ajusta rótulos
        self.fields['estado'].label_from_instance = lambda obj: f"{obj.uf}"
        self.fields['municipio'].label_from_instance = lambda obj: f"{obj.nome}"
        
        # Lógica de filtragem (POST ou Instância)
        estado_id = None
        if self.data.get(self.add_prefix('estado')):
            try:
                estado_id = int(self.data.get(self.add_prefix('estado')))
            except (ValueError, TypeError):
                pass
        elif self.instance and self.instance.pk and getattr(self.instance, 'municipio', None):
            estado_id = self.instance.municipio.estado_id
            self.initial['estado'] = estado_id

        if estado_id:
            self.fields['municipio'].queryset = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
        else:
            self.fields['municipio'].queryset = Municipio.objects.none()

# Campos repetidos definidos em uma função para evitar redundância
def get_localidade_fields():
    return {
        'estado': forms.ModelChoiceField(
            queryset=Estado.objects.all().order_by('uf'),
            widget=forms.Select(attrs={'class': 'form-select'}),
            label="Estado (UF)",
            empty_label="Selecione a UF",
            required=False
        ),
        'municipio': forms.ModelChoiceField(
            queryset=Municipio.objects.none(),  # Inicialmente vazio, será preenchido via AJAX
            widget=forms.Select(attrs={'class': 'form-select'}),
            label="Município",
            empty_label="Selecione o município",
            required=False
        )
    }

class ConscritoForm(forms.ModelForm, Localidade):
    locals().update(get_localidade_fields()) # Adiciona os campos de estado e município ao form

    class Meta:
        model = Conscrito
        # Use apenas campos que existem em 'Conscrito'
        fields = ['nome', 'cpf', 'ra', 'pai', 'mae', 'data_nascimento', 'municipio', 'rg', 'rg_orgao_emissor', 'titulo_eleitor', 'titulo_zona', 'titulo_secao', 'cnh', 'escolaridade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'ra': forms.TextInput(attrs={'class': 'form-control'}),
            'pai': forms.TextInput(attrs={'class': 'form-control'}),
            'mae': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'rg_orgao_emissor': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_eleitor': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_zona': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_secao': forms.TextInput(attrs={'class': 'form-control'}),
            'cnh': forms.Select(attrs={'class': 'form-select'}),
            'escolaridade': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configurar_localidade() # Configura os campos de estado e município

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['avaliacao_geral', 'observacoes']
        widgets = {
            'avaliacao_geral': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['telefone_pessoal', 'telefone_emergencia', 'email', 'instagram', 'facebook', 'twitter', 'linkedin']
        widgets = {
            'telefone_pessoal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'telefone_emergencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario'}),
        }

    # Se você quiser que alguns campos apareçam mas NÃO sejam editáveis (como o CPF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Exemplo: O CPF e Nome já vêm preenchidos e o usuário não pode mudar
            if 'cpf' in self.fields:
                self.fields['cpf'].disabled = True
            if 'nome' in self.fields:
                self.fields['nome'].disabled = True

class EnderecoForm(forms.ModelForm, Localidade):
    locals().update(get_localidade_fields()) # Adiciona os campos de estado e município ao form
    
    class Meta:
        model = Endereco
        fields = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'municipio']
        widgets = {
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'placeholder': 'Número'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configurar_localidade() # Configura os campos de estado e município

class ComposicaoFamiliarForm(forms.ModelForm):
    class Meta:
        model = Composicao_Familiar
        fields = ['moradia', 'sustento', 'contribuicao', 'arrimo']
        widgets = {
            'moradia': forms.Select(attrs={'class': 'form-select'}),
            'sustento': forms.RadioSelect(
                choices=[(True, 'Sim'), (False, 'Não')],
                attrs={'class': 'form-check-input me-1'}
            ),
            'contribuicao': forms.NumberInput(attrs={'class': 'form-control', 'step': '100.00', 'placeholder': '000,00'}),
            'arrimo': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

class ResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['parentesco', 'nome', 'idade', 'estudante', 'trabalha', 'renda']
        widgets = {
            'parentesco': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'estudante': forms.RadioSelect(
                choices=[(True, 'Sim'), (False, 'Não')],
                attrs={'class': 'form-check-input me-1', 'required': True}
            ),
            'trabalha': forms.RadioSelect(
                choices=[(True, 'Sim'), (False, 'Não')],
                attrs={'class': 'form-check-input me-1', 'required': True}
            ),
            'renda': forms.NumberInput(attrs={'class': 'form-control', 'step': '100.00', 'placeholder': '000,00'}),
        }

class PsicossocialForm(forms.ModelForm):
    class Meta:
        model = Psicossocial
        fields = ['drogas', 'jogos', 'movimentos_sociais', 'movimentos_politicos', 'movimentos_religiosos', 'osp', 'trafico_proximidades', 'acao_justica']
        widgets = {
            'drogas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva qual(is) droga(s) e quando utilizou'}),
            'jogos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva quais tipos de jogos'}),
            'movimentos_sociais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva quais movimentos sociais'}),
            'movimentos_politicos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva quais movimentos políticos'}),
            'movimentos_religiosos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva quais movimentos religiosos'}),
            'osp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva quem teve envolvimento, como e quando'}),
            'trafico_proximidades': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva o que ocorre e quão próximo'}),
            'acao_justica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva qual ação judicial, quando e qual o desfecho'}),
        }

class AtividadesForm(forms.ModelForm):
    class Meta:
        model = Atividades
        fields = ['trabalha', 'estuda', 'clubes_associacoes']
        widgets = {
            'trabalha': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa e função que exerce'}),
            'estuda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do estabelecimento de ensino e curso que frequenta'}),
            'clubes_associacoes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do clube ou associação que frequenta e atividade que realiza'}),
        }

class EsporteForm(forms.ModelForm):
    class Meta:
        model = Esporte
        fields = ['esporte']
        widgets = {
            'esporte': forms.Select(attrs={'class': 'form-select', 'required': True}),
        }

class HabilidadeForm(forms.ModelForm):
    class Meta:
        model = Habilidade
        fields = ['habilidade']
        widgets = {
            'habilidade': forms.Select(attrs={'class': 'form-select', 'required': True}),
        }

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ['instrumento']
        widgets = {
            'instrumento': forms.Select(attrs={'class': 'form-select', 'required': True}),
        }

class ParticularidadesForm(forms.ModelForm):
    class Meta:
        model = Particularidades
        fields = ['relacao_familiar', 'relacao_social', 'sv_militar', 'armas_fogo', 'voluntario', 'voluntario_justificativa']
        widgets = {
            'relacao_familiar': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'relacao_social': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'sv_militar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva quem serviu ou trabalhou e quando'}),
            'armas_fogo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva quando e como utilizou'}),
            'voluntario': forms.RadioSelect(
                choices=[(True, 'Sim'), (False, 'Não')],
                attrs={'class': 'form-check-input me-1', 'required': True}
            ),
            'voluntario_justificativa': forms.Textarea(attrs={'class': 'form-control', 'required': True, 'rows': 3, 'placeholder': 'Justifique sua resposta anterior'}),
        }