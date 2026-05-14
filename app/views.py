from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.db.models import Q
from .models import Municipio, Conscrito, Avaliacao, Contato, Endereco, Composicao_Familiar, Residente, Psicossocial, Atividades, Particularidades, BDI
from .forms import LoginForm, ConscritoLoginForm, ConscritoForm, AvaliacaoForm, ContatoForm, EnderecoForm, ComposicaoFamiliarForm, ResidenteForm, PsicossocialForm, AtividadesForm, ParticularidadesForm, BDIForm
from .choices import Tipo_Perfil, Tipo_Avaliacao

import re

MAPA_PERFIL_AVALIACAO = {
    Tipo_Perfil.ENTREVISTADOR: Tipo_Avaliacao.ENTREVISTA,
    Tipo_Perfil.MEDICO: Tipo_Avaliacao.MEDICA,
    Tipo_Perfil.DENTISTA: Tipo_Avaliacao.ODONTOLOGICA,
    Tipo_Perfil.ENC_MAT: Tipo_Avaliacao.ENC_MAT,
    Tipo_Perfil.SOCIAL: Tipo_Avaliacao.SOCIAL,
}

def carregar_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
    return JsonResponse(list(municipios.values('id', 'nome')), safe=False)

def login_view(request):
    form = LoginForm(request.POST or None)
    erro = None

    if request.method == 'POST' and form.is_valid():
        cpf = form.cleaned_data['cpf']
        senha = form.cleaned_data['senha']
        perfil_selecionado = int(form.cleaned_data['perfil'])

        user = authenticate(request, username=cpf, password=senha)

        if user is not None:
            # Verifica se o usuário tem esse perfil vinculado a ele
            if user.perfis.filter(nome=perfil_selecionado).exists():
                login(request, user)
                # Guardamos o perfil na sessão para usar na busca depois
                request.session['perfil_ativo'] = perfil_selecionado

                # Busca o parâmetro 'next' na URL
                proxima_pagina = request.GET.get('next')
                if proxima_pagina:
                    return redirect(proxima_pagina)
                
                return redirect('buscar')
            else:
                erro = "Você não possui permissão para este perfil."
        else:
            erro = "CPF ou Senha inválidos."

    return render(request, 'login.html', {'form': form, 'erro': erro})

def logout_view(request):
    logout(request)
    return redirect('login')

