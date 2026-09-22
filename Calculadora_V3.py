import tkinter as tk

historial = ["historial de operaciones"]
operadores = ["+", "-", "x", "÷"]
memoria = 0.0

#Funciones calculadora 

def ultimo_numero_o_parte(texto):
    for op in operadores:
        if op in texto:
            texto = texto.split(op)[-1]
    return texto


def agregar(valor):
    texto = pantalla.get()

    if texto == "0" and valor not in ["+", "-", "x", "÷", "."]:
        pantalla.delete(0, tk.END)
        texto = ""

    if valor in operadores:
        if not texto or texto[-1] in operadores:
            return

    ultimo = ultimo_numero_o_parte(texto)

    if valor == ".":
        if "." in ultimo:
            return

    if valor.isdigit() and "." in ultimo:
        decimales = ultimo.split(".")[1]
        if len(decimales) >= 2:
            return

    pantalla.insert(tk.END, valor)

def borrar_uno():
    texto = pantalla.get()

    if len(texto) <= 1:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "0")
    else:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, texto[:-1])

def limpiar():
    pantalla.delete(0, tk.END)
    pantalla.insert(0, "0")

def cambiar_signo():
    texto = pantalla.get()

    if not texto:
        return

    try:
        if texto.startswith("-"):
            pantalla.delete(0, tk.END)
            pantalla.insert(0, texto[1:])
        else:
            pantalla.delete(0, tk.END)
            pantalla.insert(0, "-" + texto)

    except:
        pass


def porcentaje():
    try:
        valor = float(pantalla.get())
        resultado = round(valor / 100, 2)

        pantalla.delete(0, tk.END)
        pantalla.insert(0, resultado)

    except:
        pass


def calcular():
    try:
        expresion_original = pantalla.get()

        expresion = expresion_original.replace("x", "*")
        expresion = expresion.replace("÷", "/")

        resultado = eval(expresion)

        if isinstance(resultado, float):
            resultado = round(resultado, 2)

        historial.append(
            f"{expresion_original} = {resultado}"
        )

        actualizar_historial()

        pantalla.delete(0, tk.END)
        pantalla.insert(0, resultado)

    except ZeroDivisionError:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "No dividir entre 0")

    except:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "Error")


def actualizar_historial():

    historial_texto.config(state="normal")
    historial_texto.delete("1.0", tk.END)

    for operacion in historial[-5:]:
        historial_texto.insert(
            tk.END,
            operacion + "\n"
        )

    historial_texto.config(state="disabled")


def valor_actual():
    texto = pantalla.get().strip()
    if texto in ["", "Error", "No dividir entre 0"]:
        return None
    try:
        return float(texto)
    except ValueError:
        return None


def mostrar_valor(valor):
    if valor is None:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "0")
        return
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    pantalla.delete(0, tk.END)
    pantalla.insert(0, str(valor))


def memoria_recall():
    mostrar_valor(memoria)


def memoria_clear():
    global memoria
    memoria = 0.0
    mostrar_valor(memoria)


def memoria_sumar():
    global memoria
    valor = valor_actual()
    if valor is not None:
        memoria += valor
        mostrar_valor(memoria)


def memoria_restar():
    global memoria
    valor = valor_actual()
    if valor is not None:
        memoria -= valor
        mostrar_valor(memoria)


#Botones cuadrados

def crear_boton_redondo(
    parent,
    x,
    y,
    radio,
    color,
    texto,
    comando,
    color_texto="white",
    fuente=("Arial", 16, "bold")
):

    canvas = tk.Canvas(
        parent,
        width=radio * 2,
        height=radio * 2,
        bg="#111111",
        highlightthickness=0
    )

    canvas.place(x=x, y=y)

    cuadro = canvas.create_oval(
        2,
        2,
        radio * 2 - 2,
        radio * 2 - 2,
        fill=color,
        outline=color
    )

    texto_canvas = canvas.create_text(
        radio,
        radio,
        text=texto,
        fill=color_texto,
        font=fuente
    )

    canvas.tag_bind(
        cuadro,
        "<Button-1>",
        lambda e: comando()
    )

    canvas.tag_bind(
        texto_canvas,
        "<Button-1>",
        lambda e: comando()
    )


#Ventana principal

ventana = tk.Tk()

ventana.title("Calculadora")
ventana.geometry("380x720")
ventana.configure(bg="#111111")
ventana.resizable(False, False)

#Guardar historial 

historial_texto = tk.Text(
    ventana,
    height=6,
    bg="#111111",
    fg="#888888",
    bd=0,
    font=("Arial", 12)
)

historial_texto.pack(
    fill="x",
    padx=15,
    pady=(10, 0)
)

historial_texto.config(state="disabled")

#Pantalla

marco_pantalla = tk.Frame(
    ventana,
    bg="#111111"
)

marco_pantalla.pack(
    fill="x",
    padx=20,
    pady=15
)

