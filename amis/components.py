"""详细文档阅读地址: https://baidu.gitee.io/amis/zh-CN/components"""
from pathlib import Path
from typing import Literal
from typing import Union, List, Optional, Any, Dict, Tuple

from jinja2 import Environment, FileSystemLoader
from pydantic import Field

from .constants import LevelEnum, DisplayModeEnum, SizeEnum, TabsModeEnum
from .types import API, Expression, AmisNode, SchemaNode, Template, BaseAmisModel, OptionsNode, Tpl

env = Environment(loader=FileSystemLoader(Path(__file__).parent / 'templates'))


class Html(AmisNode):
    """Html"""
    type: str = "html"
    """指定为 html 组件"""
    html: str = None
    """html  当需要获取数据域中变量时，使用 Tpl 。"""


class Icon(AmisNode):
    """图标"""
    type: str = "icon"
    """指定组件类型"""
    className: str = None
    """外层 CSS 类名"""
    icon: Template = None
    """icon 名称，支持 fontawesome v4 或 通过 registerIcon 注册的 icon、或使用 url"""
    vendor: str = None
    """icon 类型，默认为fa, 表示 fontawesome v4。也支持 iconfont, 如果是 fontawesome v5 以上版本或者其他框架可以设置为空字符串"""


class Remark(AmisNode):
    """标记"""
    type: str = "remark"
    """remark"""
    className: str = None
    """外层 CSS 类名"""
    content: str = None
    """提示文本"""
    shape: str = None
    """形状"""
    placement: str = None
    """弹出位置"""
    trigger: Union[str,List[str]] = ['hover', 'focus']
    """触发条件 ['hover','focus']"""
    icon: str = "fa fa-question-circle"
    """图标"""


class Badge(AmisNode):
    """角标"""
    mode: Literal["dot","text","ribbon"] = "dot"
    """角标类型，可以是 dot/text/ribbon"""
    text: Union[str, int] = None
    """角标文案，支持字符串和数字，在mode='dot'下设置无效"""
    size: int = None
    """角标大小"""
    level: Literal["info","success","warning","danger"] = None
    """角标级别, 可以是info/success/warning/danger, 设置之后角标背景颜色不同"""
    overflowCount: int = 99
    """设置封顶的数字值"""
    position: str = "top-right"
    """"角标位置， 可以是top-right/top-left/bottom-right/bottom-left"""
    offset: List[int] = [0, 0]
    """角标位置，优先级大于position，当设置了offset后，以postion为top-right为基准进行定位  number[top, left]"""
    className: str = None
    """外层 dom 的类名"""
    animation: bool = None
    """角标是否显示动画"""
    style: dict = None
    """角标的自定义样式"""
    visibleOn: Expression = None
    """控制角标的显示隐藏"""


class Page(AmisNode):
    """页面"""
    __default_template_path__: str = 'page.jinja2'

    type: str = "page"
    """指定为 Page 组件"""
    title: SchemaNode = None
    """页面标题"""
    subTitle: SchemaNode = None
    """页面副标题"""
    remark: "Remark" = None
    """标题附近会出现一个提示图标，鼠标放上去会提示该内容。"""
    aside: SchemaNode = None
    """往页面的边栏区域加内容"""
    asideResizor: bool = None
    """页面的边栏区域宽度是否可调整"""
    asideMinWidth: int = None
    """页面边栏区域的最小宽度"""
    asideMaxWidth: int = None
    """页面边栏区域的最大宽度"""
    asideSticky: bool = True
    """用来控制边栏固定与否"""
    toolbar: SchemaNode = None
    """往页面的右上角加内容，需要注意的是，当有 title 时，该区域在右上角，没有时该区域在顶部"""
    body: SchemaNode = None
    """往页面的内容区域加内容"""
    className: str = None
    """外层 dom 类名"""
    cssVars: dict = None
    """自定义 CSS 变量，请参考样式"""
    toolbarClassName: str = "v-middle wrapper text-right bg-light b-b"
    """Toolbar dom 类名"""
    bodyClassName: str = "wrapper"
    """Body dom 类名"""
    asideClassName: str = "w page-aside-region bg-auto"
    """Aside dom 类名"""
    headerClassName: str = "bg-light b-b wrapper"
    """Header 区域 dom 类名"""
    initApi: API = None
    """Page 用来获取初始数据的 api。返回的数据可以整个 page 级别使用。"""
    initFetch: bool = True
    """是否起始拉取 initApi"""
    initFetchOn: Expression = None
    """是否起始拉取 initApi, 通过表达式配置"""
    interval: int = 3000
    """刷新时间(最小 1000)"""
    silentPolling: bool = False
    """配置刷新时是否显示加载动画"""
    stopAutoRefreshWhen: Expression = ""
    """通过表达式来配置停止刷新的条件"""
    pullRefresh: dict = {"disabled": True}
    """下拉刷新配置（仅用于移动端）"""

    def render(
            self,
            template_name: str = '',
            locale: str = 'zh_CN',
            cdn: str = 'https://unpkg.com',
            version: str = 'latest',
            site_title: str = 'Amis',
            site_icon: str = '',
            theme: str = 'default',
            routerModel:str = 'createHashHistory',
            requestAdaptor: str = '',
            responseAdaptor: str = '',

    ) -> str:
        """渲染html模板"""
        if theme == 'default':
            theme_css = 'sdk.css'
            theme_name = 'cxd'
        else:
            theme_css = f'{theme}.css'
            theme_name = theme
        template_name = template_name or self.__default_template_path__
        return env.get_template(template_name).render(
            **{
                'AmisSchemaJson': self.to_json(),
                'locale': locale,
                'cdn': cdn,
                'version': version,
                'site_title': site_title,
                'site_icon': site_icon,
                'theme_css': theme_css,
                'theme_name': theme_name,
                'routerModel':routerModel,
                'requestAdaptor': requestAdaptor,
                'responseAdaptor': responseAdaptor
            }
        )


class Container(AmisNode):
    """容器"""
    type: str = "container"
    """container"""
    className: str = None
    """外层 dom 类名"""
    bodyClassName: str = None
    """	容器内容区的类名"""
    wrapperComponent: str = "div"
    """容器标签名，默认为div"""
    style: dict = None
    """自定义样式"""
    body: SchemaNode = None
    """容器内容"""


class Collapse(AmisNode):
    """折叠器"""
    type: str = "collapse"
    """指定为 collapse 渲染器"""
    disabled: bool = False
    """是否禁用，默认为False"""
    collapsed: bool = True
    """初始状态是否折叠，默认为True"""
    key: Union[str, int] = None
    """标识"""
    header: Union[str, SchemaNode] = None
    """标题"""
    body: Union[str, SchemaNode] = None
    """内容"""
    showArrow: bool = True
    """是否展示图标，默认为True"""


class CollapseGroup(AmisNode):
    """折叠器组"""
    type: str = "collapse-group"
    """指定为 collapse-group 渲染器"""
    activeKey: List[Union[str, str]] = None
    """初始化激活面板的key"""
    accordion: bool = False
    """手风琴模式，默认为False"""
    expandIcon: SchemaNode = None
    """自定义切换图标"""
    expandIconPosition: Literal["left", "right"] = "left"
    """设置图标位置，可选值left | right"""
    body: List[Collapse] = None
    """折叠列表"""


class Divider(AmisNode):
    """分割线"""
    type: str = "divider"
    """Divider"""
    className: str = None
    """外层 Dom 的类名"""
    lineStyle: Literal["dashed", "solid"] = "dashed"
    """分割线的样式，支持dashed和solid"""


class Flex(AmisNode):
    """布局"""
    type: str = "flex"
    """指定为 Flex 渲染器"""
    className: str = None
    """css 类名"""
    justify: Literal[
        "start", "flex-start", "center", "end", "flex-end", "space-around", "space-between", "space-evenly"] = None
    """start", "flex-start", "center", "end", "flex-end", "space-around", "space-between", "space-evenly"""
    alignItems: Literal["stretch", "start", "flex-start", "flex-end", "end", "center", "baseline"] = None
    """stretch", "start", "flex-start", "flex-end", "end", "center", "baseline"""
    style: dict = None
    """自定义样式"""
    items: List[SchemaNode] = None
    """组件列表"""


class Grid(AmisNode):
    """水平布局"""

    class Column(AmisNode):
        """列配置"""
        xs: Union[int, str] = None
        """宽度占比：1 - 12或'auto'"""
        ClassName: str = None
        """列类名"""
        sm: Union[int, str] = None
        """宽度占比：1 - 12或'auto'"""
        md: Union[int, str] = None
        """宽度占比：1 - 12或'auto'"""
        lg: Union[int, str] = None
        """宽度占比：1 - 12或'auto'"""
        valign: Literal['top', 'middle', 'bottom', 'between'] = None
        """当前列内容的垂直对齐"""
        body: SchemaNode = None

    type: str = "grid"
    """指定为 Grid 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    gap: Literal['xs', 'sm', 'base', 'none', 'md', 'lg'] = None
    """水平间距"""
    valign: Literal['top', 'middle', 'bottom', 'between'] = None
    """垂直对齐方式"""
    align: Literal['left', 'right', 'between', 'center'] = None
    """水平对齐方式"""
    columns: List[Column] = None


class Grid2D(AmisNode):
    """Grid 2D布局"""

    class Grid(AmisNode):
        """格子配置"""
        x: int = None
        """格子起始位置的横坐标"""
        y: int = None
        """格子起始位置的纵坐标"""
        w: int = None
        """格子横跨几个宽度"""
        h: int = None
        """格子横跨几个高度"""
        width: Union[int, str] = None
        """格子所在列的宽度"""
        height: Union[int, str] = None
        """格子所在行的高度，可以设置 auto"""
        align: Literal['left', 'right', 'center', 'auto'] = "auto"
        """格子内容水平布局"""
        valign: Literal['top', 'middle', 'bottom', 'auto'] = "auto"
        """格子内容垂直布局"""
        body: SchemaNode = None

    type: str = "grid-2d"
    """指定为 Grid 2D 渲染器"""
    gridClassName: str = None
    """外层 Dom 的类名"""
    gap: Union[int, str] = 0
    """格子间距，包括水平和垂直"""
    cols: int = 12
    """格子水平划分为几个区域"""
    rowHeight: int = 50
    """每个格子默认垂直高度"""
    rowGap: Union[int, str] = None
    """格子垂直间距"""
    grids: List[Grid] = None
    """格子集合"""


class HBox(AmisNode):
    """HBox布局"""

    class Column(AmisNode):
        """列配置"""
        columnClassName: str = "wrapper-xs"
        """列上类名"""
        valign: Literal["top", "middle", "bottom", "between"] = None
        """当前列内容的垂直对齐"""
        body: SchemaNode = None
        """内容"""

    type: str = "hbox"
    """指定为 HBox 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    gap: Literal["xs", "sm", "base", "none", "md", "lg"] = None
    """水平间距"""
    valign: Literal["top", "middle", "bottom", "between"] = None
    """垂直对齐方式"""
    align: Literal["left", "right", "between", "center"] = None
    """水平对齐方式"""
    columns: List[Column] = None
    """列集合"""


class Pagination(AmisNode):
    """分页"""
    type: str = "pagination"
    """指定为 Pagination渲染器"""
    mode: Literal["normal", "simple"] = "normal"
    """迷你版本/简易版本 只显示左右箭头，配合hasNext使用"""
    layout: Union[str, List[str]] = ["pager"]
    """通过控制layout属性的顺序，调整分页结构布局"""
    maxButtons: int = 5
    """最多显示多少个分页按钮，最小为5"""
    lastPage: int = None
    """总页数 （设置总条数total的时候，lastPage会重新计算）"""
    total: int = None
    """总条数"""
    activePage: int = 1
    """当前页数"""
    perPage: int = 10
    """每页显示多条数据"""
    showPerPage: bool = False
    """是否展示perPage切换器layout和showPerPage都可以控制"""
    perPageAvailable: List[int] = [10, 20, 50, 100]
    """指定每页可以显示多少条"""
    showPageInput: bool = False
    """是否显示快速跳转输入框layout和showPageInput都可以控制"""
    disabled: bool = False
    """是否禁用"""
    onPageChange: str = "(page: number, perPage: number) => void;"
    """分页改变触发"""


class PaginationWrapper(AmisNode):
    """分页容器"""
    type: str = "pagination-wrapper"
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
    body: SchemaNode = None
    """内容区域"""


class Panel(AmisNode):
    """面板"""
    type: str = "panel"
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
    title: SchemaNode = None
    """标题"""
    header: SchemaNode = None
    """头部容器"""
    body: SchemaNode = None
    """内容容器"""
    footer: SchemaNode = None
    """底部容器"""
    affixFooter: bool = None
    """是否固定底部容器"""
    actions: List["Action"] = None
    """按钮区域"""


class Tabs(AmisNode):
    """选项卡"""

    class Item(AmisNode):
        title: str = None
        """Tab 标题"""
        icon: Union[str, Icon] = None
        """Tab 的图标"""
        tab: SchemaNode = None
        """内容区"""
        hash: str = None
        """设置以后将跟 url 的 hash 对应"""
        reload: bool = None
        """设置以后内容每次都会重新渲染，对于 crud 的重新拉取很有用"""
        unmountOnExit: bool = None
        """每次退出都会销毁当前 tab 栏内容"""
        className: str = "bg-white b-l b-r b-b wrapper-md"
        """Tab 区域样式"""
        iconPosition: Literal["left", "right"] = "left"
        """Tab 的图标位置"""
        closable: bool = False
        """是否支持删除，优先级高于组件的 closable"""
        disabled: bool = False
        """是否禁用"""

    type: str = "tabs"
    """指定为 Tabs 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    tabsMode: TabsModeEnum = None
    """展示模式，取值可以是 line、card、radio、vertical、chrome、simple、strong、tiled、sidebar"""
    tabsClassName: str = None
    """Tabs Dom 的类名"""
    tabs: List[Item] = None
    """tabs 内容"""
    source: str = None
    """tabs 关联数据，关联后可以重复生成选项卡"""
    toolbar: SchemaNode = None
    """tabs 中的工具栏"""
    toolbarClassName: str = None
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
    showTipClassName: str = ""
    """提示的类"""
    editable: bool = False
    """收否可编辑标签名"""
    scrollable: bool = True
    """是否导航支持内容溢出滚动。（属性废弃）"""
    sidePosition: Literal['left', 'right'] = "left"
    """sidebar 模式下，标签栏位置"""
    collapseOnExceed: int = None
    """当 tabs 超出多少个时开始折叠"""
    collapseBtnLabel: str = "more"
    """用来设置折叠按钮的文字"""


class Wrapper(AmisNode):
    """包裹容器"""
    type: str = "wrapper"
    """指定为 Wrapper 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    size: Literal["xs", "sm", "md", "lg"] = None
    """支持: xs、sm、md和lg"""
    style: Union[dict, str] = None
    """	自定义样式"""
    body: SchemaNode = None
    """内容容器"""


class Portlet(Tabs):
    """门户栏目"""

    class Item(Tabs.Item):
        toolbar: SchemaNode = None

    """tabs 中的工具栏，随 tab 切换而变化"""

    type: str = "portlet"
    """指定为 Portlet 渲染器"""
    contentClassName: str = None
    """Tabs content Dom 的类名"""
    tabs: List[Item] = None
    """tabs 内容"""
    source: dict = None
    """tabs 关联数据，关联后可以重复生成选项卡"""
    toolbar: SchemaNode = None
    """tabs 中的工具栏，不随 tab 切换而变化"""
    style: Union[str, dict] = None
    """自定义样式"""
    description: Template = None
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


class Horizontal(AmisNode):
    """配置页面占比"""
    left: int = None
    """左边 label 的宽度占比"""
    right: int = None
    """右边控制器的宽度占比。"""
    offset: int = None
    """当没有设置 label 时，右边控制器的偏移量"""


class Action(AmisNode):
    """行为按钮"""
    type: str = "action"
    """指定为 Page 渲染器"""
    actionType: Literal[
        "ajax", "link", "url", "drawer", "dialog", "confirm", "cancel", "prev", "next", "copy", "close", "reload"] = None
    """这是 action 最核心的配置，来指定该 action 的作用类型，支持：ajax、link、url、drawer、dialog、confirm、cancel、prev、next、copy、close、reload。"""
    label: Union[str ,bool]= None
    """按钮文本。可用 ${xxx} 取值。"""
    level: LevelEnum = LevelEnum.default
    """按钮样式，支持：link、primary、secondary、info、success、warning、danger、light、dark、default。"""
    size: Literal["xs", "sm", "md", "lg"] = None
    """按钮大小，支持：xs、sm、md、lg。"""
    icon: str = None
    """设置图标，例如fa fa-plus。"""
    className: str = None
    """类名"""
    iconClassName: str = None
    """给图标上添加类名。"""
    rightIcon: str = None
    """在按钮文本右侧设置图标，例如fa fa-plus。"""
    rightIconClassName: str = None
    """给右侧图标上添加类名。"""
    active: bool = None
    """按钮是否高亮。"""
    activeLevel: str = None
    """按钮高亮时的样式，配置支持同level。"""
    activeClassName: str = "is-active"
    """给按钮高亮添加类名。"""
    block: bool = None
    """用display:"block"来显示按钮。"""
    confirmText: Template = None
    """当设置后，操作在开始前会询问用户。可用 ${xxx} 取值。"""
    reload: str = None
    """指定此次操作完后，需要刷新的目标组件名字（组件的name值，自己配置的），多个请用 , 号隔开。"""
    tooltip: str = None
    """鼠标停留时弹出该段文字，也可以配置对象类型：字段为title和content。可用 ${xxx} 取值。"""
    disabledTip: str = None
    """被禁用后鼠标停留时弹出该段文字，也可以配置对象类型：字段为title和content。可用 ${xxx} 取值。"""
    tooltipPlacement: Literal["top", "bottom", "left", "right"] = "top"
    """如果配置了tooltip或者disabledTip，指定提示信息位置，可配置top、bottom、left、right。"""
    close: Union[bool, str] = None
    """当action配置在dialog或drawer的actions中时，配置为true指定此次操作完后关闭当前dialog或drawer。当值为字符串，并且是祖先层弹框的名字的时候，会把祖先弹框关闭掉。"""
    required: List[str] = None
    """配置字符串数组，指定在form中进行操作之前，需要指定的字段名的表单项通过验证"""


