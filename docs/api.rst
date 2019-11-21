*******
BRP API
*******

The Biorepository Portal provides a RESTful API for retrieving and updating data in the application.

.. contents:: Contents

Users
=====

GET a Complete List of Users
----------------------------

**URL:**

.. http:get:: /api/users/

**Example Request**:

.. sourcecode:: http

    GET /api/users/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "url": "http://localhost:32782/api/users/1/",
            "username": "personp2",
            "email": "penn.person@uphs.upenn.edu",
            "groups": [],
            "first_name": "Penn",
            "last_name": "Person"
        },
        {
            "url": "http://localhost:32782/api/users/2/",
            "username": "personc1",
            "email": "personc1@email.chop.edu",
            "groups": [],
            "first_name": "Chop",
            "last_name": "Person"
        }
    ]

Organizations
=============

GET a Complete List of Organizations
------------------------------------

**URLS:**

.. http:get:: /api/organizations/

**Example Request**:

.. sourcecode:: http

    GET /api/organizations/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 2,
            "name": "AMAZING CHILDREN'S HOSPITAL",
            "subject_id_label": "Medical Record Number"
        },
        {
            "id": 6,
            "name": "Amazing Children's Hospital - CODED",
            "subject_id_label": "Research Identifier"
        },
        {
            "id": 34,
            "name": "A Very Good Research Consortium",
            "subject_id_label": "Registration No"
        }
    ]

Datasources
===========

GET a Complete List of Datasources
----------------------------------

**URLS:**

.. http:get:: /api/datasources/

**Example Request**:

.. sourcecode:: http

    GET /api/datasources/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 1,
            "name": "Nautilus test",
            "url": "http://localhost:8090/api/",
            "desc_help": "Please briefly describe this data source.",
            "description": "Nautilus Test",
            "ehb_service_es_id": 2
        },
        {
            "id": 2,
            "name": "REDCap Test System",
            "url": "https://localhost/api/",
            "desc_help": "Please briefly describe this data source.",
            "description": "Test Instance of REDCap",
            "ehb_service_es_id": 1
        }
    ]

Protocols
=========

GET a Complete and Detailed List of Protocols You Have Access To
----------------------------------------------------------------

**URLS:**

.. http:get:: /api/protocols/

**Example Request**:

.. sourcecode:: http

    GET /api/protocols/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 21,
            "name": "CBTTC - TRAINING 2",
            "users": [
                "http://localhost:32782/api/users/18/",
                "http://localhost:32782/api/users/55/",
                "http://localhost:32782/api/users/50/",
                "http://localhost:32782/api/users/48/",
                "http://localhost:32782/api/users/7/",
                "http://localhost:32782/api/users/31/",
                "http://localhost:32782/api/users/49/",
                "http://localhost:32782/api/users/279/"
            ],
            "data_sources": [
                "http://localhost:32782/api/datasources/1/",
                "http://localhost:32782/api/datasources/1/",
                "http://localhost:32782/api/datasources/6/",
                "http://localhost:32782/api/datasources/1/"
            ],
            "protocol_data_sources": "http://localhost:32782/api/protocols/21/data_sources/",
            "subjects": "http://localhost:32782/api/protocols/21/subjects/",
            "organizations": "http://localhost:32782/api/protocols/21/organizations/"
        }
    ]
GET a Complete List of Protocols - Admin users only
----------------------------------------------------------------

**URLS:**

.. http:get:: /api/protocols/all/

**Example Request**:

.. sourcecode:: http

    GET /api/protocols/all/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
      {
        "id": 21,
        "name": "CBTTC - TRAINING 2",
        }
    ]

GET a Specific Protocol
------------------------

**URL:**

.. http:get:: /api/protocols/(int: protocol_id (pk))/

**Example Request**:

.. sourcecode:: http

    GET /api/protocols/1/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
        "id": 1,
        "name": "Demonstration Protocol",
        "users": [
            "http://example.com/api/users/1/"
        ],
        "data_sources": [
            "http://example.com/api/datasources/1/",
            "http://example.com/api/datasources/2/",
            "http://example.com/api/datasources/3/"
        ],
        "protocol_data_sources": "http://example.com/api/protocols/1/data_sources/",
        "subjects": "http://example.com/api/protocols/1/subjects/",
        "organizations": "http://example.com/api/protocols/1/organizations/"
    }

