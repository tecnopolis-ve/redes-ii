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

class Pais(BaseModel):
    nombre = models.CharField(max_length=255)
    nacionalidad = models.CharField(max_length=255)

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField('email', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    nombre = models.CharField(max_length=64)
    segundo_nombre = models.CharField(max_length=64, default=None, blank=True, null=True)
    apellido = models.CharField(max_length=64)
    segundo_apellido = models.CharField(max_length=64, default=None, blank=True, null=True)
    fecha_nac = models.DateField()
    telefono = models.CharField(max_length=64, unique=True)
    nacionalidad = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='coleccionista_nacionalidad')
    vive = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='coleccionista_pais_domicilio')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

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
        return self.email

class Tienda(BaseModel):

    _ALCANCE = (
        ('LOCAL', 'Local'),
        ('MUNDIAL', 'Mundial'),
    )

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fundacion = models.DateField()
    website = models.CharField(max_length=255)
    email = models.CharField(max_length=64, default=None, blank=True, null=True)
    telefono = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nombre

class Contacto(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre

class Cliente(BaseModel):
    num_exp_unico = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
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

class Producto(BaseModel):

    _TIPO_PUJA = (
        ('DINAMICA', 'Dinámica'),
        ('SOBRE_CERRADO', 'Sobre cerrado'),
    )

    tipo_puja = models.CharField(max_length=16, choices=_TIPO_PUJA, default='DINAMICA')
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, blank=True, null=True)
    bid = models.FloatField(default=0)
    ask = models.FloatField(default=0)
    precio = models.FloatField(default=None, blank=True, null=True)
    orden = models.PositiveIntegerField(default=1)
    duracion_minima = models.PositiveIntegerField(default=1)
    ganador = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

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
    participante = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bid = models.FloatField()

    @property
    def bid_display(self):
        return '$' + str(self.bid)

class Factura(BaseModel):
    numero = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
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
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
