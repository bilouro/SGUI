from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from cadastro.utils import generic_get_absolute_url


class Familia(models.Model):
    """
    Classe com informacoes da Familia
    """
    class Meta:
        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'
        ordering = ["nome"]

    nome = models.CharField(max_length=256)
    obs = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

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
GRAU_INSTRUCAO = (
    (1, '1o grau incompleto'),
    (2, '1o grau completo'),
    (3, '2o grau incompleto'),
    (4, '2o grau completo'),
    (5, '3o grau incompleto'),
    (6, '3o grau completo'),
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
    pai = models.CharField(max_length=256)
    mae = models.CharField(max_length=256)
    endereco = models.TextField(null=True, blank=True)
    telefone = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cpf = models.CharField(max_length=15, null=True, blank=True)
    identidade = models.CharField(max_length=20, null=True, blank=True)
    orgao_expedidor = models.CharField(max_length=60, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    estado_nascimento = models.CharField(max_length=2, null=True, blank=True, choices=ESTADOS)
    data_falecimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO)
    estado_civil = models.IntegerField(null=True, blank=True, choices=ESTADO_CIVIL)
    grau_instrucao = models.IntegerField(null=True, blank=True, choices=GRAU_INSTRUCAO)
    profissao = models.CharField(max_length=256,null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    conjuge = models.CharField(max_length=256, null=True, blank=True)
    familias = models.ManyToManyField(Familia, null=True, blank=True)

    def idade(self):
        import datetime
        return int((datetime.date.today() - self.data_nascimento).days / 365.25  )

    idade = property(idade)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class Ata(models.Model):
    """
    Classe com informacoes da ATA
    """
    class Meta:
        verbose_name = 'ATA'
        verbose_name_plural = 'ATAs'

    numero = models.CharField(max_length=10)
    data = models.DateField()
    local = models.CharField(max_length=256,null=True, blank=True)
    motivo = models.CharField(max_length=256)
    topicos_discutidos = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.numero

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class Pastor(Pessoa):
    """
    Classe com informacoes do pastor
    """
    class Meta:
        verbose_name = 'Pastor'
        verbose_name_plural = 'Pastores'

    data_entrada = models.DateField()
    ata_entrada = models.ForeignKey(Ata, related_name='ata_entrada_pastor')
    data_saida = models.DateField(null=True, blank=True)
    ata_saida = models.ForeignKey(Ata, null=True, blank=True, related_name='ata_saida_pastor')
    motivo_saida = models.CharField(max_length=256,null=True, blank=True)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class StatusMembro(models.Model):
    """
    Armazena os possiveis status dos Membros
    """
    class Meta:
        verbose_name = 'Status Membro do ROL'
        verbose_name_plural = 'Status Membros do ROL'

    descricao = models.CharField(max_length=60)
    comungante = models.BooleanField()
    ativo = models.BooleanField()

    def __unicode__(self):
        return self.descricao

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Rol(models.Model):
    """
    Classe com informacoes sobre o ROL de membros
    """
    class Meta:
        verbose_name = 'ROL'
        verbose_name_plural = 'ROL'
        #ordering = ["nome"]

    numero = models.CharField(max_length=20)
    membro = models.ForeignKey(Pessoa)
    data_entrada = models.DateField()
    ata_entrada = models.ForeignKey(Ata)
    pastor = models.ForeignKey(Pastor, related_name='pastor_responsavel')
    status = models.ForeignKey(StatusMembro)
    data_saida = models.DateField(null=True, blank=True)
    ata_saida = models.ForeignKey(Ata, null=True, blank=True, related_name='ata_saida')
    motivo_saida = models.CharField(max_length=256,null=True, blank=True)

    def __unicode__(self):
        return self.membro.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Cerimonia(models.Model):
    """
    Classe com informacoes sobre os cerimonias
    """
    class Meta:
        verbose_name = 'Cerimonia'
        verbose_name_plural = 'Cerimonias'
        #ordering = ["nome"]

    nome = models.CharField(max_length=256)
    descricao = models.CharField(max_length=256,null=True, blank=True)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Igreja(models.Model):
    """
    Classe com informacoes sobre as Igrejas
    """
    class Meta:
        verbose_name = 'Igreja'
        verbose_name_plural = 'Igrejas'
        #ordering = ["nome"]

    sigla = models.CharField(max_length=40)
    nome = models.CharField(max_length=256)
    descricao = models.CharField(max_length=256, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    sinodo = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.sigla, self.nome)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class PessoaCerimonia(models.Model):
    """
    Classe com informacoes sobre a participacao das pessoas nas cerimonias
    """
    class Meta:
        verbose_name = 'Participacao em Cerimonia'
        verbose_name_plural = 'Participacoes em Cerimonias'
        #ordering = ["nome"]

    pessoa = models.ForeignKey(Pessoa)
    cerimonia = models.ForeignKey(Cerimonia)
    pastor = models.ForeignKey(Pastor, related_name='pastor_cerimonia')
    igreja = models.ForeignKey(Igreja)
    ata = models.ForeignKey(Ata)

    def __unicode__(self):
        return "%s %s" % (self.pessoa.nome, self.cerimonia.nome)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Transferencia(models.Model):
    """
    Classe com informacoes sobre a participacao das pessoas nas cerimonias
    """
    class Meta:
        verbose_name = 'Transferencia'
        verbose_name_plural = 'Transferencias'
        #ordering = ["nome"]

    pessoa = models.ForeignKey(Pessoa)
    pastor = models.ForeignKey(Pastor, related_name='pastor_transferencia')
    igreja_origem = models.ForeignKey(Igreja, related_name='igreja_origem')
    igreja_destino = models.ForeignKey(Igreja, related_name='igreja_destino')
    data = models.DateField()
    ata = models.ForeignKey(Ata)
    recepcao = models.BooleanField()

    def __unicode__(self):
        return "%s --> %s" % (self.pessoa.nome, self.igreja_destino.nome)

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
