"""Base class for price-based backtesting strategies."""

from abc import ABC, abstractmethod
from collections.abc import Sequence


class Strategy(ABC):
    """Return a target portfolio exposure at each observed closing price.

    ``on_bar`` is called after observing the current close. The returned target
    exposure is held over the following close-to-close interval. Exposure is a
    fraction of current equity: ``1`` is fully long, ``0`` is flat, and ``-1``
    is fully short. Implementations should use ``history`` only through the
    current index.
    """

    @abstractmethod
    def on_bar(self, index: int, price: float, history: Sequence[float]) -> float:
        """Return the target exposure for the next interval."""
