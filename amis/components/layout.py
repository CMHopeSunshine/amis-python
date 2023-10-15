from typing import List, Literal, Optional, TYPE_CHECKING, Union
from typing_extensions import TypedDict

from amis.event import EventAction, OnEvent
from amis.render import render_as_html
from amis.typing import DictStrAny, Expression

from .types import AmisNode, API, SchemaNode, Template

from pydantic import Field

if TYPE_CHECKING:
    from .data_presentation import Icon, Remark
    from .feature import Action


class Page(AmisNode):
    """页面

    https://aisuda.bce.baidu.com/amis/zh-CN/components/page
    """

    __default_template_path__: str = "page.jinja2"

    type: Literal["page"] = Field(default="page", init=False)
    """指定为 Page 组件"""
    title: Optional[SchemaNode] = None
    """页面标题"""
    subTitle: Optional[SchemaNode] = None
    """页面副标题"""
    remark: Optional["Remark"] = None
    """标题附近会出现一个提示图标，鼠标放上去会提示该内容。"""
    aside: Optional[SchemaNode] = None
    """往页面的边栏区域加内容"""
    asideResizor: Optional[bool] = None
    """页面的边栏区域宽度是否可调整"""
    asideMinWidth: Optional[int] = None
    """页面边栏区域的最小宽度"""
    asideMaxWidth: Optional[int] = None
    """页面边栏区域的最大宽度"""
    asideSticky: bool = True
    """用来控制边栏固定与否"""
    toolbar: Optional[SchemaNode] = None
    """往页面的右上角加内容，需要注意的是，当有 title 时，该区域在右上角，没有时该区域在顶部"""
    body: Optional[SchemaNode] = None
    """往页面的内容区域加内容"""
    className: Optional[str] = None
    """外层 dom 类名"""
    cssVars: Optional[DictStrAny] = None
    """自定义 CSS 变量，请参考样式"""
    toolbarClassName: Optional[str] = None
    """Toolbar dom 类名"""
    bodyClassName: Optional[str] = None
    """Body dom 类名"""
    asideClassName: Optional[str] = None
    """Aside dom 类名"""
    headerClassName: Optional[str] = None
    """Header 区域 dom 类名"""
    initApi: Optional[API] = None
    """Page 用来获取初始数据的 api。返回的数据可以整个 page 级别使用。"""
    initFetch: bool = True
    """是否起始拉取 initApi"""
    initFetchOn: Optional[Expression] = None
    """是否起始拉取 initApi, 通过表达式配置"""
    interval: Optional[int] = None
    """刷新时间(最小 1000)"""
    silentPolling: bool = False
    """配置刷新时是否显示加载动画"""
    stopAutoRefreshWhen: Expression = ""
    """通过表达式来配置停止刷新的条件"""
    pullRefresh: dict = {"disabled": True}
    """下拉刷新配置（仅用于移动端）"""
    onEvent: OnEvent[Literal["init", "inited", "pullRefresh"]] = None

    def to_html(
        self,
        locale: str = "zh_CN",
        cdn: str = "https://unpkg.com",
        version: str = "latest",
        site_title: str = "AMIS",
        site_icon: str = "",
        theme: Literal["default", "antd", "ang"] = "default",
        custom_style: str = "",
        request_adaptor: str = "",
        response_adaptor: str = "",
    ) -> str:
        """将 Page 渲染为 html 纯文本

        参数:
            locale: 本地化. 默认为 "zh_CN".
            cdn: cdn地址. 默认为 "https://unpkg.com".
            version: amis版本. 默认为 "latest".
            site_title: 网页标题. 默认为 "AMIS".
            site_icon: 网页图标. 默认为 "".
            theme: 主体. 默认为 "default".
            custom_style: 自定义样式. 默认为 "".
            request_adaptor: 请求适配器. 默认为 "".
            response_adaptor: 接收适配器. 默认为 "".

        返回:
            str: html 纯文本
        """
        return render_as_html(
            self,
            template_name="page.html",
            locale=locale,
            cdn=cdn,
            version=version,
            site_title=site_title,
            site_icon=site_icon,
            theme=theme,
            custom_style=custom_style,
            request_adaptor=request_adaptor,
            response_adaptor=response_adaptor,
        )


