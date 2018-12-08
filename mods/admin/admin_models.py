# -*- coding: utf-8 -*-
"""Main views.py file for current application module."""
#
# Copyright 2018 AKAT TECHNOLOGIES OOD. All rights reserved
#
# Author(s): Lyuben Bahtarliev <lyuben.bahtarliev@akat-t.com>
#
from datetime import timedelta as tdelta
from dateutil.parser import parse as dtparser
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import macro
from libs.formatters import fmt_cclient_details
from libs.formatters import fmt_eclient_details
from libs.formatters import fmt_text_bold
from libs.formatters import fmt_text_boldital
from libs.formatters import fmt_counts
from libs.formatters import fmt_elapsed_time
from libs.formatters import fmt_elapsed_time_secs
from libs.formatters import fmt_render_score
from libs.formatters import fmt_eval_details
from libs.formatters import fmt_file_details
from libs.formatters import fmt_file_results


# Custom Flask-Admin Models
# Base Model with common settings
class MyBaseView(ModelView):
    can_delete = True
    can_edit = True
    can_create = False
    can_export = True
    can_view_details = True
    details_modal = False
    edit_modal = False
    column_display_actions = False
    can_set_page_size = False
    column_auto_select_related = True
    column_display_all_relations = True
    column_display_pk = True
    page_size = 500
    export_types = ['csv', 'xls', 'json', 'yaml']


class ClientsView(MyBaseView):
    column_list = [
        'id', 'x509_cname', 'x509_orgname', 'x509_orgstate', 'date_fseen',
        'date_lseen', 'last_ip', 'evals_count'
    ]
    column_sortable_list = [
        'id', 'x509_serial', 'x509_cname', 'x509_orgdept', 'x509_orgname',
        'x509_orgstate', 'evals_count'
    ]
    column_details_list = [
        'id', 'fingerprint', 'x509_serial', 'x509_cname', 'x509_email',
        'x509_orgdept', 'x509_orgname', 'x509_orgstate', 'date_fseen',
        'date_lseen', 'last_ip', 'evals_count', 'evals'
    ]
    column_exclude_list = ['x509_data']
    column_export_list = [
        'id', 'fingerprint', 'x509_serial', 'x509_cname', 'x509_email',
        'x509_orgdept', 'x509_orgname', 'x509_orgstate', 'date_fseen',
        'date_lseen', 'last_ip', 'evals_count'
    ]
    column_export_exclude_list = ['x509_data', 'evals']
    column_formatters_export = {}
    column_searchable_list = []
    column_default_sort = ('id', True)
    column_filters = [
        'fingerprint', 'x509_serial', 'x509_cname', 'x509_orgname',
        'x509_email', 'x509_orgstate', 'x509_orgdept', 'evals_count'
    ]
    column_formatters = dict(
        x509_cname=fmt_cclient_details,
        x509_orgname=fmt_text_bold,
        evals_count=fmt_counts,
        evals=macro('render_evals'))
    column_formatters_export = dict(
        x509_serial=lambda v, c, m, p: str(getattr(m, p)),
        date_fseen=lambda v, c, m, p: str(getattr(m, p)),
        date_lseen=lambda v, c, m, p: str(getattr(m, p)))
    column_labels = dict(
        id='Id',
        fingerprint='[X.509] Thumbprint',
        last_ip='Last seen IP',
        date_fseen='First seen Date',
        date_lseen='Last seen Date',
        evals_count='# of Evaluations',
        evals='List of Evaluations',
        x509_serial='[X.509] Serial',
        x509_cname='[X.509] Common Name',
        x509_email='[X.509] Email Address',
        x509_orgdept='[X.509] Department',
        x509_orgname='[X.509] Organization',
        x509_orgstate='[X.509] BULSTAT')