class ActionType:
    """行为按钮类型"""

    class Ajax(Action):
        """发送http请求"""
        actionType: str = 'ajax'
        """点击后显示一个弹出框"""
        api: API = None
        """请求地址，参考 api 格式说明。"""
        redirect: Template = None
        """指定当前请求结束后跳转的路径，可用 ${xxx} 取值。"""
        options: dict = None
        """其他配置"""
        outputVar: str = None
        """请求响应结果缓存在${event.data.responseResult}或${event.data.{outputVar}}"""
        feedback: "Dialog" = None
        """如果 ajax 类型的，当 ajax 返回正常后，还能接着弹出一个 dialog 做其他交互。返回的数据可用于这个 dialog 中。格式可参考Dialog"""
        messages: dict = None
        """success：ajax 操作成功后提示，可以不指定，不指定时以 api 返回为准。failed：ajax 操作失败提示。"""

    class Dialog(Action):
        """打开弹窗"""
        actionType: str = 'dialog'
        """点击后显示一个弹出框"""
        dialog: Union["Dialog", "Service", SchemaNode] = None
        """指定弹框内容，格式可参考Dialog"""
        nextCondition: bool = None
        """可以用来设置下一条数据的条件，默认为 true。"""

    class CloseDialog(Action):
        """关闭弹窗"""
        actionType: str = "closeDialog"
        """点后关闭当前弹窗"""
        componentId: str = None
        """指定弹框组件 id"""

    class Drawer(Action):
        """打开抽屉"""
        actionType: str = 'drawer'
        """点击后显示一个侧边栏"""
        drawer: Union["Drawer", "Service", SchemaNode]
        """指定弹框内容，格式可参考Drawer"""

    class CloseDrawer(Action):
        """关闭抽屉"""
        actionType: str = "'closeDrawer"
        """点击后关闭当前抽屉"""
        componentId: str = None
        """指定弹框组件 id"""

    class Alert(Action):
        """打开对话框"""
        actionType: str = 'alert'
        """点击出现对话框"""
        title: str = "系统提示"
        """对话框标题"""
        msg: str = None
        """对话框提示内容"""

    class Confirm(Action):
        """打开对话框"""
        actionType: str = 'confirm'
        """点击出现对话框"""
        title: str = "系统提示"
        """对话框标题"""
        msg: str = None
        """对话框提示内容"""

    class ConfirmDialog(Action):
        """打开对话框"""
        actionType: str = 'confirmDialog'
        """点击出现对话框"""
        title: str = "系统提示"
        """对话框标题"""
        msg: str = None
        """对话框提示内容"""

    class Copy(Action):
        """复制内容"""
        actionType: str = 'copy'
        """复制一段内容到粘贴板"""
        content: Template
        """指定复制的内容。可用 ${xxx} 取值。"""
        copyFormat: str = "text/html"
        """可以通过 copyFormat 设置复制的格式，默认是文本 text/html"""

    class Url(Action):
        """直接跳转"""
        actionType: str = 'url'
        """直接跳转"""
        url: str = None
        """按钮点击后，会打开指定页面。可用 ${xxx} 取值。"""
        blank: bool = False
        """false 如果为 true 将在新 tab 页面打开。"""
        params: dict = None
        """页面参数{key:value}，支持数据映射，> 1.10.0 及以上版本"""

    class Link(Action):
        """单页跳转"""
        actionType: str = 'link'
        """单页跳转"""
        link: str = None
        """用来指定跳转地址，跟 url 不同的是，这是单页跳转方式，不会渲染浏览器，请指定 amis 平台内的页面。可用 ${xxx} 取值。"""
        params: dict = None
        """页面参数{key:value}，支持数据映射，> 1.10.0 及以上版本"""

    class GoBock(Action):
        """浏览器回退"""
        actionType: str = "gpBack"
        """点击后浏览器回退页面"""

    class GoPage(Action):
        """浏览器到指定位置"""
        actionType: str = "gpPage"
        """点击后浏览器跳转页面"""
        delta: int = 0
        """位置"""

    class Refresh(Action):
        """刷新页面"""
        actionType: str = 'refresh'
        """点击后刷新页面"""

    class Toast(Action):
        """提示"""
        actionType: str = 'toast'
        """点击提示内容"""
        msgType: Literal["info", "success", "error", "warning"] = "info"
        """消息类型"""
        msg: str = None
        """消息内容"""
        position: Literal[
            "top-right", "top-center", "top-left", "bottom-center", "bottom-left", "bottom-right", "center"] = "top-center"
        """提示显示位置（移动端为center）: top-right|top-center|top-left|bottom-center|bottom-left|bottom-right|center"""
        closeButton: bool = False
        """是否展示关闭按钮"""
        showIcon: bool = True
        """是否展示图标"""
        timeout: int = 5000
        """持续时间（error类型为6000，移动端为3000）"""

    class Emali(Action):
        """发送邮件"""
        actionType: str = 'email'
        """点击后发送邮件"""
        to: str = None
        """收件人邮箱，可用 ${xxx} 取值"""
        cc: str = None
        """抄送邮箱，可用 ${xxx} 取值"""
        bcc: str = None
        """匿名抄送邮箱，可用 ${xxx} 取值"""
        subject: str = None
        """匿名抄送邮箱，可用 ${xxx} 取值"""
        body: str = None
        """邮件正文，可用 ${xxx} 取值"""

    class Reload(Action):
        """
        刷新
        仅支持form、wizard、service、page、app、chart、crud，以及支持动态数据的输入类组件，详见组件的动作表
        """
        actionType: str = 'reload'
        """点击刷新"""
        resetPage: bool = True
        """当目标组件为 crud 时，可以控制是否重置页码，> 2.3.2 及以上版本"""
        componentId: str = None
        """指定刷新的目标组件 id"""

    class Show(Action):
        """显示"""
        actionType: str = 'show'
        """点击后显示"""
        componentId: str = None
        """指定显示的目标组件 id"""

    class Hidden(Action):
        """隐藏"""
        actionType: str = 'hidden'
        """点击后隐藏"""
        componentId: str = None
        """指定隐藏的目标组件 id"""

    class Enable(Action):
        "启用"
        actionType: str = 'enabled'
        """点击后启用"""
        componentId: str = None
        """指定启用的目标组件 id"""

    class Disable(Action):
        "禁用"
        actionType: str = 'disabled'
        """点击后禁用"""
        componentId: str = None
        """指定禁用的目标组件 id"""

    class SetValue(Action):
        """
        更新数据
        - 数据类型支持范围：基础类型、对象类型、数组类型，数据类型取决于目标组件所需数据值类型
        - 目标组件支持范围：form、dialog、drawer、wizard、service、page、app、chart，以及数据输入类组件
        - < 2.3.2 及以下版本，虽然更新数据可以实现对组件数据域的更新，但如果更新数据动作的数据值来自前面的异步动作（例如 发送 http 请求、自定义 JS（异步）），
        则后面的动作只能通过事件变量${event.data.xxx}来获取异步动作产生的数据，无法通过当前数据域${xxx}直接获取更新后的数据。
        - 它的值通常都是对象形式，比如 form 传递的值应该是类似 {"user": "amis"}，这时就会更新表单里的 user 字段值为 amis
        """
        actionType: str = 'setValue'
        """点击后更新数据"""
        value: Any = None
        """值"""
        index: int = None
        """当目标组件是combo时，可以指定更新的数据索引， 1.10.1 及以上版本"""
        componentId: str = None
        """指定赋值的目标组件 id"""

    class Custom(Action):
        """
        自定义JS
        JS 中可以访问以下对象和方法：
        - context，渲染器上下文
        - doAction() 动作执行方法，用于调用任何 actionType 指定的动作
        - event，事件对象，可以调用 setData()、stopPropagation()、preventDefault()分别实现事件上下文设置、动作干预、事件干预，可以通过 event.data 获取事件上下文
        """
        script: str = None
        """自定义 JS 脚本代码，代码内可以通过调用doAction执行任何动作 ，通过事件对象event可以实现事件动作干预"""

    class ChangeActiveKey(Action):
        """触发其他组件动作"""
        actionType: str = "changeActiveKey"
        """点击触发其他组件动作"""
        args: dict = None
        """参数"""
        componentId: str = None
        """指定触发的目标组件 id"""

    class Broadcast(Action):
        """触发广播动作"""
        actionType: str = "broadcast"
        """点击触发广播"""
        eventName: str = None
        """广播动作对应的自定义事件名称，用于广播事件的监听"""
        weight: int = 0
        """可以通过配置动作执行优先级来控制所有监听者的动作执行顺序"""

    class For(Action):
        """循环事件"""
        actionType: str = "for"
        """点击触发循环事件"""
        loopName: str = None
        """循环变量名称"""
        children: List[Action] = None
        """子动作，可以通过break动作来跳出循环"""

    class Break(Action):
        """跳出循环"""
        actionType: str = "break"
        """点击跳出循环"""

    class Continue(Action):
        """跳转循环"""
        actionType: str = "continue"
        """点击跳砖循环"""

    class Switch(Action):
        """排他事件"""
        actionType: str = "switch"
        """点击触发排他事件"""
        children: List[Action] = None
        """子动作，每个子动作可以通过配置expression来匹配的条件"""

    class Parallel(Action):
        """并行事件"""
        actionType: str = "parallel"
        """点击触发并行事件"""
        children: List[Action] = None
        """子动作"""


class PageSchema(AmisNode):
    """页面配置"""
    label: Union[Literal[False], Template,str] = None
    """菜单名称。"""
    icon: str = 'fa fa-flash'
    """菜单图标，比如：'fa fa-file'."""
    url: str = None
    """
    页面路由路径，当路由命中该路径时，启用当前页面。当路径不是 / 打头时，会连接父级路径。
    比如：父级的路径为 folder，而此时配置 pageA, 那么当页面地址为 /folder/pageA 时才会命中此页面。
    当路径是 / 开头如： /crud/list 时，则不会拼接父级路径.
    另外还支持 /crud/view/:id 这类带参数的路由，页面中可以通过 ${params.id} 取到此值。
    """
    schema_: Union[Page, "Iframe"] = Field(None, alias='schema')
    """页面的配置，具体配置请前往 Page 页面说明"""
    schemaApi: API = None
    """如果想通过接口拉取，请配置。返回路径为 json>data。schema 和 schemaApi 只能二选一。"""
    link: str = None
    """如果想配置个外部链接菜单，只需要配置 link 即可。"""
    redirect: str = None
    """跳转，当命中当前页面时，跳转到目标页面。"""
    rewrite: str = None
    """改成渲染其他路径的页面，这个方式页面地址不会发生修改。"""
    isDefaultPage: Union[str, bool] = None
    """当你需要自定义 404 页面的时候有用，不要出现多个这样的页面，因为只有第一个才会有用。"""
    visible: str = None
    """有些页面可能不想出现在菜单中，可以配置成 false，另外带参数的路由无需配置，直接就是不可见的。"""
    className: str = None
    """菜单类名。"""
    children: List["PageSchema"] = None
    """子菜单"""
    sort: int = None
    """排序"""

    def as_tabs_item(self, tabs_extra: Dict[str, Any] = None, item_extra: Dict[str, Any] = None):
        if self.children:
            tab = Tabs(
                tabs=[item.as_tabs_item(tabs_extra, item_extra) for item in self.children]
            ).update_from_dict(tabs_extra or {})
        elif self.schema_:
            tab = self.schema_
            if isinstance(tab, Iframe):
                tab.height = 1080
        elif self.schemaApi:
            tab = Service(schemaApi=self.schemaApi)
        elif self.link:
            tab = Page(body=Link(href=self.link, body=self.label, blank=True))
        else:
            tab = None
        return Tabs.Item(
            title=self.label,
            icon=self.icon,
            tab=tab,
        ).update_from_dict(item_extra or {})


class App(Page):
    """多页应用"""
    __default_template_path__: str = 'app.jinja2'
    type: str = "app"
    """指定为 app 渲染器"""
    api: API = None
    """页面配置接口，如果你想远程拉取页面配置请配置。返回配置路径 json>data>pages，具体格式请参考 pages 属性。"""
    brandName: str = None
    """应用名称"""
    logo: str = None
    """支持图片地址，或者 svg。"""
    className: str = None
    """css 类名"""
    header: SchemaNode = None
    """顶部区域"""
    asideBefore: SchemaNode = None
    """页面菜单上前面区域。"""
    asideAfter: SchemaNode = None
    """页面菜单下前面区域。"""
    footer: SchemaNode = None
    """页面。"""
    pages: List[Union[PageSchema, dict]] = None
    """Array<页面配置>具体的页面配置。通常为数组，数组第一层为分组，一般只需要配置 label 集合，如果你不想分组，直接不配置，真正的页面请在第二层开始配置，即第一层的 children 中。"""


class Button(AmisNode):
    """按钮"""
    className: str = None
    """指定添加 button 类名"""
    url: str = None
    """点击跳转的地址，指定此属性 button 的行为和 a 链接一致"""
    size: Literal['xs', 'sm', 'md', 'lg'] = None
    """设置按钮大小"""
    actionType: Literal['button', 'reset', 'submit', 'clear', 'url'] = "button"
    """设置按钮类型"""
    level: LevelEnum = LevelEnum.default
    """设置按钮样式"""
    tooltip: str = None
    """气泡提示内容"""
    tooltipPlacement: Literal['top', 'right', 'bottom', 'left'] = "top"
    """气泡框位置器"""
    tooltipTrigger: Literal['hover', 'focus'] = None
    """触发 tootip"""
    disabled: bool = False
    """按钮失效状态"""
    disabledTip: str = None
    """按钮失效状态下的提示"""
    block: bool = False
    """将按钮宽度调整为其父宽度的选项"""
    loading: bool = False
    """显示按钮 loading 效果"""
    loadingOn: str = None
    """显示按钮 loading 表达式"""


class ButtonGroup(AmisNode):
    """按钮组"""
    type: str = 'button-group'
    """指定为 button-group 渲染器"""
    buttons: List[Button] = None
    """行为按钮组"""
    className: str = None
    """外层 Dom 的类名"""
    vertical: bool = False
    """是否使用垂直模式"""
    tiled: bool = False
    """是否使用平铺模式"""
    btnLevel: Literal[
        'link', 'primary', 'secondary', 'info', 'success', 'warning', 'danger', 'light', 'dark', 'default'] = "default"
    """按钮样式"""
    btnActiveLevel: Literal[
        'link', 'primary', 'secondary', 'info', 'success', 'warning', 'danger', 'light', 'dark', 'default'] = "default"
    """激活按钮样式"""


class Breadcrumb(AmisNode):
    """面包屑"""

    class Item(AmisNode):
        label: Union[Literal[False], Template,str] = None
        """文本"""
        href: str = None
        """链接"""
        icon: str = None
        """图标"""
        dropdown: List["Breadcrumb.Item"] = None
        """下拉菜单"""

    type: str = 'breadcrumb'
    """指定为 breadcrumb 渲染器"""
    className: str = None
    """外层类名"""
    itemClassName: str = None
    """导航项类名"""
    separatorClassName: str = None
    """分割符类名"""
    dropdownClassName: str = None
    """	下拉菜单类名"""
    dropdownItemClassName: str = None
    """下拉菜单项类名"""
    separator: str = None
    """	分隔符"""
    labelMaxLength: int = 16
    """最大展示长度"""
    tooltipPosition: Literal['left', 'right', 'top', 'bottom'] = "top"
    """浮窗提示位置"""
    source: str = None
    """动态数据"""
    items: List[Item] = None


class Custom(AmisNode):
    """自定义组件"""
    type: str = 'custom'
    """指定为 custom 渲染器"""
    id: str = None
    """节点 id"""
    name: str = None
    """节点 名称"""
    className: str = None
    """节点 class"""
    inline: bool = False
    """默认使用 div 标签，如果 true 就使用 span 标签"""
    html: str = None
    """初始化节点 html"""
    onMount: str = None
    """节点初始化之后调的用函数"""
    onUpdate: str = None
    """数据有更新的时候调用的函数"""
    onUnmount: str = None
    """节点销毁的时候调用的函数"""


class DropDownButton(AmisNode):
    """下拉菜单"""
    type: str = 'dropdown-button'
    """指定为 dropdown-button 渲染器"""
    label: Union[Literal[False], Template,str] = None
    """按钮文本"""
    className: str = None
    """外层 CSS 类名"""
    btnClassName: str = None
    """按钮 CSS 类名"""
    menuClassName: str = None
    """下拉菜单 CSS 类名"""
    block: bool = None
    """块状样式"""
    size: Literal['sm', 'xs', 'md', 'lg'] = None
    """尺寸"""
    align: Literal['left', 'right'] = None
    """位置"""
    buttons: list["DropDownButton"] = None
    """配置下拉按钮"""
    iconOnly: bool = None
    """只显示icon"""
    defaultIsOpened: bool = None
    """默认是否打开"""
    closeOnOutside: bool = True
    """点击外侧区域是否收起"""
    closeOnClick: bool = False
    """点击按钮后自动关闭下拉菜单"""
    trigger: Literal['hover', 'click'] = "click"
    """	触发方式"""
    hideCaret: bool = False
    """隐藏下拉图标"""


class Service(AmisNode):
    """功能型容器"""

    class Message(AmisNode):
        fetchSuccess: str = None
        """接口请求成功时的 toast 提示文字"""
        fetchFailed: str = "初始化失败"
        """接口请求失败时 toast 提示文字"""

    type: str = "service"
    """指定为 service 渲染器"""
    name: str = None
    """节点 名称"""
    className: str = None
    """外层 Dom 的类名"""
    body: SchemaNode = None
    """内容容器"""
    api: API = None
    """初始化数据域接口地址"""
    ws: Union[str, dict] = None
    """WebScocket 地址"""
    dataProvider: str = None
    """数据获取函数"""
    initFetch: bool = None
    """是否默认拉取"""
    schemaApi: API = None
    """用来获取远程 Schema 接口地址"""
    initFetchSchema: bool = None
    """是否默认拉取 Schema"""
    messages: Message = None
    """消息提示覆写，默认消息读取的是接口返回的 toast 提示文字，但是在此可以覆写它。"""
    interval: int = None
    """轮询时间间隔(最低 3000)"""
    silentPolling: bool = None
    """False  # 配置轮询时是否显示加载动画"""
    stopAutoRefreshWhen: Expression = None
    """配置停止轮询的条件"""
    showErrorMsg: bool = True
    """是否以 Alert 的形式显示 api 接口响应的错误信息，默认展示"""


class Nav(AmisNode):
    """导航"""

    class Link(AmisNode):
        label: Union[Literal[False], Template,str] = None
        """名称"""
        to: Template = None
        """链接地址"""
        target: str = "链接关系"
        """"""
        icon: str = None
        """图标"""
        children: List["Link"] = None
        """子链接"""
        unfolded: bool = None
        """初始是否展开"""
        active: bool = None
        """是否高亮"""
        activeOn: Expression = None
        """是否高亮的条件，留空将自动分析链接地址"""
        defer: bool = None
        """标记是否为懒加载项"""
        deferApi: API = None
        """可以不配置，如果配置优先级更高"""

    class NavOverflow(AmisNode):
        enable: bool = False
        """是否开启响应式收纳"""
        overflowLabel: Union[str, SchemaNode, dict] = None
        """菜单触发按钮的文字"""
        overflowIndicator: str = "fa fa-ellipsis"
        """菜单触发按钮的图标"""
        maxVisibleCount: int = None
        """开启响应式收纳后导航最大可显示数量，超出此数量的导航将被收纳到下拉菜单中，默认为自动计算"""
        wrapperComponent: str = None
        """包裹导航的外层标签名，可以使用其他标签渲染"""
        style: str = None
        """自定义样式"""
        overflowClassName: str = ""
        """菜单按钮 CSS 类名"""
        overflowPopoverClassName: str = ""
        """Popover 浮层 CSS 类名"""
        overflowListClassName: str = ""
        """菜单外层 CSS 类名"""

    type: str = "nav"
    """指定为 Nav 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    stacked: bool = True
    """设置成 false 可以以 tabs 的形式展示"""
    source: API = None
    """可以通过变量或 API 接口动态创建导航"""
    deferApi: API = None
    """用来延时加载选项详情的接口，可以不配置，不配置公用 source 接口。"""
    itemActions: SchemaNode = None
    """更多操作相关配置"""
    draggable: bool = None
    """是否支持拖拽排序"""
    dragOnSameLevel: bool = None
    """仅允许同层级内拖拽"""
    saveOrderApi: API = None
    """保存排序的 api"""
    itemBadge: Badge = None
    """角标"""
    links: List[Link] = None
    """链接集合"""
    overflow: List[NavOverflow] = None
    """响应式收纳配置"""


class AnchorNav(AmisNode):
    """锚点导航"""

    class Link(AmisNode):
        label: Union[Literal[False], Template,str] = None
        """名称"""
        title: str = None
        """区域 标题"""
        href: str = None
        """区域 标识"""
        body: SchemaNode = None
        """区域 内容区"""
        className: str = "bg-white b-l b-r b-b wrapper-md"
        """区域成员 样式"""

    type: str = "anchor-nav"
    """指定为 AnchorNav 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    linkClassName: str = None
    """导航 Dom 的类名"""
    sectionClassName: str = None
    """锚点区域 Dom 的类名"""
    links: List[Link] = None
    """links 内容"""
    direction: Literal["vertical", "horizontal"] = "vertical"
    """可以配置导航水平展示还是垂直展示。对应的配置项分别是：vertical、horizontal"""
    active: str = None
    """需要定位的区域"""


class TooltipWrapper(AmisNode):
    """文字提示容器"""
    type: str = "tooltip-wrapper"
    """指定为 tooltip-wrapper 渲染器"""
    title: str = ""
    """文字提示标题"""
    content: str = ""
    """文字提示内容, 兼容之前的 tooltip 属性"""
    placement: Literal["top", "right", "bottom", "left"] = "top"
    """文字提示浮层出现位置"""
    tooltipTheme: Literal["dark", "light"] = "light"
    """主题样式， 默认为 light"""
    offset: Tuple[int, int] = [0, 0]
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
    wrapperComponent: str = "div"
    """容器标签名"""
    body: SchemaNode = None
    """内容容器"""
    style: Union[dict, str] = None
    """内容区自定义样式"""
    tooltipStyle: Union[dict, str] = None
    """浮层自定义样式"""
    className: str = None
    """内容区类名"""
    tooltipClassName: str = None
    """文字提示浮层类名"""


class ButtonToolbar(AmisNode):
    """按钮工具栏"""
    type: str = 'button-toolbar'
    """指定为 ButtonToolbar 组件"""
    buttons: List[Button]
    """行为按钮组"""


