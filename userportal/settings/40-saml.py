# SAML2 settings
import copy

import saml2
import saml2.saml
from saml2.config import SPConfig

# These variables are defined in 10-base.py
INSTALLED_APPS += ['djangosaml2']
MIDDLEWARE += ['djangosaml2.middleware.SamlSessionMiddleware']
AUTHENTICATION_BACKENDS += ['userportal.authentication.staffSaml2Backend']

SAML_SESSION_COOKIE_NAME = 'saml_session'
SESSION_COOKIE_SECURE = True
SAML_SESSION_COOKIE_SAMESITE = 'None'
LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SAML_CREATE_UNKNOWN_USER = True

# Hosts that this app is served on. Each one is registered as its own SP
# entity with the IdP, so users stay on whichever host they arrived on.
SAML_HOSTS = [
    'portal.vulcan.alliancecan.ca',
    'metrix.vulcan.alliancecan.ca',
]

# Base pysaml2 config. Host-specific values (entityid, ACS URL) are filled
# in by saml_config_loader below based on the incoming request's host.
SAML_CONFIG = {
    'debug': 1,
    'xmlsec_binary': '/usr/local/bin/xmlsec1',
    # entityid and assertion_consumer_service are set per-host in the loader
    'allow_unknown_attributes': True,

    'service': {
        'sp': {
            'name': 'Test Userportal',
            'name_id_format': saml2.saml.NAMEID_FORMAT_PERSISTENT,
            'name_id_format_allow_create': True,

            'endpoints': {
                # assertion_consumer_service is set per-host in the loader
            },

            'signing_algorithm': saml2.xmldsig.SIG_RSA_SHA256,
            'digest_algorithm': saml2.xmldsig.DIGEST_SHA256,

            'required_attributes': [
                'surName',
                'givenName',
                'uid',
                'eduPersonAffiliation',
                'eduPersonPrincipalName',
                'displayName',
            ],

            # When set to true, the SP will consume unsolicited SAML
            # Responses, i.e. SAML Responses for which it has not sent
            # a respective SAML Authentication Request.
            'allow_unsolicited': False,
        },
    },

    'metadata': {
        'local': ['/opt/idp/idp_metadata.xml'],  # need to remove the POST SingleSignOnService from shibboleth metadata, only redirect seems to work
    },

    # Signing
    'key_file': '/secrets/private-key/private.key',  # private part
    'cert_file': '/opt/idp/public.cert',  # public part

    # Encryption
    'encryption_keypairs': [{
        'key_file': '/secrets/private-key/private.key',  # private part
        'cert_file': '/opt/idp/public.cert',  # public part
    }],
}


def saml_config_loader(request=None):
    """Build a pysaml2 SPConfig whose entityid and ACS URL match the host
    the user actually arrived on, so SAML login/ACS stays on the same
    origin the user is browsing.

    Each host in SAML_HOSTS must be registered as its own SP entity with
    the IdP (entityid = https://<host>/saml2/metadata/, ACS =
    https://<host>/saml2/acs/).
    """
    host = None
    if request is not None:
        host = request.get_host().split(':', 1)[0]

    if host not in SAML_HOSTS:
        # Fall back to the first configured host. This only affects
        # hostless contexts (e.g. management commands); real requests
        # always carry a known host.
        host = SAML_HOSTS[0]

    config = copy.deepcopy(SAML_CONFIG)
    config['entityid'] = f'https://{host}/saml2/metadata/'
    config['service']['sp']['endpoints']['assertion_consumer_service'] = [
        (f'https://{host}/saml2/acs/', saml2.BINDING_HTTP_POST),
    ]

    sp_config = SPConfig()
    sp_config.load(config)
    return sp_config


# Tell djangosaml2 to use our host-aware loader instead of the default
# static one in djangosaml2.conf.config_settings_loader.
#
# Note: userportal/settings.py execs each settings/*.py file into the
# userportal.settings namespace, so the loader is importable as
# userportal.settings.saml_config_loader (not userportal.settings.40-saml,
# which is not a valid module name).
SAML_CONFIG_LOADER = 'userportal.settings.saml_config_loader'
