from typing import Any, Dict, List, Literal, Optional, TYPE_CHECKING, Union
from typing_extensions import NotRequired, TypedDict

from amis.event import EventAction, OnEvent
from amis.typing import DataMapping, DictStrAny, Expression

from .types import AmisNode, API, SchemaNode, Template

from pydantic import Field

if TYPE_CHECKING:
    from .data_input import Form
    from .feature import Action, PopOver
    from .other import Badge


class CRUD(AmisNode):
    """增删改查"""

    class Messages(TypedDict):
        fetchFailed: NotRequired[str]
        """获取失败时提示"""
        saveOrderFailed: NotRequired[str]
        """保存顺序失败提示"""
        saveOrderSuccess: NotRequired[str]
        """保存顺序成功提示"""
        quickSaveFailed: NotRequired[str]
        """快速保存失败提示"""
        quickSaveSuccess: NotRequired[str]
        """快速保存成功提示"""

    class FilterTogglable(TypedDict):
        label: NotRequired[str]
        icon: NotRequired[str]
        activeLabel: NotRequired[str]
        activeIcon: NotRequired[str]

    type: Literal["crud"] = Field(default="crud", init=False)
    """type 指定为 CRUD 渲染器"""
    mode: Literal["table", "cards", "list"] = "table"
    """"table" 、 "cards" 或者 "list"""
    title: str = ""
    """可设置成空，当设置成空时，没有标题栏"""
    className: Optional[str] = None
    """表格外层 Dom 的类名"""
    api: Optional[API] = None
    """CRUD 用来获取列表数据的 api。"""
    loadDataOnce: Optional[bool] = None
    """是否一次性加载所有数据（前端分页）"""
    loadDataOnceFetchOnFilter: bool = True
    """在开启 loadDataOnce 时，filter 时是否去重新请求 api"""
    source: Optional[str] = None
    """数据映射接口返回某字段的值，不设置会默认使用接口返回的${items}或者${rows}，也可以设置成上层数据源的内容"""
    filter: Optional["Form"] = None
    """设置过滤器，当该表单提交后，会把数据带给当前 mode 刷新列表。"""
    filterTogglable: Union[bool, FilterTogglable] = False
    """是否可显隐过滤器"""
    filterDefaultVisible: bool = True
    """设置过滤器默认是否可见。"""
    initFetch: bool = True
    """是否初始化的时候拉取数据, 只针对有 filter 的情况, 没有 filter 初始都会拉取数据"""
    interval: Optional[int] = Field(ge=1000)
    """刷新时间(最低 1000)"""
    silentPolling: bool = False
    """配置刷新时是否隐藏加载动画"""
    stopAutoRefreshWhen: str = ""
    """通过表达式来配置停止刷新的条件"""
    stopAutoRefreshWhenModalIsOpen: bool = False
    """当有弹框时关闭自动刷新，关闭弹框又恢复"""
    syncLocation: bool = True
    """是否将过滤条件的参数同步到地址栏, !!!开启后可能改变数据类型,无法通过fastpi数据校验"""
    draggable: bool = False
    """是否可通过拖拽排序"""
    resizable: bool = True
    """是否可以调整列宽度"""
    itemDraggableOn: Optional[bool] = None
    """用表达式来配置是否可拖拽排序"""
    saveOrderApi: Optional[API] = None
    """保存排序的 api。"""
    quickSaveApi: Optional[API] = None
    """快速编辑后用来批量保存的 API。"""
    quickSaveItemApi: Optional[API] = None
    """快速编辑配置成及时保存时使用的 API。"""
    bulkActions: Optional[List["Action"]] = None
    """批量操作列表，配置后，表格可进行选中操作。"""
    messages: Optional[Messages] = None
    """覆盖消息提示，如果不指定，将采用 api 返回的 message"""
    primaryField: str = "id"
    """设置 ID 字段名。'id'"""
    perPage: int = 10
    """设置一页显示多少条数据."""
    orderBy: Optional[str] = None
    """默认排序字段，这个是传给后端，需要后端接口实现"""
    orderDir: Optional[Literal["asc", "desc"]] = None
    """排序方向"""
    defaultParams: Optional[DictStrAny] = None
    """设置默认 filter 默认参数，会在查询的时候一起发给后端"""
    pageField: str = "page"
    """设置分页页码字段名。"""
    perPageField: str = "perPage"
    """设置分页一页显示的多少条数据的字段名。注意：最好与 defaultParams 一起使用，请看下面例子。"""
    perPageAvailable: List[int] = [5, 10, 20, 50, 100]
    """设置一页显示多少条数据下拉框可选条数。"""
    orderField: Optional[str] = None
    """设置用来确定位置的字段名，设置后新的顺序将被赋值到该字段中。"""
    hideQuickSaveBtn: bool = False
    """隐藏顶部快速保存提示"""
    autoJumpToTopOnPagerChange: bool = False
    """当切分页的时候，是否自动跳顶部。"""
    syncResponse2Query: bool = True
    """将返回数据同步到过滤器上。"""
    keepItemSelectionOnPageChange: bool = True
    """保留条目选择，默认分页、搜素后，用户选择条目会被清空，开启此选项后会保留用户选择，可以实现跨页面批量操作。"""
    labelTpl: Optional[str] = None
    """
    单条描述模板，keepItemSelectionOnPageChange
    设置为true后会把所有已选择条目列出来，此选项可以用来定制条目展示文案。
    """
    headerToolbar: Optional[List] = None  # TODO 确定类型
    """顶部工具栏配置"""
    footerToolbar: Optional[List] = None
    """底部工具栏配置"""
    alwaysShowPagination: bool = False
    """是否总是显示分页"""
    affixHeader: bool = True
    """是否固定表头(table 下)"""
    autoGenerateFilter: Optional[Union[dict, bool]] = None
    """是否开启查询区域，开启后会根据列元素的 searchable 属性值，自动生成查询条件表单"""
    resetPageAfterAjaxItemAction: bool = False
    """单条数据 ajax 操作后是否重置页码为第一页"""
    autoFillHeight: Optional[Union[bool, dict]] = None
    """内容区域自适应高度"""
    itemAction: Optional["Action"] = None
    """实现点击某一行后进行自定义操作，支持 action 里的所有配置，比如弹框、刷新其它组件等。"""
    # defaultChecked: Optional[bool] = None
    # """当可批量操作时，默认是否全部勾选。"""
    onEvent: OnEvent[
        Literal[
            "selectedChange",
            "columnSort",
            "columnFilter",
            "columnSearch",
            "orderChange",
            "columnToggled",
            "rowClick",
            "rowMouseEnter",
            "rowMouseLeave",
        ]
    ] = None


