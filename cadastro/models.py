from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from cadastro.utils import generic_get_absolute_url

ESTADOS = (
    ('RJ', 'Rio de Janeiro'),
    ('SP', 'Sao Paulo'),
)
SEXO = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)

ESTADO_CIVIL = (
    (1, 'Solteiro'),
    (2, 'Casado'),
)

class Pessoa(models.Model):
    """
    Classe com informacoes da pessoa
    """
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ["nome"]

    nome = models.CharField(max_length=256)
    pai = models.CharField(max_length=256,null=True, blank=True)
    mae = models.CharField(max_length=256,null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    telefone = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cpf = models.CharField(max_length=15, null=True, blank=True)
    identidade = models.CharField(max_length=20, null=True, blank=True)
    orgao_expedidor = models.CharField(max_length=60, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    estado_nascimento = models.CharField(max_length=2, null=True, blank=True, choices=ESTADOS)
    data_falecimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, null=True, blank=True, choices=SEXO)
    estado_civil = models.IntegerField(null=True, blank=True, choices=ESTADO_CIVIL)
    profissao = models.CharField(max_length=256,null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    conjuge = models.CharField(max_length=256,null=True, blank=True)

    def idade(self):
        import datetime
        return int((datetime.date.today() - self.data_nascimento).days / 365.25  )

    idade = property(idade)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class UserProfile(models.Model):
    """
    Permite buscar pelo usuario logado as classes de negocio ligadas a ele
    """
    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'
        #ordering = ["nome"]

    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)
