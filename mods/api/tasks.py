# -*- coding: utf-8 -*-
"""Main tasks.py file for current application module."""
import time
import os
import shutil
from datetime import datetime as dtime
from celery import group
from celery import shared_task
from flask import current_app
from libs import helpers
from exts.sqlalchemy import db
from mods.api.models import Eval
from mods.api.models import File


@shared_task(bind=True, ignore_result=True)
def client_eval(self, files, client_id=None):
    """ Client evaluation task."""
    with current_app.app_context():
        idle_time = 0.1
        new_eval = Eval.query.filter(Eval.uuid_f == self.request.id).first()
        if len(files) > 0:
            self.update_state(state='PROGRESS')
            file_tasks = []
            for file in files:
                for k, v in file.items():
                    file_tasks.append(eval_file.s(v, k, client_id))
            group(*file_tasks)()
        if helpers.eval_running(new_eval) is True:
            while helpers.eval_running(new_eval) is True:
                self.update_state(state='PROGRESS')
                time.sleep(idle_time)
                db.session.refresh(new_eval)
        new_eval.status_f, new_eval.score = helpers.eval_status(new_eval)
        new_eval.date_b = str(dtime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        db.session.commit()
        fpath = "/tmp/uploads/files/{}".format(new_eval.uuid_f)
        shutil.rmtree(str(fpath), ignore_errors=True, onerror=None)
        return self.update_state(state='SUCCESS')


@shared_task(bind=True, ignore_result=True)
def eval_file(self, fullpath, file_hash, client_id=None):
    """ Single file submission to backend task."""
    import requests
    requests.packages.urllib3.disable_warnings()
    with current_app.app_context():
        self.update_state(state='PROGRESS')
        fc = helpers.file_config(fullpath, file_hash, client_id)
        fd = open(fc["fullpath"], "rb")
        file = fd.read()
        fd.close()
        os.remove(fc["fullpath"])
        ma_files = {
            fc["filename"]: (fc["filename"], file, 'application/octet-stream')
        }
        r = requests.post(
            fc["scan_url"], files=ma_files, verify=False, headers=fc["headers"])
        if not r.ok:
            return self.update_state(state='FAILURE')
        return self.update_state(state='SUCCESS')


@shared_task(bind=True, ignore_result=True)
def eval_result(self, jdata):
    """ Single file result received from wsclient service processing task."""
    with current_app.app_context():
        out_msg = helpers.file_result(jdata)
        jdata['status_f'] = "Complete"
        if jdata['status'] == 2 or jdata['status'] == 3:
            jdata['status_f'] = "Error"
        db.session.query(File).filter(File.sha1 == jdata["sha1"]).update({
            File.status_f: jdata['status_f'],
            File.score: jdata['score'],
            File.exec_time: jdata['exec_time'],
            File.date_b: jdata['server_time'],
            File.message: out_msg,
            File.results: jdata
        })
        db.session.commit()
        return self.update_state(state='SUCCESS')
