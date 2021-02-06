from odoo import models, fields, api
from odoo.exceptions import UserError
import re
from datetime import date



class HmsPatient(models.Model):
    _name = "hms.patient"

    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char()
    birth_date = fields.Date()
    age = fields.Integer()
    age_computed = fields.Integer(compute="calc_age")
    history = fields.Html()
    cr_ratio = fields.Float()
    state = fields.Selection([
        ('Undetermined', 'Undetermined'),
        ('Serious', 'Serious'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    ], required=True, default='Undetermined')
    blood_type = fields.Selection(
        [('O+', 'O+'),
         ('O-', 'O-'),
         ('A+', 'A+'),
         ('A-', 'A-'),
         ('B+', 'B+'),
         ('B-', 'B-'),
         ('AB+', 'AB+'),
         ('AB-', 'AB-')]
    )
    pcr = fields.Boolean('PCR')
    address = fields.Text()
    image = fields.Image()
    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_id = fields.Many2many('hms.doctor')
    log_history_ids = fields.One2many('log.history', 'patient_id')

    @api.onchange("age")
    def _age_onchange(self):
        if self.age < 30:
            self.pcr = True
        else:
            self.pcr = False
            return
        return {
            'warning': {
                'title': 'Warning',
                'message': 'the PCR Value is checked'
            }
        }

    @api.depends('birth_date')
    def calc_age(self):
        for rcd in self:
            today = date.today()
            rcd.age_computed = today.year - rcd.birth_date.year - ((today.month, today.day) < (rcd.birth_date.month, rcd.birth_date.day))

    def change_state(self):
        old_state = self.state
        if self.state == 'Undetermined':
            self.state = 'Serious'
        elif self.state == 'Serious':
            self.state = 'Good'
        elif self.state == 'Good':
            self.state = 'Fair'
        self.env['log.history'].create({
            "description": f'patient state change from {old_state} to {self.state}',
            "patient_id": self.id})

    @api.model
    def create(self, vals):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not re.match(pattern, vals['email']):
            raise UserError("Enter Valid Email Address")
        return super().create(vals)

    _sql_constraints = [
        ('Unique Email', 'UNIQUE(email)', 'Email Must be unique')
    ]

    # def validation_email(email):
    #     pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    #     if not re.match(pattern, email):
    #         raise UserError("Enter Valid Email Address")
