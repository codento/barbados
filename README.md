# Barbados harbour management system

Written as a spare-time project, it aims to model a harbour and how different
kinds of users can use the data.

## Requirements

Requirements in the usual location, though `django-extensions` may have to go.

    $ pip install -r

Postgresql 9.4 with UUID support. To enable, be sure to install
`postgresql-contrib-9.4` (Debian) and create the extension:

    CREATE EXTENSION "uuid-ossp";

