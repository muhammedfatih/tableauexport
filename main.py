import argparse
import getpass
import logging

import tableauserverclient as TSC


def main():
    parser = argparse.ArgumentParser(description='Export a view as an image, pdf, or csv')
    parser.add_argument('--server', '-s', required=True, help='server address')
    parser.add_argument('--username', '-u', required=True, help='username to sign into server')
    parser.add_argument('--site', '-S', default=None)
    parser.add_argument('--password', '-p', default=None, help='password for the user')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pdf', dest='type', action='store_const', const=('populate_pdf', 'PDFRequestOptions', 'pdf', 'pdf'))
    group.add_argument('--png', dest='type', action='store_const', const=('populate_image', 'ImageRequestOptions', 'image', 'png'))
    group.add_argument('--csv', dest='type', action='store_const', const=('populate_csv', 'CSVRequestOptions', 'csv', 'csv'))
    parser.add_argument('--input-file', '-i', help='filename for imported data')
    parser.add_argument('--output-folder', '-o', help='folder to store the exported data')
    parser.add_argument('--viewName', '-v', required=True, help='view name to query and download')

    args = parser.parse_args()

    tableau_auth = TSC.TableauAuth(args.username, args.password, args.site)
    server = TSC.Server(args.server, use_server_version=True)
    with server.auth.sign_in(tableau_auth):
        inputFileContent = open(args.input_file, 'r') 
        lines = inputFileContent.readlines() 

        selectedViews = filter(lambda x: x.name == args.viewName, TSC.Pager(server.views.get))
        selectedView = list(selectedViews).pop()

        views = filter(lambda x: x.id == selectedView.id, TSC.Pager(server.views.get))
        view = list(views).pop()

        # We have a number of different types and functions for each different export type.
        # We encode that information above in the const=(...) parameter to the add_argument function to make
        # the code automatically adapt for the type of export the user is doing.
        # We unroll that information into methods we can call, or objects we can create by using getattr()
        (populate_func_name, option_factory_name, member_name, extension) = args.type
        populate = getattr(server.views, populate_func_name)
        option_factory = getattr(TSC, option_factory_name)

        for line in lines:
            lineParts = line.replace("\r", "").replace("\n", "").split(':')
            filterName=lineParts[0]
            filterValue=lineParts[1]

            options = option_factory().vf(filterName, filterValue)
            filename = '{}/{}-{}.{}'.format(args.output_folder, filterName, filterValue ,extension)

            populate(view, options)
            with open(filename, 'wb') as f:
                if member_name == 'csv':
                    f.writelines(getattr(view, member_name))
                else:
                    f.write(getattr(view, member_name))

if __name__ == '__main__':
    main()