GET a List of Subjects Within a Specific Protocol
--------------------------------------------------

**Additional Notes:**
The subjects associated with protocol `protocol_id` including their external records.
Typically this endpoint should be cached as it is expensive due to the retrieval of external records from the eHB.

**URL:**

.. http:get:: api/protocols/(int: protocol_id (pk))/subjects/

**Example Request**:

.. sourcecode:: http

      GET /api/protocols/1/subjects/ HTTP/1.1
      Host: example.com
      Accept: application/json
      Authorization: "token <your API token>"

**Example Response**:

.. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "organization_id": 1,
            "organization_subject_id": "909999",
            "dob": "2000-01-01",
            "modified": "2016-05-13T14:05:37.930839",
            "created": "2016-05-13T14:05:37.930797",
            "external_records": [
                {
                    "label_desc": "SSN",
                    "created": "2016-05-13 14:13:10.837416",
                    "pds": 3,
                    "modified": "2016-05-13 14:13:10.837454",
                    "label": 2,
                    "record_id": "1111115",
                    "path": "demo_exrecs",
                    "external_system": 3,
                    "id": 1,
                    "subject": 1
                },
                {
                    "label_desc": "Record",
                    "created": "2016-05-13 14:13:10.837416",
                    "pds": 1,
                    "modified": "2016-05-13 14:13:10.837454",
                    "label": 1,
                    "record_id": "1111115",
                    "path": "test_study:redcap",
                    "external_system": 1,
                    "id": 2,
                    "subject": 1
                }
            ],
            "external_ids": [
                {
                    "label_desc": "SSN",
                    "created": "2016-05-13 14:13:10.837416",
                    "pds": 3,
                    "modified": "2016-05-13 14:13:10.837454",
                    "label": 2,
                    "record_id": "1111115",
                    "path": "demo_exrecs",
                    "external_system": 3,
                    "id": 1,
                    "subject": 1
                }
            ],
            "organization_name": "Amazing Children's Hospital"
        }
      ]

GET a List of Datasources for a Specific Protocol
-------------------------------------------------

**URL:**

.. http:get:: /api/protocols/(int: protocol_id (pk))/data_sources/

**Example Request**:

.. sourcecode:: http

      GET /api/protocols/1/data_sources/ HTTP/1.1
      Host: example.com
      Accept: application/json
      Authorization: "token <your API token>"

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 3,
            "protocol": "http://example.com/api/protocols/1/",
            "data_source": {
                "id": 3,
                "name": "External Identifiers",
                "url": "http://example.com/noop/",
                "desc_help": "Please briefly describe this data source.",
                "description": "Placeholder for external IDs",
                "ehb_service_es_id": 3
            },
            "path": "demo_exrecs",
            "driver": 3,
            "driver_configuration": {
                "labels": [
                    [
                        2,
                        "SSN"
                    ]
                ],
                "sort_on": 2
            },
            "display_label": "External IDs",
            "max_records_per_subject": 2,
            "subjects": "http://example.com/api/protocoldatasources/3/subjects/",
            "authorized": true
        },
        {
            "id": 1,
            "protocol": "http://example.com/api/protocols/1/",
            "data_source": {
                "id": 1,
                "name": "REDCap",
                "url": "https://localhost/api/",
                "desc_help": "Please briefly describe this data source.",
                "description": "CHOP's REDCap Instance",
                "ehb_service_es_id": 1
            },
            "path": "Demo",
            "driver": 0,
            "driver_configuration": {
                "links": [
                    1,
                    2
                ],
                "labels": [
                    [
                        1,
                        "Record"
                    ]
                ],
                "event_labels": [
                    "Visit Baseline",
                    "Breakfast",
                    "Lunch",
                    "Dinner"
                ],
                "record_id_field_name": "study_id",
                "form_data": {
                    "meal_description_form": [
                        0,
                        1,
                        1,
                        1
                    ],
                    "baseline_visit_data": [
                        1,
                        0,
                        0,
                        0
                    ]
                },
                "unique_event_names": [
                    "visit_arm_1",
                    "breakfast_at_visit_arm_1",
                    "lunch_at_visit_arm_1",
                    "dinner_at_visit_arm_1"
                ]
            },
            "display_label": "Health Data",
            "max_records_per_subject": -1,
            "subjects": "http://example.com/api/protocoldatasources/1/subjects/",
            "authorized": true
        },
        {
            "id": 2,
            "protocol": "http://example.com/api/protocols/1/",
            "data_source": {
                "id": 2,
                "name": "LIMS",
                "url": "https://example.com/api/",
                "desc_help": "Please briefly describe this data source.",
                "description": "Laboratory Management",
                "ehb_service_es_id": 0
            },
            "path": "demo_lab",
            "driver": 1,
            "driver_configuration": {
                "labels": [
                    [
                        1,
                        "Record"
                    ]
                ]
            },
            "display_label": "Sample Check In",
            "max_records_per_subject": -1,
            "subjects": "http://example.com/api/protocoldatasources/2/subjects/",
            "authorized": false
        }
    ]

