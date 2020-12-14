# IDM Flask-MYSQL-Docker

Para monitorear el tráfico interno se realizó una herramienta que
enriquezca la data sobre usuarios. Para ello, entre otras fuentes, se necesita que dada
una IP de algun usuario se obtenga cierta información.

Basado en la [plantilla](https://github.com/KartikShrikantHegde/Docker-Flask-Blueprint) de [Kartik](https://github.com/KartikShrikantHegde)

## Iniciando

**Paso 1:** Asegurarse de tener instalado git en su sistema operativo.


**Step 2:** Clone el proyecto en su maquina.

```git clone https://github.com/JhoneM/JMidm2020.git```

### Requisitos

**1. Docker**

Asegurarse de tener docker y docker-compose instalado.


### Instalación

**Step 1:** Acceder al directorio donde fue clonado el repo en el paso anterior.

```
cd JMidm2020
```

**Step 3:** Construir e iniciar

```
docker-compose up --build
```
Si ya se ejecuto este comando anteriormente solo se debe ejecutar:

```
docker-compose up
```

**Step 4:** Abrir el navegador en la siguiente ruta.

```
http://localhost:8000/
```
El navegador mostrará la pagina de inicio.

El sistema tambien cuenta con un gestor de bases de datos (PhpMyAdmin) alojado en un contenedor, para ingresar se debe ir a la siguiente ruta:
```
http://localhost:8180/
```

## Test

## Deployment

## Construido Con

* [Docker](https://www.docker.com/) -  Contenedores
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web framework
* [Python](https://www.python.org/) - Lenguaje de programación

## Contribuciones

## Version

## Autores

## Licencia

## Agradecimientos
* KartikShrikantHegde
* jmlcas