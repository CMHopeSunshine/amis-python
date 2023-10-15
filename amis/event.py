from typing import Any, Dict, List, Literal, Optional, TYPE_CHECKING, TypeVar, Union
from typing_extensions import NotRequired, TypedDict

from amis.typing import DictStrAny

from .base import BaseAmisModel, Expression

from pydantic import Field

if TYPE_CHECKING:
    from .components import API, Dialog, Drawer, Template

T = TypeVar("T", bound=str)


class EventAction(BaseAmisModel):
    actionType: str
    """动作名称"""
    args: Optional[Dict[str, Any]] = None
    """动作参数{key:value}，支持数据映射"""
    data: Optional[Dict[str, Any]] = None
    """追加数据{key:value}，支持数据映射，如果是触发其他组件
    的动作，则该数据会传递给目标组件，> 2.3.2 及以上版本"""
    dataMergeMode: Literal["merge", "override"] = "merge"
    """当配置了 data 的时候，可以控制数据追加方式，支持合并(merge)
    和覆盖(override)两种模式，> 2.3.2 及以上版本"""
    preventDefault: Union[bool, Expression] = False
    """阻止事件默认行为，> 1.10.0 及以上版本支持表达式，
    > 2.9.0 及以上版本支持ConditionBuilder"""
    stopPropagation: Union[bool, Expression] = False
    """停止后续动作执行，> 1.10.0 及以上版本支持表达式，
    > 2.9.0 及以上版本支持ConditionBuilder"""
    expression: Optional[Union[bool, Expression]] = None
    """执行条件，不设置表示默认执行，> 1.10.0 及以上版本支持表达式，
    > 2.9.0 及以上版本支持ConditionBuilder"""
    outputVar: Optional[str] = None
    """输出数据变量名"""


class AjaxAction(EventAction):
    """http请求"""

    actionType: Literal["ajax"] = Field(default="ajax", init=False)
    api: "API"
    """接口配置"""
    options: Optional[DictStrAny] = None
    """其他配置"""
    data: Optional[DictStrAny] = None
    """数据"""
    outputVar: Optional[str] = None
    """请求响应结果缓存在${event.data.responseResult}或${event.data.{outputVar}}"""


class DialogAction(EventAction):
    """打开弹窗（模态）"""

    actionType: Literal["dialog"] = Field(default="dialog", init=False)
    dialog: Union[str, "Dialog"]


class CloseDialogAction(EventAction):
    """关闭弹窗（模态）"""

    actionType: Literal["closeDialog"] = Field(default="closeDialog", init=False)
    componentId: str


class DrawerAction(EventAction):
    """打开抽屉（模态）"""

    actionType: Literal["drawer"] = Field(default="drawer", init=False)
    drawer: Union[str, "Drawer"]


class CloseDrawerAction(EventAction):
    """关闭抽屉（模态）"""

    actionType: Literal["closeDrawer"] = Field(default="closeDrawer", init=False)
    componentId: str


class CommonDialog(TypedDict):
    title: NotRequired[str]
    msg: NotRequired[str]


class ConfirmDialogAction(EventAction):
    """打开确认弹窗"""

    actionType: Literal["confirmDialog"] = Field(default="confirmDialog", init=False)
    dialog: Union[CommonDialog, "Dialog"]


class AlertAction(EventAction):
    actionType: Literal["alert"] = Field(default="alert", init=False)
    args: CommonDialog


class UrlAction(EventAction):
    class UrlArgs(TypedDict):
        url: str
        blank: NotRequired[bool]
        params: NotRequired[DictStrAny]

    actionType: Literal["url"] = Field(default="url", init=False)
    args: Union[UrlArgs, DictStrAny]


class LinkAction(EventAction):
    class LinkArgs(TypedDict):
        link: str
        params: NotRequired[DictStrAny]

    actionType: Literal["link"] = Field(default="link", init=False)
    args: LinkArgs


class GoBackAction(EventAction):
    actionType: Literal["goBack"] = Field(default="goBack", init=False)


class GoPageAction(EventAction):
    class GoPageArgs(TypedDict):
        delta: int

    actionType: Literal["goPage"] = Field(default="goPage", init=False)
    args: Optional[GoPageArgs] = None


class RefreshAction(EventAction):
    actionType: Literal["refresh"] = Field(default="refresh", init=False)


class ToastAction(EventAction):
    class ToastArgs(TypedDict):
        msgType: NotRequired[Literal["info", "success", "error", "warning"]]
        msg: str
        position: NotRequired[
            Literal[
                "top-right",
                "top-center",
                "top-left",
                "bottom-center",
                "bottom-left",
                "bottom-right",
                "center",
            ]
        ]
        closeButton: NotRequired[bool]
        showIcon: NotRequired[bool]
        timeout: NotRequired[int]

    actionType: Literal["toast"] = Field(default="toast", init=False)
    args: ToastArgs


class CopyAction(EventAction):
    class CopyArgs(TypedDict):
        copyFormat: NotRequired[str]
        content: "Template"

    actionType: Literal["copy"] = Field(default="copy", init=False)
    args: CopyArgs


class EmailAction(EventAction):
    class EmailArgs(TypedDict):
        to: NotRequired[str]
        """收件人邮箱"""
        cc: NotRequired[str]
        """抄送邮箱"""
        bcc: NotRequired[str]
        """匿名抄送邮箱"""
        subject: NotRequired[str]
        """邮件主题"""
        body: NotRequired[str]
        """邮件正文"""

    actionType: Literal["email"] = Field(default="email", init=False)
    args: EmailArgs