GET a List of Organizations for a Specific Protocol
---------------------------------------------------

**URL:**

.. http:get:: /api/protocols/(int: protocol_id (pk))/organizations/

**Example Request**:

.. sourcecode:: http

      GET /api/protocols/1/organizations/ HTTP/1.1
      Host: example.com
      Accept: application/json
      Authorization: "token <your API token>"

**Example Response**:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 1,
            "name": "Amazing Children's Hospital",
            "subject_id_label": "Record ID"
        }
    ]

GET Details for a Specific Subject on a Specific Protocol
---------------------------------------------------------

**Additional Notes:**
Typically this endpoint should be cached as it is expensive due to the retrieval of external records from the eHB.

**URL:**

.. http:get:: /api/protocols/(int: protocol_id (pk))/subjects/(int: subject_id (pk))

**Example Request:**

.. sourcecode:: http

    GET /api/protocols/1/data_sources/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
        "dob": "1900-11-30",
        "organization_name": "AMAZING CHILDREN'S HOSPITAL",
        "organization_id_label": "Medical Record Number",
        "modified": "2017-04-03 13:47:50.322181",
        "group_name": "",
        "created": "2017-04-03 13:47:50.322147",
        "last_name": "Gonzalez",
        "first_name": "Alex",
        "id": 7390,
        "organization_subject_id": "2017Gonzalez",
        "external_records": [
            {
                "path": "Test Protocol Training - Redcap",
                "record_id": "record_id",
                "label": 1,
                "created": "2017-04-03 15:35:32.623135",
                "pds": 162,
                "id": 21858,
                "subject": 7390,
                "label_desc": "Record",
                "external_system": 2,
                "modified": "2017-04-03 15:37:06.851436"
            }
        ],
        "organization": 2
    }

Updated a Specific Subject's Information on a Specific Protocol Using PUT
-------------------------------------------------------------------------

**URL:**

.. http:put:: /api/protocols/(int: protocol_id (pk))/subjects/(int: subject_id (pk))/

**Example Request:**

.. sourcecode:: http

    PUT /api/protocols/8/subjects/5/record/5/ HTTP/1.1
    Host: example.com
    Content-Type: application/json
    Authorization: "token <your API token>"

    {
      	"id": 9,
        "first_name": "Another",
        "last_name": "Test",
        "organization_subject_id": "2221",
        "organization_id_label": "Record ID",
        "dob": "2000-01-01",
        "modified": "2018-06-06T15:27:56.016587",
        "created": "2018-06-06T15:27:56.016562",
        "external_records": [],
        "external_ids": [],
        "organization": 8,
        "organization_name": "Amazing Children's Hospital",
        "organization_subject_id_validation": "2221"
    }

**Example Response**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
        "first_name": "Another",
        "last_name": "Test",
        "group_name": "",
        "organization_subject_id": "2221",
        "organization": 8,
        "organization_id_label": "Record ID",
        "dob": "2000-1-1",
        "id": 9,
        "created": "2018-06-06 15:27:56.016562",
        "organization_name": "Amazing Children's Hospital"
    }

DELETE a Specific Subject from a Specific Protocol
--------------------------------------------------

**URL:**

.. http:delete:: /api/protocols/(int: protocol_id (pk))/subjects/(int: subject_id (pk))

**Example Request**

