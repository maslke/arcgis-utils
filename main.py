import argparse
import simple_server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=False, help='bind port')
    parser.add_argument('-l', '--license', type=str, required=True,
                        help="""
                            license file location, like [arcgis_server_installation_path]
                             /framework/runtime/.wine/drive_c/Program Files/ESRI/License/sysgen/keycodes'
                        """)
    args = parser.parse_args()
    port = 8080 if args.port is None else args.port
    authorization_file = args.license
    simple_server.run(port=port, authorization_file=authorization_file)


if __name__ == '__main__':
    main()