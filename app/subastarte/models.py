from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from PIL import Image
import datetime

class BaseModel(models.Model):
    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def set_password(self):
        pass

class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField('email', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Pais(BaseModel):
    nombre = models.CharField(max_length=255)
    nacionalidad = models.CharField(max_length=255)

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

class Coleccionista(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    nombre = models.CharField(max_length=64)
    segundo_nombre = models.CharField(max_length=64, default=None, blank=True, null=True)
    apellido = models.CharField(max_length=64)
    segundo_apellido = models.CharField(max_length=64, default=None, blank=True, null=True)
    fecha_nac = models.DateField()
    telefono = models.CharField(max_length=64, unique=True)
    nacionalidad = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='coleccionista_nacionalidad')
    vive = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='coleccionista_pais_domicilio')

    @property
    def edad(self):
        return int((timezone.now().date() - self.fecha_nac).days / 365.25)

    @property
    def nombre_completo(self):
        nombre = []
        nombre.append(self.nombre)
        nombre.append(self.segundo_nombre)
        nombre.append(self.apellido)
        nombre.append(self.segundo_apellido)
        nombre_apellido = ' '.join(filter(None, nombre)) 
        return nombre_apellido if nombre_apellido else None

    def __str__(self):
        return self.nombre

class Evento(BaseModel):

    _TIPO_EVENTO = (
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
    )

    nombre = models.CharField(max_length=64)
    fecha = models.DateTimeField()
    horas = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=16, choices=_TIPO_EVENTO, default='PRESENCIAL')
    cancelado = models.BooleanField(default=False)
    costo_ins_client = models.FloatField()
    costo_ins_general = models.FloatField(default=None, blank=True, null=True)
    lugar_subasta = models.TextField(default=None, blank=True, null=True)
    imagen = models.ImageField(max_length=255, default=None, blank=True, null=True)
    imagen_thumb = models.ImageField(max_length=255, default=None, blank=True, null=True)
    imagen_big = models.ImageField(max_length=255, default=None, blank=True, null=True)

    def save(self):

        if(self.imagen):
            self.imagen_thumb = "th_{}".format(self.imagen)
            self.imagen_big = "big_{}".format(self.imagen)
        else:
            self.imagen_thumb = None
            self.imagen_big = None

        super().save()

        if(self.imagen):
            img = Image.open(self.imagen.path)
            if img.width < 2048:
                fixed_width = 2048
                width_percent = (fixed_width / float(img.size[0]))
                height = int((float(img.size[1]) * float(width_percent)))
                output_size = (fixed_width, height)
                img = img.resize(output_size, Image.NEAREST)
                img.save(self.imagen_big.path)
            if img.height > 250:
                fixed_height = 250
                height_percent = (fixed_height / float(img.size[1]))
                width = int((float(img.size[0]) * float(height_percent)))
                output_size = (width, fixed_height)
                img.thumbnail(output_size)
                img.save(self.imagen_thumb.path)

    @property
    def estado(self):
        fecha_ini = self.fecha
        fecha_fin = self.fecha + datetime.timedelta(hours=self.horas)

        if self.cancelado:
            return 'CANCELADO'
        else:
            if fecha_ini > timezone.now():
                return 'PENDIENTE'
            elif fecha_ini < timezone.now() < fecha_fin:
                return 'EN CURSO'
            else:
                return 'REALIZADO'

    @property
    def costo_ins_general_display(self):
        return '$' + str(self.costo_ins_general)

    @property
    def costo_ins_client_display(self):
        return '$' + str(self.costo_ins_client)

    def __str__(self):
        return self.nombre