.. sourcecode:: http

    DELETE /api/protocols/8/subjects/5/record/5/ HTTP/1.1
    Host: example.com
    Content-Type: application/json
    Authorization: "token <your API token>"

    {
      	"id": 9,
        "first_name": "Another",
        "last_name": "Test",
        "organization_subject_id": "2221",
        "organization_id_label": "Record ID",
        "dob": "2000-01-01",
        "modified": "2018-06-06T15:27:56.016587",
        "created": "2018-06-06T15:27:56.016562",
        "external_records": [],
        "external_ids": [],
        "organization": 8,
        "organization_name": "Amazing Children's Hospital",
        "organization_subject_id_validation": "2221"
    }

**Example Response**

.. sourcecode:: http

    {
        "info": "Subject deleted"
    }

Create a New Subject and Add Them to a Protocol Using POST
----------------------------------------------------------

**URL:**

.. http:post:: /api/protocols/(int: protcol_id (pk))/subjects/create

**Example Request:**

.. sourcecode:: http

    POST /api/protocols/1/subjects/create HTTP/1.1
    Host: example.com
    Content-Type: application/json
    Authorization: "token <your API token>"

    {
        "first_name": "John",
        "last_name": "Doe",
        "organization_subject_id": "123123123",
        "organization": "1",
        "dob": "2000-01-01"
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        true,
        {
            "external_ids": [],
            "group_name": "",
            "organization_name": "The Children's Hospital of Philadelphia",
            "dob": "2000-1-1",
            "last_name": "Doe",
            "first_name": "John",
            "id": 8750,
            "organization_id_label": "MRN",
            "organization_subject_id": "123123123",
            "external_records": [],
            "organization": 1
        },
        []
    ]

Protocol Datasources
====================

GET a Complete List of Protocol Datasources
-------------------------------------------

**URL:**

.. http:get:: /api/protocoldatasources/

**Example Request:**

.. sourcecode:: http

    GET /api/protocoldatasources/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "id": 55,
            "protocol": "http://localhost:32782/api/protocols/21/",
            "data_source": "http://localhost:32782/api/datasources/1/",
            "path": "CBTTC - TRAINING 2 - Specimen Only",
            "driver": 0,
            "driver_configuration": "{\r\n\"unique_event_names\":[\"specimen_only_arm_1\"],\r\n\"event_labels\":[\"Information about Specimen Sent\"],\r\n    \"form_data\":{\"specimen_only\":[1]},\r\n    \"record_id_field_name\": \"study_id\",\r\n\"links\": [1]\r\n}",
            "display_label": "2 Sample Only Data",
            "max_records_per_subject": -1,
            "subjects": "http://localhost:32782/api/protocoldatasources/55/subjects/"
        },
        {
            "id": 28,
            "protocol": "http://localhost:32782/api/protocols/21/",
            "data_source": "http://localhost:32782/api/datasources/6/",
            "path": "CBTTC - TRAINING 2",
            "driver": 1,
            "driver_configuration": "{\r\n    \"labels\": [\r\n        1,\r\n        2,\r\n        3,\r\n        4,\r\n        5,\r\n        6,\r\n        7,\r\n        8,\r\n        9,\r\n54, 55, 56, 57\r\n    ],\r\n    \"links\": [4]\r\n}",
            "display_label": "3 Sample Check-in",
            "max_records_per_subject": -1,
            "subjects": "http://localhost:32782/api/protocoldatasources/28/subjects/"
        }
    ]

GET a List of Subjects in a Specific Protocols Specific Datasource
------------------------------------------------------------------

**Additional Notes:**
Typically this endpoint should be cached as it is expensive due to the retrieval of external records from the eHB.

**URL:**

.. http:get:: /api/protocoldatasources/(int: protocol_id (pk))/subjects/

**Example Request:**