class Container(AmisNode):
    """容器

    https://aisuda.bce.baidu.com/amis/zh-CN/components/container"""

    type: Literal["container"] = Field(default="container", init=False)
    """container"""
    className: Optional[str] = None
    """外层 dom 类名"""
    bodyClassName: Optional[str] = None
    """	容器内容区的类名"""
    wrapperComponent: Optional[str] = None
    """容器标签名，默认为div"""
    style: Optional[DictStrAny] = None
    """自定义样式"""
    body: Optional[SchemaNode] = None
    """容器内容"""
    onEvent: OnEvent[Literal["click", "mouseenter", "mouseleave"]] = None


class Collapse(AmisNode):
    """折叠器

    https://aisuda.bce.baidu.com/amis/zh-CN/components/collapse"""

    type: Literal["collapse"] = Field(default="collapse", init=False)
    """指定为 collapse 渲染器"""
    disabled: bool = False
    """是否禁用，默认为False"""
    collapsed: bool = True
    """初始状态是否折叠，默认为True"""
    key: Optional[Union[str, int]] = None
    """标识"""
    header: Optional[Union[str, SchemaNode]] = None
    """标题"""
    body: Optional[Union[str, SchemaNode]] = None
    """内容"""
    showArrow: bool = True
    """是否展示图标，默认为True"""
    onEvent: OnEvent[Literal["change"]] = None


class CollapseGroup(AmisNode):
    """折叠器组

    https://aisuda.bce.baidu.com/amis/zh-CN/components/collapse"""

    type: Literal["collapse-group"] = Field(default="collapse-group", init=False)
    """指定为 collapse-group 渲染器"""
    activeKey: Union[str, float, List[Union[str, float]], None] = None
    """初始化激活面板的 key"""
    accordion: bool = False
    """手风琴模式"""
    expandIcon: Optional[SchemaNode] = None
    """自定义切换图标"""
    expandIconPosition: Literal["left", "right"] = "left"
    """设置图标位置，可选值left | right"""
    body: List[Collapse] = []
    """折叠列表"""
    onEvent: OnEvent[Literal["change"]] = None


class Divider(AmisNode):
    """分割线

    https://aisuda.bce.baidu.com/amis/zh-CN/components/divider"""

    type: Literal["divider"] = Field(default="divider", init=False)
    """指定为 分割线 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    lineStyle: Literal["dashed", "solid"] = "dashed"
    """分割线的样式，支持 dashed 和 solid"""
    direction: Literal["horizontal", "vertical"] = "horizontal"
    """分割线的方向，支持 horizontal 和 vertical"""
    color: Optional[str] = None
    """分割线的颜色"""
    rotate: Optional[float] = None
    """分割线的旋转角度"""


class Flex(AmisNode):
    """布局

    https://aisuda.bce.baidu.com/amis/zh-CN/components/flex"""

    type: Literal["flex"] = Field(default="flex", init=False)
    """指定为 Flex 渲染器"""
    className: Optional[str] = None
    """css 类名"""
    justify: Literal[
        "start",
        "flex-start",
        "center",
        "end",
        "flex-end",
        "space-around",
        "space-between",
        "space-evenly",
    ] = "center"
    """水平对齐方式"""
    alignItems: Literal["stretch", "start", "flex-start", "flex-end", "end", "center", "baseline"] = "center"
    """垂直对齐方式"""
    direction: Literal["row", "column"] = "row"
    """布局方向"""
    style: Optional[DictStrAny] = None
    """自定义样式"""
    items: List[SchemaNode] = []
    """组件列表"""


