from typing import List, Literal, Optional, Tuple, TYPE_CHECKING, Union
from typing_extensions import NotRequired, TypedDict

from amis.event import EventAction, OnEvent
from amis.render import render_as_html
from amis.typing import DictStrAny, Expression

from .types import AmisNode, API, SchemaNode, Template

from pydantic import Field

if TYPE_CHECKING:
    from .data_presentation import Iframe
    from .layout import Page
    from .other import Badge


class Action(AmisNode):
    """行为按钮"""

    type: Literal["action"] = Field(default="action", init=False)
    """指定为 Page 渲染器"""
    actionType: Optional[
        Literal[
            "ajax",
            "link",
            "url",
            "drawer",
            "dialog",
            "confirm",
            "cancel",
            "prev",
            "next",
            "copy",
            "close",
            # "reload",
        ]
    ] = None
    """这是 action 最核心的配置，来指定该 action 的作用类型。"""
    label: Optional[str] = None
    """按钮文本。可用 ${xxx} 取值。"""
    level: Literal[
        "link",
        "primary",
        "secondary",
        "info",
        "success",
        "warning",
        "danger",
        "light",
        "dark",
        "default",
    ] = "default"
    """按钮样式。"""
    size: Optional[Literal["xs", "sm", "md", "lg"]] = None
    """按钮大小。"""
    icon: Optional[str] = None
    """设置图标，例如fa fa-plus。"""
    iconClassName: Optional[str] = None
    """给图标上添加类名。"""
    rightIcon: Optional[str] = None
    """在按钮文本右侧设置图标，例如fa fa-plus。"""
    rightIconClassName: Optional[str] = None
    """给右侧图标上添加类名。"""
    active: Optional[bool] = None
    """按钮是否高亮。"""
    activeLevel: Optional[
        Literal[
            "link",
            "primary",
            "secondary",
            "info",
            "success",
            "warning",
            "danger",
            "light",
            "dark",
            "default",
        ]
    ] = None
    """按钮高亮时的样式，配置支持同level。"""
    activeClassName: str = "is-active"
    """给按钮高亮添加类名。"""
    block: Optional[bool] = None
    """用display:"block"来显示按钮。"""
    confirmText: Optional[Template] = None
    """当设置后，操作在开始前会询问用户。可用 ${xxx} 取值。"""
    confirmTitle: Optional[Template] = None
    """确认框标题，前提是 confirmText 有内容，支持模版语法"""
    reload: Optional[str] = None
    """指定此次操作完后，需要刷新的目标组件名字（组件的name值，自己配置的），多个请用 , 号隔开。"""
    tooltip: Optional[str] = None
    """鼠标停留时弹出该段文字，也可以配置对象类型：字段为title和content。可用 ${xxx} 取值。"""
    disabledTip: Optional[str] = None
    """被禁用后鼠标停留时弹出该段文字，也可以配置对象类型：字段为title和content。可用 ${xxx} 取值。"""
    tooltipPlacement: Literal["top", "bottom", "left", "right"] = "top"
    """如果配置了tooltip或者disabledTip，指定提示信息位置，可配置top、bottom、left、right。"""
    close: Optional[Union[bool, str]] = None
    """当action配置在dialog或drawer的actions中时，配置为true指定此次操作完后关闭当前dialog或drawer。当值为字符串，并且是祖先层弹框的名字的时候，会把祖先弹框关闭掉。"""
    required: Optional[List[str]] = None
    """配置字符串数组，指定在form中进行操作之前，需要指定的字段名的表单项通过验证"""
    badge: Optional["Badge"] = None
    """角标"""
    onEvent: OnEvent[Literal["click", "mouseenter", "mouseleave"]] = None


