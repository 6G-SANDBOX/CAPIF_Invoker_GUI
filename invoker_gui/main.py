
from cmd import Cmd
from capif_ops.invoker_previous_register import PreviousRegister
from capif_ops.invoker_register_to_capif import RegisterInvoker
from capif_ops.invoker_discover_service import  DiscoverService
from capif_ops.invoker_secutiry_context import InvokerSecurityContext
from capif_ops.invoker_get_security_auth import InvokerGetSecurityAuth
from capif_ops.invoker_delete import RemoveInvoker
from capif_ops.invoker_get_auth import PreviousAuth
from capif_ops.invoker_remove_security_context import InvokerRemoveSecurityContext
from capif_ops.invoker_to_service import InvokerToService
import shlex
import subprocess
from art import *

prev_register = PreviousRegister()
regiter_capif = RegisterInvoker()
discover_service = DiscoverService()
register_security_context = InvokerSecurityContext()
security_context_auth = InvokerGetSecurityAuth()
remove_invoker = RemoveInvoker()
invoker_auth = PreviousAuth()
remove_security_service = InvokerRemoveSecurityContext()
invoker_service = InvokerToService()



class CAPIFProvider(Cmd):

  def __init__(self):
        Cmd.__init__(self)
        self.prompt = "> "
        self.intro = tprint("Welcome  to  Invoker  Console")

  def emptyline(self):
        """Do nothing on empty input line"""
        pass

  def preloop(self):
    state = prev_register.execute_previous_register_invoker()
    self.previous_register_state = state

  def precmd(self, line):

    line = line.lower()
    args = shlex.split(line)

    if len(args) >= 1 and args[0] in ["goodbye"]:
        print("The first argument is username")
        return ""

    elif len(args) >= 1 and args[0] not in ["->", "wall", "follows", "exit", "help"]:
        pass

    return line

  def do_register_invoker(self, input):
    'Register invoker to CAPIF'
    regiter_capif.execute_register_invoker(input)

  def do_discover_service(self, input):
    'Discover all services published in CAPIF'
    discover_service.execute_discover_service(input)

  def do_register_security_context(self, input):
    'Create security context to use services'
    register_security_context.execute_register_security_context(input)

  def do_get_security_auth(self, input):
    "If you select Oauth as security method use this command to obtain jwt token to access service"
    security_context_auth.execute_get_security_auth(input)

  def do_get_auth(self, input):
    'Get jwt token to register invoker in CAPIF (Optional, only if token expires)'
    invoker_auth.execute_get_auth(input)

  def do_remove_security_context(self, input):
    print("Not implemented yet")
    #remove_security_service.execute_remove_security_context(input)

  def do_remove_invoker(self, input):
    "Remove invoker from CAPIF"
    remove_invoker.execute_remove_invoker(input)

  def do_call_service(self, input):
    "Test invocation os service API"
    invoker_service.execute_invoker_to_service(input)

  def do_exit(self, input):
    print('\nExiting...')
    return True


if __name__ == '__main__':
    try:
        CAPIFProvider().cmdloop()
    except KeyboardInterrupt:
        print('\nExiting...')