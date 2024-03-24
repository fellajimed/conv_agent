import shutil
from rich.console import Console
from rich.style import Style
from rich.prompt import Prompt
from rich.table import Table


class QAFormatterIO:
    console = Console()
    prompt_style = "[bold green]"
    print_style = Style(color="cyan", bold=True)

    def __init__(self, is_table=True, width=None):
        self.input_msg = f"{self.prompt_style}>>> prompt"
        self.is_table = is_table
        # use terminal' width if width is None
        self.width = (shutil.get_terminal_size((100, 20)).columns
                      if width is None else width)

    def ask(self):
        return Prompt.ask(self.input_msg, show_default=False)

    def answer(self, response):
        if self.is_table:
            table = Table(show_header=False, width=self.width)
            table.add_row(response)
            self.console.print(table, style=self.print_style)
        else:
            self.console.print(response, style=self.print_style)
