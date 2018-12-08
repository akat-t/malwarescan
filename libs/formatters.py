# -*- coding: utf-8 -*-
"""Main views.py file for current application module."""
#
# Copyright 2018 AKAT TECHNOLOGIES OOD. All rights reserved
#
# Author(s): Lyuben Bahtarliev <lyuben.bahtarliev@akat-t.com>
#
import yaml
from datetime import datetime as dtime
from datetime import timedelta as tdelta
from dateutil.parser import parse as dtparser
from flask import url_for
from flask import Markup

# Flask-Admin Column Formatters


def fmt_file_results(view, context, model, name):
    field = getattr(model, name)
    # out_data = json.dumps(field, sort_keys = True, indent = 4)  # JSON
    out_data = yaml.dump(
        field, explicit_start=True, width=150, indent=4)  # YaML
    return Markup('<pre class="prettyprint">{}</pre>'.format(out_data))


def fmt_elapsed_time(view, context, model, name):
    date_b = getattr(model, name)
    date_f = model.date_f
    if model.status_f == "InProgress":
        etime = str(dtparser(str(dtime.now())) - dtparser(str(date_f)))
    else:
        etime = str(dtparser(str(date_b)) - dtparser(str(date_f)))
    return Markup('<strong><i>{}</i></strong>'.format(etime))


def fmt_elapsed_time_secs(view, context, model, name):
    field = getattr(model, name)
    return Markup('<strong><i>{}</i></strong>'.format(
        str(tdelta(seconds=field))))


def fmt_cclient_details(view, context, model, name):
    field = getattr(model, name)
    url = url_for('clients.details_view', id=model.id)
    return Markup('<a href="{}">{}</a>'.format(url, field))


def fmt_eclient_details(view, context, model, name):
    field = getattr(model, name)
    try:
        url = url_for('clients.details_view', id=model.client.id)
    except:  # noqa: E722
        url = '#'
    return Markup('<a href="{}">{}</a>'.format(url, field))


def fmt_eval_details(view, context, model, name):
    url = url_for('evals.details_view', id=model.id)
    return Markup('<a href="{}">{}</a>'.format(url, model.uuid_f))


def fmt_file_details(view, context, model, name):
    url = url_for('files.details_view', id=model.id)
    return Markup('<a href="{}">{}</a>'.format(url, model.name))


def fmt_files_length(view, context, model, name):
    field = getattr(model, name)
    return Markup(f'<span class="label label-primary">{len(field)}</span>')


def fmt_counts(view, context, model, name):
    field = getattr(model, name)
    return Markup(f'<span class="label label-primary">{field}</span>')


def fmt_text_bold(view, context, model, name):
    field = getattr(model, name)
    return Markup(f'<strong>{field}</strong>')


def fmt_text_italic(view, context, model, name):
    field = getattr(model, name)
    return Markup(f'<i>{field}</i>')


def fmt_text_boldital(view, context, model, name):
    field = getattr(model, name)
    return Markup(f'<strong><i>{field}</i></strong>')


def fmt_render_score(view, context, model, name):
    field = getattr(model, name)
    if field > 5:
        return str(True)
    else:
        return str(False)
