# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class HoSoSV(models.Model):
    _name = 'ho.so.sv'
    _inherit = ['mail.thread']
    _description = 'Hồ sơ sinh viên'
    _order = 'ten_sv'
    _rec_name = 'ma_sv'

    ma_sv = fields.Char('Mã sinh viên', required=True)
    ho_sv = fields.Char('Họ sinh viên', required=True)
    ten_sv = fields.Char('Tên sinh viên', required=True)
    ma_kh = fields.Char(related='khoa_hoc_id.ma_kh', string='Mã khóa học', store=False)
    ngay_sinh = fields.Date('Ngày sinh', required=True)
    gioi_tinh = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')], string='Giới tính')
    dan_toc = fields.Char('Dân tộc', required=True)
    ton_giao = fields.Char('Tôn giáo', required=True)
    que_quan = fields.Char('Quê quán', required=True)
    dia_chi = fields.Char('Địa chỉ', required=True)
    so_dt = fields.Char('Số điện thoại', required=True)
    ten_bo = fields.Char('Tên bố', required=True)
    nghe_bo = fields.Char('Nghề bố', required=False)
    ten_me = fields.Char('Tên  mẹ', required=True)
    nghe_me = fields.Char('Nghề mẹ', required=False)
    ngay_nhap_hoc = fields.Date('Ngày nhập học', required=False)
    diem_dau_vao = fields.Float('Điểm đầu vào', default=0, required=True)
    hinh_thuc_dao_tao = fields.Char('Hình thức đào tạo', required=True, default='Chính quy')
    ngay_tot_nghiep = fields.Date('Ngày tốt nghiệp')
    xep_loai_tn = fields.Char('Xếp loại tốt nghiệp')

    ma_khoa_id = fields.Many2one('khoa.khoa', 'Khoa', required=True)
    lop_id = fields.Many2one('lop.lop', 'Lớp', required=True)
    khoa_hoc_id = fields.Many2one('khoa.hoc', 'Khóa học', required=True)
    ki_luat_ids = fields.One2many('ki.luat', 'sv_id', 'Danh sách kỷ luật')
    khen_thuong_ids = fields.One2many('khen.thuong', 'sv_id', 'Danh sách khen thưởng')
    bang_diem_ids = fields.One2many('bang.diem', 'sv_id', 'Danh sách bảng điểm')

    _sql_constraints = [
        ('ma_sv_uniq', 'unique(ma_sv)', "Mã sinh viên đã tổn tại!")
    ]

    # def name_get(self):
    #     res = []
    #     for order in self:
    #         name = '%s - %s' % (order.ma_sv, order.ten_sv)
    #         res.append((order.id, name))
    #     return res

    def get_diem_tk(self, sv_id):
        cr = self.env.cr
        cr.execute("""
        select sv_id, diem_tk from (
          SELECT sv_id, nhom_mon_hoc_id,diem_tk,
          ROW_NUMBER() OVER(ORDER BY diem_tk asc) AS Row
          FROM bang_diem
        ) dups
        where 
        dups.Row > 1 and sv_id = %s """, (sv_id,))
        _list = cr.dictfetchall()

        xep_loai = ''
        diem = 0
        i = 0
        for rec in _list:
            i += 1
            diem = diem + rec.get('diem_tk')
        diem_4 = (diem / i) / 10 * 4
        if diem_4 <= 2.49 and diem_4 >= 2.0:
            xep_loai = str('Trung bình')
        elif diem_4 <= 3.19 and diem_4 >= 2.5:
            xep_loai = str('Khá')
        elif  diem_4 <= 3.59 and diem_4 >= 3.20:
            xep_loai = str('Giỏi')
        elif diem_4 >= 3.6:
            xep_loai = str('Xuất sắc')
        else:
            xep_loai = str('Chưa đủ điều kiện tốt nghiệp')
        self.write({
            'xep_loai_tn': xep_loai
        })

    @api.model
    def create(self, vals):
        ho = vals.get('ho_sv')
        ten = vals.get('ten_sv')
        ten_me = vals.get('ten_me')
        ten_bo = vals.get('ten_bo')
        vals['ho_sv'] = ho.title()
        vals['ten_sv'] = ten.title()
        vals['ten_bo'] = ten_bo.title()
        vals['ten_me'] = ten_me.title()
        return super(HoSoSV, self).create(vals)

    @api.multi
    @api.constrains('so_dt')
    def kiem_tra_so_dt(self):
        for rec in self:
            if len(rec.so_dt) < 10:
                raise exceptions.ValidationError('Số điện thoại chưa đúng')
