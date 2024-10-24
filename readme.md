# Teclado Virtual con Flask y Tkinter

Este proyecto es un **teclado virtual** interactivo creado con **Tkinter** para la interfaz gráfica y **Flask** para la exposición de una API REST. El teclado permite acciones como **mostrar**, **ocultar**, **cambiar de tamaño** y **ajustar la transparencia** mediante llamadas a la API.

⚠️ **El teclado del sistema operativo debe estar en español para poder mapear correctamente la ñ** ⚠️

## Características

- Teclado interactivo con teclas alfanuméricas y de control (Shift, Espacio, Enter, Backspace).
- API REST para controlar el comportamiento del teclado.
- Soporte para simular la presión de teclas mediante el módulo `keyboard`.
- Interfaz gráfica creada con Tkinter.
- Funciona en segundo plano mientras acepta llamadas API.

## Requisitos

- Python 3.x
- Dependencias:
  - **Flask**: Para la creación del servidor API.
  - **Tkinter**: Para la interfaz gráfica del teclado.
  - **keyboard** (opcional): Para simular la presión de teclas.

### Instalación de dependencias (solo para desarrollo)

Ejecuta el siguiente comando para instalar las dependencias requeridas:

```bash
pip install flask keyboard
```
## Ejecución

### Ejecución del proyecto en Python

Para ejecutar la aplicación directamente en Python:

```bash
python mini_vkeyboard.py
```

### Generar un archivo .exe (Build post desarrollo)

Para crear un archivo ejecutable (.exe) y poder ejecutar la aplicación sin Python instalado, sigue estos pasos:

1. Instala PyInstaller:

```bash
pip install pyinstaller
```

2. Compila el script en un ejecutable:

```bash
pyinstaller --onefile mini_vkeyboard.py
```


### Ejecucion:

```bash
./dist/mini_vkeyboard.exe
```

## API

La aplicación expone una serie de endpoints para controlar el teclado virtual.

⚠️ **Esta API esta escuchando los llamados en 127.0.0.1:5000**

`POST /keyboard`

Este endpoint permite controlar acciones del teclado virtual.

Parámetros:


* "action" (string): La acción que deseas realizar. Puede ser uno de los siguientes valores:
    * "show": Muestra el teclado.
    "hide": Oculta el teclado.
    * "resize": Cambia el tamaño del teclado. Debes proporcionar también width y height.
    * "set_transparency": Cambia la transparencia del teclado. Debes proporcionar también value (entre 0 y 1).
    * "quit": Cierra la aplicación.


### Ejemplos de solicitud:

Mostrar el teclado:

```json
{
  "action": "show"
}
```

Cambiar el tamaño del teclado:

```json
{
  "action": "resize",
  "width": 800,
  "height": 300
}
```
Cambiar la transparencia del teclado:

```json
{
  "action": "set_transparency",
  "value": 0.8
}
```


`POST /keyboard/presskey`

Este endpoint simula la presión de teclas.

Parámetros:

* content (string): La secuencia de teclas que deseas presionar.

Ejemplo de solicitud:

Simular la presión de teclas:

```json
{
  "content": "hello"
}
```

# Personalización

Puedes modificar el código fuente para ajustar las funcionalidades del teclado, los colores, o agregar nuevas acciones en la API. Consulta el archivo principal mini_vkeyboard.py para obtener más detalles sobre cómo están estructuradas las clases y los métodos.

# Licencia
Este proyecto está bajo la licencia GPLv3