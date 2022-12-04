import prettytable as pt
import textwrap
from typing import List, Optional

_MAX_WIDTH = 15

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
    max_width: Optional[int] = _MAX_WIDTH,
    column_align: Optional[List[PrettyTableColumnAlign]] = None) -> str:
    """
    Build a data table.

    @params:
        - header : array( :str )
        - data : array(array( :str ))
        - column_align : array( :PrettyTableColumnAlign ) = None
    """

    table = pt.PrettyTable(headers, max_width=max_width)

    table.border = True
    table.preserve_internal_border = True
    table.hrules = pt.ALL

    if column_align is not None:
        for col_align in column_align:
            table.align[col_align.column] = col_align.align

    table.add_rows(data)

    res_table = f"<pre>{table}</pre>"

    return res_table

def text_wrapping(text: str, max_width: Optional[int] = _MAX_WIDTH, placholder: Optional[str] = "...") -> str:
    """
    Wrap text if to long

    @params
        - text : str
        - placeholder : str = "..."
    """
    return textwrap.shorten(text, width=max_width, placeholder=placholder)

def preference_response(territory, championship, group, team):
    message = f"<b>Territorio: </b> {territory} \n<b>Campionato: </b> {championship} \n<b>Girone: </b> {group} \n<b>Squadra: </b> {team}"

    return message;

