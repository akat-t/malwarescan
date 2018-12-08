# MalwareScan Framework

## Overview
Unified API frontend to various malware analysis and sandboxing backends.

The goals of this project are to provide easy to use, RESTful interface for submitting files for threat evaluation by various Threat/Reputiation Feeds, AV Vendors, ML/AML Technologies, Sandboxing Platforms, etc.

As this project started around a customer engagement, the only supported backend platform as of now is **Symantec CAS** (Content Analysis System).

However, the design is very modular and flexible enough to support easy integration of other backends. 

## Design
This project utilizes [Connexion](https://github.com/zalando/connexion) library on top of Flask for providing REST API functionality, as well as [Celery](http://celeryproject.org/) for providing means of handling file submission tasks to the various backends and track their progress.

 ***Application Factories*** approach together with ***Flask Patterns*** are used, to allow for modularity and easy addition of new features. 

For example, the project started as [swagger-codegen](https://github.com/swagger-api/swagger-codegen) generated server stub. Due to the chosen design approach however, custom certificate-based (with the help of nginx as web frontend) authorization was added, as well as admin dashboard for easy reporting and maintenance.

## Requirements
Please note, that apart from Python and its related requirements, others should be considered more like a supported versions, than required ones.
 
For example, stable version of **nginx** on **Debian 9** is **1.10**. As this was used during development, this nginx version was assumed the required/supported/minimum one.

However, it is very likely that older, as well as newer, major releases will work _out-of-the-box_.

### Python
- Python 3.6+

### Python related
- Connexion 2.0+
- Flask 1.0+
- Flask-Uploads 0.2+
- Celery 4.0+
- SQLAlchemy 1.2+

### Web frontend
- nginx 1.10+

> Apart from **nginx**, running the application behind other Web servers should be relatively easy. As long as they are able to reverse proxy to a WSGI application, do HTTPS offloading (and eventually Client Certificate authorization), and pass some HTTP Headers along the way.

### Brokering backend
- Redis 3.2+

> Apart from **Redis**, which was used like in nginx's example above, all **Celery** supported brokers should work _out-of-the-box_.

### Database backend
- PostgreSQL 9.6+

> Apart from **PostgreSQL**, which again was used like in nginx's example above, all **SQLAlchemy** supported databases and  dialects like SQLite, PostgreSQL, MySQL, Oracle, MS-SQL, Firebird, Sybase and others, should work with only a slight modification to some of the models. The reason is two specific to **PostgreSQL** data types are used - _INET_ and _JSONB_. Despite that fact, these are used mainly by habbit and may well be replaced by other appropriate data types as applicable.

## Installation
The included `install.sh` script will:

- Install binary and development packages needed on Debian/Ubuntu system;
- Install Python requirements from requirements.txt;
- Build and Install the software in the current Python environment (using virtualenv is ***highly recommended***!);

## Usage
To run the server, please execute the following from the root directory:

```
python3 -m malwarescan
```

and open your browser to here:

```
http://localhost:8080/ui/
```

Swagger (version 2.0) definition lives here:

```
http://localhost:8080/v2/swagger.json
```

OpenAPI (version 3.0.0) definition lives here:

```
http://localhost:8080/v3/openapi.json
```

## Running with Docker
Published on Docker hub. Check out here: [akatt/malwarescan](https://hub.docker.com/r/akatt/malwarescan/)

## TODO List
- Analyze possible code optimizations, as well as further linting if possible.
- ### TBD