.. sourcecode:: http

    GET /api/protocoldatasources/1/subjects/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
        "subjects": [
            {
                "id": 7390,
                "first_name": "Alex",
                "last_name": "Gonzalez",
                "organization_subject_id": "2017Gonzalez",
                "organization_id_label": "Medical Record Number",
                "dob": "1900-10-30",
                "modified": "2017-04-03T13:47:50.322181",
                "created": "2017-04-03T13:47:50.322147",
                "external_records": [
                    {
                        "path": "Test Protocol Training - Redcap",
                        "record_id": "record_id",
                        "label": 1,
                        "created": "2017-04-03 15:35:32.623135",
                        "id": 21858,
                        "subject": 7390,
                        "external_system": 2,
                        "modified": "2017-04-03 15:37:06.851436"
                    }
                ],
                "organization": 2,
                "organization_name": "AMAZING CHILDREN'S HOSPITAL"
            },
            {
                "id": 8507,
                "first_name": "testing",
                "last_name": "tentwentyfivetwentyseventeen",
                "organization_subject_id": "10252017",
                "organization_id_label": "Medical Record Number",
                "dob": "2017-10-25",
                "modified": "2017-10-25T16:49:39.824337",
                "created": "2017-10-25T16:49:39.824299",
                "external_records": [],
                "organization": 2,
                "organization_name": "AMAZING CHILDREN'S HOSPITAL"
            },
            {
                "id": 7496,
                "first_name": "Test",
                "last_name": "EHBWork",
                "organization_subject_id": "111111234",
                "organization_id_label": "Medical Record Number",
                "dob": "1990-07-01",
                "modified": "2017-04-28T09:38:33.597771",
                "created": "2017-04-28T09:38:33.597725",
                "external_records": [],
                "organization": 2,
                "organization_name": "AMAZING CHILDREN'S HOSPITAL"
            },
            {
                "id": 8129,
                "first_name": "Practice",
                "last_name": "Subject",
                "organization_subject_id": "00000000012",
                "organization_id_label": "Medical Record Number",
                "dob": "1990-07-01",
                "modified": "2017-08-24T16:33:01.472511",
                "created": "2017-08-24T16:29:32.345534",
                "external_records": [
                    {
                        "path": "Test Protocol Training - Redcap",
                        "record_id": "record_id",
                        "label": 1,
                        "created": "2017-08-24 19:39:09.349709",
                        "id": 25494,
                        "subject": 8129,
                        "external_system": 2,
                        "modified": "2017-08-24 19:39:09.349732"
                    }
                ],
                "organization": 2,
                "organization_name": "AMAZING CHILDREN'S HOSPITAL"
            }
        ],
        "count": 4
    }

GET a List of Records For a Specific Subject Within a Specific Protocols Specific Datasource
--------------------------------------------------------------------------------------------

**URL:**

.. http:get:: /api/protocoldatasources/(int: protocol_id (pk))/subjects/(int: subject_id (pk))/records/

**Example Request:**

.. sourcecode:: http

    GET /api/protocoldatasources/1/subjects/1/records/ HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [
        {
            "path": "CBTTC - Specimen Only",
            "record_id": "record id",
            "label": 1,
            "created": "2017-02-17 12:34:39.975644",
            "id": 20752,
            "subject": 4921,
            "external_system": 2,
            "modified": "2017-02-17 12:34:39.975678"
        },
        {
            "path": "CBTTC - Specimen Only",
            "record_id": "record id",
            "label": 1,
            "created": "2018-06-04 16:47:40.320305",
            "id": 27871,
            "subject": 4921,
            "external_system": 2,
            "modified": "2018-06-04 16:47:40.320347"
        }
    ]

GET a Specific Record for a Specific Subject Within a Specific Protocols Specific Datasource
--------------------------------------------------------------------------------------------

**URL:**

.. http:get:: /api/protocoldatasources/(int: protocol_id (pk))/subjects/(int: subject_id (pk))/record/(int: record_id (pk))

**Example Request:**

.. sourcecode:: http

    GET /api/protocoldatasources/1/subjects/1/record/1 HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
        "path": "CBTTC - Specimen Only",
        "record_id": "record id",
        "label": 1,
        "created": "2018-06-04 16:47:40.320305",
        "id": 27871,
        "subject": 4921,
        "external_system": 2,
        "modified": "2018-06-04 16:47:40.320347"
    }

Change the Label of a Specific Record Using PUT
-----------------------------------------------

**Additional Notes:**
The "label" field represents the primary key of the current label and the "label_id" field represents the primary key of the new label. At this point we only support the modification of the record label.
Typically this endpoint should be cached as it is expensive due to the retrieval of external records from the eHB.

**URL:**

.. http:put:: /api/protocoldatasources/(int: protocol_id (pk))/subjects/(int: subject_id (pk))/record/(int: record_id (pk))/

**Example Request:**

