from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_tech_offer = fields.Boolean(default=True)
