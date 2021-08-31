from rest_framework.throttling import UserRateThrottle


class CreateServerRateThrottle(UserRateThrottle):
    scope = 'create_server'
    rate = '5/min'
