# manage.py
#import sys
#sys.path.append('/Users/largitdata/Train')

import os
from app import create_app, db
from app.models import User, Role, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(application)
migrate = Migrate(application, db)

#manager.add_command("shell", Shell(make_context=make_shell_context))
#manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(application=application, db=db, User=User, Role=Role)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__  == '__main__':
    print('running manager...')
    #print(db)
    manager.run()