class Table(AmisNode):
    """表格"""

    class SelectAction(EventAction):
        class Args(TypedDict):
            selected: str

        actionType: Literal["select"] = Field(default="select", init=False)
        description: Optional[str] = None
        args: Args

    class InitDragAction(EventAction):
        actionType: Literal["initDrag"] = Field(default="initDrag", init=False)

    class Column(AmisNode):
        """列配置"""

        class Copyable(TypedDict):
            icon: NotRequired[str]
            content: NotRequired[str]

        # type: Optional[str] = None
        # """Literal['text','audio','image','link','tpl','mapping','carousel','date',
        # 'progress','status','switch','list','json','operation']"""
        label: Optional[Template] = None
        """表头文本内容"""
        name: Optional[str] = None
        """通过名称关联数据"""
        width: Optional[Union[int, str]] = None
        """列宽"""
        remark: Optional["Remark"] = None
        """提示信息"""
        fixed: Optional[Literal["left", "right", "none"]] = None
        """是否固定当前列"""
        popOver: Optional["PopOver"] = None
        """弹出框"""
        copyable: Union[bool, Copyable, None] = None
        """是否可复制"""
        style: Optional[DictStrAny] = None
        """单元格自定义样式"""
        innerStyle: Optional[DictStrAny] = None
        """单元格内部组件自定义样式"""

    type: Literal["table"] = Field(default="table", init=False)
    """指定为 table 渲染器"""
    title: Optional[str] = None
    """标题"""
    source: Optional[str] = None
    """数据源, 绑定当前环境变量"""
    affixHeader: bool = True
    """是否固定表头"""
    columnsTogglable: Union[str, bool] = "auto"
    """展示列显示开关, 自动即：列数量大于或等于 5 个时自动开启"""
    placeholder: str = "暂无数据"
    """当没数据的时候的文字提示"""
    className: str = "panel-default"
    """外层 CSS 类名"""
    tableClassName: str = "table-db table-striped"
    """表格 CSS 类名"""
    headerClassName: str = "Action.md-table-header"
    """顶部外层 CSS 类名"""
    footerClassName: str = "Action.md-table-footer"
    """底部外层 CSS 类名"""
    toolbarClassName: str = "Action.md-table-toolbar"
    """工具栏 CSS 类名"""
    columns: Optional[List[Column]] = None
    """用来设置列信息"""
    combineNum: Optional[int] = None
    """自动合并单元格"""
    itemActions: Optional[List["Action"]] = None
    """悬浮行操作按钮组"""
    itemCheckableOn: Optional[Expression] = None
    """配置当前行是否可勾选的条件，要用 表达式"""
    itemDraggableOn: Optional[Expression] = None
    """配置当前行是否可拖拽的条件，要用 表达式"""
    checkOnItemClick: bool = False
    """点击数据行是否可以勾选当前行"""
    rowClassName: Optional[str] = None
    """给行添加 CSS 类名"""
    rowClassNameExpr: Optional[Template] = None
    """通过模板给行添加 CSS 类名"""
    prefixRow: Optional[list] = None
    """顶部总结行"""
    affixRow: Optional[list] = None
    """底部总结行"""
    itemBadge: Optional["Badge"] = None
    """行角标配置"""
    autoFillHeight: Optional[Union[bool, dict]] = None
    """内容区域自适应高度"""
    resizable: bool = True
    """列宽度是否支持调整"""
    selectable: bool = False
    """支持勾选"""
    multiple: bool = False
    """勾选 icon 是否为多选样式checkbox， 默认为radio"""
    onEvent: OnEvent[
        Literal[
            "selectedChange",
            "columnSort",
            "columnFilter",
            "columnSearch",
            "orderChange",
            "columnToggled",
            "rowClick",
            "rowDbClick",
            "rowMouseEnter",
            "rowMouseLeave",
        ]
    ] = None


class TableView(AmisNode):
    """表格展现，详见https://aisuda.bce.baidu.com/amis/zh-CN/components/table-view"""

    class Tds(AmisNode):
        """单元格设置"""

        weight: Union[int, str, None] = None
        """宽度"""
        background: Optional[str] = None
        """单元格背景色"""
        color: Optional[str] = None
        """单元格文字颜色"""
        bold: bool = False
        """单元格文字是否加粗"""
        width: Union[int, str, None] = None
        """单元格宽度，只需要设置第一行"""
        padding: Union[int, str, None] = None
        """单元格内间距"""
        align: Literal["left", "center", "right"] = "left"
        """单元格内的水平对齐，可以是 left、center、right"""
        valign: Literal["top", "middle", "bottom", "baseline"] = "middle"
        """单元格内的垂直对齐，可以是 top、middle、bottom、baseline"""
        colspan: Optional[int] = None
        """单元格水平跨几行"""
        rowspan: Optional[int] = None
        """单元格垂直跨几列"""
        body: Optional[SchemaNode] = None
        """其它 amis 设置"""

    class Trs(AmisNode):
        """行设置"""

        height: Union[int, str, None] = None
        """高度"""
        background: Optional[str] = None
        """行背景色"""
        tds: Optional[List["TableView.Tds"]] = None

    type: Literal["table-view"] = Field(default="table-view", init=False)
    """指定为 table-view 渲染器"""
    trs: Optional[List[Union[dict, Trs]]] = None
    """行配置"""
    width: Union[int, str, None] = None
    """宽度"""
    padding: Union[int, str, None] = None
    """单元格默认内间距"""
    border: bool = True
    """是否显示边框"""
    borderColor: Optional[str] = None
    """边框颜色"""
    caption: Optional[str] = None
    """添加段标题文本"""
    captionSide: Optional[Literal["top", "bottom"]] = None
    """控制标题显示在底部还是顶部。"""


class Calendar(AmisNode):
    """日历日程"""

    class Schedules(AmisNode):
        """日程"""

        startTime: str
        """开始时间"""
        endTime: Optional[str] = None
        """结束时间"""
        content: Any = ""
        """内容"""
        className: Optional[str] = None
        """样式类名"""

    type: Literal["calendar"] = Field(default="calendar", init=False)
    """指定为 calender 渲染器"""
    schedules: Optional[List[Union[dict, Schedules]]] = None
    """日历中展示日程，可设置静态数据或从上下文中取数据，startTime 和 endTime 格式参考文档，className 参考背景色"""
    scheduleClassNames: List[str] = ["bg-warning", "bg-danger", "bg-success", "bg-info", "bg-secondary"]
    """日历中展示日程的颜色，参考背景色"""
    scheduleAction: Optional[List["Action"]] = None
    """自定义日程展示"""
    largeMode: bool = False
    """放大模式"""
    todayActiveStyle: Optional[DictStrAny] = None
    """今日激活时的自定义样式"""
    onEvent: OnEvent[Literal["change"]] = None


