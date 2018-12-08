# mymodule/config.py
from os import environ as oe

API_DEMO = oe.get('API_DEMO', True)

API_V3 = {
    'components': {
        'schemas': {
            'Evaluation': {
                'description': 'Represents an '
                'evaluation.',
                'example': {
                    'date':
                    'datetime.datetime(2018, 8, 13, 4, 56, 6)',
                    'elapsedTime':
                    1.123,
                    'files': [{
                        'fileName':
                        'sample1.exe',
                        'malicious':
                        True,
                        'message':
                        'virus_found',
                        'sha256':
                        'a509fc81910bc9e25a5fac4cbde6d99b54ea1cfecd8d58522f17a930fc342f20',
                        'statusDate':
                        'datetime.datetime(2018, 8, 13, 4, 56, 7)'
                    }],
                    'id':
                    '651e97b6-7ab2-4cda-a91a-e1a00ef23ca8',
                    'malicious':
                    True,
                    'statusDate':
                    'datetime.datetime(2018, 8, 13, 4, 56, 6, 100000)'
                },
                'properties': {
                    'correlationID': {
                        'description': 'Correlation '
                        'ID',
                        'type': 'string'
                    },
                    'date': {
                        'description':
                        'Date/time '
                        'the '
                        'request '
                        'for '
                        'evaluation '
                        'was '
                        'made',
                        'format':
                        'date-time',
                        'type':
                        'string'
                    },
                    'elapsedTime': {
                        'description':
                        'Elapsed '
                        'time '
                        'since '
                        'the '
                        'request '
                        'for '
                        'evaluation '
                        'was '
                        'made',
                        'format':
                        'time-span',
                        'type':
                        'string'
                    },
                    'files': {
                        'description': 'Files',
                        'items': {
                            '$ref': '#/components/schemas/EvaluationFile'
                        },
                        'type': 'array'
                    },
                    'id': {
                        'description': 'ID '
                        'of '
                        'the '
                        'evaluation',
                        'type': 'string'
                    },
                    'malicious': {
                        'description':
                        'Flag '
                        'indicating '
                        'whether '
                        'the '
                        'evaluation '
                        'identified '
                        'a '
                        'file '
                        'as '
                        'malicious '
                        'or '
                        'not.',
                        'type':
                        'boolean'
                    },
                    'status': {
                        'allOf': [{
                            '$ref':
                            '#/components/schemas/EvaluationStatus'
                        }],
                        'description':
                        'Status'
                    },
                    'statusDate': {
                        'description': 'Date/time '
                        'of '
                        'the '
                        'status',
                        'format': 'date-time',
                        'type': 'string'
                    }
                },
                'required': ['date', 'id', 'status', 'statusDate'],
                'type': 'object'
            },
            'EvaluationFile': {
                'description': 'Represents an '
                'evaluation '
                'file.',
                'example': {
                    'fileName':
                    'merlinAgent-Windows-x64.exe',
                    'malicious':
                    True,
                    'message':
                    'Suspicious '
                    'or '
                    'malware-like '
                    'behavior',
                    'sha256':
                    'a509fc81910bc9e25a5fac4cbde6d99b54ea1cfecd8d58522f17a930fc342f20',
                    'statusDate':
                    'datetime.datetime(2018, 8, 13, 4, 56, 7)'
                },
                'properties': {
                    'fileName': {
                        'description': 'File '
                        'name',
                        'type': 'string'
                    },
                    'malicious': {
                        'description':
                        'Flag '
                        'indicating '
                        'whether '
                        'the '
                        'evaluation '
                        'identified '
                        'this '
                        'file '
                        'malicious '
                        'or '
                        'not',
                        'type':
                        'boolean'
                    },
                    'message': {
                        'description': 'Message',
                        'type': 'string'
                    },
                    'sha256': {
                        'description':
                        'SHA-256 '
                        'hash '
                        'of '
                        'the '
                        'file '
                        'to '
                        'evaluate',
                        'type':
                        'string'
                    },
                    'status': {
                        'allOf': [{
                            '$ref':
                            '#/components/schemas/EvaluationStatus'
                        }],
                        'description':
                        'Status'
                    },
                    'statusDate': {
                        'description': 'Date/time '
                        'of '
                        'the '
                        'status',
                        'format': 'date-time',
                        'type': 'string'
                    }
                },
                'required': ['sha256', 'status', 'statusDate'],
                'type': 'object'
            },
            'EvaluationStatus': {
                'description':
                'Represents an '
                'enumeration '
                'of the '
                'statuses of '
                'an '
                'evaluation.',
                'enum': ['InProgress', 'Complete', 'Error'],
                'type':
                'string',
                'x-enumNames': ['InProgress', 'Complete', 'Error']
            },
            'body': {
                'properties': {
                    'file': {
                        'items': {
                            'description':
                            'The '
                            'files '
                            'to '
                            'submit '
                            'for '
                            'evaluation.',
                            'format':
                            'binary',
                            'type':
                            'string'
                        },
                        'type': 'array'
                    }
                },
                'required': ['file'],
                'type': 'object'
            }
        }
    },
    'info': {
        'contact': {
            'email': 'lyuben.bahtarliev@akat-t.com',
            'name': 'Lyuben Bahtarliev',
            'url': 'https://www.akat-t.com'
        },
        'description':
        'MalwareScan.Web - Unified API frontend to various '
        'malware analysis and sandboxing backends.',
        'license': {
            'name': 'This work is licensed under the Unlicense '
            'license.',
            'url': 'http://unlicense.org/'
        },
        'title':
        'MalwareScan.Web',
        'version':
        '1.0.1'
    },
    'openapi': '3.0.0',
    'paths': {
        '/eval': {
            'post': {
                'operationId':
                'mods.api.api_controller.evaluation_submit',
                'parameters': [{
                    'description': 'the correlation '
                    'ID',
                    'explode': True,
                    'in': 'query',
                    'name': 'correlationID',
                    'required': False,
                    'schema': {
                        'type': 'string'
                    },
                    'style': 'form',
                    'x-nullable': True
                }],
                'requestBody': {
                    'content': {
                        'multipart/form-data': {
                            'schema': {
                                '$ref': '#/components/schemas/body'
                            }
                        }
                    }
                },
                'responses': {
                    201: {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'example':
                                    '651e97b6-7ab2-4cda-a91a-e1a00ef23ca8',
                                    'type':
                                    'string'
                                }
                            }
                        },
                        'description': 'the ID of '
                        'the '
                        'evaluation',
                        'x-nullable': False
                    },
                    400: {
                        'description':
                        'The request '
                        'could not be '
                        'understood '
                        'by the '
                        'server due '
                        'to malformed '
                        'syntax.'
                    },
                    401: {
                        'description':
                        'Authentication '
                        'is required '
                        'and/or has '
                        'failed.'
                    },
                    403: {
                        'description':
                        'The user is '
                        'not '
                        'permitted to '
                        'perform this '
                        'operation.'
                    },
                    413: {
                        'description': 'Payload Too '
                        'Large.'
                    },
                    500: {
                        'description': 'An internal '
                        'error has '
                        'occurred.'
                    }
                },
                'summary':
                'Submits a file for evaluation.',
                'tags': ['Evaluation'],
                'x-swagger-router-controller':
                'mods.api.api_controller'
            }
        },
        '/eval/file/sha256/{hash}': {
            'get': {
                'operationId':
                'mods.api.api_controller.evaluation_file_by_sha256',
                'parameters': [{
                    'description':
                    'the '
                    'SHA-256 '
                    'hash '
                    'of '
                    'the '
                    'file',
                    'explode':
                    False,
                    'in':
                    'path',
                    'name':
                    'hash',
                    'required':
                    True,
                    'schema': {
                        'type': 'string'
                    },
                    'style':
                    'simple',
                    'x-nullable':
                    False
                }],
                'responses': {
                    200: {
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref':
                                    '#/components/schemas/EvaluationFile'
                                }
                            }
                        },
                        'description': 'the '
                        'evaluation '
                        'file',
                        'x-nullable': True
                    },
                    400: {
                        'description':
                        'The '
                        'request '
                        'could '
                        'not '
                        'be '
                        'understood '
                        'by '
                        'the '
                        'server '
                        'due '
                        'to '
                        'malformed '
                        'syntax.'
                    },
                    401: {
                        'description':
                        'Authentication '
                        'is '
                        'required '
                        'and/or '
                        'has '
                        'failed.'
                    },
                    403: {
                        'description':
                        'The '
                        'user '
                        'is '
                        'not '
                        'permitted '
                        'to '
                        'perform '
                        'this '
                        'operation.'
                    },
                    404: {
                        'description':
                        'An '
                        'evaluation '
                        'file '
                        'with '
                        'the '
                        'specified '
                        'SHA-256 '
                        'hash '
                        'could '
                        'not '
                        'be '
                        'found.'
                    },
                    500: {
                        'description':
                        'An '
                        'internal '
                        'error '
                        'has '
                        'occurred.'
                    }
                },
                'summary':
                'Gets an evaluation '
                'file with a '
                'specified SHA-256 '
                'hash.',
                'tags': ['Evaluation'],
                'x-swagger-router-controller':
                'mods.api.api_controller'
            }
        },
        '/eval/{id}': {
            'get': {
                'operationId':
                'mods.api.api_controller.evaluation_get',
                'parameters': [{
                    'description':
                    'the ID of '
                    'the '
                    'evaluation',
                    'explode':
                    False,
                    'in':
                    'path',
                    'name':
                    'id',
                    'required':
                    True,
                    'schema': {
                        'type': 'string'
                    },
                    'style':
                    'simple',
                    'x-nullable':
                    False
                }],
                'responses': {
                    200: {
                        'content': {
                            'application/json': {
                                'schema': {
                                    '$ref': '#/components/schemas/Evaluation'
                                }
                            }
                        },
                        'description': 'the '
                        'evaluation',
                        'x-nullable': True
                    },
                    400: {
                        'description':
                        'The '
                        'request '
                        'could '
                        'not be '
                        'understood '
                        'by the '
                        'server '
                        'due to '
                        'malformed '
                        'syntax.'
                    },
                    401: {
                        'description':
                        'Authentication '
                        'is '
                        'required '
                        'and/or '
                        'has '
                        'failed.'
                    },
                    403: {
                        'description':
                        'The user '
                        'is not '
                        'permitted '
                        'to '
                        'perform '
                        'this '
                        'operation.'
                    },
                    404: {
                        'description':
                        'An '
                        'evaluation '
                        'with the '
                        'specified '
                        'ID could '
                        'not be '
                        'found.'
                    },
                    500: {
                        'description':
                        'An '
                        'internal '
                        'error '
                        'has '
                        'occurred.'
                    }
                },
                'summary':
                'Gets an evaluation with a '
                'specified ID.',
                'tags': ['Evaluation'],
                'x-swagger-router-controller':
                'mods.api.api_controller'
            }
        }
    },
    'servers': [{
        'url': '/v3'
    }]
}

