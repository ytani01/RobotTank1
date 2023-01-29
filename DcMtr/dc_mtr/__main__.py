#
# Copyright (c) 2023 Yoichi Tanibayashi
#
import click
import pigpio
from . import __prog_name__, __version__, __author__
from . import get_logger
from . import Test_DcMtr
from . import Test_DcMtrN
from . import Test_DcMtrServer


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


@cli.command(help="dc_mtr_n")
@click.argument('pin1', type=int)
@click.argument('pin2', type=int)
@click.argument('pin3', type=int)
@click.argument('pin4', type=int)
@click.option('--opt1', '-o1', 'opt1', type=str, default=None, help='opt')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def dc_mtr_n(obj, pin1, pin2, pin3, pin4, opt1, debug):
    """ DcMtrN """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, opt1=%s, args=%s', obj, opt1, (pin1, pin2, pin3, pin4))

    pi = pigpio.pi()
    test_app = Test_DcMtrN(pi, ((pin1, pin2), (pin3, pin4)), obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        pi.stop()


@cli.command(help="dc_mtr_server")
@click.argument('pin1', type=int)
@click.argument('pin2', type=int)
@click.argument('pin3', type=int)
@click.argument('pin4', type=int)
@click.option('--port', '-p', 'port', type=int, default=12345, help='port number')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
@click.pass_obj
def dc_mtr_server(obj, pin1, pin2, pin3, pin4, port, debug):
    """ DcMtrServer """
    __log = get_logger(__name__, obj['debug'] or debug)
    __log.debug('obj=%s, pin=%s, port=%s', obj,
                (pin1, pin2, pin3, pin4), port)

    pi = pigpio.pi()
    test_app = Test_DcMtrServer(pi, ((pin1, pin2), (pin3, pin4)), port,
        obj['debug'] or debug)

    try:
        test_app.main()

    finally:
        pi.stop()


#cli.add_command(cmd2)
#cli.add_command(cmd3)

if __name__ == '__main__':
    cli(prog_name=__prog_name__)
