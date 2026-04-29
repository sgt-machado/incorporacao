from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms import inlineformset_factory
from .models import Municipio, Conscrito, Contato, Endereco, Composicao_Familiar, Residente, Psicossocial, Atividades, Particularidades, Esporte, Habilidade, Instrumento
from .forms import ConscritoForm, ContatoForm, EnderecoForm, ComposicaoFamiliarForm, ResidenteForm, PsicossocialForm, AtividadesForm, ParticularidadesForm, EsporteForm, HabilidadeForm, InstrumentoForm

def buscar_conscrito(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf').replace('.', '').replace('-', '')
        conscrito = Conscrito.objects.filter(cpf=cpf).first()
        if conscrito:
            return redirect('editar_dados', pk=conscrito.pk)
        return render(request, 'conscritos/buscar_cpf.html', {'erro': 'CPF não encontrado.'})
    
    return render(request, 'conscritos/buscar_cpf.html')

def editar_dados(request, pk):
    conscrito = get_object_or_404(Conscrito, pk=pk)
    contato, _ = Contato.objects.get_or_create(conscrito=conscrito)
    endereco, _ = Endereco.objects.get_or_create(conscrito=conscrito)
    composicao_familiar, _ = Composicao_Familiar.objects.get_or_create(conscrito=conscrito)
    psicossocial, _ = Psicossocial.objects.get_or_create(conscrito=conscrito)
    atividades, _ = Atividades.objects.get_or_create(conscrito=conscrito)
    particularidades, _ = Particularidades.objects.get_or_create(conscrito=conscrito)

    # Cria as fábricas de formsets
    ResidenteFormSet = inlineformset_factory(
        Conscrito, Residente, form=ResidenteForm, 
        extra=0, can_delete=True
    )

    EsporteFormSet = inlineformset_factory(
        Conscrito, Esporte, form=EsporteForm,
        extra=0, can_delete=True
    )
    HabilidadeFormSet = inlineformset_factory(
        Conscrito, Habilidade, form=HabilidadeForm, 
        extra=0, can_delete=True
    )
    InstrumentoFormSet = inlineformset_factory(
        Conscrito, Instrumento, form=InstrumentoForm, 
        extra=0, can_delete=True
    )

    if request.method == 'POST':
        # 1. Criamos uma cópia para limpar as máscaras antes de validar
        post_data = request.POST.copy()
        if 'conscrito-cpf' in post_data:
            post_data['conscrito-cpf'] = post_data['conscrito-cpf'].replace('.', '').replace('-', '')
        
        if 'endereco-cep' in post_data:
            post_data['endereco-cep'] = post_data['endereco-cep'].replace('-', '')
        
        # 2. Inicializamos os forms com os dados já limpos
        form = ConscritoForm(post_data, instance=conscrito, prefix='conscrito')
        contato_form = ContatoForm(post_data, instance=contato, prefix='contato')
        endereco_form = EnderecoForm(post_data, instance=endereco, prefix='endereco')
        composicao_familiar_form = ComposicaoFamiliarForm(post_data, instance=composicao_familiar, prefix='composicao_familiar')
        residente_form = ResidenteFormSet(post_data, instance=conscrito, prefix='residentes')
        psicossocial_form = PsicossocialForm(post_data, instance=psicossocial, prefix='psicossocial')
        atividades_form = AtividadesForm(post_data, instance=atividades, prefix='atividades')
        esporte_form = EsporteFormSet(post_data, instance=conscrito, prefix='esportes')
        habilidade_form = HabilidadeFormSet(post_data, instance=conscrito, prefix='habilidades')
        instrumento_form = InstrumentoFormSet(post_data, instance=conscrito, prefix='instrumentos')
        particularidades_form = ParticularidadesForm(post_data, instance=particularidades, prefix='particularidades')

        # 3. Validamos e salvamos
        if all([form.is_valid(), contato_form.is_valid(), endereco_form.is_valid(), composicao_familiar_form.is_valid(), residente_form.is_valid(), psicossocial_form.is_valid(), atividades_form.is_valid(), esporte_form.is_valid(), habilidade_form.is_valid(), instrumento_form.is_valid(), particularidades_form.is_valid()]):
            form.save()
            contato_form.save()
            endereco_form.save()
            composicao_familiar_form.save()
            residente_form.save()
            psicossocial_form.save()
            atividades_form.save()
            esporte_form.save()
            habilidade_form.save()
            instrumento_form.save()
            particularidades_form.save()
            return redirect('editar_dados', pk=conscrito.pk)
        else:
            # Debug: Se não salvar, você verá o erro no terminal do VS Code/PyCharm
            print("Erros Conscrito:", form.errors)
            print("Erros Contato:", contato_form.errors)
            print("Erros Endereco:", endereco_form.errors)
            print("Erros Composição Familiar:", composicao_familiar_form.errors)
            print("Erros Residentes:", residente_form.errors)
            print("Erros Psicossocial:", psicossocial_form.errors)
            print("Erros Atividades:", atividades_form.errors)
            print("Erros Esportes:", esporte_form.errors)
            print("Erros Habilidades:", habilidade_form.errors)
            print("Erros Instrumentos:", instrumento_form.errors)
            print("Erros Particularidades:", particularidades_form.errors)
    else:
        # Carregamento inicial (GET)
        form = ConscritoForm(instance=conscrito, prefix='conscrito')
        contato_form = ContatoForm(instance=contato, prefix='contato')
        endereco_form = EnderecoForm(instance=endereco, prefix='endereco')
        composicao_familiar_form = ComposicaoFamiliarForm(instance=composicao_familiar, prefix='composicao_familiar')
        residente_form = ResidenteFormSet(instance=conscrito, prefix='residentes')
        psicossocial_form = PsicossocialForm(instance=psicossocial, prefix='psicossocial')
        atividades_form = AtividadesForm(instance=atividades, prefix='atividades')
        esporte_form = EsporteFormSet(instance=conscrito, prefix='esportes')
        habilidade_form = HabilidadeFormSet(instance=conscrito, prefix='habilidades')
        instrumento_form = InstrumentoFormSet(instance=conscrito, prefix='instrumentos')
        particularidades_form = ParticularidadesForm(instance=particularidades, prefix='particularidades')

    return render(request, 'conscritos/formulario.html', {
        'form': form, 
        'contato_form': contato_form,
        'endereco_form': endereco_form,
        'composicao_familiar_form': composicao_familiar_form,
        'residente_form': residente_form,
        'psicossocial_form': psicossocial_form,
        'atividades_form': atividades_form,
        'esporte_form': esporte_form,
        'habilidade_form': habilidade_form,
        'instrumento_form': instrumento_form,
        'particularidades_form': particularidades_form,
    })

def carregar_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
    return JsonResponse(list(municipios.values('id', 'nome')), safe=False)