.. sourcecode:: http

    PUT /api/protocoldatasources/8/subjects/5/record/5/ HTTP/1.1
    Host: example.com
    Content-Type: application/json
    Authorization: "token <your API token>"

    {
      	"id": 5,
      	"subject": 5,
      	"external_system": 4,
      	"record_id": "record id",
      	"path": "EIG-COOP-SUBJECT-RECORDS",
      	"label": 1,
      	"modified": "2018-04-16 10:42:37.629522",
      	"created": "2018-04-16 10:42:37.629502",
      	"label_desc": "Foo Label",
      	"pds": 8,
      	"label_id": 2
    }

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    [{
        "id": 5,
        "subject": 5,
        "external_system": 4,
        "record_id": "record id",
        "path": "EIG-COOP-SUBJECT-RECORDS",
        "label": 2,
        "created": "2018-04-16 10:42:37.629502"
    }]

Familial Relationships
=========

GET a list of relationships in a protocol
----------------------------------------------------------------

**URLS:**

.. http:get:: /api/protocols/(int: protocol_id (pk))/subj_fam/

**Example Request**:

.. sourcecode:: http

    GET /api/protocols/1/subj_fam HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {"relationships":
      [{"subject_1_id":10286,"subject_1_org_id":"test123","subject_2_id":6536,"subject_2_org_id":"test123456","subject_1_role":"Maternal","subject_2_role":"Maternal","protocol_id":null,"id":2},
      {"subject_1_id":6738,"subject_1_org_id":"Test1","subject_2_id":6740,"subject_2_org_id":"test22228","subject_1_role":"Brother","subject_2_role":"Sister","protocol_id":null,"id":10},
      {"subject_1_id":6738,"subject_1_org_id":"Test1","subject_2_id":6739,"subject_2_org_id":"test0128398","subject_1_role":"Brother","subject_2_role":"Sister","protocol_id":null,"id":14}]}


GET a list of relationships for a subject
----------------------------------------------------------------

**URLS:**

.. http:get:: /api/protocols/(int: protocol_id (pk))/subj_fam/subject/(int: subject_id (pk))

**Example Request**:

.. sourcecode:: http

    GET /api/protocols/1/subj_fam/subject/1 HTTP/1.1
    Host: example.com
    Accept: application/json
    Authorization: "token <your API token>"

**Example Response:**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Vary: Accept
    Content-Type: application/json

    {
    "relationships": [
        {
            "subject_1_id": 8633,
            "subject_1_org_id": "test1",
            "subject_2_id": 7694,
            "subject_2_org_id": "test11001100",
            "subject_1_role": "Paternal Female First Cousin Once Removed",
            "subject_2_role": "Paternal Female First Cousin Once Removed",
            "protocol_id": null,
            "id": 84
        },
        {
            "subject_1_id": 8633,
            "subject_1_org_id": "test1",
            "subject_2_id": 6776,
            "subject_2_org_id": "test00008",
            "subject_1_role": "Brother",
            "subject_2_role": "Sister",
            "protocol_id": null,
            "id": 73
        },
        {
            "subject_1_id": 8633,
            "subject_1_org_id": "test1",
            "subject_2_id": 9011,
            "subject_2_org_id": "Test2",
            "subject_1_role": "Brother",
            "subject_2_role": "Sister",
            "protocol_id": null,
            "id": 72
        },
        {
            "subject_1_id": 8633,
            "subject_1_org_id": "test1",
            "subject_2_id": 6594,
            "subject_2_org_id": "testas",
            "subject_1_role": "Brother",
            "subject_2_role": "Sister",
            "protocol_id": null,
            "id": 25
        },
        {
            "subject_1_id": 8633,
            "subject_1_org_id": "test1",
            "subject_2_id": 6023,
            "subject_2_org_id": "JULYTEST",
            "subject_1_role": "Brother",
            "subject_2_role": "Brother",
            "protocol_id": null,
            "id": 22
        },
        {
            "subject_1_id": 8081,
            "subject_1_org_id": "testflkjdkf",
            "subject_2_id": 8633,
            "subject_2_org_id": "test1",
            "subject_1_role": "Brother",
            "subject_2_role": "Sister",
            "protocol_id": null,
            "id": 47
        }
    ]
}

Contents:

.. toctree::
   :maxdepth: 2
