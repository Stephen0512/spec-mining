# ============================== Define spec ==============================
from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from typing import Any, Iterable, Iterator, List, Optional

import collections
import warnings

class ChangeListWhileIterating(BaseAnalysis):
    # PyLint has a check for this, code W4701
    # PyLint also has checks for dictionaries and sets (E4702, E4703). These seem more severe than the list check
    class ListMeta:
        def __init__(self, l: Iterable, it: Iterator, length: int, dyn_ast: str, iid: int, warned: bool = False):
            self.l = l
            self.it = it
            self.length = length
            self.warned = warned
            self.dyn_ast = dyn_ast
            self.iid = iid

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = {}
        self.unique_event = {}
        self.violation = 0
        self.unique_violation = 0

        # Stack of ListMeta objects
        self.iterator_stack: List[self.ListMeta] = []

    def enter_for(self, dyn_ast: str, iid: int, next_value: Any, iterable: Iterable, iterator: Iterator) -> Optional[Any]:
        # print(f"{self.analysis_name} enter_for {iid}")
        if isinstance(iterable, collections.abc.Iterator) or isinstance(iterable, type({})):
            return

        _list = iterable
        try:
            if (
                len(self.iterator_stack) == 0
                or iid != self.iterator_stack[-1].iid
                or dyn_ast != self.iterator_stack[-1].dyn_ast
                or iterator != self.iterator_stack[-1].it
            ):
                length = len(_list)
                self.iterator_stack.append(self.ListMeta(_list, iterator, length, dyn_ast, iid))
            elif len(self.iterator_stack) > 0:
                list_meta: self.ListMeta = self.iterator_stack[-1]
                if (
                    list_meta.warned is False
                    and len(_list) < list_meta.length
                    and id(_list) == id(list_meta.l)
                    and iterable == list_meta.l
                    and iterator == list_meta.it
                ):
                    # Add the event to the event dictionary
                    if "violation" not in self.event:
                        self.event["violation"] = 1
                    else:
                        self.event["violation"] += 1

                    # Add the violation to the violation dictionary
                    self.violation += 1

                    # Find the file name and line number of the function in the original file
                    call_file_name = dyn_ast
                    call_line_num = BaseAnalysis.iid_to_location(self, dyn_ast, iid).start_line

                    # Add the violation to the unique violation dictionary
                    violation_key = f'{call_file_name}:{call_line_num}'
                    if violation_key not in self.unique_event:
                        self.unique_event[violation_key] = 1
                        self.unique_violation += 1  # Increment the unique violation count
                    else:
                        self.unique_event[violation_key] += 1

                    # Print the violation message
                    warnings.warn(
                        f'Spec - {self.__class__.__name__}: List length changed while iterating initial length: {list_meta.length} current:{len(_list)}'
                        f'File {call_file_name}, line {call_line_num}.')
                    list_meta.warned = True

        # necessary for dynamically loaded lists during runtime which sometimes can not be compared in certain
        # test cases
        except Exception as e:
            print(e)

    def exit_for(self, dyn_ast, iid):
        # print(f"{self.analysis_name} exit_for {iid}")
        if len(self.iterator_stack) > 0:
            self.iterator_stack.pop()

    
    def end_execution(self) -> None:
        # Count the number of events
        event_count = 0
        for key in self.event:
            event_count += self.event[key]

        # Write the statistics to a file
        with open(f'{self.__class__.__name__}_statistics.txt', 'w') as f:
            f.write(f"DynaPyt_Event_Count: {event_count}\n")
            f.write(f'DynaPyt_Event: {self.event}\n')
            f.write(f'DynaPyt_Unique_Event: {self.unique_event}\n')
            f.write(f"DynaPyt_Violation_Count: {self.violation}\n")
            f.write(f"DynaPyt_Unique_Violation_Count: {self.unique_violation}\n")

# =========================================================================
