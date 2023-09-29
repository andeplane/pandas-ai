from abc import ABC, abstractmethod
from typing import Any
from pandasai.helpers.env import is_running_in_console
from ..helpers.df_info import polars_imported

from pandasai.exceptions import MethodNotImplementedError


class IResponseParser(ABC):
    @abstractmethod
    def parse(self, result: dict) -> Any:
        """Runs the parser"""
        raise MethodNotImplementedError


class ResponseParser(IResponseParser):
    _context = None

    def __init__(self, context) -> None:
        self._context = context

    def parse(self, result) -> Any:
        if result["type"] == "dataframe":
            return self.format_dataframe(result)
        elif result["type"] == "plot":
            return self.format_plot(result)
        else:
            return self.format_other(result)

    def format_dataframe(self, result: dict) -> Any:
        # Format and process dataframe
        from ..smart_dataframe import SmartDataframe

        df = result["value"]
        if self._context.engine == "polars":
            if polars_imported:
                import polars as pl

                df = pl.from_pandas(df)

        return SmartDataframe(
            df,
            config=self._context._config.__dict__,
            logger=self._context.logger,
        )

    def format_plot(self, result: dict) -> Any:
        """"""
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg

        # Load the image file
        image = mpimg.imread(result["value"])

        # Display the image
        plt.imshow(image)
        plt.axis("off")
        plt.show(block=is_running_in_console())
        plt.close("all")

    def format_other(self, result) -> Any:
        # Format other results
        return result["value"]