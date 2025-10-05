ECHO = False
DEBUG = True

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7


#user config
USER_PREFIX = '/users'
USER_TAGS = 'users'
USER_ROUTER_CREATE = '/create'
USER_ROUTER_DELETE = '/delete'
USER_ROUTER_CHECK = '/check'

#health config
HEALTH_PREFIX = '/health'
HEALTH_TAGS = 'health'
HEALTH_ROUTER = '/health'

#auth
AUTH_PREFIX = '/login'
AUTH_TAGS = 'login'
AUTH_ROUTER_LOGIN = '/login'

MIDDLEWARE_INGNORE = [HEALTH_ROUTER, ]