from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.db.models import Q
from .models import Municipio, Esporte, Habilidade, Instrumento, Avaliador, Conscrito, Avaliacao, Contato, Endereco, Composicao_Familiar, Residente, Psicossocial, Atividades, Particularidades
from .forms import ConscritoForm, AvaliacaoForm, ContatoForm, EnderecoForm, ComposicaoFamiliarForm, ResidenteForm, PsicossocialForm, AtividadesForm, ParticularidadesForm

import re

def carregar_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
    return JsonResponse(list(municipios.values('id', 'nome')), safe=False)

def entrevista(request, pk):
    conscrito = get_object_or_404(Conscrito, pk=pk)
    contato = Contato.objects.filter(conscrito=conscrito).first()
    endereco = Endereco.objects.filter(conscrito=conscrito).first()
    composicao_familiar = Composicao_Familiar.objects.filter(conscrito=conscrito).first()
    psicossocial = Psicossocial.objects.filter(conscrito=conscrito).first()
    atividades = Atividades.objects.filter(conscrito=conscrito).first()
    particularidades = Particularidades.objects.filter(conscrito=conscrito).first()
    avaliacao = Avaliacao.objects.filter(conscrito=conscrito, tipo=1).first()
    
    # Cria as fábricas de formsets
    ResidenteFormSet = inlineformset_factory(
        Conscrito, Residente, form=ResidenteForm, 
        extra=0, can_delete=True
    )

    if request.method == 'POST':
        # 1. Criamos uma cópia para limpar as máscaras antes de validar
        post_data = request.POST.copy()
        if 'conscrito-cpf' in post_data:
            post_data['conscrito-cpf'] = re.sub(r'\D', '', post_data['conscrito-cpf'])
        
        if 'endereco-cep' in post_data:
            post_data['endereco-cep'] = re.sub(r'\D', '', post_data['endereco-cep'])
        
        # 2. Inicializamos os forms com os dados já limpos
        conscrito_form = ConscritoForm(post_data, instance=conscrito, prefix='conscrito')
        contato_form = ContatoForm(post_data, instance=contato, prefix='contato')
        endereco_form = EnderecoForm(post_data, instance=endereco, prefix='endereco')
        composicao_familiar_form = ComposicaoFamiliarForm(post_data, instance=composicao_familiar, prefix='composicao_familiar')
        residente_form = ResidenteFormSet(post_data, instance=conscrito, prefix='residentes')
        psicossocial_form = PsicossocialForm(post_data, instance=psicossocial, prefix='psicossocial')
        atividades_form = AtividadesForm(post_data, instance=atividades, prefix='atividades')
        particularidades_form = ParticularidadesForm(post_data, instance=particularidades, prefix='particularidades')
        avaliacao_form = AvaliacaoForm(post_data, instance=avaliacao, prefix='avaliacao')

        # 3. Validamos e salvamos
        if all([conscrito_form.is_valid(), contato_form.is_valid(), endereco_form.is_valid(), composicao_familiar_form.is_valid(), residente_form.is_valid(), psicossocial_form.is_valid(), atividades_form.is_valid(), particularidades_form.is_valid(), avaliacao_form.is_valid()]):
            # 1. Salva o objeto principal primeiro
            conscrito = conscrito_form.save()

            # 2. Lista de formulários 1:1 que precisam do vínculo manual
            forms_vinculados = [
                contato_form,
                endereco_form,
                composicao_familiar_form,
                psicossocial_form,
                atividades_form,
                particularidades_form
            ]

            # 3. Loop genérico para salvar injetando o conscrito
            for forms in forms_vinculados:
                obj = forms.save(commit=False)
                obj.conscrito = conscrito
                obj.save()
                forms.save_m2m()

            # 4. Salva os Formsets (eles já gerenciam o vínculo sozinhos)
            residente_form.save()

            # 5. Salva a Avaliação com lógica específica por enquanto
            avaliacao = avaliacao_form.save(commit=False)
            avaliacao.conscrito = conscrito # Garantimos que a avaliação esteja vinculada ao conscrito correto

            ''' --------------------------- Ponto de Atenção ---------------------------
            Modificar a forma que é captado o avaliador que está executando a avaliação
            No momento, está sendo salvo baseado em um CPF fixo'''

            avaliacao.avaliador = Avaliador.objects.get(username='00712883509') # Vinculamos o avaliador logado
            avaliacao.tipo = 1
            avaliacao.save()
            ''' --------------------------- Ponto de Atenção --------------------------- '''

            # Redireciona para página de busca para iniciar nova avaliação
            ''' --------------------------- Ponto de Atenção ---------------------------
            Criar uma página para impressão da ficha de entrevista. Após impressão,
            seguir para a página de busca'''
            return redirect('buscar')
        else:
            # Debug: Se não salvar, você verá o erro no terminal do VS Code/PyCharm
            print("Erros Conscrito:", conscrito_form.errors)
            print("Erros Contato:", contato_form.errors)
            print("Erros Endereco:", endereco_form.errors)
            print("Erros Composição Familiar:", composicao_familiar_form.errors)
            print("Erros Residentes:", residente_form.errors)
            print("Erros Psicossocial:", psicossocial_form.errors)
            print("Erros Atividades:", atividades_form.errors)
            print("Erros Particularidades:", particularidades_form.errors)
            print("Erros Avaliação:", avaliacao_form.errors)
    else:
        # Carregamento inicial (GET)
        conscrito_form = ConscritoForm(instance=conscrito, prefix='conscrito')
        contato_form = ContatoForm(instance=contato, prefix='contato')
        endereco_form = EnderecoForm(instance=endereco, prefix='endereco')
        composicao_familiar_form = ComposicaoFamiliarForm(instance=composicao_familiar, prefix='composicao_familiar')
        residente_form = ResidenteFormSet(instance=conscrito, prefix='residentes')
        psicossocial_form = PsicossocialForm(instance=psicossocial, prefix='psicossocial')
        atividades_form = AtividadesForm(instance=atividades, prefix='atividades')
        particularidades_form = ParticularidadesForm(instance=particularidades, prefix='particularidades')
        avaliacao_form = AvaliacaoForm(instance=avaliacao, prefix='avaliacao')

    return render(request, 'avaliadores/entrevista.html', {
        'conscrito_form': conscrito_form,
        'contato_form': contato_form,
        'endereco_form': endereco_form,
        'composicao_familiar_form': composicao_familiar_form,
        'residente_form': residente_form,
        'psicossocial_form': psicossocial_form,
        'atividades_form': atividades_form,
        'particularidades_form': particularidades_form,
        'avaliacao_form': avaliacao_form,
    })

def buscar(request):
    # Filtra apenas quem ainda não tem avaliação do tipo 1 (Entrevista)
    conscritos = Conscrito.objects.exclude(avaliacoes__tipo=1).order_by('nome')

    # Captura o termo de pesquisa (vindo de um formulário com method="GET")
    termo_busca = request.GET.get('termo', '').strip()
    
    if termo_busca:
        # Filtra a lista inicial por Nome, CPF ou RA
        conscritos = conscritos.filter(
            Q(nome__icontains=termo_busca) | 
            Q(cpf__icontains=termo_busca) | 
            Q(ra__icontains=termo_busca)
        )

    return render(request, 'buscar.html', {
        'conscritos': conscritos,
        'termo_busca': termo_busca
    })

def medico(request, pk):
    pass

def odonto(request, pk):
    pass

def social(request, pk):
    pass