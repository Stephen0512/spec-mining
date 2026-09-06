from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from dynapyt.instrument.filters import only

from typing import Any
import warnings

"""
Name: 
Concat strings

Source:
https://peps.python.org/pep-0008/#programming-recommendations

Test description:
String concatenation via + is only (sometimes) efficient in CPython because they implemented
in place concatenation. However, other interpreters don't have this capability.
To ensure linear time string concatenation use ''.join()

Why useful in a dynamic analysis approach:
Dynamic analysis is able to infer whether plus operator is used between strings if variables are 
not constants

Discussion:

"""


class StringConcatAnalysis(BaseAnalysis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = {}
        self.unique_event = {}
        self.violation = 0
        self.unique_violation = 0

        self.concats = {}
        self.adds = {}
        self.last_add_operation = None
        self.threshold = 10000

    def add_assign(self, dyn_ast: str, iid: int, left: Any, right: Any) -> None:
        # for some reason left is a lambda
        # print(f"{self.analysis_name} += {iid}")
        self._check(dyn_ast, iid, right)

    def _check(self, dyn_ast: str, iid: int, right: Any, result: Any = None) -> None:
        if isinstance(right, type("")):
            key = str(iid) + "_" + dyn_ast
            if key not in self.concats:
                self.concats[key] = 1
            elif self.concats[key] != -1:
                self.concats[key] += 1
            if self.concats[key] > self.threshold:
                # Add the event to the event dictionary
                if "string_concat" not in self.event:
                    self.event["string_concat"] = 1
                else:
                    self.event["string_concat"] += 1

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
                warnings.warn(f'Spec - {self.__class__.__name__}: Attempted to concat strings alot with + operator at file {call_file_name}, line {call_line_num}.')

    # Removed below hooks for performance reasons
    # def add(self, dyn_ast: str, iid: int, left: Any, right: Any, result: Any) -> None:
    #     if isinstance(right, type("")):
    #         self.last_add_operation = {"iid": iid, "result": result}
    #     else:
    #         self.last_add_operation = None

    # # Only a += b or a = a + b is bad not a+b+c -> add check for a = a + b
    # def write(self, dyn_ast: str, iid: int, old_val: Any, new_val: Any) -> None:
    #     if isinstance(new_val, type("")):
    #         if self.last_add_operation is not None and self.last_add_operation["iid"] == iid - 1:
    #             if new_val == self.last_add_operation["result"]:
    #                 self._check(dyn_ast, iid, new_val)

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
