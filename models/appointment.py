from odoo import models, fields, api, _
import pytz


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "appointment_date desc"

    def test_recordset(self):
        for rec in self:
            print("odoo ORM")
            partners = self.env['res.partner'].search([])
            print('partners...', partners.mapped('email'))
            print('sort partners...', partners.sorted(lambda o: o.write_date, reverse=True))
            print('Filtered partners...', partners.filtered(lambda o: not o.customer))

    def delete_lines(self):
        for rec in self:
            print("Time in UTC", rec.appointment_datetime)
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            date_today = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            rec.appointment_lines = [(5, 0, 0)]

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed',
                    'type': 'rainbow_man'
                }
            }

    def action_done(self):
        for rec in self:
            rec.doctor_id.user_id.notofy_success(message="My success message")

    @api.model
    def create(self, vals):
        print(_('New'))
        print(type(_('New')))
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')

        result = super(HospitalAppointment, self).create(vals)
        return result

    def write(self, vals):
        res = super(HospitalAppointment, self).write()
        return res

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        print("test......")
        res['patient_id'] = 1
        res['notes'] = 'please like the video'
        return res

    # def _get_default_note(self):
    #     return 1

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    doctor_ids = fields.Many2many('hospital.doctor', 'hospital_patient_rel', 'appointment_id', 'doctor_id_rec', string='Doctors')
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note")
    doctor_note = fields.Text(string="Note", track_visibility='onchange')
    pharmacy_note = fields.Text(string="Note", track_visibility='always')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    appointment_date = fields.Date(string='Date')
    appointment_datetime = fields.Datetime(string='Date Time')
    partner_id = fields.Many2one('res.partner', string='Customer')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    amount = fields.Float(string="Total Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, default='draft')


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='product')
    product_qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')
    sequence = fields.Integer(string='Sequence')
