"""
    Biothings Web Settings Default
"""

# *****************************************************************************
# biothings.web.launcher
# *****************************************************************************
# color support is provided by tornado.log
LOGGING_FORMAT = "%(color)s[%(levelname)s %(name)s:%(lineno)d]%(end_color)s %(message)s"

# *****************************************************************************
# Elasticsearch Settings
# *****************************************************************************
ES_HOST = 'localhost:9200'
ES_INDICES = {
    None: '_all'
    # "biothing_type_1": "index1",
    # "biothing_type_2": "index1,alias1,pattern_*"
}
ES_ARGS = {
    # https://elasticsearch-py.readthedocs.io/en/v7.12.1/connection.html
    'sniff': False,  # this is a shortcut to configure multiple values
    'timeout': 60  # increase from default (10s) to support heavy query
}

# *****************************************************************************
# MongoDB Settings
# *****************************************************************************
# mongodb://username:password@host/dbname
MONGO_URI = ''
MONGO_COLS = {
    # "biothing_type_1": "collectionA",
    # "biothing_type_2": "collectionB"
}
MONGO_ARGS = {
    # https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html \
    # #pymongo.mongo_client.MongoClient
    'connect': False,  # lazy connection to speed up initialization
    'tz_aware': True  # to maintain consistency with the hub design
}

# *****************************************************************************
# SQL Settings
# *****************************************************************************
# https://docs.sqlalchemy.org/en/14/core/engines.html
# dialect[+driver]://username:password@host/dbname

# mysql+pymysql://username:password@host/dbname
# postgresql://username:password@host/dbname
# sqlite:///filepath
SQL_URI = ''
SQL_TBLS = {
    # "biothing_type_1": "customers",
    # "biothing_type_2": "students, classes",
    # "biothing_type_3": "orders JOIN customers ON orders.cid = customers.id",
}
SQL_ARGS = {
    # https://docs.sqlalchemy.org/en/14/core/engines.html
    # #sqlalchemy.create_engine
    # #custom-dbapi-args
}


# *****************************************************************************
# Web Application
# *****************************************************************************

# Routing
API_PREFIX = ''  # TODO change these to APP_SOMETHING
API_VERSION = 'v1'
APP_LIST = [
    (r"/", 'biothings.web.handlers.FrontPageHandler'),
    (r"/({pre})/", 'tornado.web.RedirectHandler', {"url": "/{0}"}),
    (r"/{pre}/status", 'biothings.web.handlers.StatusHandler'),
    (r"/{pre}/metadata/fields/?", 'biothings.web.handlers.MetadataFieldHandler'),
    (r"/{pre}/metadata/?", 'biothings.web.handlers.MetadataSourceHandler'),
    (r"/{pre}/{ver}/spec/?", 'biothings.web.handlers.APISpecificationHandler'),
    (r"/{pre}/{ver}/{typ}/metadata/fields/?", 'biothings.web.handlers.MetadataFieldHandler'),
    (r"/{pre}/{ver}/{typ}/metadata/?", 'biothings.web.handlers.MetadataSourceHandler'),
    (r"/{pre}/{ver}/{typ}/query/?", 'biothings.web.handlers.QueryHandler'),
    (r"/{pre}/{ver}/{typ}/([^\/]+)/?", 'biothings.web.handlers.BiothingHandler'),
    (r"/{pre}/{ver}/{typ}/?", 'biothings.web.handlers.BiothingHandler'),
    (r"/{pre}/{ver}/metadata/fields/?", 'biothings.web.handlers.MetadataFieldHandler'),
    (r"/{pre}/{ver}/metadata/?", 'biothings.web.handlers.MetadataSourceHandler'),
    (r"/{pre}/{ver}/query/?", 'biothings.web.handlers.QueryHandler'),
]

# *****************************************************************************
# Base API Handler
# *****************************************************************************

# For format=html
HTML_OUT_HEADER_IMG = "https://biothings.io/static/favicon.ico"
HTML_OUT_TITLE = "<p>Biothings API</p>"
METADATA_DOCS_URL = "javascript:;"
QUERY_DOCS_URL = "javascript:;"
ANNOTATION_DOCS_URL = "javascript:;"

# default static path, relative to current working dir
# (where app is launched)
STATIC_PATH = "static"


