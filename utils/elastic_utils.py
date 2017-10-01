from conf import settings

true = True


def get_unique_value_field(field, index="openadress-fr"):
    q = {
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": "*",
                            "analyze_wildcard": true
                        }
                    },
                    {
                        "query_string": {
                            "query": "*",
                            "analyze_wildcard": true
                        }
                    }
                ],
                "must_not": []
            }
        },
        "size": 0,
        "_source": {
            "excludes": []
        },
        "aggs": {
            "2": {
                "terms": {
                    "field": field,
                    "size": 2000,
                    "order": {
                        "_count": "desc"
                    }
                }
            }
        }
    }
    hits = settings.es.search(index=index, body=q)['aggregations']['2']['buckets']
    return [item['key'] for item in hits ]

def get_all_hits_field_match(field,match,index="openadress-fr"):
    q={
    "query": {
        "match" : {
            field : match
        }
    }
}
    return settings.es.search(index=index,body=q)['hits']['hits']
