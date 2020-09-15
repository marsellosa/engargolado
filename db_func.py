
import DB_Class


class reporte():
    # def __init__(self, parent=None):
    #     super(reporte, self).__init__(parent)
    #     self.var_iniciales()

    def var_iniciales(self):
        global BD
        # importamos el modulo de la base de datos
        BD = DB_Class.dataBase()
        # creamos la conexion a la base de datos
        BD.createCon()

    def consumo_personal(self, IdSocio):
        pass

    def operadores_club(self):
        self.var_iniciales()
        query = """SELECT id, Nombre, Apellido
                    FROM registro_socios
                    WHERE IsOperador=1"""
        return BD.interAct(query)

    def divisor_por_descuento(self): pass
    # que saque el nivel de descuento en la bd y devuelva el divisor
    # para calcular el sobre rojo y ganancia correspondiente

    # tiene licencia y nivel de descuento

    def actividad_diaria_personal(self, numMes, idOperador):
        self.var_iniciales()
        query = """SELECT
                     invitaciones,
                     entraron,
                     consumos_nuevos,
                     referidos,
                     consumos_totales,
                     sobre_rojo,
                     sobre_verde,
                     sobre_rojo_real,
                     sobre_verde_real
                 FROM reporte_mensual WHERE id_operador=%s AND fecha_calendario='%s' ORDER BY fecha_calendario;""" % (idOperador, numMes)
        # print query
        return BD.interAct(query)

    def actividad_diaria_club(self, fecha_calendario):
        self.var_iniciales()
        query = """SELECT
                     sum(invitaciones),
                     sum(entraron),
                     sum(consumos_nuevos),
                     sum(referidos),
                     sum(consumos_totales),
                     sum(sobre_rojo),
                     sum(sobre_verde),
                     sum(sobre_rojo_real),
                     sum(sobre_verde_real)
                 FROM reporte_mensual WHERE fecha_calendario='%s' ORDER BY fecha_calendario;""" % (fecha_calendario)
        # print query
        return BD.interAct(query)

    def reporte_mensual(self, xMes, condicion):
        # print('idOperador: ', idOperador)
        self.var_iniciales()
        query = """
                    SELECT
                        sum(consumos_totales),
                        sum(sobre_rojo),
                        sum(sobre_verde),
                        sum(consumido),
                        sum(insumos),
                        sum(descuento),
                        sum(mayoreo)
                    FROM
                        reporte_mensual
                    WHERE
                        fecha_calendario
                    LIKE
                        '%s%%'
                    %s                        
                """ % (xMes, condicion)
        return BD.interAct(query)
        # print(query)

    def sobre_verde_real(self, porGanancia, fecha_calendario, operador):
        self.var_iniciales()
        query = """
                SELECT
                    ifnull(sum()*%s,0) as SVerde
                FROM
                    operador
                WHERE
                    fecha_calendario='%s' 
                AND operador=%s
                AND id_socio<>%s""" % (porGanancia, fecha_calendario, operador, operador)
        return BD.interAct(query)

    def update_tabla_reporte(self, divisor, fecha_calendario, nombreDia, operador, vista):
        self.var_iniciales()
        query = """
                SELECT
                    ifnull(sum(efectivo),0) as ventas_totales,
                    ifnull(sum(efectivo)/%s,0) as SVerde,
                    ifnull(count(),0) as consumos_totales,
                    ifnull(sum(promocion),0) as promocion
                FROM
                    %s
                WHERE
                    fecha_calendario='%s' AND operador=%s""" % (divisor, vista, fecha_calendario, operador)
        for item in BD.interAct(query):
            ventas_totales = item[0]
            sobre_verde = item[1]
            sobre_rojo = ventas_totales - sobre_verde
            consumos_totales = item[2]
            insumos = consumos_totales
            rojo_real = sobre_rojo - insumos
            promocion = item[3]
            verde_real = sobre_verde - promocion

        nuevos = """SELECT
                        ifnull(count(),0)
                    FROM
                        %s
                    WHERE
                        fecha_calendario='%s'
                    AND
                        status='N'
                    AND
                        operador=%s""" % (vista, fecha_calendario, operador)

        referidos = """SELECT
                            ifnull(count(),0)
                        FROM
                            %s
                        WHERE
                            fecha_calendario='%s'
                        AND
                            status='R'
                        AND
                            operador=%s""" % (vista, fecha_calendario, operador)

        consumo_personal = """SELECT
                                    ifnull((sum(efectivo) - (sum(efectivo)/%s)), '0')
                                FROM
                                    %s
                                WHERE
                                    fecha_calendario='%s'
                                AND
                                    id_socio=%s""" % (divisor, vista, fecha_calendario, operador)

        query = """
            UPDATE
                reporte_mensual
            SET
                consumos_nuevos=(%s),
                referidos=(%s),
                consumo_personal=(%s),
                consumos_totales=%s,
                ventas_totales=%s,
                sobre_rojo=%s,
                promocion=%s,
                sobre_verde=%s,
                insumos=%s,
                sobre_rojo_real=%s,
                sobre_verde_real=%s
            WHERE
                fecha_calendario='%s' AND id_operador=%s""" \
            % (nuevos, referidos, consumo_personal, consumos_totales, ventas_totales, sobre_rojo, promocion, sobre_verde, insumos, rojo_real, verde_real, fecha_calendario, operador)
        BD.interAct(query)

        query = """
            INSERT INTO
                reporte_mensual (
                fecha_calendario,
                Semana,
                consumos_nuevos,
                Referidos,
                consumos_totales,
                consumo_personal,
                sobre_verde,
                ventas_totales,
                sobre_rojo,
                insumos,
                sobre_verde_real,
                sobre_rojo_real,
                Promocion,
                id_operador)
            SELECT
                '%s',
                '%s',
                (%s),
                (%s),
                %s,
                (%s),
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            WHERE NOT EXISTS
                (SELECT changes() AS change FROM reporte_mensual WHERE change <> 0)""" \
            % (fecha_calendario,
               nombreDia,
               nuevos,
               referidos,
               consumos_totales,
               consumo_personal,
               sobre_verde,
               ventas_totales,
               sobre_rojo,
               insumos,
               verde_real,
               rojo_real,
               promocion,
               operador)
        BD.interAct(query)

    def llenar_tbl_reporte_semanal(self, fechaDesde, fechaHasta, noSem):
        # pass
        query = """
                INSERT INTO
                    reporte_semanal (fechaDesde, fechaHasta, noSem)
                VALUES
                    ('%s', '%s', '%s')""" % (fechaDesde, fechaHasta, noSem)
        BD.interAct(query)
        # print(query)

    def hola_mundo(self):
        saludo = 'hola!'
        return saludo
