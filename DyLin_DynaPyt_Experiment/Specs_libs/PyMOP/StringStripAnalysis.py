# ============================== Define spec ==============================
from pythonmop import Spec, call, TRUE_EVENT, FALSE_EVENT
import pythonmop.spec.spec as spec

# spec.DONT_MONITOR_PYTHONMOP = False

class StringStripAnalysis(Spec):
    """
    String stripping only consider removing all characters in the string, not the words.
    Developers should use string split and join methods to remove words.
    src: https://peps.python.org/pep-0008/#programming-recommendations
    """
    def __init__(self):
        super().__init__()

        @self.event_before(call(str, 'strip'))
        def strip(**kw):
            _self = kw['args'][0]
            args = kw['args']

            if len(args) > 1:
                arg = args[1]
                if len(set(arg)) != len(arg):
                    return TRUE_EVENT
                if len(arg) > 1 and (
                    (_self.startswith(arg) and _self[len(arg) : len(arg) + 1] in arg)
                    or (_self.endswith(arg) and _self[-len(arg) - 1 : -len(arg)] in arg)
                ):
                    return TRUE_EVENT
            return FALSE_EVENT

    ere = 'strip+'
    creation_events = ['strip']

    def match(self, call_file_name, call_line_num):
        print(
            f'Spec - {self.__class__.__name__}: Possible misuse of str.strip, arg may contains duplicates or might have removed something not expected at file {call_file_name}, line {call_line_num}.')
# =========================================================================

"""
spec_instance = StringStripAnalysis()
spec_instance.create_monitor('D')

def test():
    "".strip("abab")  # DyLin warn
    a = "xyzz"
    "".strip(a)  # DyLin warn
    "1,2".strip(','.join([str(s) for s in range(0, 999)]))  # DyLin warn

    "".strip("a")
    "".strip("abc")
    "".strip(''.join([str(s) for s in range(0, 9)]))
    "foo.bar.rar".strip(".rar")  # DyLin warn
    "foo.kab.bak".strip(".bak")  # DyLin warn
    "<|en|>".strip("<|>")

test()
"""