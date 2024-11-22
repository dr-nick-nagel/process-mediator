import sys
import argparse
import asyncio

def send_output ( text ) :
    print( text )
    sys.stdout.flush()

def get_input () : 
    print( "Enter Text Input ... " )
    test_in = input()
    # sys.stdout.write( "\n" )
    sys.stdout.flush(  )
    return test_in 

def echo_input( obtained_in ) : 
    send_output( obtained_in )

async def send_async_output (text) :
    print( text ) 
    # sys.stdout.flush()

def test_send_async ( text ) :
    loop.run_until_complete( send_async_output( text ) )

if __name__ == "__main__" :
    print( "----    START TEST    ----" )
    parser = argparse.ArgumentParser (
        prog = 'nn_testscript',
        description = 'Test scaffolding for process mediator pattern',
        epilog = '\u266B Always look on the bright side of life... '
    )
    parser.add_argument( 'instance_label' )
    args = parser.parse_args()
    print( sys.argv[0] )
    instance_label = args.instance_label
    print(f"Instance: {instance_label}")
    loop = asyncio.new_event_loop()
    send_output ( "Testing 1, 2, 3" )
    test_in = get_input()
    test_send_async( f"ECHO: {test_in}" )
    print( "----    END TEST    ----" )