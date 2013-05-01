from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from cadastro.models import *
#from cadastro.models import Cliente, Funcionario, UserProfile

class PessoaAdmin(admin.ModelAdmin):

    def idade2(self, obj):
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


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    #date_hierarchy = 'dia'
    search_fields = ['user__username','user__first_name', 'user__last_name',]
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

#modelos uteis do django
admin.site.register(Session)
admin.site.register(Permission)
admin.site.register(ContentType)

