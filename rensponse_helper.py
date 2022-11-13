import prettytable as pt
import textwrap
from typing import List, Optional

_MAX_WIDTH = 18

class PrettyTableColumnAlign():

    LEFT = 'l' # lefT
    RIGHT = 'r' # right
    CENTER = 'c' # center

    def __init__(self, column: str, align: str):
        self.column = column
        self.align = align

def get_response_table(
    headers: List[str],
    data: List[List[str]],
    column_align: Optional[List[PrettyTableColumnAlign]] = None) -> str:
    """
    Build a data table.

    @params:
        - header : array( :str )
        - data : array(array( :str ))
        - column_align : array( :PrettyTableColumnAlign ) = None
    """

    table = pt.PrettyTable(headers, max_width=_MAX_WIDTH)

    table.border = False
    table.preserve_internal_border = True
    table.vrules = pt.NONE
    table.hrules = pt.HEADER

    if column_align is not None:
        for col_align in column_align:
            table.align[col_align.column] = col_align.align

    table.add_rows(data)

    res_table = f"<pre>{table}</pre>"

    return res_table

def text_wrapping(text: str, placholder: Optional[str] = "...") -> str:
    """
    Wrap text if to long

    @params
        - text : str
        - placeholder : str = "..."
    """
    return textwrap.shorten(text, width=_MAX_WIDTH, placeholder=placholder)
