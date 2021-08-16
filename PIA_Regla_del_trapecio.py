#UANL FCFM Licenciatura en Ciencias Computacionales
#Analisis numerico 
#Equipo 4: Regla del Trapecio 
##Brenda Sarahi Ortiz Solís      1817454
##Ian Mauricio Saucedo Aleman    1868954

import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
from matplotlib import pyplot 
from numpy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import math
matplotlib.use('TkAgg')

def calcularTrapecio(a,b,tramos,fx):    #Funcion que calcula el valor de la integral
                                        #mediante la regla del trapecio
    h = (b-a)/tramos
    xi = a
    suma = evaluar(xi, fx)
    for i in range(0,int(tramos)-1,1):
        xi = xi + h
        suma = suma + 2*evaluar(xi, fx)
    suma = suma + evaluar(b, fx)
    area = h*(suma/2)

    return area #Retornar valor calculado




def evaluar(x, expre):      #Funcion que evalua la funcion ingresada
    try:
        return eval(expre)
    except:
        return None

def noNegativos(x, expre):  #Funcion que verifica que la funcion ingresada no tenga
    for i in x:             #valores negativos en el intervalo dado
        if (evaluar(i, str(expre)) < 0):
            return -1
    else:
        return 1

def graficar(x, expr, inter, sup, n):   #Funcion que grafica la funcion ingresada
    if (noNegativos(x, expr) != -1): 
        pyplot.plot(x, [evaluar(i, str(expr)) for i in x])
        p_max = 0.0
        for j in inter:
            pyplot.plot(j, evaluar(j, expr), 'o-')
            pyplot.plot((j, j), (evaluar(j, expr), 0), '-')
            if (j + n <= sup):
                pyplot.plot((j, j + n), (evaluar(j, expr), evaluar(j + n, expr)), '-')
            if (evaluar(j, expr) > p_max):
                p_max = evaluar(j, expr)
        pyplot.axhline(0, color="black")
        pyplot.axvline(0, color="black")
        pyplot.xlabel('Eje x')
        pyplot.ylabel('Eje y')
        # Limitar los valores de los ejes.
        pyplot.xlim(0, float(sup + 2.0))
        try:
            pyplot.ylim(0.0, float(p_max + 2.0))
        except: 
            pyplot.ylim(0.0, 10.0)
        #pyplot.show()
        return pyplot.gcf()

def draw_figure(canvas, figure):        #Funcion auxiliar para pegar la grafica 
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def validarDatos (expr, inf, sup, interv):      #Funcion que verifica si los datos
    try:                                        #ingresados sean validos
        x = 1
        eval(expr)
    except: 
        return "La funcion ingresada es incorrecta"
    
    try: 
        float(inf)
    except:
        return "El limite inferior de la integral es incorrecto"

    try: 
        float(sup)
    except:
        return "El limite superior de la integral es incorrecto"
        
    try: 
        float(interv)
    except:
        return "El numero de intervalos es incorrecto"
    
    try: 
        x = arange(float(inf), float(sup), 0.1)
        expr = str(expr)
    except: 
        "Error"
    try: 
        if noNegativos(x, expr) == -1:
            return "La funcion ingresada tiene valores negativos en el intervalo dado"
    except: 
        return "Error"
    return 1

sg.ChangeLookAndFeel('GreenTan')
layout_principal = [[sg.Text('Regla del trapecio', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
                    [sg.Text("Ingrese la funcion a integrar: ", size = (15, 2)), sg.InputText()],
                    [sg.Button('Funcion de muestra 1'),
                     sg.Button('Funcion de muestra 2'),
                     sg.Button('Funcion de muestra 3')],
                    [sg.Text("Ingrese limite inferior de la integral: ", size = (15, 2)), sg.InputText()],
                    [sg.Text("Ingrese limite superior de la integral: ", size = (15, 2)), sg.InputText()],
                    [sg.Text("Ingrese el numero de intervalos: ", size = (15, 2)), sg.InputText()],
                    [sg.OK("Calcular"), sg.Cancel("Salir")]
                    ]

window_principal = sg.Window('Metodo del trapecio', layout_principal)
while True:             #Abre la ventana principal
    event_principal, values_principal = window_principal.read()
    if event_principal in (sg.WIN_CLOSED, 'Salir'):
        break
    if event_principal in ('Funcion de muestra 1', 'Funcion de muestra 2', 'Funcion de muestra 3'):
        if event_principal == 'Funcion de muestra 1':
            sg.popup("f(x) = x**2 + 4" + 
                 "\nLimite inferior = 2" + 
                 "\nLimite superior = 8" + 
                 "\nIntervalos = 4")
        elif event_principal == 'Funcion de muestra 2':
            sg.popup("f(x) = log(x) - 0.5" + 
                 "\nLimite inferior = 2" + 
                 "\nLimite superior = 8" +
                 "\nIntervalos = 4")
        elif event_principal == 'Funcion de muestra 3':
            sg.popup("f(x) = 1/x" + 
                 "\nLimite inferior = 2" + 
                 "\nLimite superior = 8" +
                 "\nIntervalos = 4")
    if event_principal == 'Calcular':
        if validarDatos(values_principal[0],values_principal[1],values_principal[2],values_principal[3]) == 1:
            valor_integral = calcularTrapecio(float(values_principal[1]),float(values_principal[2]),float(values_principal[3]),str(values_principal[0]))
            layout_res = [[sg.Text('Integral de la funcion')],
                          [sg.Canvas(key='-CANVAS-')],
                          [sg.Text('Valor de la integral por regla del trapecio: ' + str(valor_integral))],
                          [sg.Button('Ok')]]
            window_res = sg.Window('Integral de la funcion', layout_res, finalize=True, element_justification='center', font='Helvetica 18')
            x = arange(float(values_principal[1]), float(values_principal[2]), 0.1)     #Arreglo auxiliar para graficar
            n = (float(values_principal[2]) - float(values_principal[1]))/float(values_principal[3])    #Calcula delta x
            inter = arange(float(values_principal[1]), float(values_principal[2]) + n, n)   #Arreglo con los puntos de los intervalos
            fig = graficar(x, str(values_principal[0]), inter, float(values_principal[2]), n)
            fig_canvas_agg = draw_figure(window_res['-CANVAS-'].TKCanvas, fig)
            while True:     #Abre ventana de resultado 
                event_res, values_res = window_res.read()
                if event_res in (sg.WIN_CLOSED, 'Ok'):
                    break
            window_res.close()
        else:       #Manda un popup de por que no se pudo aceptar el problema
            sg.popup(validarDatos(values_principal[0], values_principal[1], values_principal[2], values_principal[3]))

window_principal.close()
