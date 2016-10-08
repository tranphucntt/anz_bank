# - *- coding: utf- 8 - *-
import unicodedata

# Help select Box
def select_box_by_objects(objects=None, field_key="id", field_value="name", selected="",  name="", id="", cls="", style="", first_option_text=""):
    results = '<select name="'+name+'" id="'+id+'" class="'+cls+'" style="'+style+'">'
    if first_option_text:
        results += '<option disabled> -- '+first_option_text+' -- </option>'
    if objects:
        for item in objects:
            key = str(getattr(item, field_key))
            value = str(getattr(item, field_value))
            if key == str(selected):
                results += '<option value="' + key + '" selected="selected">' + value.encode('utf-8') + '</option>'
            else:
                results += '<option value="' + key + '">' + value + '</option>'
    results += '</select>'
    return results


def select_box_by_list(list=None, selected="", name="", id="", cls="", style="", first_option_text=""):
    results = '<select name="'+name+'" id="'+id+'" class="'+cls+'" style="'+style+'">'
    if first_option_text:
        results += '<option disabled="disabled"> '+first_option_text+' </option>'
    if list:
        for item in list:
            key, value = item
            if str(key) == str(selected):
                results += '<option value="'+str(key)+'" selected="selected">' + value.encode('utf-8') + '</option>'
            else:
                results += '<option value="' + str(key) + '">' + value.encode('utf-8') + '</option>'
    results += '</select>'
    return results

# Constant
REGION=[
    ("HaNoi",u"Hà Nội"),
    ("HoChiMinhCity",u"Thành phố Hồ Chí Minh"),
    ("BinhDuong",u"Bình Dương"),
    ("Khac",u"Khác")
]


CARDTYPE=[
    ("classicCard",u"ANZ Classic Credit Card"),
    ("goldCard",u"ANZ Gold Credit Card"),
    ("platinumCard",u"ANZ Platinum Credit Card"),
    ("travelCard",u"ANZ Travel Platinum Credit Card")
]

CAOCH=[
    (1,u'Lương dưới 8 triệu/tháng'),
    (2,u'Lương từ 8 triệu - 16 triệu/tháng'),
    (3,u'Lương từ 16 triệu - 20 triệu/tháng'),
    (4,u'Lương trên 20 triệu/tháng')
]