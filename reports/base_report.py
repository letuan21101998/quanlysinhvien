# -*- coding:utf-8 -*-
from odoo import api, fields, models


class BaseReport(models.TransientModel):
    _name = 'base.report'
    _description = u'Báo cáo base'

    sv_id = fields.Many2one('ho.so.sv',"Mã sinh viên")

    @api.multi
    def show_report(self):
        data = {
            'form': {
                'sv_id': self.sv_id.id,
            }
        }
        return self.env.ref('quan_ly_sinh_vien.report_bang_diem_wizard_qweb').report_action(self, data=data)