def conscrito(request):
    # Verifica se já existe um conscrito autenticado na sessão
    conscrito_id = request.session.get('conscrito_id')
    form_acesso = ConscritoLoginForm(request.POST or None)
    erro = None
    conscrito = Conscrito.objects.filter(pk=conscrito_id).first() if conscrito_id else None
    bdi = BDI.objects.filter(conscrito=conscrito).first() if conscrito else None

    if request.method == 'POST':
        # Se o botão clicado foi o de 'btn_acessar' e o preenchimento do formulário ConscritoLoginForm estiver válido
        if 'btn_acessar' in request.POST and form_acesso.is_valid():
            cpf = form_acesso.cleaned_data['cpf']
            data_nasc = form_acesso.cleaned_data['data_nascimento']
            conscrito = Conscrito.objects.filter(cpf=cpf, data_nascimento=data_nasc).first()
            
            if conscrito:
                request.session['conscrito_id'] = conscrito.pk
                contato = Contato.objects.filter(conscrito=conscrito).first()
                endereco = Endereco.objects.filter(conscrito=conscrito).first()
                composicao_familiar = Composicao_Familiar.objects.filter(conscrito=conscrito).first()
                atividades = Atividades.objects.filter(conscrito=conscrito).first()
                particularidades = Particularidades.objects.filter(conscrito=conscrito).first()
                
                # Cria as fábricas de formsets
                ResidenteFormSet = inlineformset_factory(
                    Conscrito, Residente, form=ResidenteForm, 
                    extra=0, can_delete=True
                )
                
                # Carregamento inicial (GET)
                conscrito_form = ConscritoForm(instance=conscrito, prefix='conscrito')
                contato_form = ContatoForm(instance=contato, prefix='contato')
                endereco_form = EnderecoForm(instance=endereco, prefix='endereco')
                composicao_familiar_form = ComposicaoFamiliarForm(instance=composicao_familiar, prefix='composicao_familiar')
                residente_form = ResidenteFormSet(instance=conscrito, prefix='residentes')
                atividades_form = AtividadesForm(instance=atividades, prefix='atividades')
                particularidades_form = ParticularidadesForm(instance=particularidades, prefix='particularidades')

                return render(request, 'conscritos/acesso.html', {
                    'conscrito_form': conscrito_form,
                    'contato_form': contato_form,
                    'endereco_form': endereco_form,
                    'composicao_familiar_form': composicao_familiar_form,
                    'residente_form': residente_form,
                    'atividades_form': atividades_form,
                    'particularidades_form': particularidades_form,
                })
            else:
                erro = "Dados não conferem. Verifique o CPF e a Data de Nascimento."
        
        # Se o botão clicado foi o de 'btn_entrevista' e já tiver um conscrito atribuído à respectiva variável
        elif 'btn_entrevista' in request.POST and conscrito:
            contato = Contato.objects.filter(conscrito=conscrito).first()
            endereco = Endereco.objects.filter(conscrito=conscrito).first()
            composicao_familiar = Composicao_Familiar.objects.filter(conscrito=conscrito).first()
            atividades = Atividades.objects.filter(conscrito=conscrito).first()
            particularidades = Particularidades.objects.filter(conscrito=conscrito).first()
            
            # Cria as fábricas de formsets
            ResidenteFormSet = inlineformset_factory(
                Conscrito, Residente, form=ResidenteForm, 
                extra=0, can_delete=True
            )

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
            atividades_form = AtividadesForm(post_data, instance=atividades, prefix='atividades')
            particularidades_form = ParticularidadesForm(post_data, instance=particularidades, prefix='particularidades')

            # 3. Validamos e salvamos
            if all([conscrito_form.is_valid(), contato_form.is_valid(), endereco_form.is_valid(), composicao_familiar_form.is_valid(), residente_form.is_valid(), atividades_form.is_valid(), particularidades_form.is_valid()]):
                # 1. Salva o objeto principal primeiro
                conscrito = conscrito_form.save()

                # 2. Lista de formulários 1:1 que precisam do vínculo manual
                forms_vinculados = [
                    contato_form,
                    endereco_form,
                    composicao_familiar_form,
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
            else:
                # Debug: Se não salvar, você verá o erro no terminal
                print("-----------------------------------------------------")
                print("Existem erros a serem tratados:")
                print("Conscrito:", conscrito_form.errors)
                print("Contato:", contato_form.errors)
                print("Endereco:", endereco_form.errors)
                print("Composição Familiar:", composicao_familiar_form.errors)
                print("Residentes:", residente_form.errors)
                print("Atividades:", atividades_form.errors)
                print("Particularidades:", particularidades_form.errors)
                print("-----------------------------------------------------")

            return render(request, 'conscritos/acesso.html', {
                'bdi_form': BDIForm(request.POST, instance=bdi),
            })
        
        elif 'btn_bdi' in request.POST and conscrito:
            if bdi:
                erro = "Este questionário já foi preenchido por você anteriormente. Se acreditar que não tenha respondido, procure um militar responsável para auxiliá-lo."
                del request.session['conscrito_id']
            else:
                bdi_form = BDIForm(request.POST, instance=bdi)
                if bdi_form.is_valid():
                    # Cria a instância mas não salva no banco ainda
                    obj = bdi_form.save(commit=False)
                    # Vincula o conscrito da sessão ao resultado
                    obj.conscrito = conscrito
                    obj.save()
                    del request.session['conscrito_id']
                    return render(request, 'conscritos/acesso.html', {'form_acesso': form_acesso, 'sucesso': True})
                else:
                    return render(request, 'conscritos/acesso.html', {'bdi_form': bdi_form})
            
            context = {'form_acesso': form_acesso, 'erro': erro}
            return render(request, 'conscritos/acesso.html', context)
        
        else:
            erro = form_acesso.errors.get('cpf', form_acesso.non_field_errors())[0]

    return render(request, 'conscritos/acesso.html', {
        'form_acesso': form_acesso,
        'erro': erro
    })

@login_required
def buscar(request):
    # Pega o perfil selecionado no login (salvo na sessão)
    perfil_session = request.session.get('perfil_ativo')
    
    if not perfil_session:
        return redirect('login')

    # Identifica qual tipo de avaliação esse perfil deve realizar
    tipo_excluir = MAPA_PERFIL_AVALIACAO.get(perfil_session)

    # Filtra: Exclui conscritos que já possuem a avaliação do tipo correspondente
    conscritos = Conscrito.objects.exclude(
        avaliacoes__tipo=tipo_excluir
    ).order_by('nome')

    # Lógica de busca por texto (CPF, Nome, RA)
    termo_busca = request.GET.get('termo', '').strip()
    if termo_busca:
        conscritos = conscritos.filter(
            Q(nome__icontains=termo_busca) | 
            Q(cpf__icontains=termo_busca) | 
            Q(ra__icontains=termo_busca)
        )

    return render(request, 'buscar.html', {
        'conscritos': conscritos,
        'termo_busca': termo_busca,
        'perfil_ativo': perfil_session,
        'Perfil': Tipo_Perfil # Passamos o Enum para usar as constantes no template
    })

@login_required
def entrevista(request, pk):
    # Pega o perfil selecionado no login (salvo na sessão)
    perfil_session = request.session.get('perfil_ativo')
    
    if not perfil_session:
        return redirect('login')
    
    # Identifica qual tipo de avaliação esse perfil deve realizar
    tipo_avl = request.session.get('perfil_ativo')
    
    conscrito = get_object_or_404(Conscrito, pk=pk)
    contato = Contato.objects.filter(conscrito=conscrito).first()
    endereco = Endereco.objects.filter(conscrito=conscrito).first()
    composicao_familiar = Composicao_Familiar.objects.filter(conscrito=conscrito).first()
    psicossocial = Psicossocial.objects.filter(conscrito=conscrito).first()
    atividades = Atividades.objects.filter(conscrito=conscrito).first()
    particularidades = Particularidades.objects.filter(conscrito=conscrito).first()
    avaliacao = Avaliacao.objects.filter(conscrito=conscrito, tipo=tipo_avl).first()
    
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
            avaliacao.avaliador = request.user # Vinculamos o avaliador logado
            avaliacao.tipo = tipo_avl
            avaliacao.save()
            ''' --------------------------- Ponto de Atenção --------------------------- '''

            # Redireciona para página de busca para iniciar nova avaliação
            ''' --------------------------- Ponto de Atenção ---------------------------
            Criar uma página para impressão da ficha de entrevista. Após impressão,
            seguir para a página de busca'''
            return redirect('buscar')
        else:
            # Debug: Se não salvar, você verá o erro no terminal
            print("-----------------------------------------------------")
            print("Existem erros a serem tratados:")
            print("Conscrito:", conscrito_form.errors)
            print("Contato:", contato_form.errors)
            print("Endereco:", endereco_form.errors)
            print("Composição Familiar:", composicao_familiar_form.errors)
            print("Residentes:", residente_form.errors)
            print("Psicossocial:", psicossocial_form.errors)
            print("Atividades:", atividades_form.errors)
            print("Particularidades:", particularidades_form.errors)
            print("Avaliação:", avaliacao_form.errors)
            print("-----------------------------------------------------")
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

@login_required
def material(request, pk):
    pass

@login_required
def medico(request, pk):
    pass

@login_required
def odonto(request, pk):
    pass

@login_required
def social(request, pk):
    pass