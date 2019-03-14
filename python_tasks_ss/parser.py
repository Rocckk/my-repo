'''
this module is a parser of command line arguments: the arguments are processed and simple sql-like query to a database is returned  
'''
import argparse


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='the database tables which are available:', dest='table_name')

#  table 'teachers'
parser_teachers = subparsers.add_parser('teachers', help='table \'teachers\'')
# sub-subparsers
sub_subparsers= parser_teachers.add_subparsers(help='the commands which should be applied to a database table', dest='command')    
#  select
subparser_select  = sub_subparsers.add_parser('select', help='command to select something from a table')     
subparser_select.add_argument('-id', help='column \'id\'', type=int)
subparser_select.add_argument('-first_name', help='column \'first_name\'')
subparser_select.add_argument('-last_name', help='column \'last_name\'')
subparser_select.add_argument('-email', help='column \'email\'') 

#  delete
subparser_delete = sub_subparsers.add_parser('delete', help='the command which deletes record from a table')
subparser_delete.add_argument('-id', help='column \'id\'', type=int)
subparser_delete.add_argument('-first_name', help='column \'first_name\'')
subparser_delete.add_argument('-last_name', help='column \'last_name\'')
subparser_delete.add_argument('-email', help='column \'email\'')  

#  insert 
subparser_insert = sub_subparsers.add_parser('insert', help='the command which inserts new records in a table')
subparser_insert.add_argument('-id', help='column \'id\'', type=int)
subparser_insert.add_argument('-first_name', help='column \'first_name\'')
subparser_insert.add_argument('-last_name', help='column \'last_name\'')
subparser_insert.add_argument('-email', help='column \'email\'') 

#  update
subparser_update = sub_subparsers.add_parser('update', help='the command which updates records in a table')
subparser_update.add_argument('-id', help='column \'id\'', type=int)
subparser_update.add_argument('-first_name', help='column \'first_name\'')
subparser_update.add_argument('-last_name', help='column \'last_name\'')
subparser_update.add_argument('-email', help='column \'email\'')
subparser_update.add_argument('-where', help='a record in a table which should be updated', nargs=2, metavar=('field', 'value'))



# table 'students'
parser_students = subparsers.add_parser('students', help='table \'students\'')
# sub-subparsers
sub_subparsers= parser_students.add_subparsers(help='the commands which should be applied to a database table', dest='command')
# select
subparser_select  = sub_subparsers.add_parser('select', help='command to select something from a table')
subparser_select.add_argument('-id', help='column \'id\'', type=int)
subparser_select.add_argument('-first_name', help='column \'first_name\'')
subparser_select.add_argument('-last_name', help='column \'last_name\'')
subparser_select.add_argument('-group_id', help='column \'group_id\'')

#  delete
subparser_delete  = sub_subparsers.add_parser('delete', help='command to delete something from a table')
subparser_delete.add_argument('-id', help='column \'id\'', type=int)
subparser_delete.add_argument('-first_name', help='column \'first_name\'')
subparser_delete.add_argument('-last_name', help='column \'last_name\'')
subparser_delete.add_argument('-group_id', help='column \'group_id\'')

#  insert 
subparser_insert  = sub_subparsers.add_parser('insert', help='the command which inserts new records in a table')
subparser_insert.add_argument('-id', help='column \'id\'', type=int)
subparser_insert.add_argument('-first_name', help='column \'first_name\'')
subparser_insert.add_argument('-last_name', help='column \'last_name\'')
subparser_insert.add_argument('-group_id', help='column \'group_id\'')

# update
subparser_update  = sub_subparsers.add_parser('update', help='the command which updates records in a table')
subparser_update.add_argument('-id', help='column \'id\'', type=int)
subparser_update.add_argument('-first_name', help='column \'first_name\'')
subparser_update.add_argument('-last_name', help='column \'last_name\'')
subparser_update.add_argument('-group_id', help='column \'group_id\'')
subparser_update.add_argument('-where', help='a record in a table which should be updated', nargs=2, metavar=('field', 'value'))



#  table 'lessons'
parser_lessons = subparsers.add_parser('lessons', help='table \'lessons\'')
# sub-subparsers
sub_subparsers= parser_lessons.add_subparsers(help='the commands which should be applied to a database table', dest='command')
#  select
subparser_select  = sub_subparsers.add_parser('select', help='command to select something from a table')
subparser_select.add_argument('-start_time', help="column 'start_time'")
subparser_select.add_argument('-end_time', help="column 'end_time'")
subparser_select.add_argument('-auditorium_id', help="column 'auditorium_id'", type=int)
subparser_select.add_argument('-teacher_id', help="column 'teacher_id'", type=int)
subparser_select.add_argument('-subject_id', help="column 'subject_id'", type=int)