class Tienda(BaseModel):

    _ALCANCE = (
        ('LOCAL', 'Local'),
        ('MUNDIAL', 'Mundial'),
    )

    nombre = models.CharField(max_length=255)
    proposito = models.TextField()
    fundacion = models.DateField()
    website = models.CharField(max_length=255)
    email = models.CharField(max_length=64, default=None, blank=True, null=True)
    telefono = models.CharField(max_length=64, unique=True)
    alcance = models.CharField(max_length=16, choices=_ALCANCE, default='LOCAL')
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Contacto(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=64)
    segundo_nombre = models.CharField(max_length=64, default=None, blank=True, null=True)
    apellido = models.CharField(max_length=64)
    segundo_apellido = models.CharField(max_length=64, default=None, blank=True, null=True)
    telefono = models.CharField(max_length=64, unique=True)
    cargo = models.CharField(max_length=64)
    fecha_nac = models.DateField()

    def __str__(self):
        return self.nombre

class Organiza(BaseModel):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tienda', 'evento',)

class Cliente(BaseModel):
    num_exp_unico = models.AutoField(primary_key=True)
    coleccionista = models.ForeignKey(Coleccionista, on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('coleccionista', 'tienda',)

class Divisa(BaseModel):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

class Artista(BaseModel):
    nombre = CharField(max_length=255, default=None, blank=True, null=True)
    apellido = CharField(max_length=255, default=None, blank=True, null=True)
    nombre_artistico = CharField(max_length=255, default=None, blank=True, null=True)

    @property
    def nombre_completo(self):
        nombre = []
        nombre.append(self.nombre)
        nombre.append(self.apellido)
        nombre_apellido = ' '.join(filter(None, nombre)) 
        return nombre_apellido if nombre_apellido else None

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre_completo

class Moneda(BaseModel):

    _FORMA_MONEDA = (
        ('CU', 'CUADRADA'),
        ('RE', 'REDONDA'),
    )

    _METAL_MONEDA = (
        ('AG', 'PLATA'),
        ('AU', 'ORO'),
        ('PT', 'PLATINO')
    )

    _CANTO_MONEDA = (
        ('ES', 'ESTRIADO'),
        ('LI', 'LISO'),
    )

    nur = models.AutoField(primary_key=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, blank=True, null=True)
    coleccionista = models.ForeignKey(Coleccionista, on_delete=models.CASCADE, blank=True, null=True)
    nombre = CharField(max_length=255)
    divisa = models.ForeignKey(Divisa, on_delete=models.CASCADE)
    denominacion = models.PositiveIntegerField()
    forma = models.CharField(max_length=2, choices=_FORMA_MONEDA)
    metal = models.CharField(max_length=2, choices=_METAL_MONEDA)
    canto = models.CharField(max_length=2, choices=_CANTO_MONEDA)
    diametro = models.FloatField()
    peso = models.FloatField()
    anyo_emision = models.PositiveIntegerField()
    org_acunyacion = models.CharField(max_length=255)
    pais_acunyacion = models.ForeignKey(Pais, on_delete=models.CASCADE)
    motivo = models.TextField()
    anverso = models.TextField()
    reverso = models.TextField()
    total_mintage = models.PositiveIntegerField()
    imagen = models.ImageField(max_length=255, default=None, blank=True, null=True)
    imagen_thumb = models.ImageField(max_length=255, default=None, blank=True, null=True)

    def save(self):

        if(self.imagen):
            self.imagen_thumb = "th_{}".format(self.imagen)
        else:
            self.imagen_thumb = None

        super().save()

        if(self.imagen):
            img = Image.open(self.imagen.path)
            if img.height > 250:
                fixed_height = 250
                height_percent = (fixed_height / float(img.size[1]))
                width = int((float(img.size[0]) * float(height_percent)))
                output_size = (width, fixed_height)
                img.thumbnail(output_size)
                img.save(self.imagen_thumb.path)

    @property
    def tipo(self):
        return 'MONEDA'

class ArtistaMoneda(BaseModel):
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)

