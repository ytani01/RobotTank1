#
# Copyright (c) 2023 Yoichi Tanibayashi
#
import click
import pigpio
from . import __prog_name__, __version__, __author__
from .my_logger import get_logger
from .test_dc_mtr import Test_DcMtr


@click.group(invoke_without_command=True,
             context_settings=dict(help_option_names=['-h', '--help']),
             help=" by " + __author__)
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


@cli.command(help="dc_mtr")
@click.argument('pin1', type=int)
@click.argument('pin2', type=int)
@click.option('--opt1', '-o1', 'opt1', type=str, default=None, help='opt')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def dc_mtr(obj, pin1, pin2, opt1, debug):
    """ DcMtr """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, opt1=%s, args=%s', obj, opt1, (pin1, pin2))

    pi = pigpio.pi()
    test_app = Test_DcMtr(pi, (pin1, pin2), obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        pi.stop()


#cli.add_command(cmd2)
#cli.add_command(cmd3)

if __name__ == '__main__':
    cli(prog_name=__prog_name__)
