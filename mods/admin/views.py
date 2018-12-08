from flask_admin import Admin
from flask_admin.base import MenuLink
from exts.sqlalchemy import db
from mods.api.models import Client, Eval, File
from mods.admin.admin_models import ClientsView, EvalsView, FilesView
from mods.admin.admin_controller import MyHomeView

admin = Admin(
    app=None,
    name='MalwareScan Admin',
    base_template='admin/base_layout.html',
    template_mode='bootstrap3',
    endpoint='admin',
    url='/admin',
    index_view=MyHomeView(name='Dashboard'))
admin.add_view(
    ClientsView(
        Client, db.session, name='Clients', endpoint='clients', url='clients'))
admin.add_view(
    EvalsView(
        Eval, db.session, name='Evaluations', endpoint='evals', url='evals'))
admin.add_view(
    FilesView(File, db.session, name='Files', endpoint='files', url='files'))
admin.add_link(
    MenuLink(name='Upload Files', category='Tools', url='/admin/upload'))
admin.add_link(
    MenuLink(name='Session Info', category='Tools', url='/admin/info'))
