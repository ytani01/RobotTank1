#
# Copyright (c) 2023 Yoichi Tanibayashi
#
import click
from . import __prog_name__, __version__, __author__
from . import get_logger
from . import kbd
from . import robottank


@click.group(invoke_without_command=True,
             context_settings=dict(help_option_names=['-h', '--help']),
             help="Bluetooth Keyboard Package")
@click.option('--opt0', '-o0', 'opt0', type=str, default=None, help='opt1')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, opt0, debug):
    """ command group """
    __log = get_logger(__name__, debug)
    __log.debug('opt0=%s', opt0)

    ctx.obj = {'opt0': opt0, 'debug': debug}

    subcmd = ctx.invoked_subcommand
    __log.debug('subcmd=%s', subcmd)

    if not subcmd:
        print(ctx.get_help())


cli.add_command(kbd)
cli.add_command(robottank)


if __name__ == '__main__':
    cli(prog_name=__prog_name__)
