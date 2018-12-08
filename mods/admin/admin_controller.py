#!/usr/bin/env python
# coding: utf-8
'''Main views.py file for current application module.'''
# Copyright: 2018 AKAT TECHNOLOGIES OOD. All rights reserved
# Author(s): Lyuben Bahtarliev <lyuben.bahtarliev@akat-t.com>
from flask import request, session, jsonify
from mods.api.models import Client, Eval, File
from libs.decorators import cert_required

# Custom Flask-Admin Views
from flask_admin import expose
from flask_admin.base import AdminIndexView


class MyHomeView(AdminIndexView):
    @expose('/')
    @cert_required
    def index(self):
        topX = int(request.args.get('top', 10))
        clients = Client.query.all()
        evals = Eval.query.all()
        files = File.query.all()
        threats = File.query.filter(File.score > 5).count()
        return self.render('admin/index.html',
                           clients=clients,
                           evals=evals,
                           files=files,
                           topX=topX,
                           threats=threats)

    @expose('/upload')
    @cert_required
    def files_upload(self):
        return self.render('admin/upload.html',
                           client_id=session.get('client_id', 'UNKNOWN'))

    @expose('/info')
    @cert_required
    def request_info(self, req=None):
        req_data = {}
        req = request
        req_data['endpoint'] = req.endpoint
        req_data['method'] = req.method
        req_data['cookies'] = req.cookies
        req_data['args'] = req.args
        req_data['form'] = req.form
        req_data['remote_addr'] = req.remote_addr
        req_data['client_id'] = session.get('client_id', None)
        req_data['headers'] = dict(req.headers)
        req_data['headers'].pop('Cookie', None)
        if req_data['headers'].get('X-Ssl-Cert') is not None:
            req_data['SSL_CERT'] = req_data['headers']['X-Ssl-Cert']
            req_data['SSL_CERT'].replace('\t', '').encode('utf-8')
            req_data['headers'].pop('X-Ssl-Cert', None)
        return jsonify(req_data)
