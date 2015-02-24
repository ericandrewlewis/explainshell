#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, itertools, urllib, sys
import markupsafe

import bashlex.errors

from explainshell import matcher, errors, util, store, config

from explainshell.web import views

logger = logging.getLogger(__name__)

def main():
    s = store.store('explainshell', config.MONGO_URI)

    arguments = sys.argv
    arguments.remove('./explain.py')
    command = ' '.join(arguments)

    try:
        matches, helptext = views.explaincommand(command, s)
        logger.info('Parsing successful')

        print command
        for index, match in enumerate(matches):
            if match != matches[-1]:
                print '├──',
            else:
                print '└──',
            print match['match'], ' -- ',
            if 'helpclass' in match.keys():
                for text, id in helptext:
                    if id == match['helpclass']:
                        print text
            else:
                print '?'

    except errors.ProgramDoesNotExist, e:
        logger.warn('%r missing manpage: %s', command, e.message)
        # return render_template('errors/missingmanpage.html', title='missing man page', e=e)
    except bashlex.errors.ParsingError, e:
        logger.warn('%r parsing error: %s', command, e.message)
        # return render_template('errors/parsingerror.html', title='parsing error!', e=e)
    except NotImplementedError, e:
        logger.warn('not implemented error trying to explain %r', command)
        # msg = ("the parser doesn't support %r constructs in the command you tried. you may "
               # "<a href='https://github.com/idank/explainshell/issues'>report a "
               # "bug</a> to have this added, if one doesn't already exist.") % e.args[0]

        # return render_template('errors/error.html', title='error!', message=msg)
    except:
        logger.error('uncaught exception trying to explain %r', command, exc_info=True)
        # msg = 'something went wrong... this was logged and will be checked'
        # return render_template('errors/error.html', title='error!', message=msg)

if __name__ == '__main__':
    logging.basicConfig(level='CRITICAL')
    sys.exit(main())