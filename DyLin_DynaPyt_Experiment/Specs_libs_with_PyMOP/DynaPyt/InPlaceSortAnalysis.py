from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from dynapyt.instrument.filters import only

from typing import Any, Callable, Dict, Tuple
import traceback
import warnings

"""
Name: 
UseInplaceSorting

Source:
-

Test description:
Inplace sorting is much faster if a copy is not needed

Why useful in a dynamic analysis approach:
No corresponding static analysis found and we can check if for some runs the
reference to the unsorted list is not needed, indicating for some cases it might be 
useful to skip the sorted() method and do in place sorting.

Discussion:


"""


class InPlaceSortAnalysis(BaseAnalysis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = {}
        self.unique_event = {}
        self.violation = 0
        self.unique_violation = 0

        self.stored_lists = {}
        self.threshold = 1000

    @only(patterns=["sorted"])
    def pre_call(self, dyn_ast: str, iid: int, function: Callable, pos_args, kw_args) -> Any:
        # print(f"{self.analysis_name} pre_call {iid}")
        if function is sorted:
            # we have to keep the list in memory to keep id(pos_args[0]) stable ? nope!
            if self.is_sortable_inplace(pos_args[0]) and len(pos_args[0]) > self.threshold:
                self.stored_lists[id(pos_args[0])] = {
                    "iid": iid,
                    "file_name": dyn_ast,
                    "len": len(pos_args[0]),
                }

    def read_identifier(self, dyn_ast: str, iid: int, val: Any) -> Any:
        # print(f"{self.analysis_name} read id {iid} {dyn_ast}")
        if len(self.stored_lists) > 0 and self.is_sortable_inplace(val):
            self.stored_lists.pop(id(val), None)
        return None

    def is_sortable_inplace(self, obj):
        return hasattr(obj, "sort") and hasattr(obj, "__len__")

    def end_execution(self) -> None:
        for _, l in self.stored_lists.items():
            # Add the event to the event dictionary
            if "violation" not in self.event:
                self.event["violation"] = 1
            else:
                self.event["violation"] += 1

            # Add the violation to the violation dictionary
            self.violation += 1

            # Find the file name and line number of the function in the original file
            call_file_name = l["file_name"]
            call_line_num = BaseAnalysis.iid_to_location(self, l["file_name"], l["iid"]).start_line

            # Add the violation to the unique violation dictionary
            violation_key = f'{call_file_name}:{call_line_num}'
            if violation_key not in self.unique_event:
                self.unique_event[violation_key] = 1
                self.unique_violation += 1  # Increment the unique violation count
            else:
                self.unique_event[violation_key] += 1

            # Print the violation message
            warnings.warn(
                f"Spec - {self.__class__.__name__}: Unnecessary use of sorted(), len:{l['len']} in {l['file_name']}"
                f"File {call_file_name}, line {call_line_num}.")

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
