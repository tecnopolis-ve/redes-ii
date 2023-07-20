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
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def nombre_completo(self):
        nombre = []
        nombre.append(self.nombre)
        nombre.append(self.apellido)
        nombre_apellido = ' '.join(filter(None, nombre)) 
        return nombre_apellido if nombre_apellido else None

    def __str__(self):
        return self.email

class Tienda(BaseModel):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fundacion = models.DateField()
    email = models.CharField(max_length=64, default=None, blank=True, null=True)

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
        unique_together = ('cliente', 'tienda',)


class Producto(BaseModel):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    bid = models.FloatField(default=0, blank=True)
    ask = models.FloatField(default=0)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    duracion = models.PositiveIntegerField(default=1)
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
    ganador = models.BooleanField(default=False)

    @property
    def bid_display(self):
        return '$' + str(self.bid)

class Factura(BaseModel):
    numero = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    total_monto = models.FloatField()

    def __str__(self):
        return self.numero

    @property
    def total_monto_display(self):
        return '$' + str(self.total_monto)

    @property
    def gran_total_display(self):
        return '$' + str(self.total_monto)

class ItemFactura(BaseModel):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
