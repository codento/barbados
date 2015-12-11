# Barbados harbour management system

Written as a spare-time project, it aims to model a harbour and how different
kinds of users can use the data.

## Requirements

Requirements in the usual location, though `django-extensions` may have to go.

    $ pip install -r

Postgresql 9.4 with UUID support. To enable, be sure to install
`postgresql-contrib-9.4` (Debian) and create the extension:

    CREATE EXTENSION "uuid-ossp";

## Testing

Run the tests with

    $ py.test --cov=barbados.barbadosdb --cov=barbados.barbadosweb --cov-report=term-missing

To create test data for admin etc

    $ DJANGO_SETTINGS_MODULE=barbados.dev_settings python manage.py create-test-users

## Client development

    npm install -g jspm
    jspm install

Start django server and open http://127.0.0.1:8000/static/index.html
(can also be loaded straight from filesystem)