class PageSchema(AmisNode):
    """页面配置"""

    type: Literal["pageSchema"] = Field(default="pageSchema", init=False, exclude=True)
    label: Optional[Union[Literal[False], Template]] = None
    """菜单名称"""
    icon: str = "fa fa-file"
    """菜单图标，比如：'fa fa-file'."""
    url: Optional[str] = None
    """
    页面路由路径，当路由命中该路径时，启用当前页面。
    当路径不是 / 打头时，会连接父级路径。

    比如：父级的路径为 folder，而此时配置 pageA, 那么当页面地址为 /folder/pageA 时才会命中此页面。
    当路径是 / 开头如： /crud/list 时，则不会拼接父级路径.
    另外还支持 /crud/view/:id 这类带参数的路由，页面中可以通过 ${params.id} 取到此值。
    """
    schema_: Union["Page", "Iframe"] = Field(None, alias="schema")
    """页面的配置，具体配置请前往 Page 页面说明"""
    schemaApi: Optional[API] = None
    """如果想通过接口拉取，请配置。返回路径为 json>data。schema 和 schemaApi 只能二选一。"""
    link: Optional[str] = None
    """如果想配置个外部链接菜单，只需要配置 link 即可。"""
    redirect: Optional[str] = None
    """跳转，当命中当前页面时，跳转到目标页面。"""
    rewrite: Optional[str] = None
    """改成渲染其他路径的页面，这个方式页面地址不会发生修改。"""
    isDefaultPage: Optional[Union[str, bool]] = None
    """当你需要自定义 404 页面的时候有用，不要出现多个这样的页面，因为只有第一个才会有用。"""
    visible: Optional[str] = None
    """有些页面可能不想出现在菜单中，可以配置成 false，另外带参数的路由无需配置，直接就是不可见的。"""
    className: Optional[str] = None
    """菜单类名。"""
    children: Optional[List["PageSchema"]] = None
    """子菜单"""
    sort: Optional[int] = None
    """排序"""


class App(AmisNode):
    """多页应用"""

    # __default_template_path__: str = "app.jinja2"
    type: Literal["app"] = Field(default="app", init=False)
    """指定为 app 渲染器"""
    api: Optional[API] = None
    """页面配置接口，如果你想远程拉取页面配置请配置。返回配置路径 json>data>pages，具体格式请参考 pages 属性。"""
    brandName: Optional[str] = None
    """应用名称"""
    logo: Optional[str] = None
    """支持图片地址，或者 svg。"""
    className: Optional[str] = None
    """css 类名"""
    header: Optional[SchemaNode] = None
    """顶部区域"""
    asideBefore: Optional[SchemaNode] = None
    """页面菜单上前面区域。"""
    asideAfter: Optional[SchemaNode] = None
    """页面菜单下前面区域。"""
    footer: Optional[SchemaNode] = None
    """页面。"""
    pages: List[Union[PageSchema, DictStrAny]] = []
    """Array<页面配置>具体的页面配置。
    通常为数组，数组第一层为分组，一般只需要配置 label 集合，如果你不想分组，
    直接不配置，真正的页面请在第二层开始配置，即第一层的 children 中。"""
    onEvent: OnEvent[Literal["init"]] = None

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
        history_mode: Literal["Hash", "Browser"] = "Hash",
    ) -> str:
        """将 App 渲染为 html 纯文本

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
            history_mode: 历史路由模式. 默认为 "Hash".

        返回:
            str: html 纯文本
        """
        return render_as_html(
            self,
            template_name="app.html",
            locale=locale,
            cdn=cdn,
            version=version,
            site_title=site_title,
            site_icon=site_icon,
            theme=theme,
            custom_style=custom_style,
            request_adaptor=request_adaptor,
            response_adaptor=response_adaptor,
            history_mode=history_mode,
        )


