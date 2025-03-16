PROMETHEUS = {
    'url': 'http://prometheus-kube-prometheus-prometheus.prometheus.svc.cluster.local:9090',
    'headers': {},
    #'headers': {'Authorization': 'Basic changeme_base64'},
    'filter': {
        'default': "cluster='eureka'",
#        'cloudstats': "cluster='narval', instance=~'blg.*'" # example to override the default filter for a specific module
    },
}

PROM_NODE_HOSTNAME_LABEL = 'instance'