class Card(AmisNode):
    """卡片"""

    class Header(AmisNode):
        """头部内容"""

        className: Optional[str] = None
        """样式类名"""
        title: Optional[Template] = None
        """标题"""
        titleClassName: Optional[str] = None
        """标题类名"""
        subTitle: Optional[Template] = None
        """副标题"""
        subTitleClassName: Optional[str] = None
        """副标题类名"""
        subTitlePlaceholder: Optional[str] = None
        """副标题占位"""
        description: Optional[Template] = None
        """描述"""
        descriptionClassName: Optional[str] = None
        """描述类名"""
        descriptionPlaceholder: Optional[str] = None
        """描述占位"""
        avatar: Optional[Template] = None
        """图片"""
        avatarClassName: str = "pull-left thumb avatar b-3x m-r"
        """图片包括层类名"""
        imageClassName: Optional[str] = None
        """图片类名"""
        avatarText: Optional[Template] = None
        """如果不配置图片，则会在图片处显示该文本"""
        avatarTextBackground: Optional[List[str]] = None
        """设置文本背景色，它会根据数据分配一个颜色"""
        avatarTextClassName: Optional[str] = None
        """图片文本类名"""
        highlight: Union[bool, Template] = False
        """是否显示激活样式"""
        highlightClassName: Optional[str] = None
        """激活样式类名"""
        href: Optional[Template] = None
        """点击卡片跳转的链接地址"""
        blank: bool = True
        """是否新窗口打开"""

    class Media(AmisNode):
        """Card 多媒体部内容设置"""

        type: Optional[Literal["image", "video"]] = None
        """多媒体类型"""
        url: Optional[str] = None
        """图片/视频链接"""
        position: Literal["left", "right", "top", "bottom"] = "left"
        """多媒体位置"""
        className: str = "w-44 h-28"
        """多媒体类名"""
        isLive: bool = False
        """视频是否为直播"""
        autoPlay: bool = False
        """视频是否自动播放"""
        poster: Union[str, bool] = False
        """视频封面"""

    type: Literal["card"] = Field(default="card", init=False)
    """指定为 card 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    href: Optional[Template] = None
    """外部链接"""
    header: Optional[Header] = None
    """Card 头部内容设置"""
    body: Optional[List[SchemaNode]] = None
    """内容容器，主要用来放置非表单项组件"""
    bodyClassName: Optional[str] = None
    """内容区域类名"""
    actions: Optional[List["Action"]] = None
    """配置按钮集合"""
    actionsCount: int = 4
    """按钮集合每行个数"""
    itemAction: Optional["Action"] = None
    """点击卡片的行为"""
    media: Optional[Media] = None
    "Card 多媒体部内容设置"
    secondary: Optional[Template] = None
    """次要说明"""
    toolbar: Optional[List["Action"]] = None
    """工具栏按钮"""
    dragging: bool = False
    """是否显示拖拽图标"""
    selectable: bool = False
    """卡片是否可选"""
    checkable: bool = True
    """卡片选择按钮是否禁用"""
    selected: bool = False
    """卡片选择按钮是否选中"""
    hideCheckToggler: bool = False
    """卡片选择按钮是否隐藏"""
    multiple: bool = False
    """卡片是否为多选"""
    useCardLabel: bool = True
    """卡片内容区的表单项 label 是否使用 Card 内部的样式"""


class Cards(AmisNode):
    """卡片组"""

    type: Literal["cards"] = Field(default="cards", init=False)
    """指定为 cards 渲染器"""
    title: Optional[Template] = None
    """标题"""
    source: Optional[DataMapping] = None
    """数据源, 获取当前数据域中的变量"""
    placeholder: Template = "暂无数据"
    """当没数据的时候的文字提示"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    headerClassName: Optional[str] = None
    """顶部外层 CSS 类名"""
    footerClassName: Optional[str] = None
    """底部外层 CSS 类名"""
    itemClassName: Optional[str] = None
    """卡片 CSS 类名"""
    card: Optional[Card] = None
    """配置卡片信息"""
    selectable: bool = False
    """卡片组是否可选"""
    multiple: bool = True
    """卡片组是否为多选"""
    checkOnItemClick: Optional[bool] = None
    """点选卡片内容是否选中卡片"""