pantalla = tk.Entry(
    marco_pantalla,
    font=("Arial", 32, "bold"),
    bg="#111111",
    fg="white",
    bd=0,
    justify="right",
    insertbackground="white"
)

pantalla.grid(row=0, column=0, sticky="ew", padx=(0, 10))
pantalla.insert(0, "0")

btn_borrar = tk.Button(
    marco_pantalla,
    text="⌫",
    command=borrar_uno,
    bg="#262626",
    fg="white",
    bd=0,
    font=("Arial", 14, "bold"),
    width=3,
    relief="flat"
)

btn_borrar.grid(row=0, column=1)
marco_pantalla.grid_columnconfigure(0, weight=1)

radio = 35

NORMAL = "#262626"
OPERADOR = "#D6D6D6"
ESPECIAL = "#404040"

#Memoria
memoria_frame = tk.Frame(
    ventana,
    bg="#111111"
)
memoria_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 10)
)

for i, (texto, comando) in enumerate([
    ("MR", memoria_recall),
    ("MC", memoria_clear),
    ("M+", memoria_sumar),
    ("M-", memoria_restar)
]):
    btn_memoria = tk.Button(
        memoria_frame,
        text=texto,
        command=comando,
        bg=ESPECIAL,
        fg="white",
        bd=0,
        font=("Arial", 11, "bold"),
        width=5,
        height=1,
        relief="flat"
    )
    btn_memoria.grid(row=0, column=i, padx=5, pady=4, sticky="ew")

memoria_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

#Posición botones 

marco = tk.Frame(
    ventana,
    bg="#111111",
    width=380,
    height=500
)

marco.pack()

# FILA 1

crear_boton_redondo(
    marco, 20, 20, radio,
    ESPECIAL,
    "AC",
    limpiar
)

crear_boton_redondo(
    marco, 105, 20, radio,
    ESPECIAL,
    "+/-",
    cambiar_signo
)

crear_boton_redondo(
    marco, 190, 20, radio,
    ESPECIAL,
    "%",
    porcentaje
)

crear_boton_redondo(
    marco, 275, 20, radio,
    OPERADOR,
    "÷",
    lambda: agregar("÷"),
    "black"
)

# FILA 2

crear_boton_redondo(
    marco, 20, 105, radio,
    NORMAL,
    "7",
    lambda: agregar("7")
)

crear_boton_redondo(
    marco, 105, 105, radio,
    NORMAL,
    "8",
    lambda: agregar("8")
)

crear_boton_redondo(
    marco, 190, 105, radio,
    NORMAL,
    "9",
    lambda: agregar("9")
)

crear_boton_redondo(
    marco, 275, 105, radio,
    OPERADOR,
    "x",
    lambda: agregar("x"),
    "black"
)

# FILA 3

crear_boton_redondo(
    marco, 20, 190, radio,
    NORMAL,
    "4",
    lambda: agregar("4")
)

crear_boton_redondo(
    marco, 105, 190, radio,
    NORMAL,
    "5",
    lambda: agregar("5")
)

crear_boton_redondo(
    marco, 190, 190, radio,
    NORMAL,
    "6",
    lambda: agregar("6")
)

crear_boton_redondo(
    marco, 275, 190, radio,
    OPERADOR,
    "-",
    lambda: agregar("-"),
    "black"
)

# FILA 4

crear_boton_redondo(
    marco, 20, 275, radio,
    NORMAL,
    "1",
    lambda: agregar("1")
)

crear_boton_redondo(
    marco, 105, 275, radio,
    NORMAL,
    "2",
    lambda: agregar("2")
)

crear_boton_redondo(
    marco, 190, 275, radio,
    NORMAL,
    "3",
    lambda: agregar("3")
)

crear_boton_redondo(
    marco, 275, 275, radio,
    OPERADOR,
    "+",
    lambda: agregar("+"),
    "black"
)

# FILA FINAL

canvas0 = tk.Canvas(
    marco,
    width=radio * 2,
    height=radio * 2,
    bg="#111111",
    highlightthickness=0
)
canvas0.place(x=105, y=360)

rect0 = canvas0.create_oval(
    2, 2,
    radio * 2 - 2,
    radio * 2 - 2,
    fill=NORMAL,
    outline=NORMAL
)

texto0 = canvas0.create_text(
    radio,
    radio,
    text="0",
    fill="white",
    font=("Arial", 16, "bold")
)

canvas0.tag_bind(rect0, "<Button-1>", lambda e: agregar("0"))
canvas0.tag_bind(texto0, "<Button-1>", lambda e: agregar("0"))

crear_boton_redondo(
    marco, 190, 360, radio,
    NORMAL,
    ".",
    lambda: agregar(".")
)

crear_boton_redondo(
    marco, 275, 360, radio,
    OPERADOR,
    "=",
    calcular,
    "black"
)

ventana.mainloop()