class Grid(AmisNode):
    """Grid 水平分栏

    https://aisuda.bce.baidu.com/amis/zh-CN/components/grid"""

    class Column(AmisNode):
        """列配置"""

        xs: Optional[Union[int, Literal["auto"]]] = None
        """宽度占比：1 - 12或'auto'"""
        columnClassName: Optional[str] = None
        """列类名"""
        sm: Optional[Union[int, Literal["auto"]]] = None
        """宽度占比：1 - 12或'auto'"""
        md: Optional[Union[int, Literal["auto"]]] = None
        """宽度占比：1 - 12或'auto'"""
        lg: Optional[Union[int, Literal["auto"]]] = None
        """宽度占比：1 - 12或'auto'"""
        valign: Optional[Literal["top", "middle", "bottom", "between"]] = None
        """当前列内容的垂直对齐"""
        body: SchemaNode
        """内容"""

    type: Literal["grid"] = Field(default="grid", init=False)
    """指定为 Grid 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    gap: Optional[Literal["xs", "sm", "base", "none", "md", "lg"]] = None
    """水平间距"""
    valign: Optional[Literal["top", "middle", "bottom", "between"]] = None
    """垂直对齐方式"""
    align: Optional[Literal["left", "right", "between", "center"]] = None
    """水平对齐方式"""
    columns: List[Union[Column, SchemaNode]] = []


class Grid2D(AmisNode):
    """Grid 2D布局

    https://aisuda.bce.baidu.com/amis/zh-CN/components/grid-2d"""

    type: Literal["grid-2d"] = Field(default="grid-2d", init=False)
    """指定为 Grid 2D 渲染器"""
    gridClassName: Optional[str] = None
    """外层 Dom 的类名"""
    gap: Union[int, str] = 0
    """格子间距，包括水平和垂直"""
    cols: int = 12
    """格子水平划分为几个区域"""
    rowHeight: int = 50
    """每个格子默认垂直高度"""
    rowGap: Optional[Union[int, str]] = None
    """格子垂直间距"""
    grids: Optional[List[SchemaNode]] = None
    """格子集合，成员可以是其他渲染器，允许有以下额外属性:
    - x(int): 格子起始位置的横坐标
    - y(int): 格子起始位置的纵坐标
    - w(int): 格子横跨几个宽度
    - h(int): 格子横跨几个高度
    - width(int|str): 格子所在列的宽度
    - height(int|str): 格子所在行的高度，可以设置 auto
    - align("left|right|center|auto"): 格子内容水平布局
    - valign("top|middle|bottom|auto"): 格子内容垂直布局
    """


class HBox(AmisNode):
    """HBox布局

    https://aisuda.bce.baidu.com/amis/zh-CN/components/hbox"""

    type: Literal["hbox"] = Field(default="hbox", init=False)
    """指定为 HBox 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    gap: Optional[Literal["xs", "sm", "base", "none", "md", "lg"]] = None
    """水平间距"""
    valign: Optional[Literal["top", "middle", "bottom", "between"]] = None
    """垂直对齐方式"""
    align: Optional[Literal["left", "right", "between", "center"]] = None
    """水平对齐方式"""
    columns: List[SchemaNode] = []
    """列集合，成员可以是其他渲染器，允许有以下额外属性：
    - columnClassName(str): 列上类名
    - valign("top|middle|bottom|between"): 当前列内容的垂直对齐
    """


class Pagination(AmisNode):
    """分页

    https://aisuda.bce.baidu.com/amis/zh-CN/components/pagination"""

    type: Literal["pagination"] = Field(default="pagination", init=False)
    """指定为 Pagination渲染器"""
    mode: Literal["normal", "simple"] = "normal"
    """迷你版本/简易版本 只显示左右箭头，配合hasNext使用"""
    layout: Union[str, List[str]] = ["pager"]
    """通过控制layout属性的顺序，调整分页结构布局"""
    maxButtons: Union[int, str] = 5
    """最多显示多少个分页按钮，最小为5"""
    total: Optional[Union[int, str]] = None
    """总条数"""
    activePage: Union[int, str] = 1
    """当前页数"""
    perPage: Union[int, str] = 10
    """每页显示多条数据"""
    showPerPage: bool = False
    """是否展示 perPage 切换器 layout 和 showPerPage 都可以控制"""
    perPageAvailable: List[int] = [10, 20, 50, 100]
    """指定每页可以显示多少条"""
    showPageInput: bool = False
    """是否显示快速跳转输入框 layout 和 showPageInput 都可以控制"""
    disabled: bool = False
    """是否禁用"""
    onPageChange: Optional[str] = None
    """分页改变触发 (page: number, perPage: number) => void;"""


