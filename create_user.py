import arcpy

"""
    CREATE POSTGRESQL USER
"""


def create_postgresql_user(instance_name,
                           database_name,
                           database_admin,
                           database_admin_password,
                           gdb_admin_password,
                           tablespace_name,
                           authorization_file):
    database_platform = 'PostgreSQL'
    gdb_admin_name = 'sde'
    account_authentication = 'DATABASE_AUTH'
    try:
        arcpy.CreateEnterpriseGeodatabase_management(database_platform,
                                                     instance_name,
                                                     database_name,
                                                     account_authentication,
                                                     database_admin,
                                                     database_admin_password,
                                                     '',
                                                     gdb_admin_name,
                                                     gdb_admin_password,
                                                     tablespace_name,
                                                     authorization_file)
    except arcpy.ExecuteError:
        pass



"""
    CREATE ORACLE USER
"""


def create_oracle_user(instance_name,
                       database_admin,
                       database_admin_password,
                       gdb_admin_name,
                       gdb_admin_password,
                       tablespace_name,
                       authorization_file):
    database_platform = 'Oracle'
    account_authentication = 'DATABASE_AUTH'
    try:
        arcpy.CreateEnterpriseGeodatabase_management(database_platform,
                                                     instance_name,
                                                     '',
                                                     account_authentication,
                                                     database_admin,
                                                     database_admin_password,
                                                     '',
                                                     gdb_admin_name,
                                                     gdb_admin_password,
                                                     tablespace_name,
                                                     authorization_file)
    except arcpy.ExecuteError:
        pass

"""
    CREATE ARCGIS ENTERPRISME GEODATABASE USER
    SUPPORTS ORACLE AND POSTGRESQL ONLY, SQL SERVER IS NOT SUPPORTED
"""

def create(params):
    database_platform = params.get('database_platform')
    instance_name = params.get('instance_name')
    database_name = params.get('database_name')
    database_admin = params.get('database_admin')
    database_admin_password = params.get('database_admin_password')
    gdb_admin_name = params.get('gdb_admin_name')
    gdb_admin_password = params.get('gdb_admin_password')
    tablespace_name = params.get('tablespace_name')
    authorization_file = params.get('authorization_file')

    if database_platform != ' Oracle' and database_platform != 'PostgreSQL':
        message = 'only support oracle and postgresql'
        print message
        return [message]

    if database_platform == 'Oracle' and database_name is not None:
        message = 'database platform is oracle and the database_name will be ignored.'
        arcpy.AddMessage(message)

    if database_platform == 'PostgreSQL' and gdb_admin_name != 'sde':
        message = 'database platform is postgresql and the gdb_admin_name will be set to sde'
        arcpy.AddMessage(message)

    if database_platform == 'Oracle':
        create_oracle_user(instance_name=instance_name,
                           database_admin=database_admin,
                           database_admin_password=database_admin_password,
                           gdb_admin_name=gdb_admin_name,
                           gdb_admin_password=gdb_admin_password,
                           tablespace_name=tablespace_name,
                           authorization_file=authorization_file)
    elif database_platform == 'PostgreSQL':
        create_postgresql_user(instance_name=instance_name,
                               database_name=database_name,
                               database_admin=database_admin,
                               database_admin_password=database_admin_password,
                               gdb_admin_password=gdb_admin_password,
                               tablespace_name=tablespace_name,
                               authorization_file=authorization_file)
    messages = []
    for i in range(arcpy.GetMessageCount()):
        messages.append(arcpy.GetMessage(i))
    return messages
