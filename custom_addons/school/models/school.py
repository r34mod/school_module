from odoo import fields, models, api,
from odoo.exceptions import UserError


class Colegio(models.Model):
    _name = "centro.colegio"

    name = fields.Char(string="Nombre del Centro", copy=False, required=True)
    nombreJefe = fields.Char('Nombre Director', required = True)
    email = fields.Char(string="Email", copy=False)
    numeroTelefono = fields.Char("Telefono", copy=False)
    address = fields.Text(string="Address")
    tipo_centro = fields.Selection([
        ('publico','Colegio publico'),
        ('concertado', 'Colegio concertado'),
        ('privado', 'Colegio privado'),
        ('universidad_publica', 'Universidad publica'),
        ('universidad_privada', 'universidad privada')],
         string="Tipo de Centro",)
    documents = fields.Binary(string="Documents")
    document_name = fields.Char(string="File Name")
    school_image = fields.Image(string="Upload School Image", max_width=100,
                                max_height=100)
    school_description = fields.Html(string="Description", copy=False)
    auto_rank = fields.Integer(compute="_auto_rank_populate", string="Auto "
                                                                     "Rank",
                               store=True, help="This is auto populate data "
                                                "based on school type change.")

    class alumnoCentro(models.Model):
        _name = 'alumno.centro'
        nameAlumno = fields.Char(string="Nombre del Alumno", required = True)
        genero = fields.Selection([('hombre', 'Hombre'), ('mujer', 'Mujer')], required= True)
        grupoAlumno = fields.Char('Grupo Clase')
        telefonoAlumno = fields.Integer('Telefono', required = True)
        idAlumno = fields.One2Oone('centro.colegio','Id alumno', required = True)
        fechaNacimiento = fields.Date(string="Fecha Nacimiento", required=True)
        edadAlumno = fields.Char(string="Edad", compute="_getEdadAlumno")

    @api.depends("fechaNacimiento")
    def _getEdadAlumno(self):
        """Age Calculation"""

        today_date = datetime.date.today()
        fechaActual = datetime.date.today()
        for alum in self:
            if alum.fechaNacimiento:
                """
                Get only year.
                """
                # bdate = fields.Datetime.to_datetime(stud.bdate).date()
                # total_age = str(int((today_date - bdate).days / 365))
                # stud.student_age = total_age

                currentDate = datetime.date.today()

                deadlineDate = fields.Datetime.to_datetime(alum.fechaNacimiento).date()
                print(deadlineDate)
                daysLeft = currentDate - deadlineDate
                print(daysLeft)

                years = ((daysLeft.total_seconds()) / (365.242 * 24 * 3600))
                yearsInt = int(years)

                months = (years - yearsInt) * 12
                monthsInt = int(months)

                days = (months - monthsInt) * (365.242 / 12)
                daysInt = int(days)

                hours = (days - daysInt) * 24
                hoursInt = int(hours)

                minutes = (hours - hoursInt) * 60
                minutesInt = int(minutes)

                seconds = (minutes - minutesInt) * 60
                secondsInt = int(seconds)

                alum.edadAlumno = 'You are {0:d} years, {1:d}  months, {2:d}  days, {3:d}  hours, {4:d} \
                     minutes, {5:d} seconds old.'.format(yearsInt, monthsInt, daysInt, hoursInt, minutesInt, secondsInt)
            else:
                alum.edadAlumno = "Not Providated...."


    @api.model
    def name_create(self, name):
        rtn = self.create({"name":name, "email":"abc@gmail.com"})
        return rtn.name_get()[0]

    def name_get(self):
        student_list = []
        for school in self:
            name = school.name
            if school.school_type:
                name += " ({})".format(school.school_type)
            student_list.append((school.id, name))
        return student_list
