# coding:utf-8

def check_video_attribute(type_obj, type_value):
    """视频枚举属性的验证"""
    try:
        final_type_obj = type_obj(type_value)
    except:
        return {'value': type_value, 'message': '非法的值'}
    return {}
