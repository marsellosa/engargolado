from datetime import date
import locale

locale.setlocale(locale.LC_TIME, '')

def fecha(anho, mes, dia):
    try:
        fecha = date(anho,mes,dia)
        nombreDia = fecha.strftime('%A').capitalize()
        noSemana = fecha.isocalendar()[1]
        return (fecha, nombreDia, noSemana)
    except:
        return (False, False, False)
    
def verificar_fecha(anho, mes, dia):
    if date(anho, mes, dia):
        print("fecha valida")
    else:
        print("fecha NO valida")

fecha, nombreDia, noSemana = fecha(2019, 10, 23)
if fecha:
    print(type(fecha))
    print(fecha, nombreDia, noSemana)
else:
    print("fecha NO valida")