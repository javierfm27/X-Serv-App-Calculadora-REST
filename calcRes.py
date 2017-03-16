#!/usr/bin/python3
"""
    Aplicacion de una Calculadora REST
    Version con un unico recurso --> /operacion
    Para consultar el resultado--> /
    Para introducir la operacion--> operando1, operacion, operando2
    Javier Fernandez Morata
"""
import webapp
import socket

class calcRestApp (webapp.webApp):

    result = 0

    def html(self, bodyHtml):
        return "<!DOCTYPE html><html>" + bodyHtml + "</html>"

    def parse(self, request):
        try:
            request = request.decode('utf-8')
            recurso = request.split()[1][1:]
            recurso, operacion = recurso.split("/")
        except IndexError:
            return("","")
        except ValueError:
            recurso = request.split()[1][1:]
            return(recurso,"")
        return recurso, operacion

    def process(self, parsedRequest):
        recurso, operacion = parsedRequest
        print(parsedRequest," y el recurso es ", recurso)
        if recurso == "operacion" and operacion == "":
            bodyHtml = "El resultado es " + str(self.result) + "<br>" \
                    + "Recuerde Instrucciones de Uso<br>" \
                    + "================================<br>" \
                    + "Introducir /operacion/operando1,operacion,operando2<br>"
            httpCode = "200 Ok"
        elif recurso == "operacion":
            if operacion != "":
                num1, op, num2 = operacion.split(",")
                if op == "+":
                    self.result = int(num1) + int(num2)
                elif op == "-":
                    self.result = int(num1) - int(num2)
                elif op == "*":
                    self.result = int(num1) * int(num2)
                elif op == "/":
                    self.result = int(num1) / int(num2)
                bodyHtml = "Operacion Recibida " + num1 + " " + op + " " + num2
                httpCode = "200 Ok"
            else:
                bodyHtml = "Error 400! Debe introducir los datos de la operacion"
                httpCode = "400 Bad Request"
        elif recurso == "":
            bodyHtml = "Para usar la calculadora introduce <br>" \
                    + "-->'/operacion/numero1,operacion,numero2'<br>" \
                    + "--> Para consultar el resultado '/operacion'"
            httpCode = "200 OK"
        else:
            bodyHtml = "Error 400! El recurso que solicita no existe"
            httpCode = "400 Bad Request"
        htmlAnswer = self.html(bodyHtml)
        return(httpCode, htmlAnswer)
if __name__ == "__main__":
    try:
        testCalcApp = calcRestApp(socket.gethostname(), 1232)
    except KeyboardInterrupt:
        print("Closing Socket")
