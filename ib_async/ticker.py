"""Access to realtime market information."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Optional, Union

from eventkit import Event, Op

from ib_async.contract import Contract
from ib_async.objects import (
    Dividends,
    DOMLevel,
    FundamentalRatios,
    IBDefaults,
    MktDepthData,
    OptionComputation,
    TickByTickAllLast,
    TickByTickBidAsk,
    TickByTickMidPoint,
    TickData,
)
from ib_async.util import dataclassRepr, isNan

nan = float("nan")


@dataclass
class Ticker:
    """
    Current market data such as bid, ask, last price, etc. for a contract.

    Streaming level-1 ticks of type :class:`.TickData` are stored in
    the ``ticks`` list.

    Streaming level-2 ticks of type :class:`.MktDepthData` are stored in the
    ``domTicks`` list. The order book (DOM) is available as lists of
    :class:`.DOMLevel` in ``domBids`` and ``domAsks``.

    Streaming tick-by-tick ticks are stored in ``tickByTicks``.

    For options the :class:`.OptionComputation` values for the bid, ask, resp.
    last price are stored in the ``bidGreeks``, ``askGreeks`` resp.
    ``lastGreeks`` attributes. There is also ``modelGreeks`` that conveys
    the greeks as calculated by Interactive Brokers' option model.

    Events:
        * ``updateEvent`` (ticker: :class:`.Ticker`)
    """

    events: ClassVar = ("updateEvent",)

    contract: Contract | None = None
    time: datetime | None = None
    timestamp: float | None = None
    marketDataType: int = 1
    minTick: float = nan
    bid: float = nan
    bidSize: float = nan
    bidExchange: str = ""
    ask: float = nan
    askSize: float = nan
    askExchange: str = ""
    last: float = nan
    lastSize: float = nan
    lastExchange: str = ""
    lastTimestamp: datetime | None = None
    prevBid: float = nan
    prevBidSize: float = nan
    prevAsk: float = nan
    prevAskSize: float = nan
    prevLast: float = nan
    prevLastSize: float = nan
    volume: float = nan
    open: float = nan
    high: float = nan
    low: float = nan
    close: float = nan
    vwap: float = nan
    low13week: float = nan
    high13week: float = nan
    low26week: float = nan
    high26week: float = nan
    low52week: float = nan
    high52week: float = nan
    bidYield: float = nan
    askYield: float = nan
    lastYield: float = nan
    markPrice: float = nan
    halted: float = nan
    rtHistVolatility: float = nan
    rtVolume: float = nan
    rtTradeVolume: float = nan
    rtTime: Optional[datetime] = None
    avVolume: float = nan
    tradeCount: float = nan
    tradeRate: float = nan
    volumeRate: float = nan
    volumeRate3Min: float = nan
    volumeRate5Min: float = nan
    volumeRate10Min: float = nan
    shortable: float = nan
    shortableShares: float = nan
    indexFuturePremium: float = nan
    futuresOpenInterest: float = nan
    putOpenInterest: float = nan
    callOpenInterest: float = nan
    putVolume: float = nan
    callVolume: float = nan
    avOptionVolume: float = nan
    histVolatility: float = nan
    impliedVolatility: float = nan
    dividends: Optional[Dividends] = None
    fundamentalRatios: Optional[FundamentalRatios] = None
    ticks: list[TickData] = field(default_factory=list)
    tickByTicks: list[
        Union[TickByTickAllLast, TickByTickBidAsk, TickByTickMidPoint]
    ] = field(default_factory=list)
    domBids: list[DOMLevel] = field(default_factory=list)
    domBidsDict: dict[int, DOMLevel] = field(default_factory=dict)
    domAsks: list[DOMLevel] = field(default_factory=list)
    domAsksDict: dict[int, DOMLevel] = field(default_factory=dict)
    domTicks: list[MktDepthData] = field(default_factory=list)
    bidGreeks: Optional[OptionComputation] = None
    askGreeks: Optional[OptionComputation] = None
    lastGreeks: Optional[OptionComputation] = None
    modelGreeks: Optional[OptionComputation] = None
    auctionVolume: float = nan
    auctionPrice: float = nan
    auctionImbalance: float = nan
    regulatoryImbalance: float = nan
    bboExchange: str = ""
    snapshotPermissions: int = 0

    defaults: IBDefaults = field(default_factory=IBDefaults, repr=False)
    created: bool = False

    def __post_init__(self):
        # when copying a dataclass, the __post_init__ runs again, so we
        # want to make sure if this was _already_ created, we don't overwrite
        # everything with _another_ post_init clear.
        if not self.created:
            self.updateEvent = TickerUpdateEvent("updateEvent")
            self.minTick = self.defaults.unset
            self.bid = self.defaults.unset
            self.bidSize = self.defaults.unset
            self.ask = self.defaults.unset
            self.askSize = self.defaults.unset
            self.last = self.defaults.unset
            self.lastSize = self.defaults.unset
            self.prevBid = self.defaults.unset
            self.prevBidSize = self.defaults.unset
            self.prevAsk = self.defaults.unset
            self.prevAskSize = self.defaults.unset
            self.prevLast = self.defaults.unset
            self.prevLastSize = self.defaults.unset
            self.volume = self.defaults.unset
            self.open = self.defaults.unset
            self.high = self.defaults.unset
            self.low = self.defaults.unset
            self.close = self.defaults.unset
            self.vwap = self.defaults.unset
            self.low13week = self.defaults.unset
            self.high13week = self.defaults.unset
            self.low26week = self.defaults.unset
            self.high26week = self.defaults.unset
            self.low52week = self.defaults.unset
            self.high52week = self.defaults.unset
            self.bidYield = self.defaults.unset
            self.askYield = self.defaults.unset
            self.lastYield = self.defaults.unset
            self.markPrice = self.defaults.unset
            self.halted = self.defaults.unset
            self.rtHistVolatility = self.defaults.unset
            self.rtVolume = self.defaults.unset
            self.rtTradeVolume = self.defaults.unset
            self.avVolume = self.defaults.unset
            self.tradeCount = self.defaults.unset
            self.tradeRate = self.defaults.unset
            self.volumeRate = self.defaults.unset
            self.volumeRate3Min = self.defaults.unset
            self.volumeRate5Min = self.defaults.unset
            self.volumeRate10Min = self.defaults.unset
            self.shortable = self.defaults.unset
            self.shortableShares = self.defaults.unset
            self.indexFuturePremium = self.defaults.unset
            self.futuresOpenInterest = self.defaults.unset
            self.putOpenInterest = self.defaults.unset
            self.callOpenInterest = self.defaults.unset
            self.putVolume = self.defaults.unset
            self.callVolume = self.defaults.unset
            self.avOptionVolume = self.defaults.unset
            self.histVolatility = self.defaults.unset
            self.impliedVolatility = self.defaults.unset
            self.auctionVolume = self.defaults.unset
            self.auctionPrice = self.defaults.unset
            self.auctionImbalance = self.defaults.unset
            self.regulatoryImbalance = self.defaults.unset

            self.created = True

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)

    __repr__ = dataclassRepr
    __str__ = dataclassRepr

    def isUnset(self, value) -> bool:
        # if default value is nan and value is nan, it is unset.
        # else, if value matches default value, it is unset.
        dev = self.defaults.unset
        return (dev != dev and value != value) or (value == dev)

    def hasBidAsk(self) -> bool:
        """See if this ticker has a valid bid and ask."""
        return (
            self.bid != -1
            and not self.isUnset(self.bid)
            and self.bidSize > 0
            and self.ask != -1
            and not self.isUnset(self.ask)
            and self.askSize > 0
        )

    def midpoint(self) -> float:
        """
        Return average of bid and ask, or defaults.unset if no valid bid and ask
        are available.
        """
        return (self.bid + self.ask) * 0.5 if self.hasBidAsk() else self.defaults.unset

    def marketPrice(self) -> float:
        """
        Return the first available one of

        * last price if within current bid/ask or no bid/ask available;
        * average of bid and ask (midpoint).
        """
        if self.hasBidAsk():
            if self.bid <= self.last <= self.ask:
                price = self.last
            else:
                price = self.midpoint()
        else:
            price = self.last

        return price


class TickerUpdateEvent(Event):
    __slots__ = ()

    def trades(self) -> "Tickfilter":
        """Emit trade ticks."""
        return Tickfilter((4, 5, 48, 68, 71), self)

    def bids(self) -> "Tickfilter":
        """Emit bid ticks."""
        return Tickfilter((0, 1, 66, 69), self)

    def asks(self) -> "Tickfilter":
        """Emit ask ticks."""
        return Tickfilter((2, 3, 67, 70), self)

    def bidasks(self) -> "Tickfilter":
        """Emit bid and ask ticks."""
        return Tickfilter((0, 1, 66, 69, 2, 3, 67, 70), self)

    def midpoints(self) -> "Tickfilter":
        """Emit midpoint ticks."""
        return Midpoints((), self)


class Tickfilter(Op):
    """Tick filtering event operators that ``emit(time, price, size)``."""

    __slots__ = ("_tickTypes",)

    def __init__(self, tickTypes, source=None):
        Op.__init__(self, source)
        self._tickTypes = set(tickTypes)

    def on_source(self, ticker):
        for t in ticker.ticks:
            if t.tickType in self._tickTypes:
                self.emit(t.time, t.price, t.size)

    def timebars(self, timer: Event) -> "TimeBars":
        """
        Aggregate ticks into time bars, where the timing of new bars
        is derived from a timer event.
        Emits a completed :class:`Bar`.

        This event stores a :class:`BarList` of all created bars in the
        ``bars`` property.

        Args:
            timer: Event for timing when a new bar starts.
        """
        return TimeBars(timer, self)

    def tickbars(self, count: int) -> "TickBars":
        """
        Aggregate ticks into bars that have the same number of ticks.
        Emits a completed :class:`Bar`.

        This event stores a :class:`BarList` of all created bars in the
        ``bars`` property.

        Args:
            count: Number of ticks to use to form one bar.
        """
        return TickBars(count, self)

    def volumebars(self, volume: int) -> "VolumeBars":
        """
        Aggregate ticks into bars that have the same volume.
        Emits a completed :class:`Bar`.

        This event stores a :class:`BarList` of all created bars in the
        ``bars`` property.

        Args:
            count: Number of ticks to use to form one bar.
        """
        return VolumeBars(volume, self)


class Midpoints(Tickfilter):
    __slots__ = ()

    def on_source(self, ticker):
        if ticker.ticks:
            self.emit(ticker.time, ticker.midpoint(), 0)


@dataclass
class Bar:
    time: Optional[datetime]
    open: float = nan
    high: float = nan
    low: float = nan
    close: float = nan
    volume: int = 0
    count: int = 0


class BarList(list[Bar]):
    def __init__(self, *args):
        super().__init__(*args)
        self.updateEvent = Event("updateEvent")

    def __eq__(self, other) -> bool:
        return self is other


class TimeBars(Op):
    __slots__ = (
        "_timer",
        "bars",
    )
    __doc__ = Tickfilter.timebars.__doc__

    bars: BarList

    def __init__(self, timer, source=None):
        Op.__init__(self, source)
        self._timer = timer
        self._timer.connect(self._on_timer, None, self._on_timer_done)
        self.bars = BarList()

    def on_source(self, time, price, size):
        if not self.bars:
            return
        bar = self.bars[-1]

        if isNan(bar.open):
            bar.open = bar.high = bar.low = price

        bar.high = max(bar.high, price)
        bar.low = min(bar.low, price)
        bar.close = price
        bar.volume += size
        bar.count += 1
        self.bars.updateEvent.emit(self.bars, False)

    def _on_timer(self, time):
        if self.bars:
            bar = self.bars[-1]
            if self.isUnset(bar.close) and len(self.bars) > 1:
                bar.open = bar.high = bar.low = bar.close = self.bars[-2].close

            self.bars.updateEvent.emit(self.bars, True)
            self.emit(bar)

        self.bars.append(Bar(time))

    def _on_timer_done(self, timer):
        self._timer = None
        self.set_done()


class TickBars(Op):
    __slots__ = ("_count", "bars")
    __doc__ = Tickfilter.tickbars.__doc__

    bars: BarList

    def __init__(self, count, source=None):
        Op.__init__(self, source)
        self._count = count
        self.bars = BarList()

    def on_source(self, time, price, size):
        if not self.bars or self.bars[-1].count == self._count:
            bar = Bar(time, price, price, price, price, size, 1)
            self.bars.append(bar)
        else:
            bar = self.bars[-1]
            bar.high = max(bar.high, price)
            bar.low = min(bar.low, price)
            bar.close = price
            bar.volume += size
            bar.count += 1
        if bar.count == self._count:
            self.bars.updateEvent.emit(self.bars, True)
            self.emit(self.bars)


class VolumeBars(Op):
    __slots__ = ("_volume", "bars")
    __doc__ = Tickfilter.volumebars.__doc__

    bars: BarList

    def __init__(self, volume, source=None):
        Op.__init__(self, source)
        self._volume = volume
        self.bars = BarList()

    def on_source(self, time, price, size):
        if not self.bars or self.bars[-1].volume >= self._volume:
            bar = Bar(time, price, price, price, price, size, 1)
            self.bars.append(bar)
        else:
            bar = self.bars[-1]
            bar.high = max(bar.high, price)
            bar.low = min(bar.low, price)
            bar.close = price
            bar.volume += size
            bar.count += 1
        if bar.volume >= self._volume:
            self.bars.updateEvent.emit(self.bars, True)
            self.emit(self.bars)
