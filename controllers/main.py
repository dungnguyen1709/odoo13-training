from odoo import http
from odoo.http import request


class Hospital(http.Controller):
    @http.route('/hospital/patient/', website=True, auth='public')
    def hospital_patient(self, **kw):
        # return "BnkSolution"
        return request.render("om_hospital.patients_page", {})
