# -*- coding: utf-8 -*-
import logging

from odoo import fields, models
from datetime import datetime

_logger = logging.getLogger(__name__)

class ProductPricelist(models.Model):
    _inherit = "product.pricelist.item"

    applied_on = fields.Selection(selection_add=[('4_editorial','Sello Editorial'),
        ('5_supplier','Proveedor'),('6_author','Autor')], 
        ondelete={'4_editorial': 'cascade', '5_supplier': 'cascade', '6_author': 'cascade'})
    author = fields.Many2one(comodel_name='book.author', string='Autor')
    editorial = fields.Many2one(comodel_name='book.publisher', string='Sello Editorial')
    supplier_id = fields.Many2one(comodel_name='res.partner', string='Proveedor')
