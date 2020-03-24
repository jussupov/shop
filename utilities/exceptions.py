from rest_framework.exceptions import APIException


class OverflowException(APIException):
    status_code = 401
    default_detail = 'Вы указали слишком много товара'
    default_code = 'message'