class PaginationWrapper(AmisNode):
    """分页容器

    https://aisuda.bce.baidu.com/amis/zh-CN/components/pagination-wrapper"""

    type: Literal["pagination-wrapper"] = Field(default="pagination-wrapper", init=False)
    """指定为 Pagination-Wrapper 渲染器"""
    showPageInput: bool = False
    """是否显示快速跳转输入框"""
    maxButtons: int = 5
    """最多显示多少个分页按钮"""
    inputName: str = "items"
    """输入字段名"""
    outputName: str = "items"
    """输出字段名"""
    perPage: int = 10
    """每页显示多条数据"""
    position: Literal["top", "bottom", "none"] = "top"
    """分页显示位置，如果配置为 none 则需要自己在内容区域配置 pagination 组件，否则不显示"""
    body: SchemaNode
    """内容区域"""


class Panel(AmisNode):
    """面板

    https://aisuda.bce.baidu.com/amis/zh-CN/components/panel"""

    type: Literal["panel"] = Field(default="panel", init=False)
    """指定为 Panel 渲染器"""
    className: str = "panel-default"
    """外层 Dom 的类名"""
    headerClassName: str = "panel-heading"
    """header 区域的类名"""
    footerClassName: str = "panel-footer bg-light lter wrapper"
    """footer 区域的类名"""
    actionsClassName: str = "panel-footer"
    """actions 区域的类名"""
    bodyClassName: str = "panel-body"
    """body 区域的类名"""
    title: Optional[SchemaNode] = None
    """标题"""
    header: Optional[SchemaNode] = None
    """头部容器"""
    body: Optional[SchemaNode] = None
    """内容容器"""
    footer: Optional[SchemaNode] = None
    """底部容器"""
    affixFooter: Optional[bool] = None
    """是否固定底部容器"""
    actions: List["Action"] = []
    """按钮区域"""


class Tabs(AmisNode):
    """选项卡"""

    class ChangeActiveKeyAction(EventAction):
        class Args(TypedDict):
            activeKey: Union[str, int]

        actionType: Literal["changeActiveKey"] = Field(default="changeActiveKey", init=False)
        args: Args
        componentId: str

    class Item(AmisNode):
        title: Optional[Union[str, SchemaNode]] = None
        """Tab 标题，当是 SchemaNode 时，该 title 不支持 editable 为 true 的双击编辑"""
        icon: Optional[Union[str, "Icon"]] = None
        """Tab 的图标"""
        iconPosition: Literal["left", "right"] = "left"
        """Tab 的图标位置"""
        tab: SchemaNode
        """内容区"""
        hash: Optional[str] = None
        """设置以后将跟 url 的 hash 对应"""
        reload: Optional[bool] = None
        """设置以后内容每次都会重新渲染，对于 crud 的重新拉取很有用"""
        unmountOnExit: Optional[bool] = None
        """每次退出都会销毁当前 tab 栏内容"""
        className: str = "bg-white b-l b-r b-b wrapper-md"
        """Tab 区域样式"""
        tip: Optional[str] = None
        """当开启 showTip 时生效，作为 Tab 在 hover 时的提示显示，可不配置，如不设置，title 作为提示显示"""
        closable: bool = False
        """是否支持删除，优先级高于组件的 closable"""
        disabled: bool = False
        """是否禁用"""

    type: Literal["tabs"] = Field(default="tabs", init=False)
    """指定为 Tabs 渲染器"""
    defaultKey: Optional[Union[str, int]] = None
    """组件初始化时激活的选项卡，hash 值或索引值，支持使用表达式 2.7.1 以上版本"""
    activeKey: Optional[Union[str, int]] = None
    """激活的选项卡，hash 值或索引值，支持使用表达式，可响应上下文数据变化"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    linksClassName: Optional[str] = None
    """Tabs 标题区的类名"""
    contentClassName: Optional[str] = None
    """Tabs 内容区的类名"""
    tabsMode: Optional[
        Literal["line", "card", "radio", "vertical", "chrome", "simple", "strong", "tiled", "sidebar"]
    ] = None
    """展示模式，取值可以是 line、card、radio、vertical、chrome、simple、strong、tiled、sidebar"""
    tabs: List[Item] = []
    """tabs 内容"""
    source: Optional[str] = None
    """tabs 关联数据，关联后可以重复生成选项卡"""
    toolbar: Optional[SchemaNode] = None
    """tabs 中的工具栏"""
    toolbarClassName: Optional[str] = None
    """tabs 中工具栏的类名"""
    mountOnEnter: bool = False
    """只有在点中 tab 的时候才渲染"""
    unmountOnExit: bool = False
    """切换 tab 的时候销毁"""
    addable: bool = False
    """是否支持新增"""
    addBtnText: str = "增加"
    """"新增按钮文案"""
    closable: bool = False
    """是否支持删除"""
    draggable: bool = False
    """是否支持拖拽"""
    showTip: bool = False
    """是否支持提示"""
    showTipClassName: Optional[str] = None
    """提示的类"""
    editable: bool = False
    """是否可编辑标签名。当 tabs[x].title 为 SchemaNode 时，双击编辑 Tab 的 title 显示空的内容"""
    scrollable: bool = True
    """是否导航支持内容溢出滚动。（属性废弃）"""
    sidePosition: Literal["left", "right"] = "left"
    """sidebar 模式下，标签栏位置"""
    collapseOnExceed: Optional[int] = None
    """当 tabs 超出多少个时开始折叠"""
    collapseBtnLabel: str = "more"
    """用来设置折叠按钮的文字"""
    swipeable: bool = False
    """是否开启手势滑动切换（移动端生效）"""
    onEvent: OnEvent[Literal["change"]] = None


