from django.shortcuts import render
from chargemix.models import Grade, Element, Product, Chargemix, ChargemixProduct
from chargemix.serializers import GradeSerializer, ElementSerializer, ProductSerializer, ChargemixSerializer, ChargemixProductSerializer
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework.response import Response

class GradeViewSet (viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    
class ElementViewSet (viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    
class ProductViewSet (viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ChargemixViewSet (viewsets.ModelViewSet):
    queryset = Chargemix.objects.all()
    serializer_class = ChargemixSerializer
    
class ChargemixProductViewSet (viewsets.ModelViewSet):
    queryset = ChargemixProduct.objects.all()
    serializer_class = ChargemixProductSerializer

@api_view(['GET'])
def chargemix_full_object_fetch (request, pk):

    # fetch chargemix data

    try:
        cm_object = Chargemix.objects.get (id = pk)
    except:
        return Response ({"error" : "chargemix not found"})

    # assign chargemix dict

    obj = {
        "id"                  : cm_object.id,
        "name"                : cm_object.name,
        "furnace_size"        : cm_object.furnace_size,
        "tapping_time"        : cm_object.tapping_time,
        "tapping_temp"        : cm_object.tapping_temp,
        "rate_per_unit"       : cm_object.rate_per_unit,
        "is_elec_model"       : cm_object.is_elec_model,
        "grade"               : {},
        "use_elem_recov_rate" : cm_object.use_elem_recov_rate,
        "fesimg_rec_rate"     : cm_object.fesimg_rec_rate,
        "product"             : [],
        "target_chemistry"    : []
    }

    # fetch grade

    try:
        cm_grade = Grade.objects.get (id = cm_object.grade.id)
    except:
        return Response ({"error" : "grade not found"})

    # assign grade

    obj ["grade"] = {
        "id"                 : cm_grade.id,
        "name"               : cm_grade.name,
        "has_nodularization" : cm_grade.has_nodu
    }

    # fetch element

    db_element_dict = {x.id : {"id" : x.id, "name" : x.name, "symbol": x.symbol} for x in Element.objects.all ()}

    # fetch target chemistry

    cm_target = "".join (cm_object.target_chemistry).split (";")
    for x in cm_target:

        # parse target chemistry

        inclusion = x.split (",")

        included_id          = int (inclusion [0])
        included_composition = inclusion [1]
        included_rec_rate    = inclusion [2]

        # fetch tagrget chemistry elements

        target_element = {}
        try:
            target_element = db_element_dict [included_id]
        except:
            Response ({"error" : "element not found"})

        # assign target chemistry elements

        obj ["target_chemistry"].append ({
            "id"     : target_element ["id"],
            "name"   : target_element ["name"],
            "symbol" : target_element ["symbol"],
            "min"    : included_composition,
            "max"    : included_rec_rate
        })

    # fetch products

    cm_product = ChargemixProduct.objects.filter (chargemix = cm_object.id)
    for x in cm_product:
        try:
            product_fetched = Product.objects.get (id = x.product.id)
        except:
            return Response ({"error" : "product not found"})

        # temporarily store products

        product = {
            "id"               : product_fetched.id,
            "name"             : product_fetched.name,
            "price"            : product_fetched.price,
            "type"             : product_fetched.type,
            "curr_qty"         : x.curr_qty,
            "optimized_qty"    : x.optimized_qty,
            "min_qty"          : x.min_qty,
            "max_qty"          : x.max_qty,
            "qty_roundoff"     : x.qty_roundoff,
            "metal_recov_rate" : x.metal_recov_rate,
            "elements"         : []
        }

        # read product composition

        product_content = "".join (x.product_element).split (";")
        for y in product_content:

            # parse product composition

            content = y.split (",")

            elem_id          = int (content [0])
            elem_composition = content [1]
            elem_rec_rate    = content [2]

            # fetch product elements

            content_element = {}
            try:
                content_element = db_element_dict [elem_id]
            except:
                Response ({"error" : "element not found"})

            # assign product elements

            product ["elements"].append ({
                "id"          : content_element ["id"],
                "name"        : content_element ["name"],
                "symbol"      : content_element ["symbol"],
                "composition" : elem_composition,
                "rec_rate"    : elem_rec_rate
            })

        # assign product

        obj ["product"].append (product)

    return Response (obj)
