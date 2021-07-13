# -*- coding:utf-8 -*-
from odoo import api, fields, models


class MonHocBaseReport(models.TransientModel):
    _name = 'mon.hoc.base.report'
    _description = u'Báo cáo môn học base'

    monn_hoc_id = fields.Many2one('nhom.mon.hoc', 'Môn học')

    @api.multi
    def show_report(self):
        data = {
            'form': {
                'mon_hoc_id': self.monn_hoc_id.id,
                'ten_mon_hoc': self.monn_hoc_id.mon_hoc_id.ten_mh,
                'nhom_mh': self.monn_hoc_id.nhom_mh,
                'name': self.monn_hoc_id.mon_hoc_id.ten_mh + ' - ' + self.monn_hoc_id.nhom_mh,
            }
        }
        return self.env.ref('quan_ly_sinh_vien.report_mon_hoc_wizard_qweb').report_action(self, data=data)