class Validation(BaseAmisModel):
    """值检验"""
    isEmail: bool = None
    """必须是 Email。"""
    isUrl: bool = None
    """必须是 Url。"""
    isNumeric: bool = None
    """必须是 数值。"""
    isAlpha: bool = None
    """必须是 字母。"""
    isAlphanumeric: bool = None
    """必须是 字母或者数字。"""
    isInt: bool = None
    """必须是 整形。"""
    isFloat: bool = None
    """必须是 浮点形。"""
    isLength: int = None
    """是否长度正好等于设定值。"""
    minLength: int = None
    """最小长度。"""
    maxLength: int = None
    """最大长度。"""
    maximum: int = None
    """最大值。"""
    minimum: int = None
    """最小值。"""
    equals: str = None
    """当前值必须完全等于 xxx。"""
    equalsField: str = None
    """当前值必须与 xxx 变量值一致。"""
    isJson: bool = None
    """是否是合法的 Json 字符串。"""
    isUrlPath: bool = None
    """是 url 路径。"""
    isPhoneNumber: bool = None
    """是否为合法的手机号码"""
    isTelNumber: bool = None
    """是否为合法的电话号码"""
    isZipcode: bool = None
    """是否为邮编号码"""
    isId: bool = None
    """是否为身份证号码，没做校验"""
    matchRegexp: str = None
    """必须命中某个正则。 /foo/"""


class Column(AmisNode):
    """列配置"""
    xs: Union[int, str] = None
    """宽度占比：1 - 12或'auto'"""
    ClassName: str = None
    """列类名"""
    sm: Union[int, str] = None
    """宽度占比：1 - 12或'auto'"""
    md: Union[int, str] = None
    """宽度占比：1 - 12或'auto'"""
    lg: Union[int, str] = None
    """宽度占比：1 - 12或'auto'"""
    valign: Literal['top', 'middle', 'bottom', 'between'] = None
    """当前列内容的垂直对齐"""
    body: SchemaNode = None


class FormItem(AmisNode):
    """表单项通用"""
    type: str = 'input-text'
    """指定表单项类型"""

    class AutoFill(AmisNode):
        showSuggestion: bool = None
        """true 为参照录入，false 自动填充"""
        api: Expression = None
        """自动填充接口/参照录入筛选 CRUD 请求配置"""
        silent: bool = None
        """是否展示数据格式错误提示，默认为 true"""
        fillMappinng: SchemaNode = None
        """自动填充/参照录入数据映射配置，键值对形式，值支持变量获取及表达式"""
        trigger: str = None
        """showSuggestion 为 true 时，参照录入支持的触发方式，目前支持 change「值变化」｜ focus 「表单项聚焦」"""
        mode: str = None
        """showSuggestion 为 true 时，参照弹出方式 dialog, drawer, popOver"""
        labelField: str = None
        """showSuggestion 为 true 时，设置弹出 dialog,drawer,popOver 中 picker 的 labelField"""
        position: str = None
        """showSuggestion 为 true 时，参照录入 mode 为 popOver 时，可配置弹出位置"""
        size: str = None
        """showSuggestion 为 true 时，参照录入 mode 为 dialog 时，可设置大小"""
        columns: List[Column] = None
        """showSuggestion 为 true 时，数据展示列配置"""
        filter: SchemaNode = None
        """showSuggestion 为 true 时，数据查询过滤条件"""

    className: str = None
    """表单最外层类名"""
    inputClassName: str = None
    """表单控制器类名"""
    labelClassName: str = None
    """label 的类名"""
    name: str = None
    """字段名，指定该表单项提交时的 key"""
    label: Union[Literal[False], Template] = False
    """表单项标签  模板或false"""
    value: Union[int, str] = None
    """字段的值"""
    labelAligin: Literal["right", "left"] = "right"
    """表单项标签对齐方式，默认右对齐，仅在 mode为horizontal 时生效"""
    labelRemark: Remark = None
    """表单项标签描述"""
    description: Template = None
    """表单项描述"""
    placeholder: str = None
    """表单项描述"""
    inline: bool = None
    """是否为 内联 模式"""
    submitOnChange: bool = None
    """是否该表单项值发生变化时就提交当前表单。"""
    disabled: bool = None
    """当前表单项是否是禁用状态"""
    disabledOn: Expression = None
    """当前表单项是否禁用的条件"""
    visible: Expression = None
    """当前表单项是否禁用的条件"""
    visibleOn: Expression = None
    """当前表单项是否禁用的条件"""
    required: bool = None
    """是否为必填。"""
    requiredOn: Expression = None
    """过表达式来配置当前表单项是否为必填。"""
    validations: Union[Validation, Expression] = None
    """表单项值格式验证，支持设置多个，多个规则用英文逗号隔开。"""
    validateApi: Expression = None
    """表单校验接口"""
    autoFill: Union[SchemaNode, AutoFill] = None
    """数据录入配置，自动填充或者参照录入"""
    copyable: Union[bool, dict] = None
    """是否可复制  boolean 或 {icon: string, content:string}"""
    static: bool = None
    """2.4.0 当前表单项是否是静态展示，目前支持静支持静态展示的表单项"""
    staticClassName: str = None
    """2.4.0 静态展示时的类名"""
    staticLabelClassName: str = None
    """2.4.0 静态展示时的 Label 的类名"""
    staticInputClassName: str = None
    """2.4.0 静态展示时的 value 的类名"""
    staticSchema: SchemaNode = None
    """2.4.0 自定义静态展示方式"""


class Form(AmisNode):
    """表单"""

    class Messages(AmisNode):
        fetchSuccess: str = None
        """获取成功时提示"""
        fetchFailed: str = None
        """获取失败时提示"""
        saveSuccess: str = None
        """保存成功时提示"""
        saveFailed: str = None
        """保存失败时提示"""

    type: str = "form"
    """"form" 指定为 Form 渲染器"""
    name: str = None
    """设置一个名字后，方便其他组件与其通信"""
    mode: DisplayModeEnum = DisplayModeEnum.normal
    """表单展示方式，可以是：normal、horizontal 或者 inline"""
    horizontal: Horizontal = None #{"left": 2, "right": 10, "justify": False}
    """当 mode 为 horizontal 时有用
    用来控制 label {"left": "col-sm-2", "right": "col-sm-10","offset": "col-sm-offset-2"}
    """
    labelAlign: Literal["right", "left"] = "right"
    """表单项标签对齐方式，默认右对齐，仅在 mode为horizontal 时生效"""
    labelWidth: Union[int, str] = None
    """labelWidth"""
    title: str = "表单"
    """Form 的标题"""
    submitText: Optional[str] = "提交"
    """"默认的提交按钮名称，如果设置成空，则可以把默认按钮去掉。"""
    className: str = None
    """外层 Dom 的类名"""
    body: List[Union[FormItem, SchemaNode]] = None
    """Form 表单项集合"""
    actions: List[Action] = None
    """Form 提交按钮，成员为 Action"""
    actionsClassName: str = None
    """actions 的类名"""
    messages: Messages = None
    """消息提示覆写，默认消息读取的是 API 返回的消息，但是在此可以覆写它。"""
    wrapWithPanel: bool = None
    """是否让 Form 用 panel 包起来，设置为 false 后，actions 将无效。"""
    panelClassName: str = None
    """外层 panel 的类名"""
    api: API = None
    """Form 用来保存数据的 api。"""
    initApi: API = None
    """Form 用来获取初始数据的 api。"""
    rules: List = None
    """表单组合校验规则 Array<{rule:string;message:string}>"""
    interval: int = None
    """刷新时间(最低 3000)"""
    silentPolling: bool = False
    """配置刷新时是否显示加载动画"""
    stopAutoRefreshWhen: str = ""
    """通过表达式 来配置停止刷新的条件"""
    initAsyncApi: API = None
    """Form 用来获取初始数据的 api,与 initApi 不同的是，会一直轮询请求该接口，直到返回 finished 属性为 true 才 结束。"""
    initFetch: bool = None
    """设置了 initApi 或者 initAsyncApi 后，默认会开始就发请求，设置为 false 后就不会起始就请求接口"""
    initFetchOn: str = None
    """用表达式来配置"""
    initFinishedField: str = None
    """
    设置了 initAsyncApi 后，默认会从返回数据的 data.finished 来判断是否完成
    也可以设置成其他的 xxx，就会从 data.xxx 中获取
    """
    initCheckInterval: int = None
    """设置了 initAsyncApi 以后，默认拉取的时间间隔"""
    asyncApi: API = None
    """设置此属性后，表单提交发送保存接口后，还会继续轮询请求该接口，直到返回 finished 属性为 true 才 结束。"""
    checkInterval: int = None
    """轮询请求的时间间隔，默认为 3 秒。设置 asyncApi 才有效"""
    finishedField: str = "finished"
    """如果决定结束的字段名不是 finished 请设置此属性，比如 is_success"""
    submitOnChange: bool = False
    """表单修改即提交"""
    submitOnInit: bool = False
    """初始就提交一次"""
    resetAfterSubmit: bool = False
    """提交后是否重置表单"""
    primaryField: str = "id"
    """设置主键 id, 当设置后，检测表单是否完成时（asyncApi），只会携带此数据。"""
    target: str = None
    """
    默认表单提交自己会通过发送 api 保存数据，但是也可以设定另外一个 form 的 name 值
    或者另外一个 CRUD 模型的 name 值。 如果 target 目标是一个 Form ，则目标 Form 会重新触发 initApi，api 可以拿到当前 form 数据。
    如果目标是一个 CRUD 模型，则目标模型会重新触发搜索，参数为当前 Form 数据。当目标是 window 时，会把当前表单的数据附带到页面地址上。
    """
    redirect: str = None
    """设置此属性后，Form 保存成功后，自动跳转到指定页面。支持相对地址，和绝对地址（相对于组内的）。"""
    reload: str = None
    """操作完后刷新目标对象。请填写目标组件设置的 name 值，如果填写为 window 则让当前页面整体刷新。"""
    autoFocus: bool = False
    """是否自动聚焦。"""
    canAccessSuperData: bool = True
    """指定是否可以自动获取上层的数据并映射到表单项上"""
    persistData: str = ""
    """指定一个唯一的 key，来配置当前表单是否开启本地缓存"""
    persistDataKeys: Union[List[str], str] = ""
    """指指定只有哪些 key 缓存"""
    clearPersistDataAfterSubmit: bool = True
    """指定表单提交成功后是否清除本地缓存"""
    preventEnterSubmit: bool = False
    """禁用回车提交表单"""
    trimValues: bool = False
    """trim 当前表单项的每一个值"""
    promptPageLeave: bool = False
    """form 还没保存，即将离开页面前是否弹框确认。"""
    columnCount: int = 0
    """表单项显示为几列"""
    inheritData: bool = True
    """
    默认表单是采用数据链的形式创建个自己的数据域，表单提交的时候只会发送自己这个数据域的数据，
    如果希望共用上层数据域可以设置这个属性为 false，这样上层数据域的数据不需要在表单中用隐藏域或者显式映射才能发送了。
    """
    static: bool = None
    """2.4.0 整个表单静态方式展示，详情请查看示例页"""
    staticClassName: str = None
    """2.4.0 表单静态展示时使用的类名"""
    closeDialogOnSubmit: bool = None
    """提交的时候是否关闭弹窗。当 form 里面有且只有一个弹窗的时候，本身提交会触发弹窗关闭，此属性可以关闭此行为"""


class Options(FormItem):
    """选择器表单项"""
    options: OptionsNode = None
    """选项组，供用户选择"""
    source: Union[API, Any] = None
    """选项组源，可通过数据映射获取当前数据域变量、或者配置 API 对象"""
    multiple: bool = False
    """是否支持多选"""
    labelField: str = "label"
    """标识选项中哪个字段是label值"""
    valueField: str = "value"
    """标识选项中哪个字段是value值"""
    joinValues: bool = True
    """是否拼接value值"""
    extractValue: bool = False
    """是否将value值抽取出来组成新的数组，只有在joinValues是false是生效"""
    itemHeight: int = 32
    """每个选项的高度，用于虚拟渲染"""
    virtualThreshold: int = 100
    """在选项数量超过多少时开启虚拟渲染"""
    valuesNoWrap: bool = False
    """默认情况下多选所有选项都会显示，通过这个可以最多显示一行，超出的部分变成 ..."""


class InputArray(FormItem):
    """数组输入框"""
    type: str = 'input-array'
    """指明为array组件"""
    items: Union[FormItem, SchemaNode] = None
    """配置单项表单类型"""
    addable: bool = None
    """是否可新增。"""
    removable: bool = None
    """是否可删除"""
    draggable: bool = False
    """是否可以拖动排序, 需要注意的是当启用拖动排序的时候，会多一个$id 字段"""
    draggableTip: str = None
    """可拖拽的提示文字，默认为："可通过拖动每行中的【交换】按钮进行顺序调整"""
    addButtonText: str = "新增"
    """新增按钮文字"""
    minLength: int = None
    """限制最小长度"""
    maxLength: int = None
    """限制最大长度"""
    scaffold: Any = None
    """新增成员时的默认值，一般根据items的数据类型指定需要的默认值"""


class ButtonGroupSelect(FormItem):
    """按钮点选"""
    type: str = 'button-group-select'
    """指定为 button-group-select 渲染器"""
    vertical: bool = False
    """是否使用垂直模式"""
    tiled: bool = False
    """是否使用平铺模式"""
    btnLevel: LevelEnum = LevelEnum.default
    """按钮样式"""
    btnActiveLevel: LevelEnum = LevelEnum.default
    """选中按钮样式"""
    options: OptionsNode = None
    """选项组"""
    source: Union[API, str] = None
    """动态选项组"""
    multiple: bool = False
    """多选"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    autoFill: dict = None
    """自动填充"""


class ChainedSelect(FormItem):
    options: OptionsNode = None
    """选项组"""
    source: Union[API, str] = None
    """动态选项组"""
    autoComplete: Union[API, str] = None
    """自动选中"""
    delimiter: Union[str, bool] = ","
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""


class Hidden(FormItem):
    """隐藏字段"""
    type: str = 'hidden'
    """指定为 hidden 渲染器"""


class Checkbox(FormItem):
    """勾选框"""
    type: str = 'checkbox'
    """指定为 checkbox 渲染器"""
    option: str = None
    """选项说明"""
    trueValue: Union[str, int, bool] = True
    """标识真值"""
    falseValue: Union[str, int, bool] = False
    """标识假值"""
    optionType: Literal["default", "button"] = "default"


class Checkboxes(FormItem):
    """复选框"""
    type: str = 'checkboxes'
    """指定为 checkboxes 渲染器"""
    options: OptionsNode = None
    """选项组"""
    source: Union[str, API] = None
    """动态选项组"""
    delimiter: Union[str,bool] = ","
    """ 拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    columnsCount: int = 1
    """选项按几列显示，默认为一列"""
    inline: bool = True
    """是否显示为一行"""
    checkAll: bool = False
    """是否支持全选"""
    defaultCheckAll: bool = False
    """默认是否全选"""
    creatable: bool = False
    """新增选项"""
    createBtnLabel: str = "新增选项"
    """新增选项"""
    addControls: List[FormItem] = None
    """自定义新增表单项"""
    addApi: API = None
    """配置新增选项接口"""
    editable: bool = False
    """编辑选项"""
    editControls: List[FormItem] = None
    """自定义编辑表单项"""
    editApi: API = None
    """配置编辑选项接口"""
    removable: bool = False
    """删除选项"""
    deleteApi: API = None
    """配置删除选项接口"""
    optionType: Literal["default", "button"] = "default"
    """按钮模式"""
    itemClassName: str = None
    """选项样式类名"""
    labelClassName: str = None
    """选项标签样式类名"""


class InputCity(FormItem):
    """城市选择器"""
    type: str = 'input-city'
    """指定为 input-city 渲染器"""
    allowCity: bool = True
    """允许选择城市"""
    allowDistrict: bool = True
    """允许选择区域"""
    searchable: bool = False
    """是否出搜索框"""
    extractValue: bool = True
    """是否抽取值，如果设置成 false 值格式会变成对象，包含 code、province、city和district文字信息。"""


class InputColor(FormItem):
    """颜色选择器"""
    type: str = 'input-color'
    """指定为 input-color 渲染器"""
    format: Literal["hex", "hls", "rgb", "rgba"] = "hex"
    """请选择 hex、hls、rgb或者rgba。"""
    presetColors: List[str] = ['#D0021B', '#F5A623', '#F8E71C', '#8B572A', '#7ED321', '#417505', '#BD10E0', '#9013FE',
                               '#4A90E2', '#50E3C2', '#B8E986', '#000000', '#4A4A4A', '#9B9B9B', '#FFFFFF']
    """选择器底部的默认颜色，数组内为空则不显示默认颜色"""
    allowCustomColor: bool = True
    """为false时只能选择颜色，使用 presetColors 设定颜色选择范围"""
    clearable: bool = False
    """是否显示清除按钮"""
    resetValue: str = ""
    """清除后，表单项值调整成该值"""


class Combo(FormItem):
    """组合"""
    type: str = 'combo'
    """指定为 combo 渲染器"""
    formClassName: str = None
    """单组表单项的类名"""
    addButtonClassName: str = None
    """新增按钮 CSS 类名"""
    items: List[FormItem] = None
    """组合展示的表单项
    items[x].columnClassName: str = None  # 列的类名，可以用它配置列宽度。默认平均分配
    items[x].unique: bool = None  # 设置当前列值是否唯一，即不允许重复选择。
    """
    noBorder: bool = False
    """单组表单项是否显示边框"""
    scaffold: dict = {}
    """单组表单项初始值"""
    multiple: bool = False
    """是否多选"""
    multiLine: bool = False
    """默认是横着展示一排，设置以后竖着展示"""
    minLength: int = None
    """最少添加的条数"""
    maxLength: int = None
    """最多添加的条数"""
    flat: bool = False
    """是否将结果扁平化(去掉 name),只有当 items 的 length 为 1 且 multiple 为 true 的时候才有效。"""
    joinValues: bool = True
    """默认为 true 当扁平化开启的时候，是否用分隔符的形式发送给后端，否则采用 array 的方式。"""
    delimiter: Union[str,bool] = ","
    """当扁平化开启并且 joinValues 为 true 时，用什么分隔符。"""
    addable: bool = False
    """是否可新增"""
    addattop: bool = False
    """在顶部添加"""
    addButtonText: str = "新增"
    """新增按钮文字"""
    removable: bool = False
    """是否可删除"""
    deleteApi: API = None
    """如果配置了，则删除前会发送一个 api，请求成功才完成删除"""
    deleteConfirmText: str = "确认要删除？"
    """当配置 deleteApi 才生效！删除时用来做用户确认"""
    draggable: bool = False
    """是否可以拖动排序, 需要注意的是当启用拖动排序的时候，会多一个$id 字段"""
    draggableTip: str = None
    """"可通过拖动每行中的【交换】按钮进行顺序调整"  # 可拖拽的提示文字"""
    subFormMode: Literal["normal", "horizontal", "inline"] = "normal"
    """"可选normal、horizontal、inline"""
    placeholder: str = ""
    """没有成员时显示。"""
    canAccessSuperData: bool = False
    """指定是否可以自动获取上层的数据并映射到表单项上"""
    conditions: dict = None
    """数组的形式包含所有条件的渲染类型，单个数组内的test 为判断条件，数组内的items为符合该条件后渲染的schema"""
    typeSwitchable: bool = False
    """是否可切换条件，配合conditions使用"""
    strictMode: bool = True
    """默认为严格模式，设置为 false 时，当其他表单项更新是，里面的表单项也可以及时获取，否则不会。"""
    syncFields: List[str] = []
    """
    配置同步字段。只有 strictMode 为 false 时有效。
    如果 Combo 层级比较深，底层的获取外层的数据可能不同步。但是给 combo 配置这个属性就能同步下来。输入格式：["os"]
    """
    nullable: bool = False
    """允许为空，如果子表单项里面配置验证器，且又是单条模式。可以允许用户选择清空（不填）。"""
    itemClassName: str = None
    """单组 CSS 类"""
    itemsWrapperClassName: str = None
    """组合区域 CSS 类"""
    deleteBtn: Union[Button, str] = "自定义删除按钮"
    """只有当removable为 true 时有效; 如果为string则为按钮的文本；如果为Button则根据配置渲染删除按钮。"""
    addBtn: Union[Button, str] = "自定义新增按钮"
    """可新增自定义配置渲染新增按钮，在tabsMode: true下不生效。"""