class Button(AmisNode):
    """按钮"""

    type: Literal["button"] = Field(default="button", init=False)
    className: Optional[str] = None
    """指定添加 button 类名"""
    url: Optional[str] = None
    """点击跳转的地址，指定此属性 button 的行为和 a 链接一致"""
    size: Optional[Literal["xs", "sm", "md", "lg"]] = None
    """设置按钮大小"""
    actionType: Literal["button", "reset", "submit", "clear", "url"] = "button"
    """设置按钮类型"""
    level: Literal[
        "link",
        "primary",
        "secondary",
        "info",
        "success",
        "warning",
        "danger",
        "light",
        "dark",
        "default",
    ] = "default"
    """设置按钮样式"""
    tooltip: Optional[str] = None
    """气泡提示内容"""
    tooltipPlacement: Literal["top", "right", "bottom", "left"] = "top"
    """气泡框位置器"""
    tooltipTrigger: Optional[Literal["hover", "focus"]] = None
    """触发 tootip"""
    disabled: bool = False
    """按钮失效状态"""
    disabledTip: Optional[str] = None
    """按钮失效状态下的提示"""
    block: bool = False
    """将按钮宽度调整为其父宽度的选项"""
    loading: bool = False
    """显示按钮 loading 效果"""
    loadingOn: Optional[str] = None
    """显示按钮 loading 表达式"""


class ButtonGroup(AmisNode):
    """按钮组"""

    type: Literal["button-group"] = Field(default="button-group", init=False)
    """指定为 button-group 渲染器"""
    vertical: bool = False
    """是否使用垂直模式"""
    tiled: bool = False
    """是否使用平铺模式"""
    btnLevel: Literal[
        "link",
        "primary",
        "secondary",
        "info",
        "success",
        "warning",
        "danger",
        "light",
        "dark",
        "default",
    ] = "default"
    """按钮样式"""
    btnActiveLevel: Literal[
        "link",
        "primary",
        "secondary",
        "info",
        "success",
        "warning",
        "danger",
        "light",
        "dark",
        "default",
    ] = "default"
    """激活按钮样式"""
    buttons: List[Button] = []
    """行为按钮组"""
    className: Optional[str] = None
    """外层 Dom 的类名"""


class Breadcrumb(AmisNode):
    """面包屑"""

    class Item(AmisNode):
        class Dropdown(AmisNode):
            label: Optional[Template] = None
            """文本"""
            href: Optional[str] = None
            """链接"""
            icon: Optional[str] = None
            """图标"""

        label: Optional[Template] = None
        """文本"""
        href: Optional[str] = None
        """链接"""
        icon: Optional[str] = None
        """图标"""
        dropdown: Optional[List["Dropdown"]] = None
        """下拉菜单"""

    type: Literal["breadcrumb"] = Field(default="breadcrumb", init=False)
    """指定为 breadcrumb 渲染器"""
    className: Optional[str] = None
    """外层类名"""
    itemClassName: Optional[str] = None
    """导航项类名"""
    separatorClassName: Optional[str] = None
    """分割符类名"""
    dropdownClassName: Optional[str] = None
    """	下拉菜单类名"""
    dropdownItemClassName: Optional[str] = None
    """下拉菜单项类名"""
    separator: Optional[str] = None
    """分隔符"""
    labelMaxLength: int = 16
    """最大展示长度"""
    tooltipPosition: Literal["left", "right", "top", "bottom"] = "top"
    """浮窗提示位置"""
    source: Optional[str] = None
    """动态数据"""
    items: List[Item] = []


class Custom(AmisNode):
    """自定义组件"""

    type: Literal["custom"] = Field(default="custom", init=False)
    """指定为 custom 渲染器"""
    id: Optional[str] = None
    """节点 id"""
    name: Optional[str] = None
    """节点 名称"""
    className: Optional[str] = None
    """节点 class"""
    inline: bool = False
    """默认使用 div 标签，如果 true 就使用 span 标签"""
    html: Optional[str] = None
    """初始化节点 html"""
    onMount: Optional[str] = None
    """节点初始化之后调的用函数"""
    onUpdate: Optional[str] = None
    """数据有更新的时候调用的函数"""
    onUnmount: Optional[str] = None
    """节点销毁的时候调用的函数"""