class Pintura(BaseModel):
    nur = models.AutoField(primary_key=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, blank=True, null=True)
    coleccionista = models.ForeignKey(Coleccionista, on_delete=models.CASCADE, blank=True, null=True)
    estilo = models.CharField(max_length=255, default=None, blank=True, null=True)
    titulo = models.CharField(max_length=255)
    titulo_original = models.CharField(max_length=255, default=None, blank=True, null=True)
    anyo = models.PositiveIntegerField()
    ancho = models.PositiveIntegerField()
    alto = models.PositiveIntegerField()
    imagen = models.ImageField(max_length=255, default=None, blank=True, null=True)
    imagen_thumb = models.ImageField(max_length=255, default=None, blank=True, null=True)

    def save(self):

        if(self.imagen):
            self.imagen_thumb = "th_{}".format(self.imagen)
        else:
            self.imagen_thumb = None

        super().save()

        if(self.imagen):
            img = Image.open(self.imagen.path)
            if img.height > 250:
                fixed_height = 250
                height_percent = (fixed_height / float(img.size[1]))
                width = int((float(img.size[0]) * float(height_percent)))
                output_size = (width, fixed_height)
                img.thumbnail(output_size)
                img.save(self.imagen_thumb.path)

    @property
    def dimensiones(self):
        return str(self.alto) + ' cm x ' + str(self.ancho) + ' cm'

    @property
    def tipo(self):
        return 'PINTURA'

class ArtistaPintura(BaseModel):
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    pintura = models.ForeignKey(Pintura, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('artista', 'pintura',)

class Participante(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pais_envio = models.ForeignKey(Pais, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('evento', 'cliente',)

class ObjetoSubastaEvento(BaseModel):

    _TIPO_PUJA = (
        ('DINAMICA', 'Dinámica'),
        ('SOBRE_CERRADO', 'Sobre cerrado'),
    )

    tipo_puja = models.CharField(max_length=16, choices=_TIPO_PUJA, default='DINAMICA')
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, blank=True, null=True)
    pintura = models.ForeignKey(Pintura, on_delete=models.CASCADE, blank=True, null=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    bid = models.FloatField(default=0)
    ask = models.FloatField(default=0)
    porc_min_ganancia = models.FloatField()
    precio = models.FloatField(default=None, blank=True, null=True)
    orden = models.PositiveIntegerField(default=1)
    duracion_minima = models.PositiveIntegerField(default=1)
    ganador = models.ForeignKey(Coleccionista, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self):
        self.ask = self.precio + (self.precio * self.porc_min_ganancia / 100)
        super().save()

    @property
    def precio_display(self):
        return '$' + str(self.precio)

    @property
    def bid_display(self):
        return '$' + str(self.bid)

    @property
    def next_bid_display(self):
        return '$' + str(self.bid + 1)

    @property
    def ask_display(self):
        return '$' + str(self.ask)

class Puja(BaseModel):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    objeto_subasta_evento = models.ForeignKey(ObjetoSubastaEvento, on_delete=models.CASCADE)
    bid = models.FloatField()

    @property
    def bid_display(self):
        return '$' + str(self.bid)

class Factura(BaseModel):
    numero = models.AutoField(primary_key=True)
    coleccionista = models.ForeignKey(Coleccionista, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    total_monto = models.FloatField()
    total_manejo_envio = models.FloatField()

    def __str__(self):
        return self.numero

    @property
    def total_monto_display(self):
        return '$' + str(self.total_monto)

    @property
    def total_manejo_envio_display(self):
        return '$' + str(self.total_manejo_envio)

    @property
    def gran_total_display(self):
        return '$' + str(self.total_monto + self.total_manejo_envio)

class ItemFactura(BaseModel):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    objeto_subasta_evento = models.ForeignKey(ObjetoSubastaEvento, on_delete=models.CASCADE)

class CostoEnvioOtros(BaseModel):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, blank=True, null= True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, blank=True, null= True)
    costo_extra = models.FloatField(default=None, blank=True, null= True)
    recargo_envio = models.FloatField(default=None, blank=True, null= True)
    embalaje = models.FloatField(default=None, blank=True, null= True)
    seguro = models.FloatField(default=None, blank=True, null= True)