class ConditionBuilder(FormItem):
    """组合条件"""

    class Field(AmisNode):
        type: str = "text"
        """字段配置中配置成 "text"""
        label: Union[Literal[False], Template,str] = None
        """字段名称。"""
        placeholder: str = None
        """占位符"""
        operators: List[str] = ['equal', 'not_equal', 'is_empty', 'is_not_empty', 'like', 'not_like', 'starts_with',
                                'ends_with']
        """如果不要那么多，可以配置覆盖。
        默认为 ['equal','not_equal','is_empty','is_not_empty','like','not_like','starts_with','ends_with']
        """
        defaultOp: str = "equal"
        """默认为 "equal"""

    class Text(Field):
        """文本"""

    class Number(Field):
        """数字"""
        type: str = 'number'
        """数字"""
        minimum: float = None
        """最小值"""
        maximum: float = None
        """最大值"""
        step: float = None
        """步长"""

    class Date(Field):
        """日期"""
        type: str = 'date'
        """日期"""
        defaultValue: str = None
        """默认值"""
        format: str = "YYYY-MM-DD"
        """默认 "YYYY-MM-DD" 值格式"""
        inputFormat: str = "YYYY-MM-DD"
        """默认 "YYYY-MM-DD" 显示的日期格式。"""

    class Datetime(Date):
        """日期时间"""
        type: str = 'datetime'
        """日期时间"""
        timeFormat: str = "HH:mm"
        """默认 "HH:mm" 时间格式，决定输入框有哪些。"""

    class Time(Date):
        """时间"""
        type: str = 'time'

    class Select(Field):
        """下拉选择"""
        type: str = 'select'
        """下拉选择"""
        options: OptionsNode = None
        """选项列表，Array<{label: string, value: any}>"""
        source: Union[str, API] = None
        """动态选项，请配置 api。"""
        searchable: bool = None
        """是否可以搜索"""
        autoComplete: API = None
        """自动提示补全，每次输入新内容后，将调用接口，根据接口返回更新选项。"""

    class Custom(Field):
        """自定义"""
        type = "custom"
        """自定义"""
        operators: Union[list, str, dict] = []
        """默认为空，需配置自定义判断条件，支持字符串或 key-value 格式"""
        value: SchemaNode = None
        """字段配置右边值需要渲染的组件，支持 amis 输入类组件或自定义输入类组件"""

    type: str = 'condition-builder'
    """指定为 condition-builder 渲染器"""
    fields: List[Field] = None
    """为数组类型，每个成员表示一个可选字段，支持多个层，配置示例"""
    className: str = None
    """外层 dom 类名"""
    fieldClassName: str = None
    """输入字段的类名"""
    source: str = None
    """通过远程拉取配置项"""
    embed: bool = True
    """内嵌展示"""
    title: str = None
    """	弹窗配置的顶部标题"""
    showANDOR: bool = None
    """用于 simple 模式下显示切换按钮"""
    showNot: bool = None
    """是否显示「非」按钮"""
    searchable: bool = None
    """字段是否可搜索"""
    selectMode: Literal["list", "tree"] = "list"
    """组合条件左侧选项类型"""


class DiffEditor(FormItem):
    """对比编辑器"""
    type: str = 'diff-editor'
    """指定为 diff-editor 渲染器"""
    language: str = None
    """编辑器高亮的语言"""
    diffValue: Tpl = None
    """左侧值"""


class Editor(FormItem):
    """代码编辑器"""
    type: str = 'editor'
    """指定为 editor 渲染器"""
    language: str = "javascript"
    """编辑器高亮的语言，支持通过 ${xxx} 变量获取"""
    size: Literal['md', 'lg', 'xl', 'xxl'] = "md"
    """编辑器高度，取值可以是 md、lg、xl、xxl"""
    allowFullscreen: bool = False
    """是否显示全屏模式开关"""
    options: dict = None
    """monaco编辑器的其它配置，比如是否显示行号等，请参考这里，不过无法设置readOnly,只读模式需要使用disabled: true"""
    placeholder: str = None
    """	占位描述，没有值的时候展示"""


class FieldSet(FormItem):
    """表单项集合"""
    type: str = 'fieldSet'
    """指定为 fieldSet 渲染器"""
    className: str = None
    """CSS 类名"""
    headingClassName: str = None
    """标题 CSS 类名"""
    bodyClassName: str = None
    """内容区域 CSS 类名"""
    title: SchemaNode = None
    """标题"""
    body: List[FormItem] = None
    """表单项集合"""
    mode: str = None
    """展示默认，同 Form 中的模式"""
    collapsable: bool = False
    """是否可折叠"""
    collapsed: bool = False
    """默认是否折叠"""
    collapseTitle: SchemaNode = "收起"
    """收起的标题"""
    size: Literal['xs', 'sm', 'base', 'lg', 'xl'] = None
    """大小，支持 xs、sm、base、lg、xl"""


class Markdown(AmisNode):
    """Markdown渲染"""
    type: str = 'markdown'
    """指定为 markdown 渲染器"""
    name: str = None
    """字段名，指定该表单项提交时的 key"""
    value: Union[int, str] = None
    """字段的值"""
    className: str = None
    """表单最外层类名"""
    src: API = None
    """外部地址"""


class InputFile(FormItem):
    """文件上传"""
    type: str = 'input-file'
    """指定为 input-file 渲染器"""
    receiver: API = None
    """上传文件接口"""
    accept: str = "text/plain"
    """默认只支持纯文本，要支持其他类型，请配置此属性为文件后缀.xxx"""
    asBase64: bool = False
    """将文件以base64的形式，赋值给当前组件"""
    asBlob: bool = False
    """将文件以二进制的形式，赋值给当前组件"""
    maxSize: int = None
    """默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B"""
    maxLength: int = None
    """默认没有限制，当设置后，一次只允许上传指定数量文件。"""
    multiple: bool = False
    """是否多选。"""
    drag: bool = False
    """是否支持拖拽上传"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    delimiter: Union[str,bool] = ","
    """拼接符"""
    autoUpload: bool = True
    """否选择完就自动开始上传"""
    hideUploadButton: bool = False
    """隐藏上传按钮"""
    stateTextMap: dict = {"init": '', "pending": '等待上传', "uploading": '上传中', "error": '上传出错',
                          "uploaded": '已上传', "ready": ''}
    """上传状态文案"""
    fileField: str = "file"
    """如果你不想自己存储，则可以忽略此属性。"""
    nameField: str = "name"
    """接口返回哪个字段用来标识文件名"""
    valueField: str = "value"
    """文件的值用那个字段来标识。"""
    urlField: str = "url"
    """文件下载地址的字段名。"""
    btnlabel: Union[Literal[False], Template,str] = None
    """上传按钮的文字"""
    downloadUrl: Union[str, bool] = ""
    """
    1.1.6 版本开始支持 post:http://xxx.com/${value} 这种写法
    默认显示文件路径的时候会支持直接下载，可以支持加前缀如：http://xx.dom/filename= ，如果不希望这样，可以把当前配置项设置为 false。
    """
    useChunk: Union[bool, str] = "auto"
    """amis 所在服务器，限制了文件上传大小不得超出 10M，所以 amis 在用户选择大文件的时候，自动会改成分块上传模式。"""
    chunkSize: int = 5 * 1024 * 1024
    """分块大小"""
    startChunkApi: API = None
    """startChunkApi"""
    chunkApi: API = None
    """chunkApi"""
    finishChunkApi: API = None
    """finishChunkApi"""
    concurrency: int = None
    """	分块上传时并行个数"""
    documentation: str = None
    """文档内容"""
    documentLink: str = None
    """文档链接"""
    initAutoFill: bool = True
    """初表单反显时是否执行"""


class InputExcel(FormItem):
    """解析 Excel"""
    type: str = 'input-excel'
    """指定为 input-excel 渲染器"""
    allSheets: bool = False
    """是否解析所有 sheet"""
    parseMode: Literal["array", "object"] = "object"
    """解析模式"""
    includeEmpty: bool = True
    """是否包含空值"""
    plainText: bool = True
    """是否解析为纯文本"""
    placeholder: str = "拖拽 Excel 到这，或点击上传"
    """占位文本提示"""


class InputTable(FormItem):
    """表格"""
    type: str = 'input-table'
    """指定为 input-table 渲染器"""
    addable: bool = False
    """是否可增加一行"""
    editable: bool = False
    """是否可编辑"""
    removable: bool = False
    """是否可删除"""
    showTableAddBtn: bool = True
    """是否显示表格操作栏添加按钮，前提是要开启可新增功能"""
    showFooterAddBtn: bool = True
    """是否显示表格下方添加按，前提是要开启可新增功能"""
    addApi: API = None
    """新增时提交的 API"""
    footerAddBtn: SchemaNode = None
    """底部新增按钮配置"""
    updateApi: API = None
    """修改时提交的 API"""
    deleteApi: API = None
    """删除时提交的 API"""
    addBtnLabel: str = None
    """增加按钮名称"""
    addBtnIcon: str = "plus"
    """增加按钮图标"""
    copyBtnLabel: str = None
    """复制按钮文字"""
    copyBtnIcon: str = "copy"
    """复制按钮图标"""
    editBtnLabel: str = ""
    """编辑按钮名称"""
    editBtnIcon: str = "pencil"
    """编辑按钮图标"""
    deleteBtnLabel: str = ""
    """删除按钮名称"""
    deleteBtnIcon: str = "minus"
    """删除按钮图标"""
    confirmBtnLabel: str = ""
    """确认编辑按钮名称"""
    confirmBtnIcon: str = "check"
    """确认编辑按钮图标"""
    cancelBtnLabel: str = ""
    """取消编辑按钮名称"""
    cancelBtnIcon: str = "times"
    """取消编辑按钮图标"""
    needConfirm: bool = True
    """是否需要确认操作，，可用来控控制表格的操作交互"""
    canAccessSuperData: bool = False
    """是否可以访问父级数据，也就是表单中的同级数据，通常需要跟 strictMode 搭配使用"""
    strictMode: bool = True
    """为了性能，默认其他表单项项值变化不会让当前表格更新，有时候为了同步获取其他表单项字段，需要开启这个"""
    minLength: int = 0
    """最小行数, 2.4.1版本后支持变量"""
    maxLength: Union[int, str] = "Infinity"
    """最大行数, 2.4.1版本后支持变量"""
    perPage: int = 10
    """设置一页显示多少条数据"""
    columns: List= []
    """列信息 columns[x].quickEdit: boolean|object = None 配合 editable 为 true 一起使用 columns[x].quickEditOnUpdate: boolean|object = None 可以用来区分新建模式和更新模式的编辑配置"""


class InputTag(FormItem):
    """标签选择器"""
    type: str = 'input-tag'
    """指定为 input-tag 渲染器"""
    options: OptionsNode = None
    """选项组"""
    optionsTip: Union[OptionsNode, str] = "最近您使用的标签"
    """选项提示"""
    source: Union[str, API] = None
    """动态选项组"""
    delimiter: Union[str,bool] = ","
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    clearable: bool = False
    """在有值的时候是否显示一个删除图标在右侧。"""
    resetValue: str = ""
    """删除后设置此配置项给定的值。"""
    max: int = None
    """允许添加的标签的最大数量"""
    maxTagLength: int = None
    """单个标签的最大文本长度"""
    maxTagCount: int = None
    """标签的最大展示数量，超出数量后以收纳浮层的方式展示，仅在多选模式开启后生效"""
    overflowTagPopover: dict = {"placement": "top", "trigger": "hover", "showArrow": False, "offset": [0, -10]}
    """收纳浮层的配置属性，详细配置参考Tooltip"""
    enableBatchAdd: bool = False
    """	是否开启批量添加模式"""
    separator: str = "-"
    """开启批量添加后，输入多个标签的分隔符，支持传入多个符号，默认为"-"事件表"""


class ListSelect(FormItem):
    """列表"""
    type: str = 'list-select'
    """指定为 list-select 渲染器"""
    options: OptionsNode = None
    """选项组"""
    source: Union[str, API] = None
    """动态选项组"""
    multiple: bool = False
    """多选"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    autoFill: dict = None
    """自动填充"""
    listClassName: str = None
    """支持配置 list div 的 css 类名。比如: flex justify-between"""


class InputGroup(FormItem):
    """输入框组合"""
    type: str = 'input-group'
    """指定为 input-group 渲染器"""
    className: str = None
    """CSS 类名"""
    body: List[FormItem] = None
    """表单项集合"""
    validationConfig: Any = None
    """校验相关配置"""
    errorMode: Literal["full", "partial"] = "full"
    """错误提示风格, full整体飘红, partial仅错误元素飘红"""
    delimiter: str = ";"
    """单个子元素多条校验信息的分隔符"""


class Group(InputGroup):
    """表单项组"""
    type: str = 'group'
    """指定为 group 渲染器"""
    className: str = None
    """	CSS 类名"""
    label: Union[Literal[False], Template,str] = None
    """group 的标签"""
    mode: DisplayModeEnum = None
    """展示默认，同 Form 中的模式"""
    gap: Literal["xs", "sm", "normal"] = None
    """表单项之间的间距，可选：xs、sm、normal"""
    direction: str = "horizontal"
    """可以配置水平展示还是垂直展示。对应的配置项分别是：vertical、horizontal"""


class InputImage(FormItem):
    """图片上传"""

    class CropInfo(BaseAmisModel):
        aspectRatio: float = None
        """裁剪比例。浮点型，默认 1 即 1:1，如果要设置 16:9 请设置 1.7777777777777777 即 16 / 9。。"""
        rotatable: bool = False
        """裁剪时是否可旋转"""
        scalable: bool = False
        """裁剪时是否可缩放"""
        viewMode: int = 1
        """裁剪时的查看模式，0 是无限制"""

    class Limit(BaseAmisModel):
        width: int = None
        """限制图片宽度。"""
        height: int = None
        """限制图片高度。"""
        minWidth: int = None
        """限制图片最小宽度。"""
        minHeight: int = None
        """限制图片最小高度。"""
        maxWidth: int = None
        """限制图片最大宽度。"""
        maxHeight: int = None
        """限制图片最大高度。"""
        aspectRatio: float = None
        """
        限制图片宽高比，格式为浮点型数字，默认 1 即 1:1，如果要设置 16:9 
        请设置 1.7777777777777777 即 16 / 9。 如果不想限制比率，请设置空字符串。
        """

    type: str = 'input-image'
    """指定为 input-image 渲染器"""
    receiver: API = None
    """上传文件接口"""
    accept: str = ".jpeg,.jpg,.png,.gif"
    """支持的图片类型格式，请配置此属性为图片后缀，例如.jpg,.png"""
    maxSize: int = None
    """默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B"""
    maxLength: int = None
    """默认没有限制，当设置后，一次只允许上传指定数量文件。"""
    multiple: bool = False
    """是否多选。"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    delimiter: Union[str,bool] = ","
    """拼接符"""
    autoUpload: bool = True
    """否选择完就自动开始上传"""
    hideUploadButton: bool = False
    """隐藏上传按钮"""
    fileField: str = "file"
    """如果你不想自己存储，则可以忽略此属性。"""
    crop: Union[bool, CropInfo] = None
    """用来设置是否支持裁剪"""
    cropFormat: str = "image/png"
    """裁剪文件格式"""
    cropQuality: int = 1
    """裁剪文件格式的质量，用于 jpeg/webp，取值在 0 和 1 之间"""
    limit: Limit = None
    """限制图片大小，超出不让上传。"""
    frameImage: str = None
    """默认占位图地址"""
    fixedSize: bool = None
    """是否开启固定尺寸,若开启，需同时设置 fixedSizeClassName"""
    fixedSizeClassName: str = None
    """
    开启固定尺寸时，根据此值控制展示尺寸。
    例如h-30,即图片框高为 h-30,AMIS 将自动缩放比率设置默认图所占位置的宽度，最终上传图片根据此尺寸对应缩放。
    """
    initAutoFill: bool = False
    """表单反显时是否执行 autoFill"""
    uploadBtnText: Union[str, SchemaNode] = None
    """上传按钮文案。支持tpl、schema形式配置"""
    dropCrop: bool = True
    """图片上传后是否进入裁剪模式"""
    initCrop: bool = False
    """图片选择器初始化后是否立即进入裁剪模式"""


class LocationPicker(FormItem):
    """地理位置"""
    type: str = 'location-picker'
    """指定为 location-picker 渲染器"""
    vendor: str = 'baidu'
    """地图厂商，目前只实现了百度地图"""
    ak: str = ''
    """百度地图的 ak 注册地址: http://lbsyun.baidu.com/"""
    clearable: bool = False
    """输入框是否可清空"""
    placeholder: str = "请选择位置"
    """"默认提示"""
    coordinatesType: str = "bd09"
    """默为百度/高德坐标，可设置为'gcj02', 高德地图不支持坐标转换"""


class UUID(AmisNode):
    """UUID"""
    type: str = 'uuid'
    """指定为 uuid 渲染器"""
    name: str = None
    """字段名"""
    length: int = None
    """生成长度"""


class MatrixCheckboxes(FormItem):
    """矩阵勾选"""
    type: str = 'matrix-checkboxes'
    """指定为 matrix-checkboxes 渲染器"""
    columns: List[Custom] = None
    """列信息，数组中 label 字段是必须给出的"""
    rows: List[dict] = None
    """行信息， 数组中 label 字段是必须给出的"""
    rowLabel: str = None
    """行标题说明"""
    source: API = None
    """Api 地址，如果选项组不固定，可以通过配置 source 动态拉取。"""
    multiple: bool = True
    """是否多选"""
    singleSelectMode: Literal['cell', 'row', 'column'] = 'column'
    """设置单选模式，multiple为false时有效，可设置为cell, row, column 分别为全部选项中只能单选某个单元格、每行只能单选某个单元格，每列只能单选某个单元格"""


class NestedSelect(FormItem):
    """级联选择器"""
    type: str = 'nested-select'
    """指定为 nested-select 渲染器"""
    options: OptionsNode = None
    """选项组"""
    source: Union[str, API] = None
    """动态选项组"""
    delimiter: Union[str,bool] = ","
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    autoFill: dict = None
    """自动填充"""
    cascade: bool = False
    """设置 true时，当选中父节点时不自动选择子节点。"""
    withChildren: bool = False
    """设置 true时，选中父节点时，值里面将包含子节点的值，否则只会保留父节点的值。"""
    onlyChildren: bool = False
    """多选时，选中父节点时，是否只将其子节点加入到值中。"""
    searchable: bool = False
    """可否搜索"""
    searchPromptText: str = "输入内容进行检索"
    """搜索框占位文本"""
    noResultsText: str = "未找到任何结果"
    """无结果时的文本"""
    multiple: bool = False
    """可否多选"""
    hideNodePathLabel: bool = False
    """是否隐藏选择框中已选择节点的路径 label 信息"""
    onlyLeaf: bool = False
    """只允许选择叶子节点"""


class InputNumber(FormItem):
    """数字输入框"""
    type: str = 'input-number'
    """指定为 input-number 渲染器"""
    min: Union[int, Template] = None
    """最小值"""
    max: Union[int, Template] = None
    """最大值"""
    step: Union[float, int] = None
    """步长"""
    precision: int = None
    """精度，即小数点后几位"""
    showSteps: bool = True
    """是否显示上下点击按钮"""
    prefix: str = None
    """前缀"""
    suffix: str = None
    """后缀"""
    kilobitSeparator: bool = None
    """千分分隔"""
    keyboard: str = None
    """键盘事件（方向上下）"""
    big: bool = None
    """是否使用大数"""
    displayMode: str = None
    """样式类型"""
    resetValue: Union[int, str] = ""
    """清空输入内容时，组件值将设置为resetValue"""
    clearValueOnEmpty: bool = False
    """内容为空时从数据域中删除该表单项对应的值	"""


class Picker(FormItem):
    """列表选择器"""
    type: str = 'picker'
    """指定为 picker 渲染器，列表选取，在功能上和 Select 类似，但它能显示更复杂的信息。"""
    options: OptionsNode = None
    """选项组"""
    source: Union[str, API] = None
    """动态选项组"""
    multiple: bool = None
    """是否为多选。"""
    delimiter: Union[str,bool] = ","
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    autoFill: dict = None
    """自动填充"""
    modalMode: Literal["dialog", "drawer"] = "dialog"
    """"dialog" # 设置 dialog 或者 drawer，用来配置弹出方式。"""
    pickerSchema: str = """{mode: 'list', listItem: {title: '${label}'}}"""
    """即用 List 类型的渲染，来展示列表信息。更多配置参考 CRUD"""
    embed: bool = False
    """是否使用内嵌模式"""


