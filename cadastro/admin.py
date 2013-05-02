from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from cadastro.models import *

class PessoaAdmin(admin.ModelAdmin):

    def idade2(self, obj):
        if obj.data_nascimento is None:
            return 0
        import datetime
        return int((datetime.date.today() - obj.data_nascimento).days / 365.25  )

    idade2.allow_tags = True
    idade2.short_description = u'idade'
    idade2.admin_order_field = 'data_nascimento'

    list_display = ('nome','pai','telefone','email','data_nascimento','sexo','estado_civil', 'idade2')
    date_hierarchy = 'data_nascimento'
    search_fields = ['nome','pai','mae','endereco','telefone','email','cpf','identidade','estado_nascimento','profissao','obs','conjuge']
    #ordering = ('-dia',)
    list_filter = ['sexo','estado_civil'] #, 'idade'

class PastorAdmin(admin.ModelAdmin):

    def idade2(self, obj):
        if obj.data_nascimento is None:
            return 0
        import datetime
        return int((datetime.date.today() - obj.data_nascimento).days / 365.25  )

    idade2.allow_tags = True
    idade2.short_description = u'idade'
    idade2.admin_order_field = 'data_nascimento'

    list_display = ('nome','pai','telefone','email','data_nascimento','sexo','estado_civil', 'idade2', 'data_entrada', 'ata_entrada')
    date_hierarchy = 'data_nascimento'
    search_fields = ['nome','pai','mae','endereco','telefone','email','cpf','identidade','estado_nascimento','profissao','obs','conjuge']
    #ordering = ('-dia',)
    list_filter = ['sexo','estado_civil'] #, 'idade'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    #date_hierarchy = 'dia'
    search_fields = ['user__username','user__first_name', 'user__last_name',]
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

class PessoasInlineAdmin(admin.TabularInline):
    model = Pessoa.familias.through

class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome','obs')
    #date_hierarchy = 'data_admissao'
    search_fields = ['nome','obs']
    #ordering = ('-dia',)
    #list_filter = ['status',]
    inlines = [PessoasInlineAdmin,]

class TransferenciaInlineAdmin(admin.TabularInline):
    exclude = ['pastor', 'recepcao',]
    model = Transferencia
    extra = 0

class PastorEntradaInlineAdmin(admin.TabularInline):
    verbose_name = "Entrada Pastor"
    verbose_name_plural = "Entrada Pastores"
    fk_name =  'ata_entrada'
    model = Pastor
    exclude = ['pai','mae','endereco','telefone','email','cpf','identidade','estado_nascimento','profissao','obs','conjuge','orgao_expedidor', 'data_saida', 'ata_saida', 'motivo_saida', 'data_nascimento', 'data_falecimento', 'sexo', 'estado_civil', 'familias', 'grau_instrucao']
    extra = 0

class PastorSaidaInlineAdmin(admin.TabularInline):
    verbose_name = "Saida Pastor"
    verbose_name_plural = "Saida Pastores"
    fk_name =  'ata_saida'
    model = Pastor
    exclude = ['pai','mae','endereco','telefone','email','cpf','identidade','estado_nascimento','profissao','obs','conjuge','orgao_expedidor', 'data_entrada', 'ata_entrada', 'data_nascimento', 'data_falecimento', 'sexo', 'estado_civil', 'familias', 'grau_instrucao']
    extra = 0

class RolEntradaInlineAdmin(admin.TabularInline):
    verbose_name = "Entrada no Rol"
    verbose_name_plural = "Entradas no Rol"
    fk_name =  'ata_entrada'
    model = Rol
    exclude = ['numero', 'pastor', 'status', 'data_saida', 'ata_saida', 'motivo_saida']
    extra = 0

class RolSaidaInlineAdmin(admin.TabularInline):
    verbose_name = "Saida do Rol"
    verbose_name_plural = "Saidas do Rol"
    fk_name =  'ata_saida'
    model = Rol
    exclude = ['numero', 'data_entrada', 'pastor', 'status', 'ata_entrada', 'motivo_saida']
    extra = 0

class PessoaCerimoniaInlineAdmin(admin.TabularInline):
    verbose_name = "Regitro de participacao em cerimonia"
    verbose_name_plural = "Regitro de participacao em cerimonias"
    model = PessoaCerimonia
    exclude = ['pastor', 'igreja']
    extra = 0

class AtaAdmin(admin.ModelAdmin):
    list_display = ('numero','local','motivo')
    date_hierarchy = 'data'
    search_fields = ['numero','local','motivo','topicos_discutidos']
    #ordering = ('-dia',)
    #list_filter = ['status',]
    inlines =  [TransferenciaInlineAdmin,
                PastorEntradaInlineAdmin,
                PastorSaidaInlineAdmin,
                RolEntradaInlineAdmin,
                RolSaidaInlineAdmin,
                PessoaCerimoniaInlineAdmin]

class CerimoniaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    #date_hierarchy = 'data_admissao'
    search_fields = ['nome','descricao']
    #ordering = ('-dia',)
    #list_filter = ['status',]

class IgrejaAdmin(admin.ModelAdmin):
    list_display = ('sigla','nome', 'descricao', 'endereco', 'sinodo')
    #date_hierarchy = 'data_admissao'
    search_fields = ['sigla','nome', 'descricao', 'endereco', 'sinodo']
    #ordering = ('-dia',)
    list_filter = ['sinodo',]


class PessoaCerimoniaAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'cerimonia', 'pastor', 'igreja', 'ata')
    #date_hierarchy = 'data_admissao'
    search_fields = ['pessoa__nome', 'cerimonia__nome', 'pastor__nome', 'igreja__nome', 'ata__numero']
    #ordering = ('-dia',)
    list_filter = ['cerimonia',]

class StatusMembroAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'comungante', 'ativo')
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao', 'comungante', 'ativo']
    #ordering = ('-dia',)
    list_filter = ['comungante', 'ativo',]

class RolAdmin(admin.ModelAdmin):
    list_display = ('numero', 'membro', 'data_entrada', 'ata_entrada', 'pastor', 'status', 'data_saida', 'ata_saida', 'motivo_saida')
    date_hierarchy = 'data_entrada'
    search_fields = ['numero', 'membro__nome', 'ata_entrada__numero', 'ata_saida__numero', 'motivo_saida']
    #ordering = ('-dia',)
    list_filter = ['status', 'motivo_saida']

class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'pastor', 'igreja_origem', 'igreja_destino', 'data', 'ata', 'recepcao')
    date_hierarchy = 'data'
    search_fields = ['pessoa__nome', 'igreja_origem__nome', 'igreja_destino__nome', 'ata__numero']
    #ordering = ('-dia',)
    list_filter = ['recepcao', 'igreja_origem', 'igreja_destino']

admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Ata, AtaAdmin)
admin.site.register(Pastor, PastorAdmin)
admin.site.register(StatusMembro, StatusMembroAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(Cerimonia, CerimoniaAdmin)
admin.site.register(Igreja, IgrejaAdmin)
admin.site.register(PessoaCerimonia, PessoaCerimoniaAdmin)
admin.site.register(Transferencia, TransferenciaAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

#modelos uteis do django
admin.site.register(Session)
admin.site.register(Permission)
admin.site.register(ContentType)

