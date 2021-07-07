# -*- coding: utf-8 -*-

import logging
import pysftp
import paramiko

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    queryt = fields.Text()

    def execute_rapitech_query(self):
        if self.queryt:
            print(self.queryt)
            sql = self.queryt
            self._cr.execute(sql)
            self._cr.commit()

        return True


    def test_ftp(self):
        with pysftp.Connection(host="129.151.115.116",port=14422, username="jdodoo",
            private_key="/home/odoo/src/user/rapitech_query/lryodoo.pem") as sftp:
            with sftp.cd('/home/jdodoo/oddo'):             # temporarily chdir to public
                sftp.put('/home/odoo/src/user/rapitech_query/rapitech_query/hola1.txt')  # upload file to public/ on remote
                #sftp.get('/home/jdodoo/oddo/hola.txt')         # get a remote file

 
