# -*- coding: utf-8 -*-
import datetime
from lxml import etree
from odoo import models, fields, api, _
from odoo.exceptions import  UserError

class school_student(models.Model):
    _name = 'school.student'
    _description = 'school_student.school_student'

    name = fields.Char(default="Sunny Leaone")
    school_id = fields.Many2one("school.profile", string="School Name")
    hobby_list = fields.Many2many("hobby", "school_hobby_rel","student_id",
                                  "hobby_id", string="Hobby List",
                                  )
    is_virtual_school = fields.Boolean(related="school_id.is_virtual_class",
                                       string="Is Virtual Class", store=True)
    school_address = fields.Text(related="school_id.address",
                                 string="Address",
                                 help="This is school address.")
    currency_id = fields.Many2one("res.currency", string="Currency")
    student_fees = fields.Monetary(string="Student Fees",
                                   index=True)
    total_fees = fields.Float(string="Total Fees", default=200)
    ref_id = fields.Reference(selection=[('school.profile', 'School'),
                               ('account.move', 'Invoice')] ,
                              string="Reference Field",
                              default="school.profile,1")
    active = fields.Boolean(string="Active", default=True)
    bdate = fields.Date(string="Date Of Birth", required=True)
    student_age = fields.Char(string="Total Age", compute="_get_age_from_student")

    def custom_method(self):
        try:
            self.ensure_one()
            print(self.name)
            print(self.bdate)
            print(self.school_id.name)
        except ValueError:
            pass

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        res = super(school_student, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        if view_type == "form":
            doc = etree.XML(res['arch'])
            name_field = doc.xpath("//field[@name='name']")
            if name_field:
                # Added one label in form view.
                name_field[0].addnext(etree.Element('label', {'string':'Hello this is custom label from fields_view_get method'}))

            #override attribute
            address_field = doc.xpath("//field[@name='school_address']")
            if address_field:
                address_field[0].set("string", "Hello This is School Address.")
                address_field[0].set("nolabel", "0")

            res['arch'] = etree.tostring(doc, encoding='unicode')

        if view_type == 'tree':
            doc = etree.XML(res['arch'])
            school_field = doc.xpath("//field[@name='school_id']")
            if school_field:
                # Added one field in tree view.
                school_field[0].addnext(etree.Element('field', {'string':'Total Fees',
                                                                'name': 'total_fees'}))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res


    @api.model
    def default_get(self, field_list=[]):
        print("field_list ",field_list)
        rtn = super(school_student, self).default_get(field_list)
        print("Befor Edit ",rtn)
        rtn['student_fees'] = 4000
        print("return statement ",rtn)
        return rtn

    @api.depends("bdate")
    def _get_age_from_student(self):
        """Age Calculation"""
        today_date = datetime.date.today()
        for stud in self:
            if stud.bdate:
                """
                Get only year.
                """
                # bdate = fields.Datetime.to_datetime(stud.bdate).date()
                # total_age = str(int((today_date - bdate).days / 365))
                # stud.student_age = total_age

                """
                Origin of below source code
                https://gist.github.com/shahri23/1804a3acb7ffb58a1ec8f1eda304af1a
                """
                currentDate = datetime.date.today()

                deadlineDate= fields.Datetime.to_datetime(stud.bdate).date()
                print (deadlineDate)
                daysLeft = currentDate - deadlineDate
                print(daysLeft)

                years = ((daysLeft.total_seconds())/(365.242*24*3600))
                yearsInt=int(years)

                months=(years-yearsInt)*12
                monthsInt=int(months)

                days=(months-monthsInt)*(365.242/12)
                daysInt=int(days)

                hours = (days-daysInt)*24
                hoursInt=int(hours)

                minutes = (hours-hoursInt)*60
                minutesInt=int(minutes)

                seconds = (minutes-minutesInt)*60
                secondsInt =int(seconds)

                stud.student_age = 'You are {0:d} years, {1:d}  months, {2:d}  days, {3:d}  hours, {4:d} \
                 minutes, {5:d} seconds old.'.format(yearsInt,monthsInt,daysInt,hoursInt,minutesInt,secondsInt)
            else:
                stud.student_age = "Not Providated...."



    # @api.model_create_multi
    # def create(self, values):
    #     rtn = super(school_student, self).create(values)
    #     return rtn

    # @api.model
    # def create(self, values):
    #     rtn = super(school_student, self).create(values)
    #     return rtn

    #No Decorator
    # def write(self, values):
    #     rtn = super(school_student, self).write(values)
    #     return rtn

    # @api.returns('self', lambda value: value.id)
    # def copy(self, default = {}):
    #     #default['active'] = False
    #     default['name'] = "copy ("+self.name+")"
    #     rtn = super(school_student, self).copy(default=default)
    #     rtn.total_fees = 500
    #     return rtn

    # def unlink(self):
    #     print("self statement ",self)
    #     # for stud in self:
    #     #     if stud.total_fees > 0:
    #     #         raise UserError(_("You can't delete this %s student profile"%stud.name))
    #     rtn = super(school_student, self).unlink()
    #     print("Return statement ",rtn)
    #     return rtn

class SchoolProfile(models.Model):
    _inherit = "school.profile"

    school_list = fields.One2many("school.student", "school_id",
                                  string="School List",

                                  )

    # @api.model
    # def create(self, vals):
    #     rtn = super(SchoolProfile, self).create(vals)
    #     if not rtn.school_list:
    #         raise UserError(_("Student list is empty!"))
    #     return rtn


class Hobbies(models.Model):
    _name = "hobby"

    name = fields.Char("Hobby")