class Carousel(AmisNode):
    """轮播图"""

    class GotoImageAction(EventAction):
        """定位图片"""

        class Args(TypedDict):
            activeIndex: str

        actionType: Literal["goto-image"] = Field(default="goto-image", init=False)
        args: Args

    class Multiple(TypedDict):
        count: NotRequired[int]

    class Icon(TypedDict):  # TODO 确定类型
        prev: NotRequired[DictStrAny]
        next: NotRequired[DictStrAny]

    class Options(AmisNode):
        image: Optional[str] = None
        """图片链接"""
        href: Optional[str] = None
        """图片打开网址的链接"""
        imageClassName: Optional[str] = None
        """图片类名"""
        title: Optional[str] = None
        """图片标题"""
        titleClassName: Optional[str] = None
        """图片标题类名"""
        description: Optional[str] = None
        """图片描述"""
        descriptionClassName: Optional[str] = None
        """图片描述类名"""
        html: Optional[str] = None
        """HTML 自定义，同Tpl一致"""

    type: Literal["carousel"] = Field(default="carousel", init=False)
    """指定为 Carousel 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    options: List[Options] = []
    """轮播面板数据"""
    itemSchema: Optional[SchemaNode] = None
    """自定义schema来展示数据"""
    auto: bool = True
    """是否自动轮播"""
    interval: str = "5s"
    """切换动画间隔"""
    duration: int = 500
    """ 切换动画时长"""
    width: str = "auto"
    """宽度"""
    height: str = "200px"
    """高度"""
    controls: List[str] = ["dots", "arrows"]
    """显示左右箭头、底部圆点索引"""
    controlsTheme: str = "light"
    """左右箭头、底部圆点索引颜色，默认light，另有dark模式"""
    animation: str = "fade"
    """切换动画效果，默认fade，另有slide模式"""
    thumbMode: Optional[Literal["cover", "contain"]] = None
    """图片默认缩放模式"""
    multiple: Optional[Multiple] = None
    """多图展示，count表示展示的数量"""
    alwaysShowArrow: bool = False
    """是否一直显示箭头，为false时鼠标hover才会显示"""
    icons: Optional[Icon] = None
    """自定义箭头图标"""
    onEvent: OnEvent[Literal["change"]] = None


class Chart(AmisNode):
    """图表: https://echarts.apache.org/zh/option.html#title"""

    class ShowTipAction(EventAction):
        """显示提示"""

        class Args(TypedDict):
            type: str
            seriesIndex: int
            name: str
            dataIndex: int

        actionType: Literal["showTip"] = Field(default="showTip", init=False)
        args: Args

    type: Literal["chart"] = Field(default="chart", init=False)
    """指定为 chart 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    body: Optional[SchemaNode] = None
    """内容容器"""
    api: Optional[API] = None
    """配置项接口地址"""
    source: Optional[DataMapping] = None
    """通过数据映射获取数据链中变量值作为配置"""
    initFetch: Optional[bool] = None
    """组件初始化时，是否请求接口"""
    interval: Optional[int] = Field(ge=1000)
    """刷新时间(最小 1000)"""
    config: Optional[Union[DictStrAny, str]] = None
    """设置 eschars 的配置项,当为string的时候可以设置 function 等配置项"""
    style: Optional[DictStrAny] = None
    """设置根元素的 style"""
    width: Optional[str] = None
    """设置根元素的宽度"""
    height: Optional[str] = None
    """设置根元素的高度"""
    replaceChartOption: bool = False
    """每次更新是完全覆盖配置项还是追加？"""
    trackExpression: Optional[str] = None
    """当这个表达式的值有变化时更新图表"""
    dataFilter: Optional[str] = None
    """
    自定义 echart config 转换，函数签名：function(config, echarts, data) {return config;}
     配置时直接写函数体。其中 config 是当前 echart 配置，echarts 就是 echarts 对象，data 为上下文数据。
    """
    mapURL: Optional[API] = None
    """地图 geo json 地址"""
    mapName: Optional[str] = None
    """地图名称"""
    loadBaiduMap: Optional[bool] = None
    """加载百度地图"""
    onEvent: OnEvent[Literal["init", "click", "mouseover", "Legendselectchanged"]] = None


class Code(AmisNode):
    """代码高亮"""

    type: Literal["code"] = Field(default="code", init=False)
    """指定为 code 渲染器"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    value: Optional[str] = None
    """显示的颜色值"""
    name: Optional[str] = None
    """在其他组件中，时，用作变量映射"""
    language: str = "plaintext"
    """所使用的高亮语言，默认是 plaintext"""
    tabSize: int = 4
    """默认 tab 大小"""
    editorTheme: Literal["vs", "vs-dark"] = "vs"
    """主题，还有 'vs-dark'"""
    wordWrap: bool = True
    """是否折行"""
    maxHeight: Union[int, str, None] = None
    """最大高度"""


class Color(AmisNode):
    """颜色"""

    type: Literal["color"] = Field(default="color", init=False)
    """指定为 color 渲染器，如果在 Table、Card 和 List 中，为"color"；在 Form 中用作静态展示，为"static-color" """
    className: Optional[str] = None
    """外层 CSS 类名"""
    value: Optional[str] = None
    """显示的颜色值"""
    name: Optional[str] = None
    """在其他组件中，时，用作变量映射"""
    defaultColor: str = "#CCC"
    """默认颜色值"""
    showValue: bool = True
    """是否显示右边的颜色值"""


class Date(AmisNode):
    """日期时间"""

    type: Literal["date"] = Field(default="date", init=False)
    """指定为 date 渲染器"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    value: Optional[str] = None
    """显示的日期数值"""
    name: Optional[str] = None
    """在其他组件中，时，用作变量映射"""
    placeholder: str = "-"
    """占位内容"""
    displayFormat: str = "YYYY-MM-DD"
    """展示格式, 更多格式类型请参考 文档"""
    valueFormat: str = "X"
    """数据格式，默认为时间戳。更多格式类型请参考 文档"""
    fromNow: bool = False
    """是否显示相对当前的时间描述，比如: 11 小时前、3 天前、1 年前等，fromNow 为 true 时，format 不生效。"""
    updateFrequency: int = 60000
    """更新频率， 默认为 1 分钟"""


class Each(AmisNode):
    """循环渲染器"""

    type: Literal["each"] = Field(default="each", init=False)
    """指定为 each 渲染器"""
    value: List[Any] = []
    """用于循环的值"""
    name: Optional[str] = None
    """获取数据域中变量"""
    source: Optional[str] = None
    """获取数据域中变量， 支持 数据映射"""
    items: Optional[DictStrAny] = None
    """使用value中的数据，循环输出渲染器。"""
    placeholder: Optional[str] = None
    """当 value 值不存在或为空数组时的占位文本"""


class Html(AmisNode):
    """Html"""

    type: Literal["html"] = Field(default="html", init=False)
    """指定为 html 组件"""
    html: Union[str, "Tpl"]
    """html  当需要获取数据域中变量时，使用 Tpl 。"""


class Icon(AmisNode):
    """图标"""

    type: Literal["icon"] = Field(default="icon", init=False)
    """指定组件类型"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    icon: Template
    """icon 名称，支持 fontawesome v4 或 通过 registerIcon 注册的 icon、或使用 url"""
    vendor: str = "fa"
    """icon 类型，默认为fa, 表示 fontawesome v4。
    也支持 iconfont, 如果是 fontawesome v5 以上版本或者其他框架可以设置为空字符串"""
    badge: Optional["Badge"] = None
    """角标"""
    onEvent: OnEvent[Literal["click", "mouseenter", "mouseleave"]] = None


class Iframe(AmisNode):
    """Iframe"""

    type: Literal["iframe"] = Field(default="iframe", init=False)
    """指定为 iFrame 渲染器"""
    className: Optional[str] = None
    """iFrame 的类名"""
    frameBorder: Optional[list] = None
    """frameBorder"""
    style: Optional[DictStrAny] = None
    """样式对象"""
    src: Optional[str] = None
    """iframe 地址"""
    allow: Optional[str] = None
    """allow配置"""
    sandbox: Optional[str] = None
    """sandbox 配置"""
    referrerpolicy: Optional[str] = None
    """referrerpolicy 配置"""
    height: Union[int, str] = "100%"
    """iframe 高度"""
    width: Union[int, str] = "100%"
    """iframe 宽度"""


class ImageAction(AmisNode):
    key: Literal["rotateRight", "rotateLeft", "zoomIn", "zoomOut", "scaleOrigin"]
    """操作key"""
    label: Optional[str] = None
    """动作名称"""
    icon: Optional[str] = None
    """动作图标"""
    iconClassName: Optional[str] = None
    """动作自定义CSS类"""
    disabled: Optional[bool] = None
    """动作是否禁用"""


