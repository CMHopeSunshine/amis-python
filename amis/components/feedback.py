from typing import List, Literal, Optional, Union

from amis.event import OnEvent
from amis.typing import DictStrAny, Expression

from .feature import Action
from .types import AmisNode, SchemaNode

from pydantic import Field


class Alert(AmisNode):
    """提示

    https://aisuda.bce.baidu.com/amis/zh-CN/components/alert"""

    type: Literal["alert"] = Field(default="alert", init=False)
    """指定为 alert 渲染器"""
    title: Optional[str] = None
    """alert 标题"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    level: Literal["info", "success", "warning", "danger"] = "info"
    """级别，可以是：info、success、warning 或者 danger"""
    body: Optional[SchemaNode] = None
    """显示内容"""
    showCloseButton: bool = False
    """是否显示关闭按钮"""
    closeButtonClassName: Optional[str] = None
    """关闭按钮的 CSS 类名"""
    showIcon: bool = False
    """是否显示 icon"""
    icon: Optional[str] = None
    """自定义 icon"""
    iconClassName: Optional[str] = None
    """icon 的 CSS 类名"""


class Dialog(AmisNode):
    """对话框"""

    type: Literal["dialog"] = Field(default="dialog", init=False)
    """指定为 Dialog 渲染器"""
    title: Optional[SchemaNode] = None
    """弹出层标题"""
    body: Optional[SchemaNode] = None
    """往 Dialog 内容区加内容"""
    size: Optional[Literal["xs", "sm", "md", "lg", "xl", "full"]] = None
    """指定 dialog 大小，支持: xs、sm、md、lg、xl、full"""
    bodyClassName: Optional[str] = None
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
    actions: Optional[List[Action]] = None
    """如果想不显示底部按钮，可以配置：[]  默认为"【确认】和【取消】"""
    data: Optional[DictStrAny] = None
    """支持数据映射，如果不设定将默认将触发按钮的上下文中继承数据。"""
    onEvent: OnEvent[Literal["confirm", "cancel"]] = None


class Drawer(AmisNode):
    """抽屉

    https://aisuda.bce.baidu.com/amis/zh-CN/components/drawer"""

    type: Literal["drawer"] = Field(default="drawer", init=False)
    """"drawer" 指定为 Drawer 渲染器"""
    title: Optional[SchemaNode] = None
    """弹出层标题"""
    body: Optional[SchemaNode] = None
    """往 Drawer 内容区加内容"""
    size: Optional[Literal["xs", "sm", "md", "lg", "xl"]] = None
    """指定 Drawer 大小，支持: xs、sm、md、lg"""
    position: Optional[Literal["left", "right", "top", "bottom"]] = None
    """位置"""
    className: Optional[str] = None
    """Drawer 最外层容器的样式类名"""
    headerClassName: Optional[str] = None
    """Drawer 头部 区域的样式类名"""
    bodyClassName: str = "modal-body"
    """Drawer body 区域的样式类名"""
    footerClassName: Optional[str] = None
    """Drawer 页脚 区域的样式类名"""
    showCloseButton: bool = True
    """是否展示关闭按钮，当值为 false 时，默认开启 closeOnOutside"""
    closeOnEsc: bool = False
    """是否支持按 Esc 关闭 Drawer"""
    closeOnOutside: bool = False
    """点击内容区外是否关闭 Drawer"""
    overlay: bool = True
    """是否显示蒙层"""
    resizable: bool = False
    """是否可通过拖拽改变 Drawer 大小"""
    width: Union[str, int] = "500px"
    """容器的宽度，在 position 为 left 或 right 时生效"""
    height: Union[str, int] = "500px"
    """容器的高度，在 position 为 top 或 bottom 时生效"""
    actions: Optional[List[Action]] = None
    """可以不设置，默认只有两个按钮。 "【确认】和【取消】"""
    data: Optional[DictStrAny] = None
    """支持 数据映射，如果不设定将默认将触发按钮的上下文中继承数据。"""
    onEvent: OnEvent[Literal["confirm", "cancel"]] = None


class Spinner(AmisNode):
    """加载中

    https://aisuda.bce.baidu.com/amis/zh-CN/components/spinner"""

    type: Literal["spinner"] = Field(default="spinner", init=False)
    """指定为 spinner 渲染器"""
    show: bool = True
    """是否显示 spinner 组件"""
    showOn: Union[Expression, bool] = True
    """是否显示 spinner 组件的条件"""
    className: Optional[str] = None
    """spinner 图标父级标签的自定义 class"""
    spinnerClassName: Optional[str] = None
    """组件中 icon 所在标签的自定义 class"""
    spinnerWrapClassName: Optional[str] = None
    """作为容器使用时组件最外层标签的自定义 class"""
    size: Optional[Literal["sm", "lg"]] = None
    """组件大小 sm lg"""
    icon: Optional[str] = None
    """组件图标，可以是amis内置图标，也可以是字体图标或者网络图片链接，作为 ui 库使用时也可以是自定义组件"""
    tip: Optional[str] = None
    """配置组件文案，例如加载中..."""
    tipPlacement: Literal["top", "right", "bottom", "left"] = "bottom"
    """配置组件 tip 相对于 icon 的位置"""
    delay: int = 0
    """配置组件显示延迟的时间（毫秒）"""
    overlay: bool = True
    """配置组件显示 spinner 时是否显示遮罩层"""
    body: Optional[SchemaNode] = None
    """作为容器使用时，被包裹的内容"""
    loadingConfig: Optional[DictStrAny] = None
    """
    为 Spinner 指定挂载的容器, root 是一个 selector，
    在拥有Spinner的组件上都可以通过传递loadingConfig改变Spinner的挂载位置，
    开启后，会强制开启属性overlay=true，并且icon会失效
    """


class Toast(AmisNode):
    """轻提示"""

    class Item(AmisNode):
        """提示内容"""

        title: Optional[Union[str, SchemaNode]] = None
        """标题"""
        body: Optional[Union[str, SchemaNode]] = None
        """内容"""
        level: Literal["info", "success", "error", "warning"] = "info"
        """展示图标，可选'info'、'success'、'error'、'warning'"""
        position: Literal[
            "top-right",
            "top-center",
            "top-left",
            "bottom-center",
            "bottom-left",
            "bottom-right",
            "center",
        ] = "top-center"
        """提示显示位置（移动端为center）:
        top-right|top-center|top-left|bottom-center|bottom-left|bottom-right|center"""
        closeButton: bool = False
        """是否展示关闭按钮"""
        showIcon: bool = True
        """是否展示图标"""
        timeout: Optional[int] = None
        """持续时间（error类型为6000，移动端为3000）"""
        allowHtml: bool = True
        """是否会被当作 HTML 片段处理"""

    type: Literal["button"] = Field(default="button", init=False)
    actionType: Literal["toast"] = Field(default="toast", init=False)
    """指定为 toast 渲染器"""
    items: List[Item] = []
    "轻提示内容"
    position: Literal[
        "top-right",
        "top-center",
        "top-left",
        "bottom-center",
        "bottom-left",
        "bottom-right",
        "center",
    ] = "top-center"
    """提示显示位置（移动端为center）: top-right|top-center|top-left|bottom-center|bottom-left|bottom-right|center"""
    closeButton: bool = False
    """是否展示关闭按钮"""
    showIcon: bool = True
    """是否展示图标"""
    timeout: Optional[int] = None
    """持续时间（error类型为6000，移动端为3000）"""


__all__ = [
    "Alert",
    "Dialog",
    "Drawer",
    "Spinner",
    "Toast",
]
