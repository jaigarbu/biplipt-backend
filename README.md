# Biplipt Backend - v.0.1.0

Este es el repositorio oficial del proyecto [Biplipt App](https://biplipt.com), aquí encontrará la documentación oficial del proyecto, así como las metodologías y los pasos para convertirse en colaborador de **Biplipt**.

### Sobre Biplipt

Biplipt es una iniciativa que busca crear la biblioteca discográfica más grande de internet. Nuestro objetivo es diseñar una plataforma que almacene, valide y administre letras, acordes, información discográfica completa y organizada de los artistas musicales. Permitiendo la centralización de toda la información de la industria. Biplipt contará con el tiempo, soporte para todos los idiomas que hayan sido digitalizados.

## Comenzando 🚀

Para comenzar con Biplipt siga los siguintes pasos:

**Clone este repositorio y ubiquese dentro del directorio `biplipt-backend`**

```shell
git clone https://github.com/jhonjab19/biplipt-backend.git

cd biplipt-backend
```

**Cree un etorno virtual para instalar los requerimientos necesarios**

_En este caso explicaremos como administrar este proyecto utilizando un entorno virtual creado con `virtualenv` usted puede usar cualquier administrador de entornos virtuales. Si desea utilizar virtualenv siga los siguientes pasos:_

1. **Instale virtualenv**

   ```shell
   pip install virtualenv
   ```

2. **Cree su entorno virtual**

   ```shell
   virtualenv venv
   ```

3. **Active su entorno virtual**

   ```shell
   .\venv\Scripts\activate
   ```

**Installe los requrimientos del proyecto**

_Una vez creado y activado el entorno virtual es hora de instalar todas las dependencias del proyecto, para ello ejecute_:

```shell
pip install -r requirements.txt
```

**Haga las migraciones correspondientes**

```shell
py manage.py makemigrations
py manage.py migrate
```

### Pre-requisitos 📋

El backend de Biplpit se encuentra construido en [Django](https://www.djangoproject.com/) por lo que se hace necesario tener conocimientos de [Python](https://www.python.org/) en sus versiones más recientes.

### Servidor de desarrollo 🔧

Django cuenta con un servidor de desarrollo con el que usted puede probar los cambios que vaya realizando casi que al instante. Para iniciar el servidor de desarrollo ejecute:

```shell
py manage.py runserver
```

Esto iniciará el servidor en [http://localhost:8000](http://localhost:8000)

## Ejecutando las pruebas ⚙️

_Las pruebas no estan disponibles aun_

## Despliegue 📦

_El despliegue no está disponible aun_

## Construido con 🛠️

Este proyecto está construido usando las siguientes tecnologias

- [Django](https://www.djangoproject.com/) - Framewok backend escrito en Python
- [GraphQL](https://graphql.org/) - Lenguaje estructurado de consultas
- [JWT](https://jwt.io/) - Estandar JSON Web Tokens para manejo de auterización

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki]()

## Versionado 📌

Usamos [GIT](https://git-scm.com/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/jhonjab19/biplipt-backend/tags).

## Autores ✒️

- **Jhon Jairo Garzon** - _Trabajo Inicial, Autor del proyecto_ - [jhonjab19](https://github.com/jhonjab19)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/jhonjab19/biplipt-backend/contributors) quíenes han participado en este proyecto.

## Licencia 📄

Este proyecto está bajo la Licencia Privada - mira el archivo [LICENSE.md](LICENSE.md) para detalles