class Image(AmisNode):
    """图片"""

    type: Literal["image"] = Field(default="image", init=False)
    """指定为 image 渲染器，如果在 Table、Card 和 List 中，为"image"；在 Form 中用作静态展示，为"static-image"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    innerClassName: Optional[str] = None
    """组件内层 CSS 类名"""
    imageClassName: Optional[str] = None
    """图片 CSS 类名"""
    thumbClassName: Optional[str] = None
    """图片缩率图 CSS 类名"""
    height: Optional[int] = None
    """图片缩率高度"""
    width: Optional[int] = None
    """图片缩率宽度"""
    title: Optional[str] = None
    """标题"""
    imageCaption: Optional[str] = None
    """描述"""
    placeholder: Optional[str] = None
    """占位文本"""
    defaultImage: Optional[str] = None
    """无数据时显示的图片"""
    src: Optional[str] = None
    """缩略图地址"""
    href: Optional[Template] = None
    """外部链接地址"""
    originalSrc: Optional[str] = None
    """原图地址"""
    enlargeAble: Optional[bool] = None
    """支持放大预览"""
    enlargeTitle: Optional[str] = None
    """放大预览的标题"""
    enlargeCaption: Optional[str] = None
    """放大预览的描述"""
    enlargeWithGallary: bool = True
    """在表格中，图片的放大功能会默认展示所有图片信息，设置为false将关闭放大模式下图片集列表的展示"""
    thumbMode: Literal["w-full", "h-full", "contain", "cover"] = "contain"
    """预览图模式，可选：'w-full', 'h-full', 'contain', 'cover'"""
    thumbRatio: Literal["1:1", "4:3", "16:9"] = "1:1"
    """预览图比例，可选：'1:1','4:3','16:9'"""
    imageMode: Literal["thumb", "original"] = "thumb"
    """图片展示模式，可选：'thumb','original' 即：缩略图模式 或者 原图模式"""
    showToolbar: bool = False
    """放大模式下是否展示图片的工具栏"""
    toolbarActions: Optional[List[ImageAction]] = None
    """图片工具栏，支持旋转，缩放，默认操作全部开启"""


class Images(AmisNode):
    """图片集"""

    type: Literal["images"] = Field(default="images", init=False)
    """指定为 images 渲染器 如果在 Table、Card 和 List 中，为"images"；在 Form 中用作静态展示，为"static-images"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    defaultImage: Optional[str] = None
    """默认展示图片"""
    value: Optional[Union[str, List[str], List[DictStrAny]]] = None
    """图片数组"""
    source: Optional[str] = None
    """数据源"""
    delimiter: Union[str, bool] = ","
    """分隔符，当 value 为字符串时，用该值进行分隔拆分"""
    src: Optional[str] = None
    """预览图地址，支持数据映射获取对象中图片变量"""
    originalSrc: Optional[str] = None
    """原图地址，支持数据映射获取对象中图片变量"""
    enlargeAble: Optional[bool] = None
    """支持放大预览"""
    enlargeWithGallary: Optional[bool] = None
    """默认在放大功能展示图片集的所有图片信息；表格中使用时，设置为true将展示所有行的图片信息；设置为false将关闭放大模式下图片集列表的展示"""
    thumbMode: Literal["w-full", "h-full", "contain", "cover"] = "contain"
    """预览图模式，可选：'w-full', 'h-full', 'contain', 'cover'"""
    thumbRatio: Literal["1:1", "4:3", "16:9"] = "1:1"
    """预览图比例，可选：'1:1','4:3','16:9'"""
    showToolbar: bool = False
    """放大模式下是否展示图片的工具栏"""
    toolbarActions: Optional[List[ImageAction]] = None
    """图片工具栏，支持旋转，缩放，默认操作全部开启"""


class GridNav(AmisNode):
    """宫格导航"""

    class Option(AmisNode):
        icon: Optional[str] = None
        """列表项图标"""
        text: Optional[str] = None
        """列表项文案"""
        badge: Optional["Badge"] = None
        """列表项角标，详见 Badge"""
        link: Optional[str] = None
        """内部页面路径或外部跳转 URL 地址，优先级高于 clickAction"""
        blank: Optional[bool] = None
        """是否新页面打开，link 为 url 时有效"""
        clickAction: Optional["Action"] = None
        """列表项点击交互 详见 Action"""

    type: Literal["grid-nav"] = Field(default="grid-nav", init=False)
    """指定为 grid-nav"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    itemClassName: Optional[str] = None
    """列表项 css 类名"""
    contentClassName: Optional[str] = None
    """列表项内容 css 类名"""
    value: Optional[List[Option]] = None
    """图片数组"""
    source: Optional[str] = None
    """数据源"""
    square: Optional[bool] = None
    """是否将列表项固定为正方形"""
    center: bool = True
    """是否将列表项内容居中显示"""
    border: bool = True
    """是否显示列表项边框"""
    gutter: Optional[int] = None
    """列表项之间的间距，默认单位为px"""
    reverse: Optional[bool] = None
    """	是否调换图标和文本的位置"""
    iconRatio: int = 60
    """图标宽度占比，单位%"""
    direction: Literal["horizontal", "vertical"] = "vertical"
    """列表项内容排列的方向"""
    columnNum: int = 4
    """列数"""


class Json(AmisNode):
    """JSON 展示组件"""

    type: Literal["json"] = Field(default="json", init=False)
    """指定为 json 渲染器，如果在 Table、Card 和 List 中，为"json"；在 Form 中用作静态展示，为"static-json"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    value: Optional[Union[dict, str]] = None
    """json 值，如果是 string 会自动 parse"""
    source: str = ""
    """通过数据映射获取数据链中的值"""
    placeholder: str = "-"
    """占位文本"""
    levelExpand: int = 1
    """默认展开的层级"""
    jsonTheme: Literal["twilight", "eighties"] = "twilight"
    """主题，可选twilight和eighties"""
    mutable: bool = False
    """是否可修改"""
    displayDataTypes: bool = False
    """是否显示数据类型"""
    ellipsisThreshold: Union[int, bool] = False
    """设置字符串的最大展示长度，点击字符串可以切换全量/部分展示方式，默认展示全量字符串"""


class Link(AmisNode):
    """链接"""

    type: Literal["link"] = Field(default="link", init=False)
    """指定为 link 渲染器，如果在 Table、Card 和 List 中，为"link"；在 Form 中用作静态展示，为"static-link"""
    body: Optional[str] = None
    """标签内文本"""
    href: Optional[str] = None
    """链接地址"""
    blank: Optional[bool] = None
    """是否在新标签页打开"""
    htmlTarget: Optional[str] = None
    """a 标签的 target，优先于 blank 属性"""
    title: Optional[str] = None
    """a 标签的 title"""
    disabled: Optional[bool] = None
    """禁用超链接"""
    icon: Optional[str] = None
    """超链接图标，以加强显示"""
    rightIcon: Optional[str] = None
    """右侧图标"""