class EvalsView(MyBaseView):
    column_list = [
        'id', 'uuid_f', 'client', 'corrid', 'date_f', 'date_b', 'status_f',
        'score', 'files_count'
    ]
    column_sortable_list = [
        'id', 'uuid_f', 'client', 'corrid', 'date_f', 'date_b', 'status_f',
        'score', 'files_count'
    ]
    column_details_list = [
        'id', 'client', 'uuid_f', 'corrid', 'date_f', 'date_b', 'score',
        'status_f', 'files_count', 'files'
    ]
    column_exclude_list = [
        '',
    ]
    column_export_list = [
        'id', 'client', 'uuid_f', 'corrid', 'date_f', 'date_b', 'score',
        'status_f', 'files_count'
    ]
    column_export_exclude_list = ['files']
    column_formatters_export = dict(score=fmt_render_score,
                                    client=lambda v, c, m, p: str(getattr(m, p)),
                                    date_f=lambda v, c, m, p: str(getattr(m, p)),
                                    date_b=lambda v, c, m, p: str(dtparser(str(m.date_b)) -
                                                                  dtparser(str(m.date_f))))
    column_searchable_list = []
    column_default_sort = ('date_f', True)
    column_filters = [
        'uuid_f', 'corrid', 'status_f', 'score', 'client', 'files_count'
    ]
    column_formatters = dict(
        score=macro('render_score'),
        client=fmt_eclient_details,
        uuid_f=fmt_eval_details,
        corrid=fmt_text_boldital,
        date_b=fmt_elapsed_time,
        status_f=fmt_text_bold,
        files_count=fmt_counts,
        files=macro('render_files_name'))

    column_labels = dict(
        id='Id',
        client_id='Client Id',
        client='[X.509] Common Name',
        uuid_f='Evaluation UUID',
        corrid='Correlation ID',
        status_f='Status',
        date_f='Submit Date',
        date_b='Elapsed Time',
        score='Is Malicious?',
        files_count='# of Files',
        files='List of Files')


class FilesView(MyBaseView):
    column_list = [
        'id', 'name', 'sha1', 'date_b', 'status_f', 'score', 'message',
        'evals_count'
    ]
    column_sortable_list = [
        'id', 'name', 'sha1', 'date_b', 'status_f', 'score', 'message',
        'evals_count'
    ]
    column_exclude_list = [
        'uuid_f', 'evals_len', 'results', 'md5', 'mtype', 'exec_time',
        'expect_sandbox', 'hash'
    ]
    column_details_list = [
        'id', 'name', 'mtype', 'md5', 'sha1', 'hash', 'date_b', 'exec_time',
        'status_f', 'score', 'message', 'results', 'evals_count', 'evals'
    ]
    column_export_list = [
        'id', 'name', 'mtype', 'md5', 'sha1', 'hash', 'date_b', 'exec_time',
        'status_f', 'score', 'message', 'evals_count'
    ]
    column_export_exclude_list = ['evals', 'results']
    column_formatters_export = {}
    column_searchable_list = []
    column_default_sort = ('date_b', True)
    column_filters = ['name', 'mtype', 'sha1', 'score', 'evals_count']
    column_formatters_export = dict(
        score=fmt_render_score,
        date_b=lambda v, c, m, p: str(getattr(m, p)),
        exec_time=lambda v, c, m, p: str(tdelta(seconds=getattr(m, p))))
    column_formatters = dict(
        evals_count=fmt_counts,
        evals=macro('render_evals_cname'),
        exec_time=fmt_elapsed_time_secs,
        name=fmt_file_details,
        score=macro('render_score'),
        status_f=fmt_text_bold,
        message=macro('render_message'),
        results=fmt_file_results)
    column_labels = dict(
        id='Id',
        name='Filename',
        mtype='MIME Type',
        md5='MD5 Hash',
        sha1='SHA1 Hash',
        hash='SHA256 Hash',
        uuid_f='UUID',
        status_f='Status',
        date_b='Status Date',
        exec_time='Elapsed Time',
        score='Is Malicious?',
        expect_sandbox='Expect Sandbox?',
        message='Message',
        evals_count='# of Evaluations',
        evals='List of Evaluations',
        results='Results')