class ReloadAction(EventAction):
    actionType: Literal["reload"] = Field(default="reload", init=False)
    componentId: str
    resetPage: bool = True
    data: Optional[DictStrAny] = None


class ShowAction(EventAction):
    actionType: Literal["show"] = Field(default="show", init=False)
    componentId: str


class HiddenAction(EventAction):
    actionType: Literal["hidden"] = Field(default="hidden", init=False)
    componentId: str


class EnableAction(EventAction):
    actionType: Literal["enabled"] = Field(default="enabled", init=False)
    componentId: str


class DisableAction(EventAction):
    actionType: Literal["disabled"] = Field(default="disabled", init=False)
    componentId: str


class StaticAction(EventAction):
    actionType: Literal["static"] = Field(default="static", init=False)
    componentId: str


class NoStaticAction(EventAction):
    actionType: Literal["nostatic"] = Field(default="nostatic", init=False)
    componentId: str


class SetValueAction(EventAction):
    class SetValueArgs(TypedDict):
        value: Any
        """值"""
        index: NotRequired[int]
        """当目标组件是combo时，可以指定更新的数据索引"""

    actionType: Literal["setValue"] = Field(default="setValue", init=False)
    args: SetValueArgs
    componentId: Optional[str] = None
    """指定赋值的目标组件 id"""
    componentName: Optional[str] = None
    """指定赋值的目标组件 name"""


class CustomAction(EventAction):
    """自定义 JS"""

    actionType: Literal["custom"] = Field(default="custom", init=False)
    script: str
    """自定义 JS 脚本代码，代码内可以通过调用doAction执行任何动作 ，通过事件对象event可以实现事件动作干预"""


class BroadcastAction(EventAction):
    class Args(TypedDict):
        eventName: str
        """广播动作对应的自定义事件名称，用于广播事件的监听"""

    actionType: Literal["broadcast"] = Field(default="broadcast", init=False)
    args: Args
    weight: int = 0
    """可以通过配置动作执行优先级来控制所有监听者的动作执行顺序"""
    data: Optional[DictStrAny] = None


class LoopAction(EventAction):
    class LoopArgs(TypedDict):
        loopName: str

    actionType: Literal["loop"] = Field(default="loop", init=False)
    args: LoopArgs
    children: List[EventAction] = []


class BreakAction(EventAction):
    actionType: Literal["break"] = Field(default="break", init=False)


class ContinueAction(EventAction):
    actionType: Literal["continue"] = Field(default="continue", init=False)


class SwitchAction(EventAction):
    actionType: Literal["switch"] = Field(default="switch", init=False)
    children: List[EventAction] = []


class ParallelAction(EventAction):
    actionType: Literal["parallel"] = Field(default="parallel", init=False)
    children: List[EventAction] = []


class ResetAction(EventAction):
    """重置，适用于部分数据输入组件"""

    actionType: Literal["reset"] = Field(default="reset", init=False)
    componentId: str


class ClearAction(EventAction):
    """清空，适用于部分数据输入组件"""

    actionType: Literal["clear"] = Field(default="clear", init=False)
    componentId: str


class FocusAction(EventAction):
    """聚焦，用于编辑器系列组件"""

    actionType: Literal["focus"] = Field(default="focus", init=False)


class SelectAllAction(EventAction):
    """全选，用于穿梭器和部分数据展示组件"""

    actionType: Literal["selectAll"] = Field(default="selectAll", init=False)
    componentId: str


class ClearAllAction(EventAction):
    """全选，用于部分数据展示组件"""

    actionType: Literal["clearAll"] = Field(default="clearAll", init=False)
    componentId: str


class ConfirmAction(EventAction):
    """确认，用于对话框和抽屉组件"""

    actionType: Literal["confirm"] = Field(default="confirm", init=False)
    componentId: str


class CancelAction(EventAction):
    """取消，用于对话框和抽屉组件"""

    actionType: Literal["cancel"] = Field(default="cancel", init=False)
    componentId: str


class NextAction(EventAction):
    """下一步，用于向导和轮播图等组件"""

    actionType: Literal["next"] = Field(default="next", init=False)


class PrevAction(EventAction):
    """上一步，用于向导和轮播图等组件"""

    actionType: Literal["prev"] = Field(default="prev", init=False)


class Event(TypedDict):
    actions: List[EventAction]
    """动作列表"""
    weight: NotRequired[int]
    """仅在少数组件有用，未知作用"""


OnEvent = Optional[Dict[T, Event]]


__all__ = [
    "EventAction",
    "AjaxAction",
    "DialogAction",
    "CloseDialogAction",
    "DrawerAction",
    "CloseDrawerAction",
    "ConfirmDialogAction",
    "AlertAction",
    "UrlAction",
    "LinkAction",
    "GoBackAction",
    "GoPageAction",
    "RefreshAction",
    "ToastAction",
    "CopyAction",
    "EmailAction",
    "ReloadAction",
    "ShowAction",
    "HiddenAction",
    "EnableAction",
    "DisableAction",
    "StaticAction",
    "NoStaticAction",
    "SetValueAction",
    "CustomAction",
    "BroadcastAction",
    "LoopAction",
    "BreakAction",
    "ContinueAction",
    "SwitchAction",
    "ParallelAction",
    "ResetAction",
    "ClearAction",
    "FocusAction",
    "SelectAllAction",
    "ClearAllAction",
    "ConfirmAction",
    "CancelAction",
    "NextAction",
    "PrevAction",
    "Event",
]