class AmisList(AmisNode):
    """列表"""

    class ListBodyField(AmisNode):
        """列配置"""

        label: Optional[Template] = None
        """列标题"""
        className: Optional[str] = None
        """外层DOM的CSS类名"""
        labelClassName: Optional[str] = None
        """label的CSS类名"""
        innerClassName: Optional[str] = None
        """内层组件的CSS类名，className属性会添加到外层DOM，如果要在组件层级添加CSS类，请设置当前属性"""
        name: Optional[str] = None
        """绑定字段名"""
        popOver: Optional[Union[SchemaNode, dict]] = None
        """配置查看详情功能"""
        quickEdit: Optional[Union[SchemaNode, dict, str]] = None
        """配置快速编辑功能"""
        copyable: Optional[Union[SchemaNode, dict, str]] = None
        """配置点击复制功能"""

    class Item(AmisNode):
        """单条信息"""

        title: Optional[Template] = None
        """标题"""
        titleClassName: str = "h5"
        """标题 CSS 类名"""
        subTitle: Optional[Template] = None
        """副标题"""
        avatar: Optional[Template] = None
        """图片地址"""
        avatarClassName: Optional[str] = None
        """图片 CSS 类名"""
        desc: Optional[Template] = None
        """描述"""
        body: Optional[List["AmisList.ListBodyField"]] = None  # TODO 确认类型
        """内容容器，主要用来放置非表单项组件"""
        actions: Optional[List["Action"]] = None
        """按钮区域"""
        actionsPosition: Literal["left", "right"] = "right"
        """按钮位置"""

    type: Literal["list"] = Field(default="list", init=False)
    """指定为 list 渲染器"""
    title: Optional[str] = None
    """标题"""
    source: Optional[str] = None
    """数据源, 获取当前数据域变量，支持数据映射"""
    placeholder: str = "暂无数据"
    """当没数据的时候的文字提示"""
    selectable: bool = False
    """列表是否可选"""
    multiple: bool = True
    """列表是否为多选"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    headerClassName: str = "amis-list-header"
    """顶部外层 CSS 类名"""
    footerClassName: str = "amis-list-footer"
    """底部外层 CSS 类名"""
    listItem: Optional[Item] = None
    """配置单条信息"""
    onEvent: OnEvent[Literal["itemClick"]] = None


class Log(AmisNode):
    """实时日志"""

    type: Literal["log"] = Field(default="log", init=False)
    """指定为 log 渲染器"""
    height: int = 500
    """展示区域高度"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    autoScroll: bool = True
    """是否自动滚动"""
    disableColor: bool = False
    """是否禁用 ansi 颜色支持"""
    placeholder: Optional[str] = None
    """加载中的文字"""
    encoding: str = "utf-8"
    """"返回内容的字符编码"""
    source: Optional[API] = None
    """支持变量,可以初始设置为空，这样初始不会加载，而等这个变量有值的时候再加载"""
    credentials: str = "include"
    """fetch 的 credentials 设置"""
    rowHeight: Optional[int] = None
    """设置每行高度，将会开启虚拟渲染"""
    maxLength: Optional[int] = None
    """最大显示行数"""
    operation: Optional[List[Literal["stop", "restart", "clear", "showLineNumber", "filter"]]] = None
    """可选日志操作"""


class Mapping(AmisNode):
    """映射"""

    type: Literal["mapping"] = Field(default="mapping", init=False)
    """指定为 mapping 渲染器，如果在 Table、Card 和 List 中，为"mapping"；在 Form 中用作静态展示，为"static-mapping"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    placeholder: Optional[str] = None
    """占位文本"""
    map: Optional[Union[DictStrAny, List[DictStrAny]]] = None
    """映射配置"""
    source: Optional[API] = None
    """API 或 数据映射"""
    valueField: str = "value"
    """2.5.2 map或source为Array<object>时，用来匹配映射的字段名"""
    labelField: str = "label"
    """
    2.5.2 map或source为List[dict]时，用来展示的字段名
    注：配置后映射值无法作为schema组件渲染
    """
    itemSchema: Optional[Union[str, SchemaNode]] = None
    """
    2.5.2 自定义渲染模板，支持html或schemaNode；
    当映射值是非object时，可使用${item}获取映射值；
    当映射值是object时，可使用映射语法: ${xxx}获取object的值；
    也可使用数据映射语法：${xxx}获取数据域中变量值。
    """


class Number(AmisNode):
    """展示"""

    type: Literal["number"] = Field(default="number", init=False)
    """指定为 number 渲染器，如果在 Table、Card 和 List 中，为"number"；在 Form 中用作静态展示，为"static-number"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    value: Optional[str] = None
    """数值"""
    name: Optional[str] = None
    """在其他组件中，时，用作变量映射"""
    placeholder: str = "-"
    """占位内容"""
    kilobitSeparator: bool = True
    """是否千分位展示"""
    precision: Optional[int] = None
    """用来控制小数点位数"""
    percent: Union[bool, int, None] = None
    """是否用百分比展示，如果是数字，还可以控制百分比小数点位数"""
    prefix: Optional[str] = None
    """前缀"""
    affix: Optional[str] = None
    """后缀"""


class Markdown(AmisNode):
    """Markdown渲染"""

    type: Literal["markdown"] = Field(default="markdown", init=False)
    """指定为 markdown 渲染器"""
    name: Optional[str] = None
    """字段名，指定该表单项提交时的 key"""
    value: Optional[Union[int, str]] = None
    """字段的值"""
    className: Optional[str] = None
    """表单最外层类名"""
    src: Optional[API] = None
    """外部地址"""


class OfficeViewer(AmisNode):
    """文档渲染"""

    class SaveAsAction(EventAction):
        """保存为"""

        actionType: Literal["saveAs"] = Field(default="saveAs", init=False)
        name: Optional[str] = None
        """文件名"""

    class PrintAction(EventAction):
        """打印"""

        actionType: Literal["print"] = Field(default="print", init=False)

    type: Literal["office-viewer"] = Field(default="office-viewer", init=False)
    """指定为 office-viewer 渲染器"""
    src: Optional[API] = None
    """文档地址"""
    loading: bool = False
    """是否显示 loading 图标"""
    enableVar: Optional[bool] = None
    """是否开启变量替换功能"""
    wordOptions: Optional[DictStrAny] = None
    """Word 渲染配置"""