class DropDownButton(AmisNode):
    """下拉菜单

    https://aisuda.bce.baidu.com/amis/zh-CN/components/dropdown-button"""

    class ButtonGroup(AmisNode):
        label: Optional[Template] = None
        """文本"""
        icon: Optional[str] = None
        """图标"""
        children: List[Button] = []

    type: Literal["dropdown-button"] = Field(default="dropdown-button", init=False)
    """指定为 dropdown-button 渲染器"""
    label: Optional[Template] = None
    """按钮文本"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    btnClassName: Optional[str] = None
    """按钮 CSS 类名"""
    menuClassName: Optional[str] = None
    """下拉菜单 CSS 类名"""
    block: Optional[bool] = None
    """块状样式"""
    size: Optional[Literal["sm", "xs", "md", "lg"]] = None
    """尺寸"""
    align: Optional[Literal["left", "right"]] = None
    """位置"""
    buttons: List[Union[Button, ButtonGroup]] = []
    """配置下拉按钮"""
    iconOnly: Optional[bool] = None
    """只显示icon"""
    defaultIsOpened: Optional[bool] = None
    """默认是否打开"""
    closeOnOutside: bool = True
    """点击外侧区域是否收起"""
    closeOnClick: bool = False
    """点击按钮后自动关闭下拉菜单"""
    trigger: Literal["hover", "click"] = "click"
    """触发方式"""
    hideCaret: bool = False
    """隐藏下拉图标"""
    rightIcon: Optional[str] = None
    """右侧图标"""
    onEvent: OnEvent[Literal["mouseenter", "mouseleave"]] = None


class Service(AmisNode):
    """功能型容器

    https://aisuda.bce.baidu.com/amis/zh-CN/components/service"""

    class RebuildAction(EventAction):
        class Args(TypedDict):
            schemaType: NotRequired[str]

        actionType: Literal["rebuild"] = Field(default="rebuild", init=False)
        componentId: str
        args: Optional[Args] = None

    class WS(TypedDict):
        url: str
        data: DictStrAny

    class Message(TypedDict):
        fetchSuccess: NotRequired[str]
        """接口请求成功时的 toast 提示文字"""
        fetchFailed: NotRequired[str]
        """接口请求失败时 toast 提示文字"""

    type: Literal["service"] = Field(default="service", init=False)
    """指定为 service 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    body: SchemaNode
    """内容容器"""
    api: Optional[API] = None
    """初始化数据域接口地址"""
    ws: Union[str, WS, None] = None
    """WebScocket 地址"""
    dataProvider: Optional[str] = None
    """数据获取函数"""
    initFetch: Optional[bool] = None
    """是否默认拉取"""
    schemaApi: Optional[API] = None
    """用来获取远程 Schema 接口地址"""
    initFetchSchema: Optional[bool] = None
    """是否默认拉取 Schema"""
    messages: Optional[Message] = None
    """消息提示覆写，默认消息读取的是接口返回的 toast 提示文字，但是在此可以覆写它。"""
    interval: Optional[int] = Field(default=None, ge=1000)
    """轮询时间间隔(最低 3000)"""
    silentPolling: bool = False
    """配置轮询时是否显示加载动画"""
    stopAutoRefreshWhen: Optional[Expression] = None
    """配置停止轮询的条件"""
    showErrorMsg: bool = True
    """是否以 Alert 的形式显示 api 接口响应的错误信息，默认展示"""
    onEvent: OnEvent[Literal["init", "fetchInited", "fetchSchemaInited"]] = None


class Nav(AmisNode):
    """导航

    https://aisuda.bce.baidu.com/amis/zh-CN/components/nav"""

    class UpdateItemsAction(EventAction):
        class Args(TypedDict):
            value: Union[str, List[str]]

        actionType: Literal["updateItems"] = Field(default="updateItems", init=False)
        componentId: str
        args: Args

    class Link(AmisNode):
        label: Optional[Template] = None
        """名称"""
        to: Optional[Template] = None
        """链接地址"""
        target: Optional[str] = None
        """链接关系"""
        icon: Optional[str] = None
        """图标"""
        children: Optional[List["Nav.Link"]] = None
        """子链接"""
        unfolded: Optional[bool] = None
        """初始是否展开"""
        active: Optional[bool] = None
        """是否高亮"""
        activeOn: Optional[Expression] = None
        """是否高亮的条件，留空将自动分析链接地址"""
        defer: Optional[bool] = None
        """标记是否为懒加载项"""
        deferApi: Optional[API] = None
        """可以不配置，如果配置优先级更高"""
        disabled: Optional[bool] = None
        """是否禁用"""
        disabledTip: Optional[str] = None
        """禁用提示信息"""
        className: Optional[str] = None
        """菜单项自定义样式"""
        mode: Optional[Literal["group", "divider"]] = None
        """菜菜单项模式，分组模式："group"、分割线："divider" """
        overflow: Optional["Nav.Overflow"] = None
        """导航项响应式收纳配置"""

    class Overflow(AmisNode):
        enable: bool = False
        """是否开启响应式收纳"""
        overflowLabel: Optional[Union[str, DictStrAny]] = None
        """菜单触发按钮的文字"""
        overflowIndicator: str = "fa fa-ellipsis"
        """菜单触发按钮的图标"""
        maxVisibleCount: Optional[int] = None
        """开启响应式收纳后导航最大可显示数量，超出此数量的导航将被收纳到下拉菜单中，默认为自动计算"""
        wrapperComponent: Optional[str] = None
        """包裹导航的外层标签名，可以使用其他标签渲染"""
        style: Optional[str] = None
        """自定义样式"""
        overflowClassName: Optional[str] = None
        """菜单按钮 CSS 类名"""
        overflowPopoverClassName: Optional[str] = None
        """Popover 浮层 CSS 类名"""

    type: Literal["nav"] = Field(default="nav", init=False)
    """指定为 Nav 渲染器"""
    model: Literal["float", "inline"] = "inline"
    """导航模式，悬浮或者内联，默认内联模式"""
    collapsed: Optional[bool] = None
    """控制导航是否缩起"""
    indentSize: int = 16
    """层级缩进值，仅内联模式下生效"""
    level: Optional[int] = None
    """控制导航最大展示层级数"""
    defaultOpenLevel: Optional[int] = None
    """控制导航最大默认展开层级"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    popupClassName: Optional[str] = None
    """当为悬浮模式时，可自定义悬浮层样式"""
    expandIcon: Optional[str] = None
    """自定义展开按钮"""
    expandPosition: Optional[Literal["before", "after"]] = None
    """展开按钮位置，"before"或者"after"，不设置默认在前面"""
    stacked: bool = True
    """设置成 false 可以以 tabs 的形式展示"""
    accordion: Optional[bool] = None
    """是否开启手风琴模式"""
    source: Optional[API] = None
    """可以通过变量或 API 接口动态创建导航"""
    deferApi: Optional[API] = None
    """用来延时加载选项详情的接口，可以不配置，不配置公用 source 接口。"""
    itemActions: Optional[SchemaNode] = None
    """更多操作相关配置"""
    draggable: Optional[bool] = None
    """是否支持拖拽排序"""
    dragOnSameLevel: Optional[bool] = None
    """仅允许同层级内拖拽"""
    saveOrderApi: Optional[API] = None
    """保存排序的 api"""
    itemBadge: Optional["Badge"] = None
    """角标"""
    links: Optional[List[Link]] = None
    """链接集合"""
    overflow: Optional[List[Overflow]] = None
    """响应式收纳配置"""
    onEvent: OnEvent[Literal["loaded", "collapsed", "toggled", "change", "click"]] = None


class AnchorNav(AmisNode):
    """锚点导航"""

    class Link(AmisNode):
        label: Optional[Template] = None
        """名称"""
        title: Optional[str] = None
        """区域 标题"""
        href: Optional[str] = None
        """区域 标识"""
        body: Optional[SchemaNode] = None
        """区域 内容区"""
        className: str = "bg-white b-l b-r b-b wrapper-md"
        """区域成员 样式"""

    type: Literal["anchor-nav"] = Field(default="anchor-nav", init=False)
    """指定为 AnchorNav 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    linkClassName: Optional[str] = None
    """导航 Dom 的类名"""
    sectionClassName: Optional[str] = None
    """锚点区域 Dom 的类名"""
    links: Optional[List[Link]] = None
    """links 内容"""
    direction: Literal["vertical", "horizontal"] = "vertical"
    """可以配置导航水平展示还是垂直展示。对应的配置项分别是：vertical、horizontal"""
    active: Optional[str] = None
    """需要定位的区域"""


