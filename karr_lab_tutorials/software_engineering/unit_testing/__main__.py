""" Example command line program

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-05-12
:Copyright: 2017, Karr Lab
:License: MIT
"""

from cement.core import foundation
from cement.core import controller


class BaseController(controller.CementBaseController):

    class Meta:
        label = 'base'
        description = 'Example command line interface'
        arguments = [
            # we can make these arguments "positional" (required) by not adding "--arg" and just writing "arg"
            # the action 'store' will store the value passed for the option in self.app.pargs
            (['arg'], dict(type=str, help="Example argument")),

        ]

    @controller.expose(hide=True)
    def default(self):
        print('Arg = `{}`'.format(self.app.pargs.arg))


class App(foundation.CementApp):

    class Meta:
        label = "karr_lab_tutorials"
        base_controller = "base"
        handlers = [
            BaseController,
        ]


def main():
    with App() as app:
        app.run()

if __name__ == "__main__":
    main()
