# Con la nueva actualización que inacap le dio a su sistema, lamentablemente este proyecto dejo de funcionar.
# mihorario-Inacap
Imprime tu horario de clases del día en la terminal. Tambien puedes conocer que días son feriados.
<br>
La gracia es que puedes ver tu horario incluso cuando estás offline, desde la comodidad de una consola.

![alt text](https://raw.githubusercontent.com/whitesoundcl/mihorario-inacap/master/terminal.png)
# Este no es un proyecto oficial de INACAP y solo debe ser utilizado para fines educativos.
(o para ver tu horario de vez en cuando =) ).

## Dependencias:
- Selenium 
- Navegador Firefox
- [última versión de GECKODRIVER para tu arquitectura y SO](https://github.com/mozilla/geckodriver/releases)

## Instalación:
### Linux (Probado en una distro basada en UBUNTU y en ArchLinux):
- Primero debes clonar este repositorio en el directorio que desees utilizando la terminal:
```terminal
git clone https://github.com/whitesoundcl/mihorario-Inacap.git
```
- Debes instalar el módulo [selenium](https://www.seleniumhq.org/projects/webdriver/) en python, normalmente esto se consigue utilizando el siguiente comando: 
```terminal
pip3 install selenium
```
- Debes descargar la última versión de [geckodriver](https://github.com/mozilla/geckodriver/releases) correspondiente con tu sistema operativo y arquitectura, para luego extraerlo en la carpeta raíz del proyecto.

- Crear un alias en .bashrc:
<br>
Concatenar al final de ~/.bashrc

```terminal
alias horario='python3 <Directorio donde clonaste este repositorio>/mihorario-Inacap/mihorario.py'
```
Por ejemplo:

```terminal 
alias horario='python3 $HOME/Programas/mihorario-inacap-github/mihorario.py'
``` 
Si no realizas este último paso, puedes continuar utilizando el programa de la siguiente forma: 
(Ya estando en el directorio del proyecto)
```terminal
python3 mihorario.py
```
### Mac OS:
Creo que deberían ser los mísmos pasos que en linux, pero no aseguro nada.

## Uso:
Abrir una terminal en el directorio dónde clonaste el proyecto y escribir según necesites.
- #### Ver horario del día:
```terminal
horario
```
La primera vez que ejecutes este comando se te pedirán tus credenciales de INACAP para poder acceder a tu sesión de usuario y descargar el horario del semestre.
- #### Refrescar cache de horario:
```terminal
horario -a
```
No es necesario recargar el cache del horario del semestre a cada rato, con tal de que se haga de vez en cuando basta y sobra. Si te quedas con el mismo cache durante mucho tiempo, y te actualizaron el horario (Cancelación de clases, cambio de aula, etc) no verás estos cambios en el programa. En un intel pentium del año del que no se dice, tarda unos 59 segundos en actualizarse.
- #### Ver horario en 7 días:
```terminal
horario -s
```
- #### Ver horario en N días:
```terminal
horario -d N
```
Funciona tanto para ver el horario de los días anteriores (número negativo), como para ver el horario de los días siguientes (número positivo).
- #### Ver todo el horario del semestre:
```terminal
horario -t
```
- #### Ver horario resumido en una línea:
Útil si se desea imprimir el horario en algún widget
```terminal
horario -l
```
### Widget
He creado un pequeño script (mihorario-wid.py) que solo muestra la sala en la que deberías estar como en el siguiente ejemplo:
```terminal
[507] 
```
Lo cual lo hace ideal para insertarlo en un widget en la barra de tareas.<br>
![alt text](https://raw.githubusercontent.com/whitesoundcl/mihorario-inacap/master/widget.png)
<br>(
Nota: para que funcione debes haber actualizado el caché del horario con mihorario.py)
