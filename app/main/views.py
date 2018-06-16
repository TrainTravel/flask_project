# main/views.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir, remove, path
from flask import render_template, session, redirect, url_for, current_app, send_file, after_this_request, make_response
from .. import db
from ..models import User
from ..EMAIL import send_email
from . import main
from .forms import NameForm

import pandas as pd
from itertools import combinations
from io import BytesIO

base_dir = path.dirname(path.realpath(__file__))
lottery_dir = base_dir + '/lottery_files/'

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        print(db)
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User', \
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), \
                           known=session.get('known', False))

@main.route('/lottery')
def lottery_usage():
    #usage = [b"使用方法: eg. 39選7 => 35.229.113.88/lottery/39/7 "]
    usage = "使用方法:  ex. 39選7   網址：trainchen.me/lottery/39/7 "
    return make_response(usage)


@main.route('/lottery/<total>/<pick>')
def combination(total, pick):
    total = int(total)
    pick = int(pick)
    df = pd.DataFrame(list(combinations(range(1, total+1), pick)))
    arrays = [['組合'], list(range(1, pick+1))]
    df.index = range(1, df.shape[0]+1)
    col_index = pd.MultiIndex.from_product(arrays)
    df.columns = col_index

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, '組合')
    writer.save()
    output.seek(0)
    #writer = pd.ExcelWriter(output)
    # writer.close() # causes TypeError: string argument expected, got 'bytes'
    
    resp = make_response(output.getvalue())
    resp.headers['Content-Disposition'] = 'attachment; filename={}_pick_{}.xlsx'.format(total, pick)
    resp.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return resp
'''
@main.route('/lottery/<total>/<pick>')
def combination(total, pick):
    filename = '{}_pick_{}.xlsx'.format(total, pick)
    #if filename in listdir(base_dir):
    #    print('already exist')
    #    return send_file(base_dir + filename, attachment_filename=filename)

    total = int(total)
    pick = int(pick)
    df = pd.DataFrame(list(combinations(range(total), pick)))
    arrays = [['組合'],list(range(1, pick+1))]
    col_index = pd.MultiIndex.from_product(arrays)
    df.columns = col_index
    F = lottery_dir + filename
    df.to_excel(F)
    f_handle = open(F, 'r')

    @after_this_request
    def remove_file(response):
        try:
            remove(F)
            f_handle.close()
        except Exception as error:
            main.logger.error("Error removing or closing downloaded file handle", error)
        return response
        
    return send_file(F, attachment_filename=filename)
#output = io.BytesIO()
#writer = pd.ExcelWriter(output, engine='xlsxwriter')
'''

    #def f_gen():
    #    with open(F) as f:
    #        yield from f

    #'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #if total > 20:
    #    remove(base_dir + filename)
