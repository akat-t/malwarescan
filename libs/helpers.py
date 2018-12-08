# -*- coding: utf-8 -*-
import os
import re
import shutil
import sys
import time
from datetime import datetime as dtime
from datetime import timedelta as tdelta
from hashlib import md5, sha1, sha256
from dateutil.parser import parse as dtparser

# Some RegExes
re_md5 = re.compile("^([0-9]|[a-f]){32}$", re.I)
re_sha1 = re.compile("^([0-9]|[a-f]){40}$", re.I)
re_sha256 = re.compile("^([0-9]|[a-f]){64}$", re.I)

re_email = re.compile(
    r"^[A-Z0-9._%+-]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$", re.I)
re_uuid4 = re.compile(
    r"^([0-9]|[a-f]){8}\-([0-9]|[a-f]){4}\-([0-9]|[a-f]){4}\-([0-9]|[a-f]){4}\-([0-9]|[a-f]){12}$",  # noqa: E501
    re.I,
)  # noqa: E501


# Jinja2 Filters
def fltr_elapsedTime(date_f, date_b=None):
    if date_b is None:
        date_b = dtime.now()
    return str(dtparser(str(date_b)) - dtparser(str(date_f)))


def fltr_elapsedTime_secs(value):
    return str(tdelta(seconds=value))


# Nice log messages
def timed(message, level):
    now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    return "%s | %-8s | %-6d | %-13s | %s" % (
        now,
        level,
        os.getpid(),
        sys._getframe(1).f_code.co_name,
        message,
    )


# Evaluation helpers
def eval_cleanup(new_eval):
    shutil.rmtree(
        "/tmp/uploads/files/{}".format(new_eval.uuid_f),
        ignore_errors=True,
        onerror=None,
    )


def eval_running(new_eval):
    for file in new_eval.files:
        if file.status_f == "InProgress":
            return True
    return False


def eval_status(new_eval):
    has_score = 0
    has_error = 0
    eval_result = "Complete"
    for file in new_eval.files:
        if file.score > has_score:
            has_score = file.score
        if file.status_f == "Error":
            has_error += 1
    if has_error > 0:
        eval_result = "Error"
    return eval_result, has_score


# File results marshaling helper per OpenAPI specification
def marshal_file(sfile):
    r_file = {
        "fileName": "",
        "malicious": False,
        "message": "",
        "sha256": "",
        "statusDate": "",
        "status": "InProgress",
    }
    # EvaluationFile
    r_file["fileName"] = sfile["name"]
    if sfile["score"] > 5:
        r_file["malicious"] = True
    r_file["message"] = sfile.get("message")
    r_file["sha256"] = sfile["hash"]
    r_file["statusDate"] = sfile["date_b"]
    r_file["status"] = sfile["status_f"]
    if r_file["status"] == "InProgress":
        file_keys = ["malicious", "message"]
        for key in file_keys:
            r_file.pop(key, None)
        dtime_fmt = "%Y-%m-%d %H:%M:%S.%f"
        r_file["statusDate"] = dtime.strptime(
            dtime.now().strftime(dtime_fmt)[:-3], dtime_fmt)
    elif r_file["status"] == "Error":
        r_file.pop("malicious", None)
    return r_file


