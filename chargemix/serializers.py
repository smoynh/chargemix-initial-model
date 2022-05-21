from rest_framework import serializers
from chargemix.models import Grade, Element, Product, Chargemix, ChargemixProduct

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
    class Meta:
        model  = Chargemix
        fields = '__all__'

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

        # check validtor fields are provided

        if fetch_grade is None:
            raise serializers.ValidationError ("grade required")

        elif fetch_is_elec_model is None:
            raise serializers.ValidationError ("electricity model flag required")

        elif fetch_use_elem_recov_rate is None:
            raise serializers.ValidationError ("element recov-rate flag required")

        elif fetch_target_chemistry is None:
            raise serializers.ValidationError ("target chemistry required")

        # validate grade

        try:
            check_grade = Grade.objects.get (id = fetch_grade.id)
        except:
            raise serializers.ValidationError ("Invalid grade")
 
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

        # split target chemistry

        check_target_chemistry = [x.split (",") for x in fetch_target_chemistry.split (";")]
        for x in check_target_chemistry:

            # check if it contains triplets

            if (len (x) != 3):
                raise serializers.ValidationError ("Malformed target chemistry")

            # validate target element id

            check_id = int (x [0])

            try:
                Element.objects.get (id = check_id)
            except:
                raise serializers.ValidationError ("Invalid target-element id")

            # validate target element quantity parameters

            try:
                check_min = float (x [1])
                check_max = float (x [2])
            except:
                raise serializers.ValidationError ("Invalid target-range characters")

            # validate target element quantity range

            if check_min < 0 or check_max < 0 or check_min > 100 or check_max > 100:
                raise serializers.ValidationError ("Invalid target composition")

            elif check_min > 0 and check_max > 0 and check_min > check_max:
                raise serializers.ValidationError ("Invalid target range")

        return data

class ChargemixProductSerializer (serializers.ModelSerializer):
    class Meta:
        model  = ChargemixProduct
        fields = '__all__'

    def validate (self, data):

        fetch_element_list = data.get ("product_element", None)

        if fetch_element_list is None:
            raise serializers.ValidationError ("Invalid element list")

        check_element_list = [x.split (",") for x in fetch_element_list.split (";")]
        for x in check_element_list:

            # check if it contains triplets

            if (len (x) != 3):
                raise serializers.ValidationError ("Malformed product-element list")

            # validate product element id

            check_id = int (x [0])

            try:
                Element.objects.get (id = check_id)
            except:
                raise serializers.ValidationError ("Invalid product-element id")

            # validate product element contents characters

            try:
                composition = float (x [1])
                recov_rate  = float (x [2])
            except:
                raise serializers.ValidationError ("Invalid product-composition/rec-rate characters")

            # validate product element contents values

            if composition < 0 or recov_rate < 0 or composition > 100 or recov_rate > 100:
                raise serializers.ValidationError ("Invalid product-composition/rec-rate")

        return data