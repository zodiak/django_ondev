from optparse import make_option

from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from django.core.management.color import no_style
from django.core.management.sql import sql_reset
from django.db import connections, transaction, DEFAULT_DB_ALIAS

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to clear. '
                'Defaults to the "default" database.'),
    )
    help = "Removes all tables from the current database."

    output_transaction = True

    def handle_noargs(self, **options):
        using = options.get('database', DEFAULT_DB_ALIAS)
        connection = connections[using]

        self.style = no_style()

        sql_list = sql_cleardb(connection)

        if options.get('interactive'):
            confirm = raw_input("""
You have requested a database full clear.
This will IRREVERSIBLY DESTROY "%s" database 
structure and data.
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: """ % (connection.settings_dict['NAME']),)
        else:
            confirm = 'yes'

        if sql_list and confirm == 'yes':
            try:
                cursor = connection.cursor()
                cursor.execute(sql_list)
            except Exception, e:
                transaction.rollback_unless_managed()
                raise CommandError("""Error: database couldn't be clear. Possible reasons:
  * The database isn't running or isn't configured correctly.
  * The SQL was invalid.
The full error: %s""" % (e,))
            transaction.commit_unless_managed()
            
def sql_cleardb(connection):
    "Returns a list of the DROP TABLE SQL statements for all existing tables."

    # This should work even if a connection isn't available
    try:
        cursor = connection.cursor()
    except:
        cursor = None

    # Figure out which tables already exist
    if cursor:
        table_names = connection.introspection.get_table_list(cursor)
    else:
        table_names = []

    output = 'DROP TABLE `%s`;' % ('`, `'.join(table_names),) if table_names else None
    # Close database connection explicitly, in case this output is being piped
    # directly into a database client, to avoid locking issues.
    if cursor:
        cursor.close()
        connection.close()

    return output