#  delete
subparser_delete  = sub_subparsers.add_parser('delete', help='command to delete something from a table')
subparser_delete.add_argument('-start_time', help="column 'start_time'")
subparser_delete.add_argument('-end_time', help="column 'end_time'")
subparser_delete.add_argument('-auditorium_id', help="column 'auditorium_id'", type=int)
subparser_delete.add_argument('-teacher_id', help="column 'teacher_id'", type=int)
subparser_delete.add_argument('-subject_id', help="column 'subject_id'", type=int)

#  insert 
subparser_insert  = sub_subparsers.add_parser('insert', help='the command which inserts new records in a table')
subparser_insert.add_argument('-start_time', help="column 'start_time'")
subparser_insert.add_argument('-end_time', help="column 'end_time'")
subparser_insert.add_argument('-auditorium_id', help="column 'auditorium_id'", type=int)
subparser_insert.add_argument('-teacher_id', help="column 'teacher_id'", type=int)
subparser_insert.add_argument('-subject_id', help="column 'subject_id'", type=int)

# update
subparser_update  = sub_subparsers.add_parser('update', help='the command which updates records in a table')
subparser_update.add_argument('-start_time', help="column 'start_time'")
subparser_update.add_argument('-end_time', help="columnargs.table_name 'end_time'")
subparser_update.add_argument('-auditorium_id', help="column 'auditorium_id'", type=int)
subparser_update.add_argument('-teacher_id', help="column 'teacher_id'", type=int)
subparser_update.add_argument('-subject_id', help="column 'subject_id'", type=int)
subparser_update.add_argument('-where', help='a record in a table which should be updated (for update command only)', nargs=2, metavar=('field', 'value'))


args = parser.parse_args()



#  action handling


fields = []
field_values = []

#  checking all the arguments possible
args_list = [i for i in dir(args) if not i.startswith('_')]

#  checking which arguments were passed and creating a list of optional arguments
for i in args_list:
    #  if the argument is None or command or table name - it should not be added to the field and value list
    if not getattr(args, i) or i == 'command' or i == 'table_name':
        continue
    else:
        fields.append(str(i))
        if isinstance(getattr(args, i), list):
            field_values.append(getattr(args, i))
        else:
            field_values.append(str(getattr(args, i)))
print fields
print field_values

#  OUTPUT
print 'the arguments you passed are equivalent to the following sql query:'

#  for select command:
if not fields and args.command == 'select':
    print '{} * from {};'.format(args.command, args.table_name)
elif fields and args.command == 'select':
    phrase = 'select * from db where '
    empty = ''
    for i in range(len(field_values)):
        temp = fields[i] + ' = ' + '\'' + str(field_values[i]) + '\'' + ' and '
        empty = empty + temp
    empty = empty.rstrip(' and')
    phrase = phrase + empty
    print phrase


#  for delete command
elif not fields and args.command == 'delete':
    print '{} from {};'.format(args.command, args.table_name)
elif fields and args.command == 'delete':
    phrase  = 'delete from db where '
    empty = ''
    for i in range(len(field_values)):
        temp = fields[i] + ' = ' + '\'' + str(field_values[i]) + '\'' + ' and '
        empty = empty + temp
    empty = empty.rstrip(' and')
    phrase = phrase + empty
    print phrase


#  for insert command
elif not fields and args.command == 'insert':
    print 'you have to indicate what and where to insert'
elif fields and args.command == 'insert':
    phrase = '{} into {} ({}) values ({})'.format(args.command, args.table_name, ', '.join(fields), ', '.join(field_values))
    print phrase

#  for update command
elif not fields and args.command == 'update':
    print 'you have to indicate which fields should be updated and which new values should be inserted instead'
elif fields and args.command == 'update' and 'where' in fields:
    set_clause = ''
    fields.pop()
    where = field_values.pop()
    for i in range(len(fields)):
        temp = fields[i] + ' = ' + str(field_values[i]) + ', '
        set_clause += temp
    set_clause = set_clause.rstrip(', ')
    phrase  = '{} {} set {} where {}'.format(args.command, args.table_name, set_clause, ' = '.join(where))
    print phrase
else:
    print 'please pass the \'where\' argument for update command to indicate which record should be updated, e.g.\n\n... -some_field \'some_value\' -where id 32\n\nto put \'some_value\' in \'some_field\' in the record with the id \'32\''