class Switch(FormItem):
    """开关"""

    class IconSchema(AmisNode):
        type: str = "icon"
        """指定为图标"""
        icon: str = None
        """图标"""

    type: str = 'switch'
    """指定为 switch 渲染器"""
    option: str = None
    """选项说明"""
    onText: Union[str, IconSchema] = None
    """开启时的文本"""
    offText: Union[str, IconSchema] = None
    """关闭时的文本"""
    trueValue: Union[bool, str, int] = True
    """标识真值"""
    falseValue: Union[bool, str, int] = False
    """标识假值"""
    size: Literal["sm", "md"] = "md"
    """开关大小"""


class Static(FormItem):
    """静态展示/标签"""
    type: str = 'static'
    """指定为 static 渲染器"""

    class Json(FormItem):
        type: str = 'static-json'
        """展示Json数据"""
        value: Union[dict, str] = None
        """值"""

    class Date(FormItem):
        type: str = "static-date"
        """展示日期"""
        value: str = None
        """值"""

    class Datetime(FormItem):
        """显示日期"""
        type: str = 'static-datetime'
        """展示日期"""
        value: Union[int, str]
        """值"""

    class Mappping(FormItem):
        type: str = "static-mapping"
        """映射"""
        map: dict = None
        """选项组"""
        value: str = None
        """值"""

    class Progress(FormItem):
        type: str = "static-progress"
        """进度"""
        value: str = None
        """值"""

    class Image(FormItem):
        type: str = "static-image"
        """图片"""
        thumbMode: str = None
        """预览图模式"""
        thumbRatio: str = None
        """预览比例"""
        title: str = None
        """图片标题"""
        imageCaption: str = None
        """图片描述信息"""
        enlargeAble: bool = False
        """是否启用放大功能"""
        originalSrc: str = None
        """大图地址"""


class InputText(FormItem):
    """输入框"""
    type: Literal["input-text", "input-url", "input-email", "input-password"] = 'input-text'
    """指定为 input-text 渲染器 可选 input-text|input-url|input-email|input-password 渲染器"""

    class AddOn(AmisNode):
        type: Literal["text", "button", "submit"] = None
        """	请选择 text 、button 或者 submit。"""
        label: Union[str, bool] = None
        """文字说明"""
        position: Literal["left", "right"] = "right"
        """addOn位置"""

    options: OptionsNode = None
    """选项组"""
    source: Union[str, API] = None
    """动态选项组"""
    autoComplete: Union[str, API] = None
    """自动补全"""
    multiple: bool = False
    """是否多选"""
    delimiter: Union[str,bool] = ","
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    addOn: Union[SchemaNode, AddOn] = None
    """输入框附加组件，比如附带一个提示文字，或者附带一个提交按钮。"""
    trimContents: bool = None
    """是否去除首尾空白文本。"""
    creatable: bool = None
    """是否可以创建，默认为可以，除非设置为 false 即只能选择选项中的值"""
    clearable: bool = None
    """是否可清除"""
    resetValue: str = ""
    """清除后设置此配置项给定的值。"""
    prefix: str = ""
    """前缀"""
    suffix: str = ""
    """后缀"""
    showCounter: bool = None
    """是否显示计数器"""
    minLength: int = None
    """限制最小字数"""
    maxLength: int = None
    """限制最大字数"""
    transform: dict = None
    """自动转换值，可选 transform: { lowerCase: true, upperCase: true }"""
    borderMode: Literal["full", "half", "none"] = "full"
    """输入框边框模式，全边框，还是半边框，或者没边框"""
    inputControlClassName: str = None
    """control 节点的 CSS 类名"""
    nativeInputClassName: str = None
    """nativeInputClassName"""


class InputPassword(InputText):
    """密码输框"""
    type: str = 'input-password'
    """指定为 input-password 渲染器"""
    revealPassword: bool = True
    """是否展示密码显/隐按钮"""


class InputRichText(FormItem):
    """富文本编辑器"""
    type: str = 'input-rich-text'
    """"指定为 input-rich-text 渲染器"""
    saveAsUbb: bool = None
    """是否保存为 ubb 格式"""
    receiver: API = None
    """默认的图片保存 API"""
    videoReceiver: API = None
    """默认的视频保存 API"""
    size: Literal['md', 'lg'] = None
    """框的大小，可设置为 md 或者 lg"""
    options: OptionsNode = None
    """需要参考 tinymce 或 froala 的文档"""
    buttons: List[str] = None
    """froala 专用，配置显示的按钮，tinymce 可以通过前面的 options 设置 toolbar 字符串"""


class Select(FormItem):
    """下拉框"""
    type: str = 'select'
    """指定为 select 渲染器"""
    options: OptionsNode = None
    """选项组"""
    source: API = None
    """动态选项组"""
    autoComplete: API = None
    """自动提示补全"""
    delimiter: Union[bool, str] = False
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    checkAll: bool = False
    """是否支持全选"""
    checkAllLabel: str = "全选"
    """全选的文字"""
    checkAllBySearch: bool = True
    """有检索时只全选检索命中的项"""
    defaultCheckAll: bool = False
    """默认是否全选"""
    creatable: bool = False
    """新增选项"""
    multiple: bool = False
    """多选"""
    searchable: bool = False
    """检索"""
    createBtnLabel: str = "新增选项"
    """新增选项"""
    addControls: List[FormItem] = None
    """自定义新增表单项"""
    addApi: API = None
    """配置新增选项接口"""
    editable: bool = False
    """编辑选项"""
    editControls: List[FormItem] = None
    """自定义编辑表单项"""
    editApi: API = None
    """配置编辑选项接口"""
    removable: bool = False
    """删除选项"""
    deleteApi: API = None
    """配置删除选项接口"""
    autoFill: dict = None
    """自动填充"""
    menuTpl: str = None
    """支持配置自定义菜单"""
    clearable: bool = None
    """单选模式下是否支持清空"""
    hideSelected: bool = False
    """隐藏已选选项"""
    mobileClassName: str = None
    """移动端浮层类名"""
    selectMode: Literal['group', 'table', 'tree', 'chained', 'associated'] = ""
    """可选：group、table、tree、chained、associated。分别为：列表形式、表格形式、树形选择形式、级联选择形式， 关联选择形式（与级联选择的区别在于，级联是无限极，而关联只有一级，关联左边可以是个 tree）。"""
    searchResultMode: str = None
    """如果不设置将采用 selectMode 的值，可以单独配置，参考 selectMode，决定搜索结果的展示形式。"""
    columns: List[dict] = None
    """当展示形式为 table 可以用来配置展示哪些列，跟 table 中的 columns 配置相似，只是只有展示功能。"""
    leftOptions: List[dict] = None
    """当展示形式为 associated 时用来配置左边的选项集。"""
    leftMode: Literal['list', 'tree'] = "list"
    """当展示形式为 associated 时用来配置左边的选择形式，支持 list 或者 tree。默认为 list。"""
    rightMode: Literal['list', 'tree', 'table', 'chained'] = None
    """当展示形式为 associated 时用来配置右边的选择形式，可选：list、table、tree、chained。"""
    maxTagCount: int = None
    """标签的最大展示数量，超出数量后以收纳浮层的方式展示，仅在多选模式开启后生效"""
    overflowTagPopover: dict = {"placement": "top", "trigger": "hover", "showArrow": False, "offset": [0, -10]}
    """收纳浮层的配置属性，详细配置参考Tooltip"""
    optionClassName: str = None
    """选项 CSS 类名"""
    popOverContainerSelector: str = None
    """弹层挂载位置选择器，会通过querySelector获取"""
    overlay: dict = None
    """弹层宽度与对齐方式 2.8.0 以上版本"""
    showInvalidMatch: bool = False
    """选项值与选项组不匹配时选项值是否飘红"""


class InputSubForm(FormItem):
    """子表单"""
    type: str = 'input-sub-form'
    """指定为 input-sub-form 渲染器"""
    multiple: bool = False
    """是否为多选模式"""
    labelField: str = None
    """当值中存在这个字段，则按钮名称将使用此字段的值来展示。"""
    btnLabel: str = "设置"
    """按钮默认名称"""
    minLength: int = 0
    """限制最小个数。"""
    maxLength: int = 0
    """限制最大个数。"""
    draggable: bool = None
    """是否可拖拽排序"""
    addable: bool = None
    """是否可新增"""
    removable: bool = None
    """是否可删除"""
    addButtonClassName: str = ""
    """新增按钮 CSS 类名"""
    itemClassName: str = ""
    """值元素 CSS 类名"""
    itemsClassName: str = ""
    """值包裹元素 CSS 类名"""
    form: Form = None
    """子表单配置，同 Form"""
    addButtonText: str = ""
    """自定义新增一项的文本"""
    showErrorMsg: bool = True
    """是否在左下角显示报错信息"""


class Textarea(FormItem):
    """多行文本输入框"""
    type: str = 'textarea'
    """指定为 textarea 渲染器"""
    minRows: int = 3
    """最小行数"""
    maxRows: int = 20
    """最大行数"""
    trimContents: bool = True
    """是否去除首尾空白文本"""
    readOnly: bool = False
    """是否只读"""
    showCounter: bool = False
    """是否显示计数器"""
    maxLength: int = None
    """限制最大字数"""
    clearable: bool = False
    """是否可清除"""
    resetValue: str = ""
    """清除后设置此配置项给定的值。"""


class InputMonth(FormItem):
    """月份"""
    type: str = 'input-month'
    """指定为 input-month 渲染器"""
    value: str = None
    """默认值"""
    format: str = "X"
    """月份选择器值格式，更多格式类型请参考 moment"""
    inputFormat: str = "YYYY-MM"
    """月份选择器显示格式，即时间戳格式，更多格式类型请参考 moment"""
    placeholder: str = "请选择月份"
    """占位文本"""
    clearable: bool = True
    """是否可清除"""


class InputTime(FormItem):
    """时间"""
    type: str = 'input-time'
    """指定为 input-time 渲染器"""
    value: str = None
    """默认值"""
    timeFormat: str = "HH:mm"
    """时间选择器值格式，更多格式类型请参考 moment"""
    format: str = "X"
    """时间选择器值格式，更多格式类型请参考 moment"""
    inputFormat: str = "HH:mm"
    """时间选择器显示格式，即时间戳格式，更多格式类型请参考 moment"""
    placeholder: str = "请选择时间"
    """占位文本"""
    clearable: bool = True
    """ 是否可清除"""
    timeConstraints: Union[dict, bool] = True
    """请参考： react-datetime"""


class InputDatetime(FormItem):
    """日期"""
    type: str = 'input-datetime'
    """指定为 input-datetime 渲染器"""
    value: str = None
    """默认值"""
    format: str = "X"
    """日期时间选择器值格式，更多格式类型请参考 文档"""
    inputFormat: str = "YYYY-MM-DD HH:mm:ss"
    """日期时间选择器显示格式，即时间戳格式，更多格式类型请参考 文档"""
    placeholder: str = "请选择日期以及时间"
    """占位文本"""
    shortcuts: str = None
    """日期时间快捷键"""
    minDate: str = None
    """限制最小日期时间"""
    maxDate: str = None
    """限制最大日期时间"""
    utc: bool = False
    """保存 utc 值"""
    clearable: bool = True
    """ 是否可清除"""
    embed: bool = False
    """是否内联"""
    timeConstraints: Union[dict, bool] = None
    """请参考： react-datetime"""


class InputDate(FormItem):
    """日期"""
    type: str = 'input-date'
    """指定为 input-date渲染器"""
    value: str = None
    """默认值"""
    format: str = "X"
    """日期选择器值格式，更多格式类型请参考 文档"""
    inputFormat: str = "YYYY-DD-MM"
    """日期选择器显示格式，即时间戳格式，更多格式类型请参考 文档"""
    closeOnSelect: bool = False
    """点选日期后，是否马上关闭选择框"""
    placeholder: str = "请选择日期"
    """占位文本"""
    shortcuts: str = None
    """日期快捷键"""
    minDate: str = None
    """限制最小日期"""
    maxDate: str = None
    """限制最大日期"""
    utc: bool = False
    """保存 utc 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""


class InputQuarter(InputDate):
    """季度"""
    type: str = 'input-quarter'
    """指定为 input-quarter 渲染器"""


class InputQuarterRange(FormItem):
    """季度范围"""
    type: str = 'input-quarter-range'
    """"指定为 input-quarter-range 渲染器"""
    format: str = "X"
    """日期选择器值格式"""
    inputFormat: str = "YYYY-DD"
    """日期选择器显示格式"""
    placeholder: str = "请选择季度范围"
    """占位文本"""
    minDate: str = None
    """限制最小日期，用法同 限制范围"""
    maxDate: str = None
    """限制最大日期，用法同 限制范围"""
    minDuration: str = None
    """限制最小跨度，如： 2quarter"""
    maxDuration: str = None
    """限制最大跨度，如：4quarter"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""


class InputYear(InputDate):
    """年份选择"""
    type: str = 'input-year'
    """指定为 input-year 渲染器"""


class Radios(FormItem):
    """单选框"""
    type: str = 'radios'
    """指定为 radios 渲染器"""
    options: OptionsNode = None
    """选项组"""
    source: Union[API, str] = None
    """动态选项组"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    columnsCount: int = 1
    """选项按几列显示，默认为一列"""
    inline: bool = True
    """是否显示为一行"""
    selectFirst: bool = False
    """是否默认选中第一个"""
    autoFill: dict = None
    """自动填充"""


class ChartRadios(FormItem):
    """图表单选框"""
    type: str = 'chart-radios'
    """指定为 chart-radios 渲染器"""
    config: dict = None
    """echart图表配置"""
    showTooltipOnHighlight: bool = False
    """高亮的时候是否显示 tooltip"""
    chartValueField: str = "value"
    """	图表数值字段名"""


class InputRating(FormItem):
    """评分"""
    type: str = 'input-rating'
    """指定为 input-rating 渲染器"""
    value: int = None
    """当前值"""
    half: bool = False
    """是否使用半星选择"""
    count: int = 5
    """总星数"""
    readOnly: bool = False
    """只读"""
    allowClear: bool = True
    """是否允许再次点击后清除"""
    colors: Union[str, dict] = {'2': '#abadb1', '3': '#787b81', '5': '#ffa900'}
    """星星被选中的颜色。 若传入字符串，则只有一种颜色。若传入对象，可自定义分段，键名为分段的界限值，键值为对应的类名"""
    inactiveColor: str = "#e7e7e8"
    """未被选中的星星的颜色"""
    texts: dict = None
    """星星被选中时的提示文字。可自定义分段，键名为分段的界限值，键值为对应的类名"""
    textPosition: Literal['right', 'left'] = "right"
    """文字的位置"""
    char: str = "★"
    """自定义字符"""
    className: str = None
    """自定义样式类名"""
    charClassName: str = None
    """自定义字符类名"""
    textClassName: str = None
    """自定义文字类名"""


class InputRange(FormItem):
    """滑块"""
    type: str = 'input-range'
    """指定为 input-rang 渲染器"""
    className: str = None
    """css 类名"""
    value: Union[int, str, dict, List[int]] = None
    """默认值"""
    min: int = 0
    """最小值"""
    max: int = 100
    """最大值"""
    disabled: bool = False
    """是否禁用"""
    step: int = 1
    """步长"""
    showSteps: bool = None
    """是否显示步长"""
    parts: Union[int, List[int]] = 1
    """分割的块数 主持数组传入分块的节点"""
    marks: dict = None
    """刻度标记- 支持自定义样式- 设置百分比"""
    tooltipVisible: bool = False
    """是否显示滑块标签"""
    tooltipPlacement: Literal["auto", "bottom", "left", "right"] = "top"
    """滑块标签的位置，默认auto，方向自适应 前置条件：tooltipVisible 不为 false 时有效"""
    tipFormatter: str = None
    """控制滑块标签显隐函数 前置条件：tooltipVisible 不为 false 时有效"""
    multiple: bool = False
    """支持选择范围"""
    joinValues: bool = True
    """默认为 true，选择的 value 会通过 delimiter 连接起来，否则直接将以{min: 1, max: 100}的形式提交 前置条件：开启multiple时有效"""
    delimiter: Union[str,bool] = ","
    """分隔符"""
    unit: str = None
    """单位"""
    clearable: bool = False
    """是否可清除 前置条件：开启showInput时有效"""
    showInput: bool = False
    """是否显示输入框"""
    onChange: str = None
    """当 组件 的值发生改变时，会触发 onChange 事件，并把改变后的值作为参数传入"""
    onAfterChange: str = None
    """与 onmouseup 触发时机一致，把当前值作为参数传入"""


class InputRepeat(FormItem):
    """重复频率选择器"""
    type: str = 'input-repeat'
    """指定为 input-repeat 渲染器"""
    options: Union[str, List[Literal[
        'secondly', 'minutely', 'hourly', 'daily', 'weekdays', 'weekly', 'monthly', 'yearly']]] = "hourly,daily,weekly,monthly"
    """可用配置"""
    placeholder: str = "不重复"
    """当不指定值时的说明。"""


class InputTimeRange(FormItem):
    """时间范围"""
    type: str = 'input-time-range'
    """指定为 input-time-range 渲染器"""
    timeFormat: str = "HH:mm"
    """时间范围选择器值格式"""
    format: str = "HH:mm"
    """时间范围选择器值格式"""
    inputFormat: str = "HH:mm"
    """时间范围选择器显示格式"""
    placeholder: str = "请选择时间范围"
    """占位文本"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""


class InputDatetimeRange(FormItem):
    """日期时间范围"""
    type: str = 'input-datetime-range'
    """指定为 input-datetime-range 渲染器"""
    format: str = "X"
    """日期时间选择器值格式"""
    inputFormat: str = "YYYY-MM-DD"
    """日期时间选择器显示格式"""
    placeholder: str = "请选择日期时间范围"
    """占位文本"""
    ranges: Union[str, List[str]] = "yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter"
    """ 日期范围快捷键，"""
    minDate: str = None
    """限制最小日期时间，用法同 限制范围"""
    maxDate: str = None
    """限制最大日期时间，用法同 限制范围"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    animation: bool = True
    """是否启用游标动画"""


class InputDateRange(FormItem):
    """日期范围"""
    type: str = 'input-date-range'
    """指定为 input-date-range 渲染器"""
    format: str = "X"
    """日期时间选择器值格式"""
    inputFormat: str = "YYYY-MM-DD"
    """日期时间选择器显示格式"""
    placeholder: str = "请选择日期范围"
    """占位文本"""
    ranges: Union[str, List[str]] = "yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter"
    """ 日期范围快捷键，"""
    minDate: str = None
    """限制最小日期时间，用法同 限制范围"""
    maxDate: str = None
    """限制最大日期时间，用法同 限制范围"""
    minDuration: str = None
    """限制最小跨度，如： 2days"""
    maxDuration: str = None
    """限制最大跨度，如：1year"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    animation: bool = True
    """是否启用游标动画"""


class InputMonthRange(FormItem):
    """月份范围"""
    type: str = 'input-month-range'
    """指定为 input-month-range 渲染器"""
    format: str = "X"
    """日期时间选择器值格式"""
    inputFormat: str = "YYYY-MM-DD"
    """日期时间选择器显示格式"""
    placeholder: str = "请选择月份范围"
    """占位文本"""
    minDate: str = None
    """限制最小日期时间，用法同 限制范围"""
    maxDate: str = None
    """限制最大日期时间，用法同 限制范围"""
    minDuration: str = None
    """限制最小跨度，如： 2days"""
    maxDuration: str = None
    """限制最大跨度，如：1year"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""


