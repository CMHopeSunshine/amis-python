from typing import List, Literal, Optional, Tuple, Union

from amis.event import EventAction, OnEvent
from amis.typing import DictStrAny, Expression

from .data_input import FormItem
from .feature import Button
from .types import AmisNode, API, Horizontal, SchemaNode, Template

from pydantic import Field


class Avatar(AmisNode):
    """头像"""

    type: Literal["avatar"] = Field(default="avatar", init=False)
    """指定为 avatar 渲染器"""
    className: Optional[str] = None
    """外层 dom 的类名"""
    style: Optional[DictStrAny] = None
    """外层 dom 的样式"""
    fit: Literal["contain", "cover", "fill", "none", "scale-down"] = "cover"
    """图片缩放类型"""
    src: Optional[str] = None
    """图片地址"""
    text: Optional[str] = None
    """文字"""
    icon: Optional[str] = None
    """图标"""
    shape: Literal["circle", "square", "rounded"] = "circle"
    """形状，有三种 'circle' （圆形）、'square'（正方形）、'rounded'（圆角）"""
    size: Literal["default", "normal", "small"] = "default"
    """'default' | 'normal' | 'small'三种字符串类型代表不同大小（分别是48、40、32）"""
    gap: int = 4
    """控制字符类型距离左右两侧边界单位像素"""
    alt: Optional[str] = None
    """图像无法显示时的替代文本"""
    draggable: Optional[bool] = None
    """图片是否允许拖动"""
    crossOrigin: Optional[Literal["anonymous", "use-credentials", ""]] = None
    """图片的 CORS 属性设置"""
    onError: Optional[str] = None
    """
    图片加载失败的字符串，这个字符串是一个New Function内部执行的字符串，
    参数是event（使用event.nativeEvent获取原生dom事件），这个字符串需要返回boolean值。
    设置 "return ture;" 会在图片加载失败后，使用 text 或者 icon 代表的信息来进行替换。
    目前图片加载失败默认是不进行置换。注意：图片加载失败，不包括$获取数据为空情况
    """
    badge: Optional["Badge"] = None


class Audio(AmisNode):
    """音频"""

    type: Literal["audio"] = Field(default="audio", init=False)
    """指定为 audio 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    inline: bool = True
    """是否是内联模式"""
    src: Optional[str] = None
    """音频地址"""
    loop: bool = False
    """是否循环播放"""
    autoPlay: bool = False
    """是否自动播放"""
    rates: Optional[List[float]] = None
    """可配置音频播放倍速如：[1.0, 1.5, 2.0]"""
    controls: Optional[List[Literal["rates", "play", "time", "process", "volume"]]] = None
    """内部模块定制化"""


class Tasks(AmisNode):
    """任务操作集合

    https://aisuda.bce.baidu.com/amis/zh-CN/components/tasks"""

    class Item(AmisNode):
        label: Optional[Template] = None
        """任务名称"""
        key: Optional[str] = None
        """任务键值，请唯一区分"""
        remark: Optional[str] = None
        """当前任务状态，支持 html"""
        status: Optional[str] = None
        """
        任务状态： 0: 初始状态，不可操作。1: 就绪，可操作状态。2: 进行中，还没有结束。
        3：有错误，不可重试。4: 已正常结束。5：有错误，且可以重试。
        """

    type: Literal["tasks"] = Field(default="tasks", init=False)
    """指定为 Tasks 渲染器"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    tableClassName: Optional[str] = None
    """table Dom 的类名"""
    items: Optional[List[Item]] = None
    """任务列表"""
    checkApi: Optional[API] = None
    """返回任务列表，返回的数据请参考 items。"""
    submitApi: Optional[API] = None
    """提交任务使用的 API"""
    reSubmitApi: Optional[API] = None
    """如果任务失败，且可以重试，提交的时候会使用此 API"""
    interval: Optional[int] = None
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
    statusLabelMap: List[str] = [
        "label-warning",
        "label-info",
        "label-success",
        "label-danger",
        "label-default",
        "label-danger",
    ]
    """状态显示对应的类名配置"""
    statusTextMap: List[str] = ["未开始", "就绪", "进行中", "出错", "已完成", "出错"]
    """"状态显示对应的文字显示配置"""


class Badge(AmisNode):
    """角标

    可以设置在头像、按钮、链接、模板组件的badge属性中"""

    mode: Literal["dot", "text", "ribbon"] = "dot"
    """角标类型，可以是 dot/text/ribbon"""
    text: Optional[Union[str, int]] = None
    """角标文案，支持字符串和数字，在mode='dot'下设置无效"""
    size: Optional[int] = None
    """角标大小"""
    level: Optional[Literal["info", "success", "warning", "danger"]] = None
    """角标级别, 可以是info/success/warning/danger, 设置之后角标背景颜色不同"""
    overflowCount: int = 99
    """设置封顶的数字值"""
    position: Literal["top-right", "top-left", "bottom-right", "bottom-left"] = "top-right"
    """"角标位置， 可以是top-right/top-left/bottom-right/bottom-left"""
    offset: Tuple[int, int] = (0, 0)
    """角标位置，优先级大于position，当设置了offset后，以postion为top-right为基准进行定位  number[top, left]"""
    className: Optional[str] = None
    """外层 dom 的类名"""
    animation: Optional[bool] = None
    """角标是否显示动画"""
    style: Optional[dict] = None
    """角标的自定义样式"""
    visibleOn: Optional[Expression] = None
    """控制角标的显示隐藏"""


