from rest_framework import serializers
from chargemix.models import Grade, Element, Product, Chargemix, ChargemixProduct
import io
from rest_framework.parsers import JSONParser

class GradeSerializer (serializers.ModelSerializer):
    class Meta:
        model  = Grade
        fields = '__all__'

class ElementSerializer (serializers.ModelSerializer):
    class Meta:
        model  = Element
        fields = '__all__'

class ProductSerializer (serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__'

class ChargemixSerializer (serializers.ModelSerializer):
    target_chemistry = serializers.ListField ()

    class Meta:
        model  = Chargemix
        fields = '__all__'

    def to_representation (self, instance):

        # call the original function

        data = super ().to_representation (instance)

        # process the stored target chemistry

        stored_target_chemistry = [x.split (",") for x in "".join (data ["target_chemistry"]).split (";")]

        # create json output

        displayed_target_chemistry = []

        db_element_dict = {x.id : {"id" : x.id, "name" : x.name, "symbol": x.symbol} for x in Element.objects.all ()}

        for x in stored_target_chemistry:
            displayed_target_chemistry.append ({
                "id"     : int (x[0]), 
                "name"   : db_element_dict [int (x[0])]["name"],
                "symbol" : db_element_dict [int (x[0])]["symbol"],
                "min"    : float (x[1]), 
                "max"    : float (x[2])
                })

        # replace previous data with beautified data

        data ["target_chemistry"] = displayed_target_chemistry

        return data

    def validate (self, data):

        # pick fields for validation

        fetch_grade               = data.get ("grade",               None)
        fetch_tapping_time        = data.get ("tapping_time",        None)
        fetch_tapping_temp        = data.get ("tapping_temp",        None)
        fetch_rate_per_unit       = data.get ("rate_per_unit",       None)
        fetch_is_elec_model       = data.get ("is_elec_model",       None)
        fetch_use_elem_recov_rate = data.get ("use_elem_recov_rate", None)
        fetch_fesimg_rec_rate     = data.get ("fesimg_rec_rate",     None)
        fetch_target_chemistry    = data.get ("target_chemistry",    None)

        # validate grade

        try:
            check_grade = Grade.objects.get (id = fetch_grade.id)
        except:
            raise serializers.ValidationError ("Invalid Grade")
 
        # has_nodulrization flag for grade

        fetch_has_nodularization = check_grade.has_nodu

        # validate tapping time, tapping temp, rate/unit with has_nodulrization flag

        if fetch_has_nodularization:

            if fetch_tapping_time is None or not bool (fetch_tapping_time):
                raise serializers.ValidationError ("positive value for tapping time required")

            elif fetch_tapping_temp is None or not bool (fetch_tapping_temp):
                raise serializers.ValidationError ("positive value for tapping temp required")

        # validate tapping temp, rate/unit with is_elec_model flag

        if fetch_is_elec_model:

            if fetch_tapping_temp is None or not bool (fetch_tapping_temp):
                raise serializers.ValidationError ("positive value for tapping temp required")

            elif fetch_rate_per_unit is None or not bool (fetch_rate_per_unit):
                raise serializers.ValidationError ("positive value for rate/unit required")

        # validate FeSiMg recovery rate with use_elem_recov_rate flag

        if not fetch_use_elem_recov_rate:

            if fetch_fesimg_rec_rate is None or not bool (fetch_fesimg_rec_rate):
                raise serializers.ValidationError ("Mg recovery rate in FeSiMg required")
        
        # check if target chemistry is provided

        if fetch_target_chemistry is None:
            raise serializers.ValidationError ("target chemistry required")

        # analyze target chemistry

        stored_target_chemistry = ""

        for x in fetch_target_chemistry:

            # check if it contains triplets

            if (len (x) != 3):
                raise serializers.ValidationError ("Malformed target chemistry")

            # validate target element id

            check_id = int (x ["id"])

            try:
                Element.objects.get (id = check_id)
            except:
                raise serializers.ValidationError ("Invalid target-element id")

            # validate target element quantity parameters

            try:
                check_min = float (x ["min"])
                check_max = float (x ["max"])
            except:
                raise serializers.ValidationError ("Invalid target-range characters") 

            # validate target element quantity range

            if check_min < 0 or check_max < 0 or check_min > 100 or check_max > 100:
                raise serializers.ValidationError ("Invalid target composition")

            elif check_min > 0 and check_max > 0 and check_min > check_max:
                raise serializers.ValidationError ("Invalid target range")

            stored_target_chemistry += str (x ["id"]) + "," + str (x ["min"]) + "," + str (x ["max"]) + ";"

        data ["target_chemistry"] = str (stored_target_chemistry [:-1])

        return data


class ChargemixProductSerializer (serializers.ModelSerializer):
    product_element = serializers.ListField ()

    class Meta:
        model  = ChargemixProduct
        fields = '__all__'

    def to_representation (self, instance):

        # call the original function

        data = super ().to_representation (instance)

        # process the stored product_element

        stored_product_element = [x.split (",") for x in "".join (data ["product_element"]).split (";")]

        # create json output

        displayed_product_element = []

        db_element_dict = {x.id : {"id" : x.id, "name" : x.name, "symbol": x.symbol} for x in Element.objects.all ()}

        for x in stored_product_element:
            displayed_product_element.append ({ 
                "id"          : int (x [0]), 
                "name"        : db_element_dict [int (x [0])]["name"],
                "symbol"      : db_element_dict [int (x [0])]["symbol"],
                "composition" : float (x[1]), 
                "rec_rate"    : float (x[2])
                })

        # replace previous data with beautified data

        data ["product_element"] = displayed_product_element

        return data

    def validate (self, data):

        fetch_element_list = data.get ("product_element", None)

        if fetch_element_list is None:
            raise serializers.ValidationError ("Invalid element list")

        # analyze element list

        stored_element_list = ""

        db_element_id_list = [x.id for x in Element.objects.all ()]
        
        for x in fetch_element_list:

            # check if it contains triplets

            if (len (x) != 3):
                raise serializers.ValidationError ("Malformed product-element list")

            # validate product element id

            check_id = int (x ["id"])

            if check_id not in db_element_id_list:
                raise serializers.ValidationError ("Invalid product-element id")

            # validate product element contents characters

            try:
                composition = float (x ["composition"])
                recov_rate  = float (x ["rec_rate"])
            except:
                raise serializers.ValidationError ("Invalid product-composition/rec-rate characters")

            # validate product element contents values

            if composition < 0 or recov_rate < 0 or composition > 100 or recov_rate > 100:
                raise serializers.ValidationError ("Invalid product-composition/rec-rate")

            stored_element_list += str (x ["id"]) + "," + str (x ["composition"]) + "," + str (x ["rec_rate"]) + ";"

        data ["product_element"] = str (stored_element_list [:-1])

        return data


"""
{
    "product_element": [{"id":1,"composition":0.5,"rec_rate":0.3},{"id":2,"composition":0.5,"rec_rate":0.3},{"id":3,"composition":0.5,"rec_rate":0.3},{"id":4,"composition":0.5,"rec_rate":0.3},{"id":5,"composition":0.5,"rec_rate":0.3},{"id":6,"composition":0.5,"rec_rate":0.3},{"id":1,"composition":0.5,"rec_rate":0.3}],
    "curr_qty": 5,
    "optimized_qty": 5,
    "min_qty": 5,
    "max_qty": 5,
    "qty_roundoff": 5,
    "metal_recov_rate": 97,
    "chargemix": 5,
    "product": 1
}

"""