class InputYearRange(FormItem):
    """年份范围"""
    type: str = 'input-year-range'
    """指定为 input-year-range 渲染器"""
    format: str = "X"
    """日期时间选择器值格式"""
    inputFormat: str = "YYYY-MM-DD"
    """日期时间选择器显示格式"""
    placeholder: str = "请选择年份范围"
    """占位文本"""
    minDate: str = None
    """限制最小日期时间，用法同 限制范围"""
    maxDate: str = None
    """限制最大日期时间，用法同 限制范围"""
    minDuration: str = None
    """限制最小跨度，如： 2days"""
    maxDuration: str = None
    """限制最大跨度，如：1year"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""


class InputKV(FormItem):
    """键值对"""
    type: str = 'input-kv'
    """指定为 input-kv 渲染器"""
    valueType: Union[str, SchemaNode] = "input-text"
    """值类型"""
    keyPlaceholder: str = None
    """key 的提示信息"""
    valuePlaceholder: str = None
    """value 的提示信息"""
    draggable: bool = True
    """是否可拖拽排序"""
    defaultValue: Any = ""
    """默认值"""


class InputKVS(FormItem):
    """键值对象"""
    type: str = 'input-kvs'
    """指定为 input-kvs 渲染器"""
    addButtonText: str = "新增字段"
    """新增按钮文本"""
    keyItem: dict = None
    """key 的配置"""
    valueItems: List[SchemaNode] = None
    """value 的配置"""


class Formula(FormItem):
    """公式"""
    type: str = 'formula'
    """指定为 formula 渲染器"""
    name: str = None
    """需要应用的表单项name值，公式结果将作用到此处指定的变量中去。"""
    formula: Expression = None
    """应用的公式"""
    condition: Expression = None
    """公式作用条件"""
    initSet: bool = True
    """初始化时是否设置"""
    autoSet: bool = True
    """观察公式结果，如果计算结果有变化，则自动应用到变量上"""
    id: str = None
    """定义个名字，当某个按钮的目标指定为此值后，会触发一次公式应用。这个机制可以在 autoSet 为 false 时用来手动触发"""


class InputFormula(FormItem):
    """公式编辑器"""
    type: str = 'input-formula'
    """指定为 input-formula 渲染器"""
    title: str = '公式编辑器'
    """弹框标题"""
    header: str = None
    """编辑器 header 标题，如果不设置，默认使用表单项label字段"""
    evalMode: bool = True
    """表达式模式 或者 模板模式，模板模式则需要将表达式写在 ${ 和 } 中间。"""
    variables: Union[dict, list] = []
    """可用变量"""
    variableMode: Literal['tabs', 'list', 'tree'] = "list"
    """可配置成 tabs 或者 tree 默认为列表，支持分组。"""
    functions: List[dict] = None
    """可以不设置，默认就是 amis-formula 里面定义的函数，如果扩充了新的函数则需要指定"""
    inputMode: Literal['button', 'input-button', 'input-group'] = None
    """控件的展示模式"""
    icon: str = None
    """按钮图标，例如fa fa-list"""
    btnLabel: str = '公示编辑'
    """按钮文本，inputMode为button时生效"""
    level: LevelEnum = LevelEnum.default
    """按钮样式"""
    allowInput: bool = None
    """输入框是否可输入"""
    btnSize: Literal['xs', 'sm', 'md', 'lg'] = None
    """按钮大小"""
    borderMode: Literal['full', 'half', 'none'] = None
    """输入框边框模式"""
    placeholder: str = '暂无数据'
    """输入框占位符"""
    className: str = None
    """控件外层 CSS 样式类名"""
    variableClassName: str = None
    """变量面板 CSS 样式类名"""
    functionClassName: str = None
    """函数面板 CSS 样式类名"""


class Transfer(FormItem):
    """穿梭器"""
    type: str = 'transfer'
    """指定为 transfer 渲染器"""
    options: OptionsNode = None
    """选项组"""
    source: Union[str, API] = None
    """动态选项组"""
    delimiter: Union[str,bool] = ","
    """拼接符"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    searchable: bool = False
    """当设置为 true 时表示可以通过输入部分内容检索出选项。"""
    searchApi: API = None
    """如果想通过接口检索，可以设置个 api。"""
    resultListModeFollowSelect: bool = False
    """结果面板跟随模式，目前只支持list、table、tree（tree 目前只支持非延时加载的tree）"""
    statistics: bool = True
    """是否显示统计数据"""
    selectTitle: str = "请选择"
    """左侧的标题文字"""
    resultTitle: str = "当前选择"
    """右侧结果的标题文字"""
    sortable: bool = False
    """结果可以进行拖拽排序"""
    selectMode: Literal["list", "table", "tree", "chained", "associated"] = "list"
    """可选：list、table、tree、chained、associated。分别为：列表形式、表格形式、树形选择形式、级联选择形式，关联选择形式（与级联选择的区别在于，级联是无限极，而关联只有一级，关联左边可以是个 tree）。"""
    searchResultMode: str = None
    """如果不设置将采用 selectMode 的值，可以单独配置，参考 selectMode，决定搜索结果的展示形式。"""
    searchPlaceholder: str = None
    """左侧列表搜索框提示"""
    columns: List[dict] = None
    """当展示形式为 table 可以用来配置展示哪些列，跟 table 中的 columns 配置相似，只是只有展示功能。"""
    leftOptions: List[dict] = None
    """当展示形式为 associated 时用来配置左边的选项集。"""
    leftMode: str = None
    """当展示形式为 associated 时用来配置左边的选择形式，支持 list 或者 tree。默认为 list。"""
    rightMode: str = None
    """当展示形式为 associated 时用来配置右边的选择形式，可选：list、table、tree、chained。"""
    resultSearchable: bool = False
    """结果（右则）列表的检索功能，当设置为 true 时，可以通过输入检索模糊匹配检索内容（目前树的延时加载不支持结果搜索功能）"""
    menuTpl: SchemaNode = None
    """用来自定义选项展示"""
    valueTpl: SchemaNode = None
    """用来自定义值的展示"""
    multiple: bool = None
    """是否多选"""
    itemHeight: int = 32
    """每个选项的高度，用于虚拟渲染"""
    virtualThreshold: int = 100
    """在选项数量超过多少时开启虚拟渲染"""


class TransferPicker(Transfer):
    """穿梭选择器"""
    type: str = 'transfer-picker'
    """指定为 transfer-picker 渲染器"""


class TabsTransfer(Transfer):
    """组合穿梭器"""
    type: str = 'tabs-transfer'
    """指定为 tabs-transfer 渲染器"""


class TabsTransferPicker(Transfer):
    """组合穿梭选择器"""
    type: str = 'tabs-transfer-picker'
    """指定为 tabs-transfer-picker 渲染器"""


class InputTree(FormItem):
    """树形选择框"""
    type: str = 'input-tree'
    """指定为 input-tree 渲染器"""
    options: OptionsNode = None
    """选项组"""
    source: Union[str, API] = None
    """动态选项组"""
    autoComplete: API = None
    """自动提示补全"""
    multiple: bool = False
    """是否多选"""
    delimiter: Union[str, bool] = False
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    iconField: str = "icon"
    """图标值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    creatable: bool = False
    """新增选项"""
    addControls: List[FormItem] = None
    """自定义新增表单项"""
    addApi: API = None
    """配置新增选项接口"""
    editable: bool = None
    """False  # 编辑选项"""
    editControls: List[FormItem] = None
    """自定义编辑表单项"""
    editApi: API = None
    """配置编辑选项接口"""
    removable: bool = False
    """删除选项"""
    deleteApi: API = None
    """配置删除选项接口"""
    searchable: bool = False
    """是否可检索，仅在 type 为 tree-select 的时候生效"""
    hideRoot: bool = True
    """如果想要显示个顶级节点，请设置为 false"""
    rootLabel: str = "顶级"
    """当 hideRoot 不为 false 时有用，用来设置顶级节点的文字。"""
    showIcon: bool = True
    """是否显示图标"""
    showRadio: bool = False
    """是否显示单选按钮，multiple 为 false 是有效。"""
    initiallyOpen: bool = True
    """设置是否默认展开所有层级。"""
    unfoldedLevel: int = 1
    """设置默认展开的级数，只有initiallyOpen不是true时生效。"""
    autoCheckChildren: bool = True
    """当选中父节点时级联选择子节点。"""
    cascade: bool = False
    """当选中父节点时不自动选择子节点。"""
    withChildren: bool = False
    """选中父节点时，值里面将包含子节点的值，否则只会保留父节点的值。"""
    onlyChildren: bool = False
    """多选时，选中父节点时，是否只将其子节点加入到值中。"""
    onlyLeaf: bool = False
    """只允许选择叶子节点"""
    rootCreatable: bool = False
    """是否可以创建顶级节点"""
    rootCreateTip: str = "添加一级节点"
    """创建顶级节点的悬浮提示"""
    minLength: int = None
    """最少选中的节点数"""
    maxLength: int = None
    """最多选中的节点数"""
    treeContainerClassName: str = None
    """tree 最外层容器类名"""
    enableNodePath: bool = False
    """是否开启节点路径模式"""
    pathSeparator: str = "/"
    """节点路径的分隔符，enableNodePath为true时生效"""
    highlightTxt: str = None
    """标签中需要高亮的字符，支持变量"""
    itemHeight: int = 32
    """每个选项的高度，用于虚拟渲染"""
    virtualThreshold: int = 100
    """在选项数量超过多少时开启虚拟渲染"""
    menuTpl: str = None
    """选项自定义渲染 HTML 片段"""
    enableDefaultIcon: bool = True
    """是否为选项添加默认的前缀 Icon，父节点默认为folder，叶节点默认为file"""
    heightAuto: bool = False
    """默认高度会有个 maxHeight，即超过一定高度就会内部滚动，如果希望自动增长请设置此属性"""


class TreeSelect(InputTree):
    """树形选择器"""
    type: str = 'tree-select'
    """指定为 tree-select 渲染器"""
    hideNodePathLabel: bool = False
    """是否隐藏选择框中已选择节点的路径 label 信息"""
    onlyLeaf: bool = False
    """只允许选择叶子节点"""
    searchable: bool = False
    """是否可检索，仅在 type 为 tree-select 的时候生效"""


class JSONSchema(FormItem):
    """JSON生成页面"""
    type: str = 'json-schema'
    """指定为 json-schema 渲染器"""
    schema_: Union[str, dict] = Field(None, alias='schema')
    """指定 json-schema"""


class JSONSchemaEditor(FormItem):
    """JSON页面编辑器"""
    type: str = 'json-schema-editor'
    """指定为 json-schema-editor 渲染器"""
    rootTypeMutable: bool = False
    """顶级类型是否可配置"""
    showRootInfo: bool = False
    """是否显示顶级类型信息"""
    disabledTypes: List[Literal['string', 'number', 'interger', 'object', 'number', 'array', 'boolean', 'null']] = None
    """	用来禁用默认数据类型，默认类型有：string、number、interger、object、number、array、boolean、null"""
    definitions: dict = None
    """用来配置预设类型"""
    placeholder: Union[str, dict] = {"key": "字段名", "title": "名称", "description": "描述", "default": "默认值",
                                     "empty": "<空>"}
    """属性输入控件的占位提示文本"""


class ImageAction(AmisNode):
    """图片动作"""
    key: Literal['rotateRight', 'rotateLeft', 'zoomIn', 'zoomOut', 'scaleOrigin'] = None
    """操作key"""
    label: Union[Literal[False], Template,str] = None
    """动作名称"""
    icon: str = None
    """动作图标"""
    iconClassName: str = None
    """动作自定义CSS类"""
    disabled: bool = None
    """动作是否禁用"""


class Image(AmisNode):
    """图片"""
    type: str = 'image'
    """指定为 image 渲染器，如果在 Table、Card 和 List 中，为"image"；在 Form 中用作静态展示，为"static-image"""
    className: str = None
    """外层 CSS 类名"""
    innerClassName: str = None
    """组件内层 CSS 类名"""
    imageClassName: str = None
    """图片 CSS 类名"""
    thumbClassName: str = None
    """图片缩率图 CSS 类名"""
    height: int = None
    """图片缩率高度"""
    width: int = None
    """图片缩率宽度"""
    title: str = None
    """标题"""
    imageCaption: str = None
    """描述"""
    placeholder: str = None
    """占位文本"""
    defaultImage: str = None
    """无数据时显示的图片"""
    src: str = None
    """缩略图地址"""
    href: Template = None
    """外部链接地址"""
    originalSrc: str = None
    """原图地址"""
    enlargeAble: bool = None
    """支持放大预览"""
    enlargeTitle: str = None
    """放大预览的标题"""
    enlargeCaption: str = None
    """放大预览的描述"""
    thumbMode: Literal['w-full', 'h-full', 'contain', 'cover'] = "contain"
    """预览图模式，可选：'w-full', 'h-full', 'contain', 'cover'"""
    thumbRatio: Literal['1:1', '4:3', '16:9'] = "1:1"
    """预览图比例，可选：'1:1','4:3','16:9'"""
    imageMode: Literal['thumb', 'original'] = "thumb"
    """图片展示模式，可选：'thumb','original' 即：缩略图模式 或者 原图模式"""
    showToolbar: bool = False
    """放大模式下是否展示图片的工具栏"""
    toolbarActions: List[ImageAction] = None
    """图片工具栏，支持旋转，缩放，默认操作全部开启"""


class Images(AmisNode):
    """图片集"""
    type: str = "images"
    """指定为 images 渲染器 如果在 Table、Card 和 List 中，为"images"；在 Form 中用作静态展示，为"static-images"""
    className: str = None
    """外层 CSS 类名"""
    defaultImage: str = None
    """默认展示图片"""
    value: Union[str, List[str], List[dict]] = None
    """图片数组"""
    source: str = None
    """数据源"""
    delimiter: Union[str,bool] = ","
    """分隔符，当 value 为字符串时，用该值进行分隔拆分"""
    src: str = None
    """预览图地址，支持数据映射获取对象中图片变量"""
    originalSrc: str = None
    """原图地址，支持数据映射获取对象中图片变量"""
    enlargeAble: bool = None
    """支持放大预览"""
    thumbMode: Literal['w-full', 'h-full', 'contain', 'cover'] = "contain"
    """预览图模式，可选：'w-full', 'h-full', 'contain', 'cover'"""
    thumbRatio: Literal['1:1', '4:3', '16:9'] = "1:1"
    """预览图比例，可选：'1:1','4:3','16:9'"""
    showToolbar: bool = False
    """放大模式下是否展示图片的工具栏"""
    toolbarActions: List[ImageAction] = None
    """图片工具栏，支持旋转，缩放，默认操作全部开启"""


class GridNav(AmisNode):
    """宫格导航"""

    class Option(AmisNode):
        icon: str = None
        """列表项图标"""
        text: str = None
        """列表项文案"""
        badge: Badge = None
        """列表项角标，详见 Badge"""
        link: str = None
        """内部页面路径或外部跳转 URL 地址，优先级高于 clickAction"""
        blank: bool = None
        """是否新页面打开，link 为 url 时有效"""
        clickAction: Action = None
        """列表项点击交互 详见 Action"""

    type: str = 'grid-nav'
    """指定为 grid-nav"""
    className: str = None
    """外层 CSS 类名"""
    itemClassName: str = None
    """列表项 css 类名"""
    value: List[Option] = None
    """图片数组"""
    source: str = None
    """数据源"""
    square: bool = None
    """是否将列表项固定为正方形"""
    center: bool = True
    """是否将列表项内容居中显示"""
    border: bool = True
    """是否显示列表项边框"""
    gutter: int = None
    """	列表项之间的间距，默认单位为px"""
    reverse: bool = None
    """	是否调换图标和文本的位置"""
    iconRatio: int = 60
    """图标宽度占比，单位%"""
    direction: Literal['horizontal', 'vertical'] = "vertical"
    """	列表项内容排列的方向"""
    columnNum: int = 4
    """列数"""


class Carousel(AmisNode):
    """轮播图"""

    class Options(AmisNode):
        image: str = None
        """图片链接"""
        href: str = None
        """图片打开网址的链接"""
        imageClassName: str = None
        """图片类名"""
        title: str = None
        """图片标题"""
        titleClassName: str = None
        """图片标题类名"""
        description: str = None
        """图片描述"""
        descriptionClassName: str = None
        """图片描述类名"""
        html: str = None
        """HTML 自定义，同Tpl一致"""

    type: str = "carousel"
    """指定为 Carousel 渲染器"""
    className: str = "panel-default"
    """外层 Dom 的类名"""
    options: List[Options] = []
    """轮播面板数据"""
    itemSchema: dict = None
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
    controls: List[str] = ['dots', 'arrows']
    """显示左右箭头、底部圆点索引"""
    controlsTheme: str = "light"
    """左右箭头、底部圆点索引颜色，默认light，另有dark模式"""
    animation: str = "fade"
    """切换动画效果，默认fade，另有slide模式"""
    thumbMode: str = None
    """图片默认缩放模式"""
    multiple: dict = {"count": 1}
    """多图展示，count表示展示的数量"""
    alwaysShowArrow: bool = False
    """是否一直显示箭头，为false时鼠标hover才会显示"""
    icons: Union[str, dict] = None
    """自定义箭头图标"""


class CRUD(AmisNode):
    """增删改查"""

    class Messages(AmisNode):
        fetchFailed: str = None
        """获取失败时提示"""
        saveOrderFailed: str = None
        """保存顺序失败提示"""
        saveOrderSuccess: str = None
        """保存顺序成功提示"""
        quickSaveFailed: str = None
        """快速保存失败提示"""
        quickSaveSuccess: str = None
        """快速保存成功提示"""

    type: str = "crud"
    """type 指定为 CRUD 渲染器"""
    mode: Literal["table", "cards", "list"] = "table"
    """"table" 、 "cards" 或者 "list"""
    title: str = ""
    """可设置成空，当设置成空时，没有标题栏"""
    className: str = None
    """表格外层 Dom 的类名"""
    api: API = None
    """CRUD 用来获取列表数据的 api。"""
    loadDataOnce: bool = None
    """是否一次性加载所有数据（前端分页）"""
    loadDataOnceFetchOnFilter: bool = True
    """在开启 loadDataOnce 时，filter 时是否去重新请求 api"""
    source: str = None
    """数据映射接口返回某字段的值，不设置会默认使用接口返回的${items}或者${rows}，也可以设置成上层数据源的内容"""
    filter: Union[SchemaNode, Form] = None
    """设置过滤器，当该表单提交后，会把数据带给当前 mode 刷新列表。"""
    filterTogglable: bool = False
    """是否可显隐过滤器"""
    filterDefaultVisible: bool = True
    """设置过滤器默认是否可见。"""
    initFetch: bool = True
    """是否初始化的时候拉取数据, 只针对有 filter 的情况, 没有 filter 初始都会拉取数据"""
    interval: int = 3000
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
    itemDraggableOn: bool = None
    """用表达式来配置是否可拖拽排序"""
    saveOrderApi: API = None
    """保存排序的 api。"""
    quickSaveApi: API = None
    """快速编辑后用来批量保存的 API。"""
    quickSaveItemApi: API = None
    """快速编辑配置成及时保存时使用的 API。"""
    bulkActions: List[Action] = None
    """批量操作列表，配置后，表格可进行选中操作。"""
    messages: Messages = None
    """覆盖消息提示，如果不指定，将采用 api 返回的 message"""
    primaryField: str = "id"
    """设置 ID 字段名。'id'"""
    perPage: int = 10
    """设置一页显示多少条数据."""
    defaultParams: dict = None
    """设置默认 filter 默认参数，会在查询的时候一起发给后端"""
    pageField: str = "page"
    """设置分页页码字段名。"""
    perPageField: str = "perPage"
    """设置分页一页显示的多少条数据的字段名。注意：最好与 defaultParams 一起使用，请看下面例子。"""
    perPageAvailable: List[int] = [5, 10, 20, 50, 100]
    """设置一页显示多少条数据下拉框可选条数。"""
    orderField: str = None
    """设置用来确定位置的字段名，设置后新的顺序将被赋值到该字段中。"""
    hideQuickSaveBtn: bool = False
    """隐藏顶部快速保存提示"""
    autoJumpToTopOnPagerChange: bool = False
    """当切分页的时候，是否自动跳顶部。"""
    syncResponse2Query: bool = True
    """将返回数据同步到过滤器上。"""
    keepItemSelectionOnPageChange: bool = True
    """保留条目选择，默认分页、搜素后，用户选择条目会被清空，开启此选项后会保留用户选择，可以实现跨页面批量操作。"""
    labelTpl: str = None
    """
    单条描述模板，keepItemSelectionOnPageChange
    设置为true后会把所有已选择条目列出来，此选项可以用来定制条目展示文案。
    """
    headerToolbar: list = ['bulkActions', 'pagination']
    """顶部工具栏配置"""
    footerToolbar: list = ['statistics', 'pagination']
    """底部工具栏配置"""
    alwaysShowPagination: bool = False
    """是否总是显示分页"""
    affixHeader: bool = True
    """是否固定表头(table 下)"""
    autoGenerateFilter: Union[dict, bool] = None
    """是否开启查询区域，开启后会根据列元素的 searchable 属性值，自动生成查询条件表单"""
    resetPageAfterAjaxItemAction: bool = False
    """单条数据 ajax 操作后是否重置页码为第一页"""
    autoFillHeight: Union[bool, dict] = None
    """内容区域自适应高度"""
    itemAction: Action = None
    """实现点击某一行后进行自定义操作，支持 action 里的所有配置，比如弹框、刷新其它组件等。"""

    defaultChecked: bool = None
    """当可批量操作时，默认是否全部勾选。"""


