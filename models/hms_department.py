from odoo import fields, models


class HmsDepartment(models.Model):
    _name = 'hms.department'
    name = fields.Char()
    capacity = fields.Integer()
    is_open = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_id')