# Evaluation results marshaling helper per OpenAPI specification
def marshal_eval(sfile):
    r_eval = {
        "id": "",
        "correlationID": "",
        "date": "",
        "elapsedTime": "",
        "statusDate": "",
        "status": "InProgress",
        "malicious": False,
        "files": [],
    }
    # Evaluation
    r_eval["id"] = sfile["uuid_f"]
    r_eval["correlationID"] = sfile["corrid"]
    r_eval["date"] = sfile["date_f"]
    if sfile["score"] > 5:
        r_eval["malicious"] = True
    r_eval["statusDate"] = sfile["date_b"]
    r_eval["status"] = sfile["status_f"]
    if r_eval["status"] == "InProgress":
        eval_keys = ["malicious", "date_b"]
        for key in eval_keys:
            r_eval.pop(key, None)
        r_eval["elapsedTime"] = str(dtime.now() -
                                    dtparser(str(sfile.get("date_f"))))
        dtime_fmt = "%Y-%m-%d %H:%M:%S.%f"
        r_eval["statusDate"] = dtime.strptime(
            dtime.now().strftime(dtime_fmt)[:-3], dtime_fmt)
    elif r_eval["status"] == "Error":
        r_eval.pop("malicious", None)
        r_eval["elapsedTime"] = str(
            dtparser(str(sfile.get("date_b"))) -
            dtparser(str(sfile.get("date_f"))))
    else:
        r_eval["elapsedTime"] = str(
            dtparser(str(sfile.get("date_b"))) -
            dtparser(str(sfile.get("date_f"))))
    return r_eval


def del_none(original):
    filtered = {k: v for k, v in original.items() if v is not None}
    # If you want yo update the original one.
    # original.clear()
    # original.update(filtered)
    return filtered


def hash_checksum(alg, filename, block_size=65536):
    if alg.lower() == "md5":
        hash_alg = md5()
    elif alg.lower() == "sha1":
        hash_alg = sha1()
    elif alg.lower() == "sha256":
        hash_alg = sha256()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hash_alg.update(block)
    return hash_alg.hexdigest()


def file_hash(alg, filename, block_size=65536):
    if alg.lower() == "md5":
        hash_alg = md5()
    elif alg.lower() == "sha1":
        hash_alg = sha1()
    elif alg.lower() == "sha256":
        hash_alg = sha256()
    for block in iter(lambda: filename.stream.read(block_size), b""):
        hash_alg.update(block)
    return hash_alg.hexdigest()


def file_config(fullpath, hash, client_id):
    fc = {"fullpath": fullpath, "hash": hash, "client_id": client_id}
    fc["filename"] = fullpath.split("/")[-1]
    # Little delay trick based on filename
    fc["delay"] = 0
    if re.match("^delay_[0-9]{1,3}_.*$", fc["filename"]):
        fc["delay"] = int(fc["filename"].split("_")[1])
    # Backend information
    from flask import current_app

    CAS_CONF = current_app.config["CAS_API"]
    fc["host"] = CAS_CONF["host"]
    fc["token"] = CAS_CONF["token"]
    fc["headers"] = {
        "X-API-TOKEN": fc["token"],
        "X-Response-Wait-MS": CAS_CONF["wait_ms"],
    }
    if fc["client_id"] is None:
        url_base = "https://{host}/rapi/cas/scan?token={token}"
    else:
        url_base = "https://{host}/rapi/cas/scan?token={token}&client-id={client_id}"
    fc["scan_url"] = url_base.format(**fc)
    return fc


def file_result(jdata):
    # Parse and collect meaningful 'message'
    if jdata.get("score") < 6:
        return "Clean"
    out_msg = []
    cas_modules = {
        "file_reputation": "File Reputation",
        "user_hash_list": "Custom Blacklist",
        "policy": "Global Policy",
        "cylance": "Predictive Analysis",
        # "symantec": "Predictive Analysis",
        "symantec": "Antivirus/AML",
        "sophos": "Antivirus",
        "kaspersky": "Antivirus",
        "mcafee": "Antivirus",
        "malware_analysis": "Sandboxing",
        "fireeye": "Sandboxing",
        "lastline": "Sandboxing",
        "cloud_sandboxing": "Sandboxing",
    }
    for k, v in jdata.items():
        if k in cas_modules.keys():
            if v.get("status") == 1 and v.get("score", 0) > 5:
                out_msg.append("Blocked by {}".format(cas_modules[k]))
                if k == "policy":
                    out_msg.append(v.get("details", None))
    return "; ".join(out_msg)


class ReverseProxied(object):
    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name):]

        scheme = environ.get("HTTP_X_SCHEME", "")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)