class AmisList(AmisNode):
    """列表"""

    class Item(AmisNode):
        """单条信息"""

        class ListBodyField(AmisNode):
            """列配置"""
            label: Union[Literal[False], Template,str] = None
            """列标题"""
            className: str = None
            """外层DOM的CSS类名"""
            labelClassName: str = None
            """label的CSS类名"""
            innerClassName: str = None
            """内层组件的CSS类名，className属性会添加到外层DOM，如果要在组件层级添加CSS类，请设置当前属性"""
            name: str = None
            """绑定字段名"""
            popOver: Union[SchemaNode, dict] = None
            """配置查看详情功能"""
            quickEdit: Union[SchemaNode, dict, str] = None
            """配置快速编辑功能"""
            copyable: Union[SchemaNode, dict, str] = None
            """配置点击复制功能"""

        title: Template = None
        """标题"""
        titleClassName: str = "h5"
        """标题 CSS 类名"""
        subTitle: Template = None
        """副标题"""
        avatar: Template = None
        """图片地址"""
        avatarClassName: str = "thumb-sm avatar m-r"
        """图片 CSS 类名"""
        desc: Template = None
        """描述"""
        body: List[ListBodyField] = None
        """内容容器，主要用来放置非表单项组件"""
        actions: List[Action] = None
        """按钮区域"""
        actionsPosition: Literal['left', 'right'] = "right"
        """按钮位置"""

    type: str = 'list'
    """指定为 list 渲染器"""
    title: str = None
    """标题"""
    source: str = "${items}"
    """数据源, 获取当前数据域变量，支持数据映射"""
    placeholder: str = "暂无数据"
    """当没数据的时候的文字提示"""
    selectable: bool = False
    """列表是否可选"""
    multiple: bool = True
    """列表是否为多选"""
    className: str = None
    """外层 CSS 类名"""
    headerClassName: str = "amis-list-header"
    """顶部外层 CSS 类名"""
    footerClassName: str = "amis-list-footer"
    """底部外层 CSS 类名"""
    listItem: Item = None
    """配置单条信息"""


class TableColumn(AmisNode):
    """列配置"""
    type: str = None
    """Literal['text','audio','image','link','tpl','mapping','carousel','date', 'progress','status','switch','list','json','operation']"""
    label: Template = None
    """表头文本内容"""
    name: str = None
    """通过名称关联数据"""
    tpl: Template = None
    """模板"""
    fixed: str = None
    """是否固定当前列 left|right|none"""
    popOver: Union[bool, dict, str] = None
    """弹出框"""
    quickEdit: Union[bool, dict] = None
    """快速编辑"""
    copyable: Union[bool, dict] = None
    """是否可复制  boolean 或 {icon: string, content:string}"""
    sortable: bool = False
    """是否可排序"""
    searchable: Union[bool, SchemaNode] =False
    """是否可快速搜索  boolean|Schema"""
    width: Union[str, int] = None
    """列宽"""
    style: dict = None
    """单元格自定义样式"""
    innerStyle: dict = None
    """单元格内部组件自定义样式"""
    remark: Remark = None
    """提示信息"""
    breakpoint: str = None
    """*,ls"""
    filterable: Dict[str, OptionsNode] = None
    """过滤"""
    map: dict = None
    """映射"""


class ColumnOperation(TableColumn):
    """操作列"""
    type: str = 'operation'
    label: Template = None
    """操作"""
    toggled: bool = True
    buttons: List[Union[Action, AmisNode]] = None


class ColumnList(AmisList, TableColumn):
    """列表列"""
    pass


class ColumnImage(Image, TableColumn):
    """图片列"""
    pass


class ColumnImages(Images, TableColumn):
    """图片集列"""
    pass


class Table(AmisNode):
    """表格"""

    type: str = "table"
    """指定为 table 渲染器"""
    title: str = None
    """标题"""
    source: str = "${items}"
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
    columns: List[Union[TableColumn, SchemaNode]] = None
    """用来设置列信息"""
    combineNum: int = None
    """自动合并单元格"""
    itemActions: List[Action] = None
    """悬浮行操作按钮组"""
    itemCheckableOn: Expression = None
    """配置当前行是否可勾选的条件，要用 表达式"""
    itemDraggableOn: Expression = None
    """配置当前行是否可拖拽的条件，要用 表达式"""
    checkOnItemClick: bool = False
    """点击数据行是否可以勾选当前行"""
    rowClassName: str = None
    """给行添加 CSS 类名"""
    rowClassNameExpr: Template = None
    """通过模板给行添加 CSS 类名"""
    prefixRow: list = None
    """顶部总结行"""
    affixRow: list = None
    """底部总结行"""
    itemBadge: Badge = None
    """行角标配置"""
    autoFillHeight: Union[bool, dict] = None
    """内容区域自适应高度"""
    resizable: bool = True
    """列宽度是否支持调整"""
    selectable: bool = False
    """支持勾选"""
    multiple: bool = False
    """勾选 icon 是否为多选样式checkbox， 默认为radio"""


class TableView(AmisNode):
    """表格展现，详见https://aisuda.bce.baidu.com/amis/zh-CN/components/table-view"""

    class Trs(AmisNode):
        """行设置"""

        class Tds(AmisNode):
            """单元格设置"""
            weight: Union[int, str] = None
            """宽度"""
            background: str = None
            """单元格背景色"""
            color: str = None
            """单元格文字颜色"""
            bold: bool = False
            """单元格文字是否加粗"""
            padding: Union[int, str] = "集成表格的设置"
            """单元格内间距"""
            align: Literal["left", "center", "right"] = "left"
            """单元格内的水平对齐，可以是 left、center、right"""
            valign: Literal["top", "middle", "bottom", "baseline"] = "middle"
            """单元格内的垂直对齐，可以是 top、middle、bottom、baseline"""
            colspan: int = None
            """单元格水平跨几行"""
            rowspan: int = None
            """单元格垂直跨几列"""
            body: SchemaNode = None
            """其它 amis 设置"""

        height: Union[int, str] = None
        """高度"""
        background: str = None
        """行背景色"""
        tds: List[Union[Tds,dict]] = None

    type: str = 'table-view'
    """指定为 table-view 渲染器"""
    trs: List[Union[dict, Trs]] = None
    """行配置"""
    width: Union[int, str] = "100%"
    """宽度"""
    padding: Union[int, str] = 'var(--TableCell-paddingY) var(--TableCell-paddingX)'
    """单元格默认内间距"""
    border: bool = True
    """是否显示边框"""
    borderColor: str = "var(--borderColor)"
    """边框颜色"""
    caption: str = None
    """添加段标题文本"""
    captionSide: Union[str, Literal["top", "bottom"]] = None
    """控制标题显示在底部还是顶部。"""


class Calendar(AmisNode):
    """日历日程"""

    class Schedules(AmisNode):
        """日程"""
        startTime: str
        """开始时间"""
        endTime: str = None
        """结束时间"""
        content: Any = ""
        """内容"""
        className: str = None
        """样式类名"""

    type: str = 'calendar'
    """指定为 calender 渲染器"""
    schedules: List[Union[dict,Schedules]] = None
    """日历中展示日程，可设置静态数据或从上下文中取数据，startTime 和 endTime 格式参考文档，className 参考背景色"""
    scheduleClassNames: List[str] = ['bg-warning', 'bg-danger', 'bg-success', 'bg-info', 'bg-secondary']
    """日历中展示日程的颜色，参考背景色"""
    scheduleAction: List[Action] = None
    """自定义日程展示"""
    largeMode: bool = False
    """放大模式"""
    todayActiveStyle: Any = None
    """今日激活时的自定义样式"""


class Card(AmisNode):
    """卡片"""

    class Header(AmisNode):
        """头部内容"""
        className: str = None
        """样式类名"""
        title: Template = None
        """标题"""
        titleClassName: str = None
        """标题类名"""
        subTitle: Template = None
        """副标题"""
        subTitleClassName: str = None
        """副标题类名"""
        subTitlePlaceholder: str = None
        """副标题占位"""
        description: Template = None
        """描述"""
        descriptionClassName: str = None
        """描述类名"""
        descriptionPlaceholder: str = None
        """描述占位"""
        avatar: Template = None
        """图片"""
        avatarClassName: str = "pull-left thumb avatar b-3x m-r"
        """图片包括层类名"""
        imageClassName: str = None
        """图片类名"""
        avatarText: Template = None
        """如果不配置图片，则会在图片处显示该文本"""
        avatarTextBackground: List[str] = None
        """设置文本背景色，它会根据数据分配一个颜色"""
        avatarTextClassName: str = None
        """图片文本类名"""
        highlight: Union[bool, Template] = False
        """是否显示激活样式"""
        highlightClassName: str = None
        """激活样式类名"""
        href: Template = None
        """点击卡片跳转的链接地址"""
        blank: bool = True
        """是否新窗口打开"""

    class Media(AmisNode):
        """Card 多媒体部内容设置"""
        type: Literal["image", "video"] = None
        """多媒体类型"""
        url: str = None
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

    type: str = "card"
    """指定为 card 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    href: Template = None
    """外部链接"""
    header: Header = None
    """Card 头部内容设置"""
    body: List[SchemaNode] = None
    """内容容器，主要用来放置非表单项组件"""
    bodyClassName: str = None
    """内容区域类名"""
    actions: List[Action] = None
    """配置按钮集合"""
    actionsCount: int = 4
    """按钮集合每行个数"""
    itemAction: Action = None
    """点击卡片的行为"""
    media: Media = None
    "Card 多媒体部内容设置"
    secondary: Template = None
    """次要说明"""
    toolbar: List[SchemaNode] = None
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
    type: str = 'cards'
    """指定为 cards 渲染器"""
    title: Template = None
    """标题"""
    source: str = "${items}"
    """数据源, 获取当前数据域中的变量"""
    placeholder: Template = "暂无数据"
    """当没数据的时候的文字提示"""
    className: str = None
    """外层 CSS 类名"""
    headerClassName: str = "amis-grid-header"
    """顶部外层 CSS 类名"""
    footerClassName: str = "amis-grid-footer"
    """底部外层 CSS 类名"""
    itemClassName: str = "col-sm-4 col-md-3"
    """卡片 CSS 类名"""
    card: Card = None
    """配置卡片信息"""
    selectable: bool = False
    """卡片组是否可选"""
    multiple: bool = True
    """卡片组是否为多选"""
    checkOnItemClick: bool = None
    """点选卡片内容是否选中卡片"""


class Chart(AmisNode):
    """图表: https://echarts.apache.org/zh/option.html#title"""
    type: str = "chart"
    """指定为 chart 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    body: SchemaNode = None
    """内容容器"""
    api: API = None
    """配置项接口地址"""
    source: Union[dict, str] = None
    """通过数据映射获取数据链中变量值作为配置"""
    initFetch: bool = None
    """组件初始化时，是否请求接口"""
    interval: int = None
    """刷新时间(最小 1000)"""
    config: Union[dict, str] = None
    """设置 eschars 的配置项,当为string的时候可以设置 function 等配置项"""
    style: dict = None
    """设置根元素的 style"""
    width: str = None
    """设置根元素的宽度"""
    height: str = None
    """设置根元素的高度"""
    replaceChartOption: bool = False
    """每次更新是完全覆盖配置项还是追加？"""
    trackExpression: str = None
    """当这个表达式的值有变化时更新图表"""
    dataFilter: str = None
    """
    自定义 echart config 转换，函数签名：function(config, echarts, data) {return config;}
     配置时直接写函数体。其中 config 是当前 echart 配置，echarts 就是 echarts 对象，data 为上下文数据。
    """
    mapURL: API = None
    """地图 geo json 地址"""
    mapName: str = None
    """地图名称"""
    loadBaiduMap: bool = None
    """加载百度地图"""


class Code(AmisNode):
    """代码高亮"""
    type: str = "code"
    """指定为 code 渲染器"""
    className: str = None
    """外层 CSS 类名"""
    value: str = None
    """显示的颜色值"""
    name: str = None
    """在其他组件中，时，用作变量映射"""
    language: str = "plaintext"
    """所使用的高亮语言，默认是 plaintext"""
    tabSize: int = 4
    """默认 tab 大小"""
    editorTheme: str = "vs"
    """主题，还有 'vs-dark'"""
    wordWrap: Union[str, bool] = True
    """是否折行"""


class Color(AmisNode):
    """颜色"""
    type: str = 'color'
    """指定为 color 渲染器，如果在 Table、Card 和 List 中，为"color"；在 Form 中用作静态展示，为"static-color" """
    className: str = None
    """外层 CSS 类名"""
    value: str = None
    """显示的颜色值"""
    name: str = None
    """在其他组件中，时，用作变量映射"""
    defaultColor: str = "#CCC"
    """默认颜色值"""
    showValue: bool = True
    """是否显示右边的颜色值"""


class Date(AmisNode):
    """日期时间"""
    type: str = 'date'
    """指定为 date 渲染器"""
    className: str = None
    """外层 CSS 类名"""
    value: str = None
    """显示的日期数值"""
    name: str = None
    """在其他组件中，时，用作变量映射"""
    placeholder: str = "-"
    """占位内容"""
    format: str = "YYYY-MM-DD"
    """展示格式, 更多格式类型请参考 文档"""
    valueFormat: str = "X"
    """数据格式，默认为时间戳。更多格式类型请参考 文档"""
    fromNow: bool = False
    """是否显示相对当前的时间描述，比如: 11 小时前、3 天前、1 年前等，fromNow 为 true 时，format 不生效。"""
    updateFrequency: int = 60000
    """更新频率， 默认为 1 分钟"""


class Each(AmisNode):
    """循环渲染器"""
    type: str = 'each'
    """指定为 each 渲染器"""
    value: list = []
    """用于循环的值"""
    name: str = None
    """获取数据域中变量"""
    source: str = None
    """获取数据域中变量， 支持 数据映射"""
    items: dict = None
    """使用value中的数据，循环输出渲染器。"""
    placeholder: str = None
    """当 value 值不存在或为空数组时的占位文本"""


class Json(AmisNode):
    """JSON 展示组件"""
    type: str = "json"
    """指定为 json 渲染器，如果在 Table、Card 和 List 中，为"json"；在 Form 中用作静态展示，为"static-json"""
    className: str = None
    """外层 CSS 类名"""
    value: Union[dict, str] = None
    """json 值，如果是 string 会自动 parse"""
    source: str = ""
    """通过数据映射获取数据链中的值"""
    placeholder: str = "-"
    """占位文本"""
    levelExpand: int = 1
    """默认展开的层级"""
    jsonTheme: str = "twilight"
    """主题，可选twilight和eighties"""
    mutable: bool = False
    """是否可修改"""
    displayDataTypes: bool = False
    """是否显示数据类型"""
    ellipsisThreshold: Union[int, bool] = False
    """设置字符串的最大展示长度，点击字符串可以切换全量/部分展示方式，默认展示全量字符串"""


class Link(AmisNode):
    """链接"""
    type: str = "link"
    """指定为 link 渲染器，如果在 Table、Card 和 List 中，为"link"；在 Form 中用作静态展示，为"static-link"""
    body: str = None
    """标签内文本"""
    href: str = None
    """链接地址"""
    blank: bool = None
    """是否在新标签页打开"""
    htmlTarget: str = None
    """a 标签的 target，优先于 blank 属性"""
    title: str = None
    """a 标签的 title"""
    disabled: bool = None
    """禁用超链接"""
    icon: str = None
    """超链接图标，以加强显示"""
    rightIcon: str = None
    """右侧图标"""


class Log(AmisNode):
    """实时日志"""
    type: str = "log"
    """指定为 log 渲染器"""
    source: API = None
    """支持变量,可以初始设置为空，这样初始不会加载，而等这个变量有值的时候再加载"""
    height: int = 500
    """展示区域高度"""
    className: str = None
    """外层 CSS 类名"""
    autoScroll: bool = True
    """是否自动滚动"""
    placeholder: str = None
    """加载中的文字"""
    encoding: str = "utf-8"
    """"返回内容的字符编码"""
    rowHeight: int = None
    """设置每行高度，将会开启虚拟渲染"""
    maxLength: int = None
    """最大显示行数"""
    operation: List[Literal['stop', 'clear', 'showLineNumber', 'filter']] = None
    """可选日志操作"""


class Mapping(AmisNode):
    """映射"""
    type: str = "mapping"
    """指定为 mapping 渲染器，如果在 Table、Card 和 List 中，为"mapping"；在 Form 中用作静态展示，为"static-mapping"""
    className: str = None
    """外层 CSS 类名"""
    placeholder: str = None
    """占位文本"""
    map: Union[dict, List[dict]] = None
    """映射配置"""
    source: Union[str, API] = None
    """API 或 数据映射"""
    valueField: str = "value"
    """2.5.2 map或source为Array<object>时，用来匹配映射的字段名"""
    labelField: str = "label"
    """
    2.5.2 map或source为List[dict]时，用来展示的字段名
    注：配置后映射值无法作为schema组件渲染
    """
    itemSchema: Union[str, SchemaNode] = None
    """
    2.5.2 自定义渲染模板，支持html或schemaNode；
    当映射值是非object时，可使用${item}获取映射值；
    当映射值是object时，可使用映射语法: ${xxx}获取object的值；
    也可使用数据映射语法：${xxx}获取数据域中变量值。
    """


class Progress(AmisNode):
    """进度条"""
    type: str = "progress"
    """指定为 progress 渲染器 如果在 Form 中用作静态展示，为"static-progress" """
    mode: Literal['line', 'circle', 'dashboard'] = "line"
    """进度条的类型"""
    className: str = None
    """外层 CSS 类名"""
    value: int = None
    """	进度值"""
    placeholder: str = "-"
    """占位文本"""
    showLabel: bool = True
    """是否展示进度文本"""
    striped: bool = False
    """背景是否显示条纹"""
    animated: bool = False
    """	type 为 line，可支持动画"""
    map: Union[str, List[Union[str, dict]]] = ['bg-danger', 'bg-warning', 'bg-info', 'bg-success', 'bg-success']
    """进度颜色映射"""
    threshold: Union[dict, List[dict]] = None
    """阈值（刻度）"""
    showThresholdText: bool = False
    """是否显示阈值（刻度）数值"""
    valueTpl: str = "${value}%"
    """自定义格式化内容"""
    strokeWidth: int = 10
    """进度条线宽度"""
    gapDegree: int = 75
    """仪表盘缺角角度，可取值 0 ~ 295"""
    gapPosition: Literal['top', 'bottom', 'left', 'right'] = "bottom"
    """仪表盘进度条缺口位置"""


class Steps(AmisNode):
    """步骤条"""

    class Step(AmisNode):
        """步骤"""
        title: Union[str, SchemaNode] = None
        """标题"""
        subTitle: Union[str, SchemaNode] = None
        """子标题"""
        description: Union[str, SchemaNode] = None
        """详细描述"""
        icon: str = None
        """icon 名，支持 fontawesome v4 或使用 url"""
        value: str = None
        """value"""
        className: str = None
        """自定义类名"""

    type: str = 'steps'
    """指定为 steps 渲染器"""
    steps: List[Step] = None
    """数组，配置步骤信息"""
    source: API = None
    """选项组源，可通过数据映射获取当前数据域变量、或者配置 API 对象"""
    name: str = None
    """关联上下文变量"""
    value: Union[str, int] = "-"
    """	设置默认值，注意不支持表达式"""
    status: Union[
        Literal['wait', 'process', 'finish', 'error'], Dict[str, Literal['wait', 'process', 'finish', 'error']]] = None
    """状态"""
    className: str = None
    """自定义类名"""
    mode: Literal['horizontal', 'vertical', "simple"] = 'horizontal'
    """指定步骤条模式。目前支持水平（horizontal）、竖直（vertical）和简单（simple）模式"""
    labelPlacement: Literal['horizontal', 'vertical'] = "horizontal"
    """指定标签放置位置，默认水平放图标右侧，可选 (vertical) 放图标下方"""
    progressDot: bool = False
    """	点状步骤条"""