class Progress(AmisNode):
    """进度条"""

    class ValueColor(TypedDict):
        value: int
        color: str

    type: Literal["progress"] = Field(default="progress", init=False)
    """指定为 progress 渲染器 如果在 Form 中用作静态展示，为"static-progress" """
    mode: Literal["line", "circle", "dashboard"] = "line"
    """进度条的类型"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    value: Optional[Template] = None
    """	进度值"""
    placeholder: str = "-"
    """占位文本"""
    showLabel: bool = True
    """是否展示进度文本"""
    stripe: bool = False
    """背景是否显示条纹"""
    animated: bool = False
    """	type 为 line，可支持动画"""
    map: Union[str, List[Union[str, ValueColor]], None] = None
    """进度颜色映射"""
    threshold: Optional[Union[ValueColor, List[ValueColor]]] = None
    """阈值（刻度）"""
    showThresholdText: bool = False
    """是否显示阈值（刻度）数值"""
    valueTpl: Optional[str] = None
    """自定义格式化内容"""
    strokeWidth: int = 10
    """进度条线宽度"""
    gapDegree: int = Field(default=75, ge=0, le=295)
    """仪表盘缺角角度，可取值 0 ~ 295"""
    gapPosition: Literal["top", "bottom", "left", "right"] = "bottom"
    """仪表盘进度条缺口位置"""


class Steps(AmisNode):
    """步骤条"""

    class Step(AmisNode):
        """步骤"""

        title: Optional[SchemaNode] = None
        """标题"""
        subTitle: Optional[SchemaNode] = None
        """子标题"""
        description: Optional[SchemaNode] = None
        """详细描述"""
        icon: Optional[str] = None
        """icon 名，支持 fontawesome v4 或使用 url"""
        value: Optional[str] = None
        """value"""
        className: Optional[str] = None
        """自定义类名"""

    type: Literal["steps"] = Field(default="steps", init=False)
    """指定为 steps 渲染器"""
    steps: Optional[List[Step]] = None
    """数组，配置步骤信息"""
    source: Optional[API] = None
    """选项组源，可通过数据映射获取当前数据域变量、或者配置 API 对象"""
    name: Optional[str] = None
    """关联上下文变量"""
    value: Union[str, int] = "-"
    """	设置默认值，注意不支持表达式"""
    status: Union[
        None,
        Literal["wait", "process", "finish", "error"],
        Dict[str, Literal["wait", "process", "finish", "error"]],
    ] = None
    """状态"""
    className: Optional[str] = None
    """自定义类名"""
    mode: Literal["horizontal", "vertical", "simple"] = "horizontal"
    """指定步骤条模式。目前支持水平（horizontal）、竖直（vertical）和简单（simple）模式"""
    labelPlacement: Literal["horizontal", "vertical"] = "horizontal"
    """指定标签放置位置，默认水平放图标右侧，可选 (vertical) 放图标下方"""
    progressDot: bool = False
    """	点状步骤条"""


class Property(AmisNode):
    """属性表"""

    class Item(AmisNode):
        label: Optional[Template] = None
        """属性名"""
        content: Optional[Template] = None
        """属性值"""
        span: Optional[Template] = None
        """属性值跨几列"""
        visibleOn: Optional[Expression] = None
        """显示表达式"""
        hiddenOn: Optional[Expression] = None
        """隐藏表达式"""

    type: Literal["property"] = Field(default="property", init=False)
    """指定为 property 渲染器"""
    className: Optional[str] = None
    """外层 dom 的类名"""
    style: Optional[dict] = None
    """外层 dom 的样式"""
    labelStyle: Optional[dict] = None
    """属性名的样式"""
    contentStyle: Optional[dict] = None
    """属性值的样式"""
    column: int = 3
    """每行几列"""
    mode: Literal["table", "simple"] = "table"
    """显示模式，目前只有 'table' 和 'simple'"""
    separator: str = ","
    """'simple' 模式下属性名和值之间的分隔符"""
    source: Optional[Template] = None
    """数据源"""
    title: Optional[str] = None
    """标题"""
    items: Optional[List[Item]] = None
    """数据项"""


class QRCode(AmisNode):
    """二维码"""

    class ImageSettings(AmisNode):
        """QRCode 图片配置"""

        src: Optional[str] = None
        """图片链接地址"""
        width: Optional[float] = None
        """图片宽度"""
        height: Optional[float] = None
        """图片高度"""
        x: Optional[float] = None
        """图片水平方向偏移量"""
        y: Optional[float] = None
        """图片垂直方向偏移量"""
        excavate: bool = False
        """图片是否挖孔嵌入"""

    type: Literal["qr-code"] = Field(default="qr-code", init=False)
    """指定为 QRCode 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    qrcodeClassName: Optional[str] = None
    """二维码 SVG 的类名"""
    codeSize: int = 128
    """二维码的宽高大小"""
    backgroundColor: str = "#FFF"
    """二维码背景色"""
    foregroundColor: str = "#000"
    """二维码前景色"""
    level: Literal["L", "M", "Q", "H"] = "L"
    """二维码复杂级别，有（'L' 'M' 'Q' 'H'）四种"""
    value: Optional[Template] = None
    """扫描二维码后显示的文本，如果要显示某个页面请输入完整 url
    （"http://..."或"https://..."开头），支持使用 模板"""
    imageSettings: Optional[ImageSettings] = None
    """QRCode 图片配置"""


class BarCode(AmisNode):
    """条形码"""

    type: Literal["barcode"] = Field(default="barcode", init=False)
    """指定为 barcode 渲染器"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    value: Optional[str] = None
    """	显示的颜色值"""
    name: Optional[str] = None
    """在其他组件中，时，用作变量映射"""


class Remark(AmisNode):
    """标记"""

    class Content(TypedDict):
        title: NotRequired[str]
        body: NotRequired[str]

    type: Literal["remark"] = Field(default="remark", init=False)
    """remark"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    content: Union[str, Content]
    """提示文本"""
    placement: Literal["top", "bottom", "left", "right"] = "right"
    """弹出位置"""
    trigger: Optional[List[Literal["hover", "focus"]]] = None
    """触发条件 ['hover','focus']"""
    icon: str = "fa fa-question-circle"
    """图标"""
    shape: Literal["circle", "square"] = "square"
    """图标形状

    - circle: 圆形
    - square: 方形
    """


