# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, tools
from datetime import datetime

_logger = logging.getLogger(__name__)

def year_now():
    return datetime.now().year

YEAR_SELECTION = [(str(year), year) for year in range(1450, year_now()+2)]

class BookLanguage(models.Model):
    _name = 'book.language'

    name = fields.Char(string='Idioma')


class BookFormat(models.Model):
    _name = 'book.format'

    name = fields.Char(string='Formato')


class BookAuthor(models.Model):
    _name = 'book.author'

    name = fields.Char(string='Autor')
    country_id = fields.Many2one(comodel_name='res.country', string='País')
    image = fields.Binary(string="Logo", attachment=True, help="This field holds the image used as logo for the brand, limited to 1024x1024px.")
    image_medium = fields.Binary(string="Medium-sized image", attachment=True, help="Medium-sized logo of the brand. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    """

    image_small = fields.Binary(string="Small-sized image", attachment=True, help="Small-sized logo of the brand. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        return super(BookAuthor, self).create(vals_list)

    def write(self, vals):
        tools.image_resize_images(vals)
        return super(BookAuthor, self).write(vals)
    """

class BookPublisher(models.Model):
    _name = 'book.publisher'

    name = fields.Char(string='Editorial')

class FillingType(models.Model):
    _name = 'filling.type'

    name = fields.Char(string='Tipo de estampe')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    name = fields.Char('Titulo')
    list_price = fields.Float('PVP (S/)')
    isbn_13 = fields.Float(string='ISBN', size=15, digits=(15, 0))
    author = fields.Many2one(comodel_name='book.author', string='Autor')
    editorial = fields.Many2one(comodel_name='book.publisher', string='Sello Editorial')
    year = fields.Selection(selection=YEAR_SELECTION, string='Año de Publicación')
    edition_number = fields.Integer(string='Nº Edicion')
    language_book = fields.Char(comodel_name='book.language', string='Idioma')
    book_format = fields.Many2one(comodel_name='book.format', string='Formato')
    type_of_filling = fields.Many2one(comodel_name='filling.type', string='Tipo de empaste')
    number_of_pages = fields.Integer(string='N° Pags.')
    weight_book = fields.Float(string='Peso (GR).')
    long_dimension = fields.Float(string='Dimension Largo (CM)')
    widht_dimension = fields.Float(string='Dimension ancho (CM)')
    summary = fields.Text(string='Resumen (Sinopsis)')
    observation = fields.Text(string='Observación 1')
    supplier_id = fields.Many2one(comodel_name='res.partner', string='Proveedor')