class Wizard(AmisNode):
    """向导"""

    class StepSubmitAction(EventAction):
        """分步提交"""

        actionType: Literal["step-submit"] = Field(default="step-submit", init=False)

    class GotoStepAction(EventAction):
        """定位步骤"""

        actionType: Literal["goto-step"] = Field(default="goto-step", init=False)
        step: int

    class Step(AmisNode):
        """步骤"""

        title: Optional[str] = None
        """步骤标题"""
        mode: Optional[Literal["normal", "horizontal", "inline"]] = None
        """展示默认，跟 Form 中的模式一样，选择： normal、horizontal或者inline。"""
        horizontal: Optional[Horizontal] = None
        """当为水平模式时，用来控制左右占比"""
        api: Optional[API] = None
        """当前步骤保存接口，可以不配置。"""
        initApi: Optional[API] = None
        """当前步骤数据初始化接口。"""
        initFetch: Optional[bool] = None
        """当前步骤数据初始化接口是否初始拉取。"""
        initFetchOn: Optional[Expression] = None
        """当前步骤数据初始化接口是否初始拉取，用表达式来决定。"""
        body: Optional[List[FormItem]] = None
        """当前步骤的表单项集合，请参考 FormItem。"""
        closeDialogOnSubmit: Optional[bool] = None
        """提交的时候是否关闭弹窗。
        当 widzard 里面有且只有一个弹窗的时候，本身提交会触发弹窗关闭，此属性可以关闭此行为"""
        jumpableOn: Optional[str] = None
        """配置是否可跳转的表达式"""
        actions: Optional[List[Button]] = None
        """自定义每一步的操作按钮"""

    type: Literal["wizard"] = Field(default="wizard", init=False)
    """指定为 Wizard 组件"""
    mode: Literal["horizontal", "vertical"] = "horizontal"
    """展示模式，选择：horizontal 或者 vertical"""
    api: Optional[API] = None
    """最后一步保存的接口。"""
    initApi: Optional[API] = None
    """初始化数据接口"""
    initFetch: Optional[API] = None
    """初始是否拉取数据。"""
    initFetchOn: Optional[Expression] = None
    """初始是否拉取数据，通过表达式来配置"""
    actionPrevLabel: str = "上一步"
    """上一步按钮文本"""
    actionNextLabel: str = "下一步"
    """下一步按钮文本"""
    actionNextSaveLabel: str = "保存并下一步"
    """保存并下一步按钮文本"""
    actionFinishLabel: str = "完成"
    """完成按钮文本"""
    className: Optional[str] = None
    """外层 CSS 类名"""
    actionClassName: str = "btn-sm btn-default"
    """按钮 CSS 类名"""
    reload: Optional[str] = None
    """操作完后刷新目标对象。请填写目标组件设置的 name 值，如果填写为 window 则让当前页面整体刷新。"""
    redirect: Template = "3000"
    """操作完后跳转。"""
    target: Union[str, bool] = False
    """
    可以把数据提交给别的组件而不是自己保存。请填写目标组件设置的 name 值，
    如果填写为 window 则把数据同步到地址栏上，同时依赖这些数据的组件会自动重新刷新。
    """
    steps: Optional[List[Step]] = None
    """数组，配置步骤信息"""
    startStep: int = 1
    """
    起始默认值，从第几步开始。可支持模版，但是只有在组件创建时渲染模版并设置当前步数，在之后组件被刷新时，
    当前 step 不会根据 startStep 改变"""
    onEvent: OnEvent[
        Literal[
            "inited",
            "stepChange",
            "change",
            "stepSubmitSucc",
            "stepSubmitFail",
            "finished",
            "submitSucc",
            "submitFail",
        ]
    ] = None


class WebComponent(AmisNode):
    """Web Component"""

    type: Literal["web-component"] = Field(default="web-component", init=False)
    """指定为 web-component 组件"""
    tag: Optional[str] = None
    """具体使用的 web-component 标签"""
    props: Optional[DictStrAny] = None
    """标签上的属性"""
    body: Optional[SchemaNode] = None
    """子节点"""


class AmisRender(AmisNode):
    """amis 渲染器

    https://aisuda.bce.baidu.com/amis/zh-CN/components/amis"""

    type: Literal["amis"] = Field(default="amis", init=False)
    """指定为 amis 渲染器"""
    name: Optional[str] = None
    """绑定上下文变量名"""
    props: Optional[DictStrAny] = None
    """向下传递的 props"""
    schema_: Optional[SchemaNode] = Field(default=None, alias="schema")
    """渲染的 schema"""


Avatar.update_forward_refs()


__all__ = [
    "Avatar",
    "Audio",
    "Badge",
    "Tasks",
    "Wizard",
    "WebComponent",
    "AmisRender",
]
