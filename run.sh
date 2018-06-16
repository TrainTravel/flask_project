#!/bin/sh

usage()
{
    echo ""
    echo "    Usage:"
    echo ""
    echo "        `basename $0` start/stop/reload [\$MODE] [\$PORT]"
    echo ""
    echo "        \$MODE: [prod] default is prod"
    echo "        \$PORT: default will bind to 9999"
    echo ""
    echo ""
    echo "            for production:   ./run.sh start"
    echo "                NOTE: You should bind sock file and static folder by any web server."
    echo ""
    exit
}

if [ -z $1 ];
then
    usage
fi

MODE=${2-prod}
PORT=${3-9999}
echo ""
echo "Running in Mode: <${MODE}>, Action: <${1}> and binding to port: <${PORT}>"
echo ""

case $MODE in

    "prod")
        case $1 in
            "start")
                uwsgi --ini lottery_app_uwsgi.ini
                ;;
            "stop")
                uwsgi --stop /tmp/lottery_app_uwsgi.pid
                ;;
            "reload")
                uwsgi --reload /tmp/lottery_app_uwsgi.pid
                ;;
            *)
                usage
                ;;
        esac
        ;;
    *)
        usage
        ;;
esac
