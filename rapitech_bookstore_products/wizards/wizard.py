# -*- coding: utf-8 -*-
from odoo import fields, models

class UploadImages(models.TransientModel):
    _name = 'book.wizard.upload.images'

    folder_images = fields.Many2many('ir.attachment', string="Image")

    def import_files(self):
        if self.folder_images:
            for img in self.folder_images:
                product_id = self.env['product.template'].sudo().search([('isbn_13','=',img.name.split('.')[0])])
                if product_id:
                    product_id.write({'image_1920':img.datas})
