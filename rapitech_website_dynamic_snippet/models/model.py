# -*- coding: utf-8 -*-
import logging

from odoo import fields, models, api, _
# -*- coding: utf-8 -*-

from ast import literal_eval
from odoo.osv import expression
from odoo.exceptions import ValidationError
from odoo.tools import html_escape as escape

_logger = logging.getLogger(__name__)

class SnippetFilter(models.Model):
    _inherit = "website.snippet.filter"

    product_ids = fields.Many2many('product.template', string='Productos', 
        domain="[('is_published','=',True)]")
    field_names = fields.Char(default='display_name,description_sale,image_512,list_price')
    filter_id = fields.Many2one(domain="[('model_id','=','product.template')]")

    @api.model
    def escape_falsy_as_empty(self, s):
        return escape(s) if s else ''
    
    @api.constrains('action_server_id', 'filter_id', 'product_ids')
    def _check_data_source_is_provided(self):
        for record in self:
            if bool(record.action_server_id) == bool(record.filter_id) == bool(record.product_ids):
                raise ValidationError(_("Either action_server_id or filter_id or product_ids must be provided."))

    def _prepare_values(self, limit=None, search_domain=[]):
        """Gets the data and returns it the right format for render."""
        self.ensure_one()
        limit = limit and min(limit, self.limit) or self.limit
        if self.filter_id:
            filter_sudo = self.filter_id.sudo()
            domain = filter_sudo._get_eval_domain()
            if 'is_published' in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, [('is_published', '=', True)]])
            if search_domain:
                domain = expression.AND([domain, search_domain]),

            records = self.env[filter_sudo.model_id].search(
                domain,
                order=','.join(literal_eval(filter_sudo.sort)) or None,
                limit=limit
            )
            return self._filter_records_to_dict_values(records)
        elif self.action_server_id:
            return self.action_server_id.with_context(
                dynamic_filter=self,
                limit=limit,
                search_domain=search_domain,
                get_rendering_data_structure=self._get_rendering_data_structure,
            ).sudo().run()


        elif self.product_ids:
            records = self.env['product.template'].search([('id','in',self.product_ids.ids)],
                limit=limit)
            return self._filter_records_to_dict_values(records)


    def _filter_records_to_dict_values(self, records):
        """Extract the fields from the data source and put them into a dictionary of values

            [{
                'fields':
                    OrderedDict([
                        ('name', 'Afghanistan'),
                        ('code', 'AF'),
                    ]),
                'image_fields':
                    OrderedDict([
                        ('image', '/web/image/res.country/3/image?unique=5d9b44e')
                    ]),
             }, ... , ...]

        """

        self.ensure_one()
        values = []
        model = self.env[self.filter_id and self.filter_id.model_id or 'product.template']
        Website = self.env['website']
        for record in records:
            data = self._get_rendering_data_structure()
            for field_name in self.field_names.split(","):
                field_name, _, field_widget = field_name.partition(":")
                field = model._fields.get(field_name)
                field_widget = field_widget or field.type
                if field.type == 'binary':
                    data['image_fields'][field_name] = self.escape_falsy_as_empty(Website.image_url(record, field_name))
                elif field_widget == 'image':
                    data['image_fields'][field_name] = self.escape_falsy_as_empty(record[field_name])
                elif field_widget == 'monetary':
                    FieldMonetary = self.env['ir.qweb.field.monetary']
                    model_currency = None
                    if field.type == 'monetary':
                        model_currency = record[record[field_name].currency_field]
                    elif 'currency_id' in model._fields:
                        model_currency = record['currency_id']
                    if model_currency:
                        website_currency = self._get_website_currency()
                        data['fields'][field_name] = FieldMonetary.value_to_html(
                            model_currency._convert(
                                record[field_name],
                                website_currency,
                                Website.get_current_website().company_id,
                                fields.Date.today()
                            ),
                            {'display_currency': website_currency}
                        )
                    else:
                        data['fields'][field_name] = self.escape_falsy_as_empty(record[field_name])
                elif ('ir.qweb.field.%s' % field_widget) in self.env:
                    data['fields'][field_name] = self.env[('ir.qweb.field.%s' % field_widget)].record_to_html(record, field_name, {})
                else:
                    data['fields'][field_name] = self.escape_falsy_as_empty(record[field_name])

            data['fields']['call_to_action_url'] = 'website_url' in record and record['website_url']
            values.append(data)
        return values