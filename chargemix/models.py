from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

# chargemix grade model

class Grade (models.Model):
    name     = models.TextField    ()
    has_nodu = models.BooleanField (default = False)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index (fields = ['name'])
        ]

# element model

class Element (models.Model):
    name   = models.TextField ()
    symbol = models.CharField (max_length = 30, unique=True)

    class Meta:
        ordering = ['id']

# product model

class Product (models.Model):

    FURNACE_MAT         = "furnace_mat"
    LADLE_MAT           = "ladle_mat"
    ADDITIVE            = "additive"
    NODULARIZATION_MAT  = "nodularization_mat"
    PRODUCT_TYPE_CHOICE = (
        (FURNACE_MAT,        "furnace material"),
        (LADLE_MAT,          "ladle material"),
        (ADDITIVE,           "additive"),
        (NODULARIZATION_MAT, "nodularization material")
    )

    name  = models.TextField    ()
    price = models.DecimalField (max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1)])
    type  = models.CharField    (max_length = 50, default = FURNACE_MAT, choices = PRODUCT_TYPE_CHOICE)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index (fields = ['name']),
            models.Index (fields = ['type'])
        ]

# chargemix model

class Chargemix (models.Model):
    name                = models.TextField     ()
    furnace_size        = models.DecimalField  (max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1)])
    tapping_time        = models.DecimalField  (blank = True, null = False, default = 0, max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    tapping_temp        = models.DecimalField  (blank = True, null = False, default = 0, max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    rate_per_unit       = models.DecimalField  (blank = True, null = False, default = 0, max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    is_elec_model       = models.BooleanField  (default = False)
    grade               = models.ForeignKey    (Grade, related_name = 'grade', on_delete = models.CASCADE)
    use_elem_recov_rate = models.BooleanField  (default = False)
    fesimg_rec_rate     = models.DecimalField  (blank = True,  null = False, default = 0, max_digits = 10, decimal_places = 2)
    target_chemistry    = models.TextField     ()
    created             = models.DateTimeField (auto_now_add = True)
    updated             = models.DateTimeField (auto_now = True)
    
    class Meta:
        ordering = ['id']
        indexes = [
            models.Index (fields = ['name']),
            models.Index (fields = ['created'])
        ]

# chargemix-product relation model

class ChargemixProduct (models.Model):
    chargemix        = models.ForeignKey           (Chargemix, related_name = 'chargemix', on_delete = models.CASCADE)
    product          = models.ForeignKey           (Product,   related_name = 'product',   on_delete = models.CASCADE)
    curr_qty         = models.DecimalField         (blank = True, null = False, default = 0, max_digits = 10, decimal_places = 2)
    optimized_qty    = models.DecimalField         (blank = True, null = False, default = 0, max_digits = 10, decimal_places = 2)
    min_qty          = models.DecimalField         (blank = True, null = False, default = 0, max_digits = 10, decimal_places = 2)
    max_qty          = models.DecimalField         (blank = True, null = False, default = 0, max_digits = 10, decimal_places = 2)
    qty_roundoff     = models.PositiveIntegerField (blank = True, null = False, default = 0, validators = [MaxValueValidator(6)])
    metal_recov_rate = models.DecimalField         (blank = True, null = False, default = 100, max_digits = 5, decimal_places = 2, validators = [MaxValueValidator(100), MinValueValidator(0)])
    product_element  = models.TextField            (blank = True, null = False, default = '')

    class Meta:
        ordering = ['id']