class TooltipWrapper(AmisNode):
    """文字提示容器

    https://aisuda.bce.baidu.com/amis/zh-CN/components/tooltip"""

    type: Literal["tooltip-wrapper"] = Field(default="tooltip-wrapper", init=False)
    """指定为 tooltip-wrapper 渲染器"""
    title: Optional[str] = None
    """文字提示标题"""
    content: Optional[str] = None
    """文字提示内容, 兼容之前的 tooltip 属性"""
    placement: Literal["top", "right", "bottom", "left"] = "top"
    """文字提示浮层出现位置"""
    tooltipTheme: Literal["dark", "light"] = "light"
    """主题样式， 默认为 light"""
    offset: Tuple[int, int] = (0, 0)
    """文字提示浮层位置相对偏移量，单位 px"""
    showArrow: bool = True
    """是否展示浮层指向箭头"""
    enterable: bool = True
    """是否鼠标可以移入到浮层中"""
    disabled: bool = False
    """是否禁用浮层提示"""
    trigger: Union[Literal["hover", "click", "focus"], List[Literal["hover", "click", "focus"]]] = "hover"
    """浮层触发方式，支持数组写法["hover", "click"]"""
    mouseEnterDelay: int = 0
    """浮层延迟展示时间，单位 ms"""
    mouseLeaveDelay: int = 300
    """浮层延迟隐藏时间，单位 ms"""
    rootClose: bool = True
    """是否点击非内容区域关闭提示"""
    inline: bool = False
    """内容区是否内联显示"""
    wrapperComponent: Optional[Literal["div", "span"]] = None
    """容器标签名"""
    body: Optional[SchemaNode] = None
    """内容容器"""
    style: Optional[Union[DictStrAny, str]] = None
    """内容区自定义样式"""
    tooltipStyle: Optional[Union[DictStrAny, str]] = None
    """浮层自定义样式"""
    className: Optional[str] = None
    """内容区类名"""
    tooltipClassName: Optional[str] = None
    """文字提示浮层类名"""