class Wrapper(AmisNode):
    """包裹容器"""

    type: Literal["wrapper"] = Field(default="wrapper", init=False)
    """指定为 Wrapper 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    size: Optional[Literal["xs", "sm", "md", "lg"]] = None
    """支持: xs、sm、md和lg"""
    style: Optional[Union[DictStrAny, str]] = None
    """	自定义样式"""
    body: SchemaNode
    """内容容器"""


class Portlet(AmisNode):
    """门户栏目"""

    class Item(AmisNode):
        title: Optional[str] = None
        """Tab 标题"""
        icon: Optional[Union[str, "Icon"]] = None
        """Tab 的图标"""
        tab: Optional[SchemaNode] = None
        """内容区"""
        toolbar: Optional[SchemaNode] = None
        """tabs 中的工具栏，随 tab 切换而变化"""
        reload: Optional[bool] = None
        """设置以后内容每次都会重新渲染，对于 crud 的重新拉取很有用"""
        unmountOnExit: Optional[bool] = None
        """每次退出都会销毁当前 tab 栏内容"""
        className: str = "bg-white b-l b-r b-b wrapper-md"
        """Tab 区域样式"""

    """tabs 中的工具栏，随 tab 切换而变化"""

    type: Literal["portlet"] = Field(default="portlet", init=False)
    """指定为 Portlet 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    tabsClassName: Optional[str] = None
    """Tabs Dom 的类名"""
    contentClassName: Optional[str] = None
    """Tabs content Dom 的类名"""
    tabs: List[Item] = []
    """tabs 内容"""
    source: Optional[DictStrAny] = None
    """tabs 关联数据，关联后可以重复生成选项卡"""
    toolbar: Optional[SchemaNode] = None
    """tabs 中的工具栏，不随 tab 切换而变化"""
    style: Optional[Union[str, DictStrAny]] = None
    """自定义样式"""
    description: Optional[Template] = None
    """标题右侧信息"""
    hideHeader: bool = False
    """隐藏头部"""
    divider: bool = False
    """去掉分隔线"""
    mountOnEnter: bool = False
    """只有在点中 tab 的时候才渲染"""
    unmountOnExit: bool = False
    """切换 tab 的时候销毁"""
    scrollable: bool = False
    """是否导航支持内容溢出滚动，vertical和chrome模式下不支持该属性；chrome模式默认压缩标签"""


__all__ = [
    "Page",
    "Container",
    "Collapse",
    "CollapseGroup",
    "Divider",
    "Flex",
    "Grid",
    "Grid2D",
    "HBox",
    "Pagination",
    "PaginationWrapper",
    "Panel",
    "Tabs",
    "Wrapper",
    "Portlet",
]