# *****************************************************************************
# User Input Control
# *****************************************************************************
COMMON_KWARGS = {
    # control flow interrupt
    'raw': {'type': bool, 'default': False},
    'rawquery': {'type': bool, 'default': False},
    # query builder stage
    '_source': {'type': list, 'max': 1000, 'alias': ('fields', 'field', 'filter')},
    'size': {'type': int, 'max': 1000, 'alias': 'limit'},
    # formatter stage
    'dotfield': {'type': bool, 'default': False},
    '_sorted': {'type': bool, 'default': True},  # alaphabetically
    'always_list': {'type': list, 'max': 1000},
    'allow_null': {'type': list, 'max': 1000}
}
ANNOTATION_KWARGS = {
    '*': COMMON_KWARGS.copy(),
    'GET': {'id': {'type': str, 'path': 0, 'required': True}},
    'POST': {'id': {'type': list, 'max': 1000, 'required': True, 'alias': 'ids'}}
}
QUERY_KWARGS = {
    '*': COMMON_KWARGS.copy(),
    'GET': {
        'q': {'type': str, 'default': None},
        'aggs': {'type': list, 'max': 1000, 'alias': 'facets'},
        'facet_size': {'type': int, 'default': 10, 'max': 1000},
        'from': {'type': int, 'max': 10000, 'alias': 'skip'},
        'userquery': {'type': str, 'alias': ['userfilter']},
        'sort': {'type': list, 'max': 10},
        'explain': {'type': bool},
        'fetch_all': {'type': bool},
        'scroll_id': {'type': str}},
    'POST': {
        'q': {'type': list, 'required': True},
        'scopes': {'type': list, 'default': ['_id'], 'max': 1000},
        'from': {'type': int, 'max': 10000, 'alias': 'skip'},
        'sort': {'type': list, 'max': 10},
    }
}

# REMOVE THESE COMPATIBILITY SETTINGS
# ONCE BIOTHINGS.CLIENT OLDER VERSIONS ARE NO LONGER USED
# TODO FINALIZE WHAT TO PUT HERE & REMOVE FROM ABOVE
# TODO VALIDATE COMMON PARAM STRICTNESS IS PROPAGATED
COMMON_KWARGS['_source']['strict'] = False
COMMON_KWARGS['always_list']['strict'] = False
COMMON_KWARGS['allow_null']['strict'] = False
ANNOTATION_KWARGS['POST']['id']['strict'] = False
QUERY_KWARGS['GET']['q']['strict'] = False
QUERY_KWARGS['POST']['q']['strict'] = False
QUERY_KWARGS['POST']['scopes']['strict'] = False


# *****************************************************************************
# Elasticsearch Query Pipeline
# *****************************************************************************
ES_QUERY_PIPELINE = 'biothings.web.query.AsyncESQueryPipeline'
ES_QUERY_BUILDER = 'biothings.web.query.ESQueryBuilder'
# For the userquery folder for this app
USERQUERY_DIR = 'userquery'
# Allow "truly" random order for q= __any__
ALLOW_RANDOM_QUERY = False
# Allow facets to be nested with ( )
ALLOW_NESTED_AGGS = False

# Amount of time a scroll request is kept open
ES_SCROLL_TIME = '1m'
# Size of each scroll request return
ES_SCROLL_SIZE = 1000


ES_QUERY_BACKEND = 'biothings.web.query.AsyncESQueryBackend'
ES_RESULT_TRANSFORM = 'biothings.web.query.ESResultFormatter'

# TODO
# A list of fields to exclude from metadata/fields endpoint
AVAILABLE_FIELDS_EXCLUDED = ['all']
# A path to the available fields notes
AVAILABLE_FIELDS_NOTES_PATH = ''

LICENSE_TRANSFORM = {
    # "alias" :  "datasource",
    # "dot.field" :  "datasource"
}

# *****************************************************************************
# Analytics Settings
# *****************************************************************************

# Sentry project address
SENTRY_CLIENT_KEY = ''

# Google Analytics Account ID
GA_ACCOUNT = ''

# *****************************************************************************
# Endpoints Specifics & Others
# *****************************************************************************
# Annotation # TODO THESES SETTINGS WILL BECOME QUERY PIPELINE SETTINGS
ANNOTATION_DEFAULT_SCOPES = ['_id']
ANNOTATION_ID_REGEX_LIST = []  # [(re.compile(r'rs[0-9]+', re.I), 'dbsnp.rsid')]
#
# Status #
# https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-get.html
STATUS_CHECK = {
    # 'index': ''
    # 'id': '',
}
