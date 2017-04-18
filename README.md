# EntHub

[![Build Status](https://travis-ci.org/juanmtriguero/EntHub.svg?branch=master)](https://travis-ci.org/juanmtriguero/EntHub)

EntHub es la abreviatura de "Entertainment Hub" (centro de entretinimiento). Es una red social de ocio desarollada en Django para marcar, comentar y compartir con amigos películas, series, juegos, libros, etc.

Este proyecto utiliza [Travis CI](https://travis-ci.org/) para la **integración continua**.

> Actualmente se encuentra en desarrollo

## Contraseñas

Las contraseñas, por seguridad, no están incluidas en el control de versiones. En vez de eso, están almacenadas en variables de entorno que deben ser creadas al inicializar el proyecto. Para crear dichas variables, hay que ejecutar los siguientes comandos:

```
// Email host
$ export ENTHUB_EMAIL_HOST_USER=your_email_user
$ export ENTHUB_EMAIL_HOST_PASSWORD=your_email_password

// The Movie Database API key
$ export TMDB_API_KEY=your_api_key

// Google Books API key
$ export GOOGLE_API_KEY=your_api_key

// Giant Bomb API key
$ export GBOMB_API_KEY=your_api_key

// Comic Vine API key
$ export CVINE_API_KEY=your_api_key
```
