# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)

YEAR_SELECTION = [(str(year), year) for year in range(1450, year_now())]

class BookFormat(models.Model):
	_inherit = 'book.format'

	name = fields.Char(string='Formato')


class BookAuthor(models.Model):
	_inherit = 'book.Author'

	name = fields.Char(string='Autor')
	country_id = fields.Many2one(comodel_name='res.country', string='País')
    image = fields.Binary("Logo", attachment=True,
        help="This field holds the image used as logo for the brand, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized logo of the brand. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized logo of the brand. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        return super(BookAuthor, self).create(vals_list)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(BookAuthor, self).write(vals)

class BookPublisher(models.Model):
	_inherit = 'book.publisher'

	name = fields.Char(string='Editorial')

class FillingType(models.Model):
	_inherit = 'filling.type'

	name = fields.Char(string='Tipo de estampe')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    isbn_13 = fields.Integer(string='ISBN-13')
    edition_number = fields.Integer(string='N° de edición')
    year = fields.Selection(selection=YEAR_SELECTION.reverse(), string='Año')
    book_format = fields.Many2one(comodel_name='book.format', string='Formato')
    author = fields.Many2one(comodel_name='book.author', string='Autor')
    editorial = fields.Many2one(comodel_name='book.publisher', string='Editorial')
    type_of_filling = fields.Many2one(comodel_name='filling.type', string='Tipo de empaste')
    number_of_pages = fields.Integer(string='Ń° de páginas')
    weight_book = fields.Float(string='Peso libro')
    long_dimension = fields.Float(string='Dimensión largo')
    widht_dimension = fields.Float(string='Dimensión ancho')
    summary = fields.Text(string='Resumen')
