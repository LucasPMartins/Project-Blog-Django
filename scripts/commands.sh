#!/bin/sh

# O shell irá encerrar o script se qualquer comando falhar
set -e

collectstatic.sh
migrate.sh
runserver.sh