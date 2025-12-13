# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('PORTAL_DB_NAME'),
        'USER': os.environ.get('PORTAL_DB_USER'),
        'PASSWORD': os.environ.get('PORTAL_DB_PASS'),
        'HOST': os.environ.get('PORTAL_DB_HOST'),
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    },
    'slurm': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('SLURM_DB_NAME'),
        'USER': os.environ.get('SLURM_DB_USER'),
        'PASSWORD': os.environ.get('SLURM_DB_PASS'),
        'HOST': os.environ.get('SLURM_DB_HOST'),
        'PORT': '3306',
        'OPTIONS': {
        },
    },
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': os.environ.get('LDAP_SERVER'),
        'USER': os.environ.get('LDAP_USER'),
        'PASSWORD': os.environ.get('LDAP_PASS'),
    },
}

WATCHMAN_DATABASES = ['default', 'slurm']

DATABASE_ROUTERS = ['database_routers.dbrouters.DbRouter']
