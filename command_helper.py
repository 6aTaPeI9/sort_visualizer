class BarCommand:

    @staticmethod
    def execute_command(
        command: str,
        bar_cont: object,
        *args,
        **kwargs
    ):
        COMMANDS = {
            'Swap': BarCommand.swap_bars,
            'Colorized': BarCommand.mark_bar_color
        }

        method = COMMANDS.get(command)

        if not method:
            Warning(f'Указанный метод {method} не реализован.')
            return

        return method(bar_cont, *args, **kwargs)

    @staticmethod
    def swap_bars(
        bar_cont: object,
        left_bar_index: int,
        right_bar_index: int,
        **kwargs
    ) -> None:
        temp_heigt = bar_cont[left_bar_index]._height
        bar_cont[left_bar_index].set_height(bar_cont[right_bar_index]._height)
        bar_cont[right_bar_index].set_height(temp_heigt)

    @staticmethod
    def mark_bar_color(bar_cont: object, *args, **kwargs):
        for i in [*args]:
            bar_cont[i].set_color({**kwargs}.get('color'))