# Práctica 1: Web scraping

## Descripción

Esta práctica se ha realizado bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer así datos de la web https://www.ferreteriasindustriales.es/ y generar un _dataset_.

## Miembros del equipo

La actividad ha sido realizada en equipo por los siguientes alumnos:
* Daniel Cañete Román <dcanete@uoc.edu>
* Balpreet Kaur Singh <bkaur@uoc.edu>


## Ficheros del código fuente

* **src/main.py**: punto de entrada al programa. Inicia el proceso de scraping.
* **src/scraper.py**: contiene la implementación de la clase _AccidentsScraper_ cuyos métodos generan el conjunto de datos a partir de la base de datos online [PlaneCrashInfo](http://www.planecrashinfo.com/database.htm).
* **src/reason_classifier.py**: contiene la implementación de la clase que se encarga de asignar una causa a un resumen de accidente dado. Para ello, utiliza la librería *TextBlob*.

## Recursos

1. Materiales de la asignatura
2. Práctica ejemplo