class PopOver(AmisNode):
    mode: Literal["popOver", "dialog"] = "popOver"
    """ 可配置成 popOver、dialog 或者 drawer。 默认为 popOver。"""
    size: Optional[int] = None
    """当配置成 dialog 或者 drawer 的时候有用。"""
    position: Optional[Literal["center", "left-top", "right-top", "left-bottom", "right-bottom"]] = None
    """配置弹出位置，只有 popOver 模式有用，默认是自适应。"""
    offset: Tuple[int, int] = (0, 0)
    """默认 {top: 0, left: 0}，如果要来一定的偏移请设置这个"""
    trigger: Literal["click", "hover"] = "click"
    """触发弹出的条件"""
    showIcon: Optional[bool] = None
    """是否显示图标。默认会有个放大形状的图标出现在列里面。如果配置成 false，则触发事件出现在列上就会触发弹出。"""
    title: Optional[str] = None
    """弹出框的标题"""
    body: Optional[SchemaNode] = None
    """弹出框的内容"""


__all__ = [
    "Action",
    "PageSchema",
    "App",
    "Button",
    "ButtonGroup",
    "Breadcrumb",
    "Custom",
    "DropDownButton",
    "Service",
    "Nav",
    "AnchorNav",
    "TooltipWrapper",
    "PopOver",
]
