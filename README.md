
# Comunicación cliente-servidor con waspmote mediante módulos *Xbee*

Este repositorio contiene el código de un programa cliente-servidor para comunicar un Waspmote con un PC mediante modulos *XBee*.

## Instalación

### Instalación del servidor

El servidor puede ser instalado con *conda* mediante el comando:

> conda env create -f xbee_env.yml

O mediante *pip* mediante:

> pip install -r requirements.txt

## Uso

Para arrancar el servidor, el programa debe llamarse de la siguiente forma:

> python main.py

Opcionalmente podemos indicar otros parámetros:

```
--help                Mensaje de ayuda
--scantime [5-60]     Frecuencia en la que el servidor busca dispositivos cercanos (por defecto 10 segundos).
--notifytime [5-60]   Frecuencia en la que el cliente indica su estado (por defecto 10 segundos).
--usb [USB]           Dispositivo donde se encuentra el xbee (por defecto /dev/ttyUSB0).

```

El cliente debe arrancarse con el [IDE de Waspmote](https://development.libelium.com/waspmote-ide-v06/)