class Property(AmisNode):
    """属性表"""

    class Item(AmisNode):
        label: Template = None
        """属性名"""
        content: Template = None
        """属性值"""
        span: int = None
        """属性值跨几列"""
        visibleOn: Expression = None
        """显示表达式"""
        hiddenOn: Expression = None
        """隐藏表达式"""

    type: str = 'property'
    """指定为 property 渲染器"""
    className: str = None
    """外层 dom 的类名"""
    style: dict = None
    """外层 dom 的样式"""
    labelStyle: dict = None
    """属性名的样式"""
    contentStyle: dict = None
    """属性值的样式"""
    column: int = 3
    """每行几列"""
    mode: Literal["table", "simple"] = "table"
    """显示模式，目前只有 'table' 和 'simple'"""
    separator: str = ","
    """'simple' 模式下属性名和值之间的分隔符"""
    source: Template = None
    """数据源"""
    title: str = None
    """标题"""
    items: List[Item] = None
    """数据项"""


class QRCode(AmisNode):
    """二维码"""

    class ImageSettings(AmisNode):
        """QRCode 图片配置"""
        src: str = None
        """图片链接地址"""
        width: float = 12.8
        """图片宽度"""
        height: float = 12.8
        """图片高度"""
        x: float = None
        """图片水平方向偏移量"""
        y: float = None
        """图片垂直方向偏移量"""
        excavate: bool = False
        """图片是否挖孔嵌入"""

    type: str = "qr-code"
    """指定为 QRCode 渲染器"""
    value: Template = "https://www.baidu.com"
    """扫描二维码后显示的文本，如果要显示某个页面请输入完整 url（"http://..."或"https://..."开头），支持使用 模板"""
    className: str = None
    """外层 Dom 的类名"""
    qrcodeClassName: str = None
    """二维码 SVG 的类名"""
    codeSize: int = 128
    """二维码的宽高大小"""
    backgroundColor: str = "#FFF"
    """二维码背景色"""
    foregroundColor: str = "#000"
    """二维码前景色"""
    level: Literal['L', 'M', 'Q', 'H'] = "L"
    """二维码复杂级别，有（'L' 'M' 'Q' 'H'）四种"""
    imageSettings: ImageSettings = None
    """QRCode 图片配置"""


class BarCode(AmisNode):
    """条形码"""
    type: str = 'barcode'
    """指定为 barcode 渲染器"""
    className: str = None
    """外层 CSS 类名"""
    value: str = None
    """	显示的颜色值"""
    name: str = None
    """在其他组件中，时，用作变量映射"""


class Tag(AmisNode):
    """标签"""
    type: str = 'tag'
    """指定为 tag 渲染器"""
    displayMode: Literal['normal', 'rounded', 'status'] = "normal"
    """展现模式"""
    color: str = None
    """颜色主题，提供默认主题，并支持自定义颜色值"""
    label: str = "-"
    """标签内容"""
    icon: Icon = "fa fa-dot"
    """status 模式下的前置图标"""
    className: str = None
    """自定义 CSS 样式类名"""
    style: dict = {}
    """自定义样式（行内样式），优先级最高"""
    closable: bool = False
    """是否展示关闭按钮"""


class Video(AmisNode):
    """视频"""
    type: str = "video"
    """指定为 video 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    src: str = None
    """视频地址"""
    isLive: bool = False
    """ 是否为直播，视频为直播时需要添加上，支持flv和hls格式"""
    videoType: str = None
    """指定直播视频格式"""
    poster: str = None
    """视频封面地址"""
    muted: bool = None
    """是否静音"""
    loop: bool = None
    """是否循环播放"""
    autoPlay: bool = None
    """是否自动播放"""
    rates: List[float] = None
    """倍数，格式为[1.0, 1.5, 2.0]"""
    frames: dict = None
    """key 是时刻信息，value 可以可以为空，可有设置为图片地址，请看上方示例"""
    jumpBufferDuration: Union[bool, int, str] = None
    """点击帧的时候默认是跳转到对应的时刻，如果想提前 3 秒钟，可以设置这个值为 3"""
    stopOnNextFrame: bool = None
    """到了下一帧默认是接着播放，配置这个会自动停止"""


class Timeline(AmisNode):
    """时间轴"""

    class Item(AmisNode):
        """节点配置"""
        time: str = None
        """节点时间"""
        title: Union[str, SchemaNode] = None
        """节点标题"""
        detail: str = None
        """节点详细描述（折叠）"""
        detailCollapsedText: str = "展开"
        """详细内容折叠时按钮文案"""
        detailExpandedText: str = "折叠"
        """详细内容展开时按钮文案"""
        color: Union[str, LevelEnum] = "#DADBDD"
        """时间轴节点颜色"""
        icon: str = None
        """icon 名，支持 fontawesome v4 或使用 url（优先级高于 color）"""

    type: str = "timeline"
    """指定为 timeline 渲染器"""
    items: List[Item] = None
    """配置节点数据"""
    source: API = None
    """数据源，可通过数据映射获取当前数据域变量、或者配置 API 对象"""
    mode: Literal["left", "right", "alternate"] = "right"
    """指定文字相对于时间轴的位置，仅 direction=vertical 时支持"""
    direction: Literal["vertical", "horizontal"] = "vertical"
    """时间轴方向"""
    reverse: bool = False
    """根据时间倒序显示"""


class Alert(AmisNode):
    """提示"""
    type: str = "alert"
    """指定为 alert 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    level: str = "info"
    """级别，可以是：info、success、warning 或者 danger"""
    body: SchemaNode = None
    """显示内容"""
    showCloseButton: bool = False
    """是否显示关闭按钮"""
    closeButtonClassName: str = None
    """关闭按钮的 CSS 类名"""
    showIcon: bool = False
    """是否显示 icon"""
    icon: str = None
    """自定义 icon"""
    iconClassName: str = None
    """icon 的 CSS 类名"""


class Dialog(AmisNode):
    """对话框"""
    type: str = "dialog"
    """指定为 Dialog 渲染器"""
    title: SchemaNode = None
    """弹出层标题"""
    body: SchemaNode = None
    """往 Dialog 内容区加内容"""
    size: Union[str, SizeEnum] = None
    """指定 dialog 大小，支持: xs、sm、md、lg、xl、full"""
    bodyClassName: str = "modal-body"
    """Dialog body 区域的样式类名"""
    closeOnEsc: bool = False
    """是否支持按 Esc 关闭 Dialog"""
    showCloseButton: bool = True
    """是否显示右上角的关闭按钮"""
    showErrorMsg: bool = True
    """是否在弹框左下角显示报错信息"""
    showLoading: bool = True
    """是否在弹框左下角显示 loading 动画"""
    disabled: bool = False
    """如果设置此属性，则该 Dialog 只读没有提交操作。"""
    actions: List[Action] = None
    """如果想不显示底部按钮，可以配置：[]  "【确认】和【取消】"""
    data: dict = None
    """支持数据映射，如果不设定将默认将触发按钮的上下文中继承数据。"""


class Drawer(AmisNode):
    """抽屉"""
    type: str = "drawer"
    """"drawer" 指定为 Drawer 渲染器"""
    title: SchemaNode = None
    """弹出层标题"""
    body: SchemaNode = None
    """往 Drawer 内容区加内容"""
    size: Union[str, SizeEnum] = None
    """指定 Drawer 大小，支持: xs、sm、md、lg"""
    position: Literal["left", "right", "top", "bottom"] = None
    """位置"""
    className: str = None
    """Drawer 最外层容器的样式类名"""
    headerClassName: str = None
    """Drawer 头部 区域的样式类名"""
    bodyClassName: str = "modal-body"
    """Drawer body 区域的样式类名"""
    footerClassName: str = None
    """Drawer 页脚 区域的样式类名"""
    closeOnEsc: bool = False
    """是否支持按 Esc 关闭 Drawer"""
    closeOnOutside: bool = False
    """点击内容区外是否关闭 Drawer"""
    overlay: bool = True
    """是否显示蒙层"""
    resizable: bool = False
    """是否可通过拖拽改变 Drawer 大小"""
    width: Union[int, str] = "500px"
    """容器的宽度，在 position 为 left 或 right 时生效"""
    height: Union[str, int] = "500px"
    """容器的高度，在 position 为 top 或 bottom 时生效"""
    actions: List[Action] = None
    """可以不设置，默认只有两个按钮。 "【确认】和【取消】"""
    data: dict = None
    """支持 数据映射，如果不设定将默认将触发按钮的上下文中继承数据。"""


class Iframe(AmisNode):
    """Iframe"""
    type: str = "iframe"
    """指定为 iFrame 渲染器"""
    className: str = None
    """iFrame 的类名"""
    frameBorder: list = None
    """frameBorder"""
    style: dict = None
    """样式对象"""
    src: str = None
    """iframe 地址"""
    allow: str = None
    """allow配置"""
    sandbox: str = None
    """sandbox 配置"""
    referrerpolicy: str = None
    """referrerpolicy 配置"""
    height: Union[int, str] = "100%"
    """iframe 高度"""
    width: Union[int, str] = "100%"
    """iframe 宽度"""


class Spinner(AmisNode):
    """加载中"""
    type: str = "spinner"
    """指定为 spinner 渲染器"""
    show: bool = True
    """是否显示 spinner 组件"""
    showOn: Union[Expression, bool] = True
    """是否显示 spinner 组件的条件"""
    className: str = None
    """spinner 图标父级标签的自定义 class"""
    spinnerClassName: str = None
    """组件中 icon 所在标签的自定义 class"""
    spinnerWrapClassName: str = None
    """作为容器使用时组件最外层标签的自定义 class"""
    size: Literal["sm", "lg"] = None
    """组件大小 sm lg"""
    icon: str = None
    """组件图标，可以是amis内置图标，也可以是字体图标或者网络图片链接，作为 ui 库使用时也可以是自定义组件"""
    tip: str = None
    """配置组件文案，例如加载中..."""
    tipPlacement: Literal["top", "right", "bottom", "left"] = "bottom"
    """配置组件 tip 相对于 icon 的位置"""
    delay: int = 0
    """配置组件显示延迟的时间（毫秒）"""
    overlay: bool = True
    """配置组件显示 spinner 时是否显示遮罩层"""
    body: SchemaNode = None
    """作为容器使用时，被包裹的内容"""
    loadingConfig: dict = None
    """
    为 Spinner 指定挂载的容器, root 是一个 selector，
    在拥有Spinner的组件上都可以通过传递loadingConfig改变Spinner的挂载位置，
    开启后，会强制开启属性overlay=true，并且icon会失效
    """


class TableCRUD(CRUD, Table):
    """表格CRUD"""
    pass


class CardsCRUD(CRUD, Cards):
    """卡片CRUD"""
    columnsCount: int = 4
    """每行显示的卡片数量"""


class Avatar(AmisNode):
    """头像"""
    type: str = "avatar"
    """指定为 avatar 渲染器"""
    className: str = None
    """外层 dom 的类名"""
    style: dict = None
    """外层 dom 的样式"""
    fit: Literal['contain', 'cover', 'fill', 'none', 'scale-down'] = "cover"
    """ 图片缩放类型"""
    src: str = None
    """图片地址"""
    text: str = None
    """文字"""
    icon: str = "fa fa-user"
    """图标"""
    shape: Literal['circle', 'square', 'rounded'] = "circle"
    """形状，有三种 'circle' （圆形）、'square'（正方形）、'rounded'（圆角）"""
    size: Union[int, Literal['default', 'normal', 'small']] = "default"
    """'default' | 'normal' | 'small'三种字符串类型代表不同大小（分别是48、40、32），也可以直接数字表示"""
    gap: int = 4
    """控制字符类型距离左右两侧边界单位像素"""
    alt: str = None
    """图像无法显示时的替代文本"""
    draggable: bool = None
    """图片是否允许拖动"""
    crossOrigin: Literal['anonymous', 'use-credentials', ''] = None
    """图片的 CORS 属性设置"""
    onError: str = None
    """
    图片加载失败的字符串，这个字符串是一个New Function内部执行的字符串，
    参数是event（使用event.nativeEvent获取原生dom事件），这个字符串需要返回boolean值。
    设置 "return ture;" 会在图片加载失败后，使用 text 或者 icon 代表的信息来进行替换。
    目前图片加载失败默认是不进行置换。注意：图片加载失败，不包括$获取数据为空情况
    """


class Toast(AmisNode):
    """轻提示"""

    class ToastItem(AmisNode):
        """提示内容"""
        title: Union[str, SchemaNode] = None
        """标题"""
        body: Union[str, SchemaNode] = None
        """内容"""
        level: Literal['info', 'success', 'error', 'warning'] = "info"
        """展示图标，可选'info'、'success'、'error'、'warning'"""
        position: Literal[
            "top-right", "top-center", "top-left", "bottom-center", "bottom-left", "bottom-right", "center"] = "top-center"
        """提示显示位置（移动端为center）: top-right|top-center|top-left|bottom-center|bottom-left|bottom-right|center"""
        closeButton: bool = False
        """是否展示关闭按钮"""
        showIcon: bool = True
        """是否展示图标"""
        timeout: int = 5000
        """持续时间（error类型为6000，移动端为3000）"""

    actionType: str = 'toast'
    """点击提示内容"""
    items: List[ToastItem] = []
    position: Literal[
        "top-right", "top-center", "top-left", "bottom-center", "bottom-left", "bottom-right", "center"] = "top-center"
    """提示显示位置（移动端为center）: top-right|top-center|top-left|bottom-center|bottom-left|bottom-right|center"""
    closeButton: bool = False
    """是否展示关闭按钮"""
    showIcon: bool = True
    """是否展示图标"""
    timeout: int = 5000
    """持续时间（error类型为6000，移动端为3000）"""


class Audio(AmisNode):
    """音频"""
    type: str = "audio"
    """指定为 audio 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    inline: bool = True
    """是否是内联模式"""
    src: str = None
    """音频地址"""
    loop: bool = False
    """是否循环播放"""
    autoPlay: bool = False
    """是否自动播放"""
    rates: List[float] = None
    """可配置音频播放倍速如：[1.0, 1.5, 2.0]"""
    controls: List[Literal['rates', 'play', 'time', 'process', 'volume']] = None
    """内部模块定制化"""


class SearchBox(AmisNode):
    """搜索框"""
    type: str = "search-box"
    """指定为 search-box 渲染器"""
    className: str = None
    """外层 CSS 类名"""
    mini: bool = None
    """是否为 mini 模式"""
    searchImediately: bool = None
    """	是否立即搜索"""
    clearAndSubmit: bool = None
    """清空搜索框内容后立即执行搜索 	"""


class Sparkline(AmisNode):
    """走势图"""
    type: str = "sparkline"
    """指定为 sparkline渲染器"""
    name: str = None
    """关联的变量"""
    width: int = None
    """宽度"""
    height: int = None
    """高度"""
    placeholder: str = None
    """数据为空时显示的内容"""


class Status(AmisNode):
    """状态"""

    class Source(AmisNode):
        """数据源"""
        label: Union[Literal[False], Template,str] = None
        """映射文本"""
        icon: str = None
        """映射图标"""
        color: str = None
        """映射状态颜色"""
        className: str = None
        """映射状态的 独立 CSS 类名"""

    type: str = "status"
    """指定为 Status 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    placeholder: str = "-"
    """占位文本"""
    map: dict = None
    """映射图标"""
    labelMap: dict = None
    """映射文本"""
    source: Union[Source, str, dict] = None
    """自定义映射状态，支持数据映射"""


class Tasks(AmisNode):
    """任务操作集合"""

    class Item(AmisNode):
        label: Union[Literal[False], Template,str] = None
        """任务名称"""
        key: str = None
        """任务键值，请唯一区分"""
        remark: str = None
        """当前任务状态，支持 html"""
        status: str = None
        """
        任务状态： 0: 初始状态，不可操作。1: 就绪，可操作状态。2: 进行中，还没有结束。
        3：有错误，不可重试。4: 已正常结束。5：有错误，且可以重试。
        """

    type: str = "tasks"
    """指定为 Tasks 渲染器"""
    className: str = None
    """外层 Dom 的类名"""
    tableClassName: str = None
    """table Dom 的类名"""
    items: List[Item] = None
    """任务列表"""
    checkApi: API = None
    """返回任务列表，返回的数据请参考 items。"""
    submitApi: API = None
    """提交任务使用的 API"""
    reSubmitApi: API = None
    """如果任务失败，且可以重试，提交的时候会使用此 API"""
    interval: int = 3000
    """当有任务进行中，会每隔一段时间再次检测，而时间间隔就是通过此项配置，默认 3s。"""
    taskNameLabel: str = "任务名称"
    """任务名称列说明"""
    operationLabel: str = "操作"
    """操作列说明"""
    statusLabel: str = "状态"
    """状态列说明"""
    remarkLabel: str = "备注"
    """备注列说明"""
    btnText: str = "上线"
    """操作按钮文字"""
    retryBtnText: str = "重试"
    """重试操作按钮文字"""
    btnClassName: str = "btn-sm btn-default"
    """配置容器按钮 className"""
    retryBtnClassName: str = "btn-sm btn-danger"
    """配置容器重试按钮 className"""
    statusLabelMap: List[str] = ["label-warning", "label-info", "label-success", "label-danger", "label-default",
                                 "label-danger"]
    """状态显示对应的类名配置"""
    statusTextMap: List[str] = ["未开始", "就绪", "进行中", "出错", "已完成", "出错"]
    """"状态显示对应的文字显示配置"""


class Wizard(AmisNode):
    """向导"""

    class Step(AmisNode):
        """步骤"""
        title: str = None
        """步骤标题"""
        mode: str = None
        """展示默认，跟 Form 中的模式一样，选择： normal、horizontal或者inline。"""
        horizontal: Horizontal = None
        """当为水平模式时，用来控制左右占比"""
        api: API = None
        """当前步骤保存接口，可以不配置。"""
        initApi: API = None
        """当前步骤数据初始化接口。"""
        initFetch: bool = None
        """当前步骤数据初始化接口是否初始拉取。"""
        initFetchOn: Expression = None
        """当前步骤数据初始化接口是否初始拉取，用表达式来决定。"""
        body: List[FormItem] = None
        """当前步骤的表单项集合，请参考 FormItem。"""

    type: str = "wizard"
    """指定为 Wizard 组件"""
    mode: Literal["horizontal", "vertical"] = "horizontal"
    """ 展示模式，选择：horizontal 或者 vertical"""
    api: API = None
    """最后一步保存的接口。"""
    initApi: API = None
    """初始化数据接口"""
    initFetch: API = None
    """初始是否拉取数据。"""
    initFetchOn: Expression = None
    """初始是否拉取数据，通过表达式来配置"""
    actionPrevLabel: str = "上一步"
    """上一步按钮文本"""
    actionNextLabel: str = "下一步"
    """下一步按钮文本"""
    actionNextSaveLabel: str = "保存并下一步"
    """保存并下一步按钮文本"""
    actionFinishLabel: str = "完成"
    """完成按钮文本"""
    className: str = None
    """外层 CSS 类名"""
    actionClassName: str = "btn-sm btn-default"
    """按钮 CSS 类名"""
    reload: str = None
    """操作完后刷新目标对象。请填写目标组件设置的 name 值，如果填写为 window 则让当前页面整体刷新。"""
    redirect: Template = "3000"
    """操作完后跳转。"""
    target: Union[str, bool] = False
    """
    可以把数据提交给别的组件而不是自己保存。请填写目标组件设置的 name 值，
    如果填写为 window 则把数据同步到地址栏上，同时依赖这些数据的组件会自动重新刷新。
    """
    steps: List[Step] = None
    """数组，配置步骤信息"""
    startStep: int = 1
    """
    起始默认值，从第几步开始。可支持模版，但是只有在组件创建时渲染模版并设置当前步数，在之后组件被刷新时，
    当前 step 不会根据 startStep 改变"""


class WebComponent(AmisNode):
    """Web Component"""
    type: str = 'web-component'
    tag: str = None
    """具体使用的 web-component 标签"""
    props: dict = None
    """标签上的属性"""
    body: SchemaNode = None
    """子节点"""


PageSchema.update_forward_refs()
ActionType.Dialog.update_forward_refs()
ActionType.Drawer.update_forward_refs()
TableCRUD.update_forward_refs()
Form.update_forward_refs()
Tpl.update_forward_refs()
InputText.update_forward_refs()
InputNumber.update_forward_refs()
Picker.update_forward_refs()