class SearchBox(AmisNode):
    """搜索框"""

    type: Literal["search-box"] = Field(default="search-box", init=False)
    """指定为 search-box 渲染器"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    mini: Optional[bool] = None
    """是否为 mini 模式"""
    searchImediately: Optional[bool] = None
    """	是否立即搜索"""
    clearAndSubmit: Optional[bool] = None
    """清空搜索框内容后立即执行搜索"""
    onEvent: OnEvent[Literal["search", "change", "focus", "blur"]] = None


class Sparkline(AmisNode):
    """走势图"""

    type: Literal["sparkline"] = Field(default="sparkline", init=False)
    """指定为 sparkline渲染器"""
    name: Optional[str] = None
    """关联的变量"""
    width: Optional[int] = None
    """宽度"""
    height: Optional[int] = None
    """高度"""
    placeholder: Optional[str] = None
    """数据为空时显示的内容"""


class Status(AmisNode):
    """状态"""

    class Source(AmisNode):
        """数据源"""

        label: Optional[Template] = None
        """映射文本"""
        icon: Optional[str] = None
        """映射图标"""
        color: Optional[str] = None
        """映射状态颜色"""
        className: Optional[str] = None
        """映射状态的 独立 CSS 类名"""

    type: Literal["status"] = Field(default="status", init=False)
    """指定为 Status 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    placeholder: str = "-"
    """占位文本"""
    map: Optional[dict] = None
    """映射图标"""
    labelMap: Optional[DictStrAny] = None
    """映射文本"""
    source: Optional[Union[Source, str]] = None
    """自定义映射状态，支持数据映射"""


class Tpl(AmisNode):
    type: Literal["tpl"] = Field(default="tpl", init=False)
    """指定为 Tpl 组件"""
    class_name: Optional[str] = None
    """外层 Dom 的类名"""
    tpl: Template
    """配置模板"""
    showNativeTitle: Optional[bool] = None
    """是否设置外层 DOM 节点的 title 属性为文本内容"""
    onEvent: OnEvent[Literal["click", "mouseenter", "mouseleave"]] = None


class Tag(AmisNode):
    """标签"""

    type: Literal["tag"] = Field(default="tag", init=False)
    """指定为 tag 渲染器"""
    displayMode: Literal["normal", "rounded", "status"] = "normal"
    """展现模式"""
    color: Optional[str] = None
    """颜色主题，提供默认主题，并支持自定义颜色值

    'active' | 'inactive' | 'error' | 'success' | 'processing' | 'warning'"""
    label: str = "-"
    """标签内容"""
    icon: Union[Icon, str] = "fa fa-dot"
    """status 模式下的前置图标"""
    className: Optional[str] = None
    """自定义 CSS 样式类名"""
    style: Optional[DictStrAny] = None
    """自定义样式（行内样式），优先级最高"""
    closable: bool = False
    """是否展示关闭按钮"""
    onEvent: OnEvent[Literal["click", "mouseenter", "mouseleave", "close"]] = None


class Video(AmisNode):
    """视频"""

    type: Literal["video"] = Field(default="video", init=False)
    """指定为 video 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    src: Optional[str] = None
    """视频地址"""
    isLive: bool = False
    """ 是否为直播，视频为直播时需要添加上，支持flv和hls格式"""
    videoType: Optional[str] = None
    """指定直播视频格式"""
    poster: Optional[str] = None
    """视频封面地址"""
    muted: Optional[bool] = None
    """是否静音"""
    loop: Optional[bool] = None
    """是否循环播放"""
    autoPlay: Optional[bool] = None
    """是否自动播放"""
    rates: Optional[List[float]] = None
    """倍数，格式为[1.0, 1.5, 2.0]"""
    frames: Optional[DictStrAny] = None
    """key 是时刻信息，value 可以可以为空，可有设置为图片地址，请看上方示例"""
    jumpBufferDuration: Optional[Union[bool, int, str]] = None
    """点击帧的时候默认是跳转到对应的时刻，如果想提前 3 秒钟，可以设置这个值为 3"""
    stopOnNextFrame: Optional[bool] = None
    """到了下一帧默认是接着播放，配置这个会自动停止"""


class Timeline(AmisNode):
    """时间轴"""

    class Item(AmisNode):
        """节点配置"""

        time: Optional[str] = None
        """节点时间"""
        title: Optional[SchemaNode] = None
        """节点标题"""
        detail: Optional[str] = None
        """节点详细描述（折叠）"""
        detailCollapsedText: str = "展开"
        """详细内容折叠时按钮文案"""
        detailExpandedText: str = "折叠"
        """详细内容展开时按钮文案"""
        color: Union[str, Literal["info", "success", "warning", "danger"]] = "#DADBDD"
        """时间轴节点颜色"""
        icon: Optional[str] = None
        """icon 名，支持 fontawesome v4 或使用 url（优先级高于 color）"""
        iconClassName: Optional[str] = None
        """节点图标 CSS 类"""
        timeClassName: Optional[str] = None
        """节点时间 CSS 类"""
        titleClassName: Optional[str] = None
        """节点标题 CSS 类"""
        detailClassName: Optional[str] = None
        """节点详细描述 CSS 类"""

    type: Literal["timeline"] = Field(default="timeline", init=False)
    """指定为 timeline 渲染器"""
    items: Optional[List[Item]] = None
    """配置节点数据"""
    source: Optional[API] = None
    """数据源，可通过数据映射获取当前数据域变量、或者配置 API 对象"""
    mode: Literal["left", "right", "alternate"] = "right"
    """指定文字相对于时间轴的位置，仅 direction=vertical 时支持"""
    direction: Literal["vertical", "horizontal"] = "vertical"
    """时间轴方向"""
    reverse: bool = False
    """根据时间倒序显示"""
    iconClassName: Optional[str] = None
    """统一配置的节点图标 CSS 类"""
    timeClassName: Optional[str] = None
    """统一配置的节点时间 CSS 类"""
    titleClassName: Optional[str] = None
    """统一配置的节点标题 CSS 类"""
    detailClassName: Optional[str] = None
    """统一配置的节点详细描述 CSS 类"""


__all__ = [
    "CRUD",
    "Table",
    "TableView",
    "Calendar",
    "Card",
    "Cards",
    "Carousel",
    "Chart",
    "Code",
    "Color",
    "Date",
    "Each",
    "Html",
    "Icon",
    "Iframe",
    "ImageAction",
    "Image",
    "Images",
    "GridNav",
    "Json",
    "Link",
    "AmisList",
    "Log",
    "Mapping",
    "Number",
    "Markdown",
    "OfficeViewer",
    "Progress",
    "Steps",
    "Property",
    "QRCode",
    "BarCode",
    "Remark",
    "SearchBox",
    "Sparkline",
    "Status",
    "Tpl",
    "Tag",
    "Video",
    "Timeline",
]
