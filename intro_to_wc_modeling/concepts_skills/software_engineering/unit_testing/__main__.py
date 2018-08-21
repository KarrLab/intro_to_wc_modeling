""" Example command line program

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-05-12
:Copyright: 2017, Karr Lab
:License: MIT
"""

import cement


class BaseController(cement.Controller):

    class Meta:
        label = 'base'
        description = 'Example command line interface'
        arguments = [
            # we can make these arguments "positional" (required) by not adding "--arg" and just writing "arg"
            # the action 'store' will store the value passed for the option in self.app.pargs
            (['arg'], dict(type=str, help="Example argument")),

        ]

    @cement.ex(hide=True)
    def _default(self):
        print('Arg = `{}`'.format(self.app.pargs.arg))


class App(cement.App):

    class Meta:
        label = "intro_to_wc_modeling"
        base_controller = "base"
        handlers = [
            BaseController,
        ]


def main():
    with App() as app:
        app.run()