API_V2 = {
    'basePath': '/v2',
    'consumes': ['application/json'],
    'definitions': {
        'Evaluation': {
            'description': 'Represents an evaluation of '
            'one or more files.',
            'example': {
                'date':
                '2018-08-13T04:56:06.000+00:00',
                'elapsedTime':
                '00:00:01.123',
                'files': [{
                    'fileName':
                    'sample1.exe',
                    'malicious':
                    True,
                    'message':
                    'virus_found',
                    'sha256':
                    'a509fc81910bc9e25a5fac4cbde6d99b54ea1cfecd8d58522f17a930fc342f20',
                    'statusDate':
                    '2018-08-13T04:56:07.000+00:00'
                }],
                'id':
                '651e97b6-7ab2-4cda-a91a-e1a00ef23ca8',
                'malicious':
                True,
                'statusDate':
                '2018-08-13T04:56:06.100+00:00'
            },
            'properties': {
                'correlationID': {
                    'description': 'Correlation '
                    'ID',
                    'type': 'string'
                },
                'date': {
                    'description':
                    'Date/time '
                    'the '
                    'request '
                    'for '
                    'evaluation '
                    'was '
                    'made',
                    'format':
                    'date-time',
                    'type':
                    'string'
                },
                'elapsedTime': {
                    'description':
                    'Elapsed '
                    'time '
                    'since '
                    'the '
                    'request '
                    'for '
                    'evaluation '
                    'was '
                    'made',
                    'format':
                    'time-span',
                    'type':
                    'string'
                },
                'files': {
                    'description': 'Files',
                    'items': {
                        '$ref': '#/definitions/EvaluationFile'
                    },
                    'type': 'array'
                },
                'id': {
                    'description': 'ID of '
                    'the '
                    'evaluation',
                    'type': 'string'
                },
                'malicious': {
                    'description':
                    'Flag '
                    'indicating '
                    'whether '
                    'the '
                    'evaluation '
                    'identified '
                    'a '
                    'file '
                    'as '
                    'malicious '
                    'or '
                    'not.',
                    'type':
                    'boolean'
                },
                'status': {
                    'allOf': [{
                        '$ref': '#/definitions/EvaluationStatus'
                    }],
                    'description': 'Status'
                },
                'statusDate': {
                    'description': 'Date/time '
                    'of '
                    'the '
                    'status',
                    'format': 'date-time',
                    'type': 'string'
                }
            },
            'required': ['id', 'date', 'statusDate', 'status'],
            'type': 'object'
        },
        'EvaluationFile': {
            'description': 'Represents an evaluation '
            'file.',
            'example': {
                'fileName':
                'merlinAgent-Windows-x64.exe',
                'malicious':
                True,
                'message':
                'Suspicious or '
                'malware-like '
                'behavior',
                'sha256':
                'a509fc81910bc9e25a5fac4cbde6d99b54ea1cfecd8d58522f17a930fc342f20',
                'statusDate':
                '2018-08-13T04:56:07.000+00:00'
            },
            'properties': {
                'fileName': {
                    'description': 'File '
                    'name',
                    'type': 'string'
                },
                'malicious': {
                    'description':
                    'Flag '
                    'indicating '
                    'whether '
                    'the '
                    'evaluation '
                    'identified '
                    'this '
                    'file '
                    'malicious '
                    'or '
                    'not',
                    'type':
                    'boolean'
                },
                'message': {
                    'description': 'Message',
                    'type': 'string'
                },
                'sha256': {
                    'description':
                    'SHA-256 '
                    'hash '
                    'of '
                    'the '
                    'file '
                    'to '
                    'evaluate',
                    'type':
                    'string'
                },
                'status': {
                    'allOf': [{
                        '$ref': '#/definitions/EvaluationStatus'
                    }],
                    'description': 'Status'
                },
                'statusDate': {
                    'description': 'Date/time '
                    'of '
                    'the '
                    'status',
                    'format': 'date-time',
                    'type': 'string'
                }
            },
            'required': ['sha256', 'statusDate', 'status'],
            'type': 'object'
        },
        'EvaluationStatus': {
            'description':
            'Represents an '
            'enumeration of the '
            'statuses of an '
            'evaluation.',
            'enum': ['InProgress', 'Complete', 'Error'],
            'type':
            'string',
            'x-enumNames': ['InProgress', 'Complete', 'Error']
        }
    },
    'info': {
        'contact': {
            'email': 'lyuben.bahtarliev@akat-t.com',
            'name': 'Lyuben Bahtarliev',
            'url': 'https://www.akat-t.com'
        },
        'description':
        'MalwareScan.Web - Unified API frontend to various '
        'malware analysis and sandboxing backends.',
        'license': {
            'name': 'This work is licensed under the Unlicense '
            'license.',
            'url': 'http://unlicense.org/'
        },
        'title':
        'MalwareScan.Web',
        'version':
        '1.0.0'
    },
    'paths': {
        '/eval': {
            'post': {
                'consumes': ['multipart/form-data'],
                'operationId':
                'mods.api.api_controller.evaluation_submit',
                'parameters': [{
                    'description': 'the file to '
                    'evaluate',
                    'in': 'formData',
                    'name': 'file',
                    'required': True,
                    'type': 'file',
                    'x-nullable': False
                },
                               {
                                   'description': 'the correlation '
                                   'ID',
                                   'in': 'query',
                                   'name': 'correlationID',
                                   'type': 'string',
                                   'x-nullable': True
                               }],
                'responses': {
                    201: {
                        'description': 'the ID of '
                        'the '
                        'evaluation',
                        'schema': {
                            'example': '651e97b6-7ab2-4cda-a91a-e1a00ef23ca8',
                            'type': 'string'
                        },
                        'x-nullable': False
                    },
                    400: {
                        'description':
                        'The request '
                        'could not be '
                        'understood '
                        'by the '
                        'server due '
                        'to malformed '
                        'syntax.'
                    },
                    401: {
                        'description':
                        'Authentication '
                        'is required '
                        'and/or has '
                        'failed.'
                    },
                    403: {
                        'description':
                        'The user is '
                        'not '
                        'permitted to '
                        'perform this '
                        'operation.'
                    },
                    413: {
                        'description': 'Payload Too '
                        'Large.'
                    },
                    500: {
                        'description': 'An internal '
                        'error has '
                        'occurred.'
                    }
                },
                'summary':
                'Submits a file for evaluation.',
                'tags': ['Evaluation']
            }
        },
        '/eval/file/sha256/{hash}': {
            'get': {
                'operationId':
                'mods.api.api_controller.evaluation_file_by_sha256',
                'parameters': [{
                    'description':
                    'the '
                    'SHA-256 '
                    'hash '
                    'of '
                    'the '
                    'file',
                    'in':
                    'path',
                    'name':
                    'hash',
                    'required':
                    True,
                    'type':
                    'string',
                    'x-nullable':
                    False
                }],
                'responses': {
                    200: {
                        'description': 'the '
                        'evaluation '
                        'file',
                        'schema': {
                            '$ref': '#/definitions/EvaluationFile'
                        },
                        'x-nullable': True
                    },
                    400: {
                        'description':
                        'The '
                        'request '
                        'could '
                        'not '
                        'be '
                        'understood '
                        'by '
                        'the '
                        'server '
                        'due '
                        'to '
                        'malformed '
                        'syntax.'
                    },
                    401: {
                        'description':
                        'Authentication '
                        'is '
                        'required '
                        'and/or '
                        'has '
                        'failed.'
                    },
                    403: {
                        'description':
                        'The '
                        'user '
                        'is '
                        'not '
                        'permitted '
                        'to '
                        'perform '
                        'this '
                        'operation.'
                    },
                    404: {
                        'description':
                        'An '
                        'evaluation '
                        'file '
                        'with '
                        'the '
                        'specified '
                        'SHA-256 '
                        'hash '
                        'could '
                        'not '
                        'be '
                        'found.'
                    },
                    500: {
                        'description':
                        'An '
                        'internal '
                        'error '
                        'has '
                        'occurred.'
                    }
                },
                'summary':
                'Gets an evaluation '
                'file with a '
                'specified SHA-256 '
                'hash.',
                'tags': ['Evaluation']
            }
        },
        '/eval/{id}': {
            'get': {
                'operationId':
                'mods.api.api_controller.evaluation_get',
                'parameters': [{
                    'description':
                    'the ID of '
                    'the '
                    'evaluation',
                    'in':
                    'path',
                    'name':
                    'id',
                    'required':
                    True,
                    'type':
                    'string',
                    'x-nullable':
                    False
                }],
                'responses': {
                    200: {
                        'description': 'the '
                        'evaluation',
                        'schema': {
                            '$ref': '#/definitions/Evaluation'
                        },
                        'x-nullable': True
                    },
                    400: {
                        'description':
                        'The '
                        'request '
                        'could '
                        'not be '
                        'understood '
                        'by the '
                        'server '
                        'due to '
                        'malformed '
                        'syntax.'
                    },
                    401: {
                        'description':
                        'Authentication '
                        'is '
                        'required '
                        'and/or '
                        'has '
                        'failed.'
                    },
                    403: {
                        'description':
                        'The user '
                        'is not '
                        'permitted '
                        'to '
                        'perform '
                        'this '
                        'operation.'
                    },
                    404: {
                        'description':
                        'An '
                        'evaluation '
                        'with the '
                        'specified '
                        'ID could '
                        'not be '
                        'found.'
                    },
                    500: {
                        'description':
                        'An '
                        'internal '
                        'error '
                        'has '
                        'occurred.'
                    }
                },
                'summary':
                'Gets an evaluation with a '
                'specified ID.',
                'tags': ['Evaluation']
            }
        }
    },
    'produces': ['application/json'],
    'schemes': ['http'],
    'swagger': '2.0'
}
