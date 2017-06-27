from flask import Flask

from controllers.status import status_route

def get_app():
    application = Flask('kessel-run')

    routes = [
        status_route
    ]

    for route in routes:
        application.register_blueprint(route, url_prefix='/api/v1')

    return application

def main():
    application = get_app()

    # todo: make configurable
    app.run(host='127.0.0.1', port=8080, debug=True)

app = get_app()

if __name__ == '__main__':
    main()
