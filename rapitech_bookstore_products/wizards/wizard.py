# -*- coding: utf-8 -*-
from odoo import fields, models
import base64
import requests
from xlrd import open_workbook

class UploadImages(models.TransientModel):
    _name = 'book.wizard.upload.images'

    folder_images = fields.Many2many('ir.attachment', string="Image")
    type_files = fields.Selection([('images','Imagenes'),('file','Archivo')], default="images")
    files_images = fields.Binary()
    
    def get_as_base64(url):

        return base64.b64encode(requests.get(url).content)

    def import_files(self):
        if self.type_files:
            if self.type_files == 'images':
                if self.folder_images:
                    for img in self.folder_images:
                        product_id = self.env['product.template'].sudo().search([('isbn_13','=',img.name.split('.')[0])])
                        if product_id:
                            product_id.write({'image_1920':img.datas})
            else:
                workbook = open_workbook(file_contents = base64.decodebytes(self.files_images))
                worksheet = workbook.sheet_by_index(0)
                for row in range(1,worksheet.nrows):
                    product = worksheet.cell(row,0).value
                    image_path = worksheet.cell(row,1).value
                    try:

                        binimg = base64.b64encode(requests.get(image_path).content)
                        product_obj = self.env['product.template']
                        product_id = product_obj.search([('isbn_13', '=', product)])
                        if product_id:
                            vals = {'image_1920': binimg}
                            product_id.write(vals)
                    except:
                        raise Warning("Please provide correct URL for product '%s' or check your image size.!" % product)
