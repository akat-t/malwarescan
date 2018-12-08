from datetime import datetime as dtime
from exts.sqlalchemy import db
from mods.api.models import Client

from functools import wraps
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from flask import session, request, abort, current_app


def cert_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if dict(request.headers).get('X-Ssl-Verify') != "SUCCESS":
            if current_app.config.get("API_DEMO") is True:
                client_cert = Client.query.filter(Client.id == 1).order_by(
                    Client.id.desc()).first()
                session['client_id'] = client_cert.x509_cname
                return f(*args, **kwargs)
            session['client_id'] = None
            abort(401)
        else:
            if session.get('client_id') is None:
                cert_data = dict(request.headers).get('X-Ssl-Cert').replace(
                    "\t", "").encode("utf-8")
                cert = x509.load_pem_x509_certificate(cert_data,
                                                      default_backend())
                session['client_id'] = str(
                    cert.fingerprint(cert.signature_hash_algorithm).hex())
                client_cert = Client.query.filter(
                    Client.fingerprint == session['client_id']).order_by(
                        Client.id.desc()).first()
                if client_cert is None:
                    cname = str(
                        cert.subject.get_attributes_for_oid(
                            x509.OID_COMMON_NAME)[0].value)
                    serial = str(cert.serial_number)
                    try:
                        email = str(
                            cert.subject.get_attributes_for_oid(
                                x509.OID_EMAIL_ADDRESS)[0].value)
                    except:  # noqa: E722
                        email = "UNKNOWN"
                    try:
                        orgdept = str(
                            cert.subject.get_attributes_for_oid(
                                x509.OID_ORGANIZATIONAL_UNIT_NAME)[0].value)
                    except:  # noqa: E722
                        orgdept = "UNKNOWN"
                    try:
                        orgname = str(
                            cert.subject.get_attributes_for_oid(
                                x509.OID_ORGANIZATION_NAME)[0].value)
                    except:  # noqa: E722
                        orgname = "UNKNOWN"
                    try:
                        orgstate = str(
                            cert.subject.get_attributes_for_oid(
                                x509.OID_STATE_OR_PROVINCE_NAME)[0].value)
                    except:  # noqa: E722
                        orgstate = "UNKNOWN"
                    scert = Client(
                        fingerprint=session['client_id'],
                        last_ip=dict(request.headers).get('X-Real-Ip'),
                        x509_data=cert_data,
                        x509_cname=cname,
                        x509_serial=serial,
                        x509_email=email,
                        x509_orgdept=orgdept,
                        x509_orgname=orgname,
                        x509_orgstate=orgstate)
                    db.session.add(scert)
                    db.session.commit()
                else:
                    last_ip = dict(request.headers).get('X-Real-Ip')
                    if client_cert.last_ip != last_ip:
                        current_app.Logger.warning(
                            "Client IP: ({last_ip}) differs from last ({client_cert.last_ip})!"
                        )
                    date_lseen = dtime.strptime(
                        dtime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                        "%Y-%m-%d %H:%M:%S.%f")
                    db.session.query(Client).filter(
                        Client.id == client_cert.id).update({
                            'last_ip': last_ip,
                            'date_lseen': date_lseen
                        })
                    db.session.flush()
                    db.session.commit()
                session['client_id'] = str(
                    cert.subject.get_attributes_for_oid(
                        x509.OID_COMMON_NAME)[0].value)
        return f(*args, **kwargs)

    return decorated_function
