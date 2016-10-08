# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, Blueprint, request, render_template, url_for, send_from_directory
import logging
import datetime
import requests
import urllib
import json
import uuid

from .forms import BankForm
from .utils import *

logger = logging.getLogger(__name__)
app = Flask(__name__, template_folder="templates", static_folder="statics")
#app.config.from_object("at.config")
app.secret_key = 'citibankfajdslkf'

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/", methods=['POST', 'GET'])
def index():
    form = BankForm()
    if form.luong.data not in ["yes", "no"]:
	form.luong.data = ''
    slbox_region = select_box_by_list(REGION, form.region.data, 'region', 'region', 'form-control styled', '',
                                      'Khu vực sinh sống')
    slbox_caoch = select_box_by_list(CAOCH, form.caoch.data, 'caoch', 'caoch', 'form-control styled', '',
                                      'Mức thu nhập của bạn')
    slbox_cardtype = select_box_by_list(CARDTYPE, form.cardtype.data, 'cardtype', 'cardtype', 'form-control styled', '',
                                        'Loại thẻ đăng ký')

    if request.method == 'POST':
        if form.validate_on_submit():

            salary_method = "CASH_IN_HAND"
            if form.luong.data == "yes":
                salary_method = "BANK_TRANSFER"

            data = {
                "properties": [
                    {"property":"identifier", "value":str(uuid.uuid4())},
                    {"property":"firstname", "value":form.name.data},
                    {"property":"lastname", "value":""},
                    {"property":"email", "value":form.email.data},
                    {"property":"phone", "value":form.phone.data},
                    {"property":"hs_lead_status", "value":"NEW"},
                    {"property":"region", "value": form.region.data},
                    {"property":"cardtype", "value": form.cardtype.data},
                    {"property":"salary_payment_method", "value":salary_method},
                    {"property":"monthly_income_level", "value":int(form.caoch.data)},
                    {"property":"aff_source", "value":form.aff_source.data},
                    {"property":"aff_sid", "value":form.aff_sid.data},
                ]
            }

            url = "https://api.hubapi.com/contacts/v1/contact/?hapikey=3f028fdd-3630-4098-a4aa-e93f123cf781"
            header = {'Content-Type': 'application/json'}
            res = requests.post(url=url, data=json.dumps(data), headers=header)
            res_json = res.json()

            if res_json:
                if "status" in res_json and res_json["status"] == "error":
                    if "error" in res_json and res_json["error"] == "CONTACT_EXISTS":
                        form.email.errors.append(u"Email đã tồn tại")
                    else:
                        form.email.errors.append(res_json["message"])

                    return render_template('index.html', form=form, slbox_region=slbox_region, slbox_caoch=slbox_caoch, slbox_cardtype=slbox_cardtype)
                else:
                    return render_template('thankyou.html')

            form.email.errors.append("Invalid data!")
            return render_template('index.html', form=form, slbox_region=slbox_region, slbox_caoch=slbox_caoch, slbox_cardtype=slbox_cardtype)

        else:
            return render_template('index.html', form=form, slbox_region=slbox_region, slbox_caoch=slbox_caoch, slbox_cardtype=slbox_cardtype)

    return render_template('index.html', form=form, slbox_region=slbox_region, slbox_caoch=slbox_caoch, slbox_cardtype=slbox_cardtype)
