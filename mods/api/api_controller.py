"""API Controller module.
Also contains db and api validation models.
"""

import os
from datetime import datetime as dtime
import magic
from flask import request, jsonify, session
from libs import helpers
from libs.decorators import cert_required
from exts.sqlalchemy import db
from exts.uploads import submissions
from mods.api import tasks


@cert_required
def evaluation_submit(file, correlationID=None):  # noqa: E501
    """Submits a file for evaluation.

     # noqa: E501

    :param file: the file to evaluate
    :type file: werkzeug.datastructures.FileStorage
    :param correlationID: the correlation ID
    :type correlationID: str

    :rtype: str
    """
    # Is the upload using Ajax, or a direct POST by the form?
    from mods.api.models import Client, Eval, File
    is_ajax = False
    if request.form.get("__ajax", None) == "true":
        is_ajax = True

    # Init file as list for future use with multiple files
    files = request.files.getlist("file")
    fd_file = {}
    eval_files = []
    fd_data = {
        'name': '',
        'mtype': '',
        'hash': '',
        'uuid': None,
        'eval_status': None,
        'eval_result': None,
        'eval_date': None
    }
    # Create evaluation
    time_now = str(dtime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    new_eval = Eval(date_f=time_now, corrid=correlationID)
    db.session.add(new_eval)  # noqa: E1101
    # Add evaluation to client
    client = Client.query.filter(
        Client.x509_cname == session.get('client_id')).first()
    if client is not None:
        client.evals.append(new_eval)
    for fd in files:
        data = fd_data.copy()
        file_eval = fd_file.copy()
        data['name'] = submissions.save(fd, folder=new_eval.uuid_f)
        fd.close()
        filename = data['name'].split("/")[-1]
        fullpath = submissions.path(data['name'])
        data["hash"] = str(helpers.hash_checksum("sha256", fullpath))
        data["sha1"] = str(helpers.hash_checksum("sha1", fullpath))
        data["md5"] = str(helpers.hash_checksum("md5", fullpath))
        data['mtype'] = magic.from_file(f'{fullpath}', mime=True)

        has_file = File.query.filter(File.hash == data["hash"]).order_by(
            File.id.desc()).first()
        if has_file is not None:
            new_eval.files.append(has_file)
            os.remove(f"{fullpath}")
        else:
            new_file = File(
                name=filename,
                mtype=data['mtype'],
                sha1=data['sha1'],
                md5=data['md5'],
                hash=data['hash'])
            db.session.add(new_file)
            new_eval.files.append(new_file)
            file_eval[data['hash']] = fullpath
            eval_files.append(file_eval)
    db.session.commit()
    if client is None:
        tasks.client_eval.apply_async(
            args=(eval_files,), task_id=new_eval.uuid_f)
    else:
        tasks.client_eval.apply_async(
            args=(
                eval_files,
                client.x509_cname,
            ), task_id=new_eval.uuid_f)
    if is_ajax is True:
        return jsonify({"status": "ok", "msg": new_eval.uuid_f}), 201
    return new_eval.uuid_f, 201


@cert_required
def evaluation_file_by_sha256(hash):  # noqa: E501
    """Gets an evaluation file with a specified SHA-256 hash.

    :param hash: the SHA-256 hash of the file
    :type hash: str

    :rtype: EvaluationFile
    """
    from mods.api.models import File
    # Some RegEx Validation to avoid injections etc.
    if helpers.re_sha256.match(hash) is None:
        return {
            "detail": "An evaluation file with the specified "
                      "SHA-256 hash could not be found."
        }, 404
    # file = File.query.filter(File.hash == hash).first()
    file = File.query.filter(File.hash == hash).order_by(File.id.desc()).first()
    if file is None:
        return {
            "detail": "An evaluation file with the specified "
                      "SHA-256 hash could not be found."
        }, 404
    sfile = file.toDict()
    r_file = helpers.marshal_file(sfile)
    return r_file, 200


@cert_required
def evaluation_get(id):  # noqa: E501
    """Gets an evaluation with a specified ID.

    :param id: the ID of the evaluation
    :type id: str

    :rtype: Evaluation
    """
    from mods.api.models import Eval
    # Some RegEx Validation to avoid injections etc.
    if helpers.re_uuid4.match(id) is None:
        return {
            "detail": "An evaluation with the specified "
                      "ID could not be found."
        }, 404
    eval = Eval.query.filter(Eval.uuid_f == id).first()
    if eval is None:
        return {
            "detail": "An evaluation with the specified "
                      "ID could not be found."
        }, 404
    sfile = eval.toDict()
    r_eval = helpers.marshal_eval(sfile)
    # EvaluationFile
    for file in eval.files:
        r_file = helpers.marshal_file(file.toDict())
        r_eval['files'].append(r_file)
    if sfile.get('corrid') is not None:
        r_eval['correlationID'] = sfile.get('corrid')
    else:
        r_eval.pop('correlationID', None)
    return r_eval, 200
