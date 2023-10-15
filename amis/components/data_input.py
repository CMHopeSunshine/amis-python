from typing import Any, List, Literal, Optional, Tuple, Union
from typing_extensions import NotRequired, TypedDict

from amis.event import EventAction, OnEvent
from amis.typing import DataMapping, DictStr, DictStrAny, Expression, OptionsType

from .data_presentation import Remark, Tpl
from .feature import Action, Button
from .types import AmisNode, API, Horizontal, SchemaNode, Template, Validation

from pydantic import Field, validator


class Form(AmisNode):
    """表单"""

    class ValidateAction(EventAction):
        """校验表单"""

        actionType: Literal["validate"] = Field(default="validate", init=False)
        componentId: str

    class SubmitAction(EventAction):
        """提交表单"""

        actionType: Literal["submit"] = Field(default="submit", init=False)
        componentId: str

    class Messages(TypedDict):
        fetchSuccess: NotRequired[str]
        """获取成功时提示"""
        fetchFailed: NotRequired[str]
        """获取失败时提示"""
        saveSuccess: NotRequired[str]
        """保存成功时提示"""
        saveFailed: NotRequired[str]
        """保存失败时提示"""

    type: Literal["form"] = Field(default="form", init=False)
    """"form" 指定为 Form 渲染器"""
    name: Optional[str] = None
    """设置一个名字后，方便其他组件与其通信"""
    mode: Literal["normal", "horizontal", "inline"] = "normal"
    """表单展示方式，可以是：normal、horizontal 或者 inline"""
    horizontal: Optional[Horizontal] = None
    """当 mode 为 horizontal 时有用，用来控制 label"""
    labelAlign: Literal["right", "left"] = "right"
    """表单项标签对齐方式，默认右对齐，仅在 mode 为 horizontal 时生效"""
    labelWidth: Optional[Union[int, str]] = None
    """表单项标签自定义宽度"""
    title: str = "表单"
    """Form 的标题"""
    submitText: Optional[str] = "提交"
    """"默认的提交按钮名称，如果设置成空，则可以把默认按钮去掉。"""
    className: Optional[str] = None
    """外层 Dom 的类名"""
    body: Optional[List[Union["FormItem", SchemaNode]]] = None
    """Form 表单项集合"""
    actions: Optional[List[Action]] = None
    """Form 提交按钮，成员为 Action"""
    actionsClassName: Optional[str] = None
    """actions 的类名"""
    messages: Optional[Messages] = None
    """消息提示覆写，默认消息读取的是 API 返回的消息，但是在此可以覆写它。"""
    wrapWithPanel: bool = True
    """是否让 Form 用 panel 包起来，设置为 false 后，actions 将无效。"""
    panelClassName: Optional[str] = None
    """外层 panel 的类名"""
    api: Optional[API] = None
    """Form 用来保存数据的 api。"""
    initApi: Optional[API] = None
    """Form 用来获取初始数据的 api。"""
    rules: Optional[List] = None  # TODO 确认类型
    """表单组合校验规则 Array<{rule:string;message:string}>"""
    interval: Optional[int] = Field(default=None, ge=3000)
    """刷新时间(最低 3000)"""
    silentPolling: bool = False
    """配置刷新时是否显示加载动画"""
    stopAutoRefreshWhen: Optional[str] = None
    """通过表达式 来配置停止刷新的条件"""
    initAsyncApi: Optional[API] = None
    """Form 用来获取初始数据的 api,与 initApi 不同的是，会一直轮询请求该接口，直到返回 finished 属性为 true 才 结束。"""
    initFetch: Optional[bool] = None
    """设置了 initApi 或者 initAsyncApi 后，默认会开始就发请求，设置为 false 后就不会起始就请求接口"""
    initFetchOn: Optional[str] = None
    """用表达式来配置"""
    initFinishedField: Optional[str] = None
    """
    设置了 initAsyncApi 后，默认会从返回数据的 data.finished 来判断是否完成
    也可以设置成其他的 xxx，就会从 data.xxx 中获取
    """
    initCheckInterval: Optional[int] = None
    """设置了 initAsyncApi 以后，默认拉取的时间间隔"""
    asyncApi: Optional[API] = None
    """设置此属性后，表单提交发送保存接口后，还会继续轮询请求该接口，直到返回 finished 属性为 true 才 结束。"""
    checkInterval: Optional[int] = None
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
    target: Optional[str] = None
    """
    默认表单提交自己会通过发送 api 保存数据，但是也可以设定另外一个 form 的 name 值
    或者另外一个 CRUD 模型的 name 值。
    如果 target 目标是一个 Form ，则目标 Form 会重新触发 initApi，api 可以拿到当前 form 数据。
    如果目标是一个 CRUD 模型，则目标模型会重新触发搜索，参数为当前 Form 数据。
    当目标是 window 时，会把当前表单的数据附带到页面地址上。
    """
    redirect: Optional[str] = None
    """设置此属性后，Form 保存成功后，自动跳转到指定页面。支持相对地址，和绝对地址（相对于组内的）。"""
    reload: Optional[str] = None
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
    static: Optional[bool] = None
    """整个表单静态方式展示"""
    staticClassName: Optional[str] = None
    """表单静态展示时使用的类名"""
    closeDialogOnSubmit: Optional[bool] = None
    """提交的时候是否关闭弹窗。当 form 里面有且只有一个弹窗的时候，本身提交会触发弹窗关闭，此属性可以关闭此行为"""
    onEvent: OnEvent[
        Literal[
            "inited",
            "change",
            "formItemValidateSucc",
            "formItemValidateError",
            "validateSucc",
            "validateError",
            "submit",
            "submitSucc",
            "submitFail",
            "asyncApiFinished",
        ]
    ] = None


class Column(AmisNode):
    """列配置"""

    xs: Optional[Union[int, str]] = None
    """宽度占比：1 - 12或'auto'"""
    ClassName: Optional[str] = None
    """列类名"""
    sm: Optional[Union[int, str]] = None
    """宽度占比：1 - 12或'auto'"""
    md: Optional[Union[int, str]] = None
    """宽度占比：1 - 12或'auto'"""
    lg: Optional[Union[int, str]] = None
    """宽度占比：1 - 12或'auto'"""
    valign: Optional[Literal["top", "middle", "bottom", "between"]] = None
    """当前列内容的垂直对齐"""
    body: Optional[SchemaNode] = None
    """内容"""


class FormItem(AmisNode):
    """表单项通用"""

    class AutoFill(AmisNode):
        showSuggestion: Optional[bool] = None
        """true 为参照录入，false 自动填充"""
        api: Optional[Expression] = None
        """自动填充接口/参照录入筛选 CRUD 请求配置"""
        silent: Optional[bool] = None
        """是否展示数据格式错误提示，默认为 true"""
        fillMappinng: Optional[SchemaNode] = None
        """自动填充/参照录入数据映射配置，键值对形式，值支持变量获取及表达式"""
        trigger: Optional[str] = None
        """showSuggestion 为 true 时，参照录入支持的触发方式，目前支持 change「值变化」｜ focus 「表单项聚焦」"""
        mode: Optional[str] = None
        """showSuggestion 为 true 时，参照弹出方式 dialog, drawer, popOver"""
        labelField: Optional[str] = None
        """showSuggestion 为 true 时，设置弹出 dialog,drawer,popOver 中 picker 的 labelField"""
        position: Optional[str] = None
        """showSuggestion 为 true 时，参照录入 mode 为 popOver 时，可配置弹出位置"""
        size: Optional[str] = None
        """showSuggestion 为 true 时，参照录入 mode 为 dialog 时，可设置大小"""
        columns: Optional[List[Column]] = None
        """showSuggestion 为 true 时，数据展示列配置"""
        filter: Optional[SchemaNode] = None
        """showSuggestion 为 true 时，数据查询过滤条件"""

    type: str
    """指定表单项类型"""
    className: Optional[str] = None
    """表单最外层类名"""
    inputClassName: Optional[str] = None
    """表单控制器类名"""
    labelClassName: Optional[str] = None
    """label 的类名"""
    name: Optional[str] = None
    """字段名，指定该表单项提交时的 key"""
    value: Optional[Union[int, str]] = None
    """字段的值"""
    label: Union[Literal[False], Template, None] = None
    """表单项标签  模板或false"""
    labelAligin: Literal["right", "left"] = "right"
    """表单项标签对齐方式，默认右对齐，仅在 mode为horizontal 时生效"""
    labelRemark: Optional[Remark] = None
    """表单项标签描述"""
    description: Optional[Template] = None
    """表单项描述"""
    placeholder: Optional[str] = None
    """表单项描述"""
    inline: Optional[bool] = None
    """是否为 内联 模式"""
    submitOnChange: Optional[bool] = None
    """是否该表单项值发生变化时就提交当前表单。"""
    disabled: Optional[bool] = None
    """当前表单项是否是禁用状态"""
    disabledOn: Optional[Expression] = None
    """当前表单项是否禁用的条件"""
    visible: Optional[Expression] = None
    """当前表单项是否禁用的条件"""
    visibleOn: Optional[Expression] = None
    """当前表单项是否禁用的条件"""
    required: Optional[bool] = None
    """是否为必填。"""
    requiredOn: Optional[Expression] = None
    """过表达式来配置当前表单项是否为必填。"""
    validations: Optional[Union[Validation, Expression]] = None
    """表单项值格式验证，支持设置多个，多个规则用英文逗号隔开。"""
    validateApi: Optional[Expression] = None
    """表单校验接口"""
    autoFill: Optional[Union[SchemaNode, AutoFill]] = None  # TODO 确认类型
    """数据录入配置，自动填充或者参照录入"""
    static: Optional[bool] = None
    """当前表单项是否是静态展示，目前支持静支持静态展示的表单项"""
    staticClassName: Optional[str] = None
    """静态展示时的类名"""
    staticLabelClassName: Optional[str] = None
    """静态展示时的 Label 的类名"""
    staticInputClassName: Optional[str] = None
    """静态展示时的 value 的类名"""
    staticSchema: Optional[SchemaNode] = None
    """自定义静态展示方式"""


class Control(AmisNode):
    """表单项包裹

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/control"""

    type: Literal["control"] = Field(default="control", init=False)
    """指定为 Control 组件"""
    label: Optional[str] = None
    """组件标签"""
    description: Optional[str] = None
    """组件描述"""
    body: Optional[SchemaNode] = None
    """表单项内容"""


class Options(FormItem):
    """选择器表单项"""

    options: Optional[OptionsType] = None
    """选项组，供用户选择"""
    source: Optional[Union[API, DataMapping]] = None
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
    """数组输入框

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/input-array"""

    type: Literal["input-array"] = Field(default="input-array", init=False)
    """指明为array组件"""
    items: SchemaNode
    """配置单项表单类型"""
    addable: Optional[bool] = None
    """是否可新增。"""
    removable: Optional[bool] = None
    """是否可删除"""
    draggable: bool = False
    """是否可以拖动排序, 需要注意的是当启用拖动排序的时候，会多一个$id 字段"""
    draggableTip: Optional[str] = None
    """可拖拽的提示文字，默认为："可通过拖动每行中的【交换】按钮进行顺序调整"""
    addButtonText: str = "新增"
    """新增按钮文字"""
    minLength: Optional[int] = None
    """限制最小长度"""
    maxLength: Optional[int] = None
    """限制最大长度"""
    scaffold: Optional[Any] = None
    """新增成员时的默认值，一般根据items的数据类型指定需要的默认值"""


class ButtonToolbar(AmisNode):
    """按钮工具栏

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/button-toolbar"""

    type: Literal["button-toolbar"] = Field(default="button-toolbar", init=False)
    """指定为 ButtonToolbar 组件"""
    label: Optional[str] = None
    """组件标签"""
    description: Optional[str] = None
    """组件描述"""
    buttons: List[Action]
    """行为按钮组"""


class ButtonGroupSelect(FormItem):
    """按钮点选"""

    type: Literal["button-group-select"] = Field(default="button-group-select", init=False)
    """指定为 button-group-select 渲染器"""
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
    """选中按钮样式"""
    options: Optional[OptionsType] = None  # TODO 允许角标
    """选项组"""
    source: Optional[API] = None
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
    onEvent: OnEvent[Literal["change"]] = None


class ChainedSelect(FormItem):
    """链式下拉框

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/chain-select"""

    type: Literal["chained-select"] = Field(default="chained-select", init=False)
    """指定为 chained-select 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
    """动态选项组"""
    autoComplete: Optional[API] = None
    """自动选中"""
    delimiter: str = ","
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    onEvent: OnEvent[Literal["change"]] = None


class Checkbox(FormItem):
    """勾选框"""

    type: Literal["checkbox"] = Field(default="checkbox", init=False)
    """指定为 checkbox 渲染器"""
    option: Optional[str] = None
    """选项说明"""
    trueValue: Union[str, int, bool] = True
    """标识真值"""
    falseValue: Union[str, int, bool] = False
    """标识假值"""
    optionType: Literal["default", "button"] = "default"
    """设置 option 类型"""
    onEvent: OnEvent[Literal["change"]] = None


class Checkboxes(FormItem):
    """复选框"""

    type: Literal["checkboxes"] = Field(default="checkboxes", init=False)
    """指定为 checkboxes 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
    """动态选项组"""
    delimiter: str = ","
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
    menuTpl: Optional[str] = None
    """支持自定义选项渲染"""
    checkAll: bool = False
    """是否支持全选"""
    inline: bool = True
    """是否显示为一行"""
    defaultCheckAll: bool = False
    """默认是否全选"""
    creatable: bool = False
    """新增选项"""
    createBtnLabel: str = "新增选项"
    """新增选项"""
    addControls: Optional[List[FormItem]] = None
    """自定义新增表单项"""
    addApi: Optional[API] = None
    """配置新增选项接口"""
    editable: bool = False
    """编辑选项"""
    editControls: Optional[List[FormItem]] = None
    """自定义编辑表单项"""
    editApi: Optional[API] = None
    """配置编辑选项接口"""
    removable: bool = False
    """删除选项"""
    deleteApi: Optional[API] = None
    """配置删除选项接口"""
    optionType: Literal["default", "button"] = "default"
    """按钮模式"""
    itemClassName: Optional[str] = None
    """选项样式类名"""
    labelClassName: Optional[str] = None
    """选项标签样式类名"""
    onEvent: OnEvent[Literal["change"]] = None


class InputCity(FormItem):
    """城市选择器"""

    type: Literal["input-city"] = Field(default="input-city", init=False)
    """指定为 input-city 渲染器"""
    allowCity: bool = True
    """允许选择城市"""
    allowDistrict: bool = True
    """允许选择区域"""
    searchable: bool = False
    """是否出搜索框"""
    extractValue: bool = True
    """是否抽取值，如果设置成 false 值格式会变成对象，包含 code、province、city和district文字信息。"""
    onEvent: OnEvent[Literal["change"]] = None


class InputColor(FormItem):
    """颜色选择器"""

    type: Literal["input-color"] = Field(default="input-color", init=False)
    """指定为 input-color 渲染器"""
    format: Literal["hex", "hls", "rgb", "rgba"] = "hex"
    """请选择 hex、hls、rgb或者rgba。"""
    presetColors: List[str] = [
        "#D0021B",
        "#F5A623",
        "#F8E71C",
        "#8B572A",
        "#7ED321",
        "#417505",
        "#BD10E0",
        "#9013FE",
        "#4A90E2",
        "#50E3C2",
        "#B8E986",
        "#000000",
        "#4A4A4A",
        "#9B9B9B",
        "#FFFFFF",
    ]
    """选择器底部的默认颜色，数组内为空则不显示默认颜色"""
    allowCustomColor: bool = True
    """为false时只能选择颜色，使用 presetColors 设定颜色选择范围"""
    clearable: bool = True
    """是否显示清除按钮"""
    resetValue: str = ""
    """清除后，表单项值调整成该值"""


class Combo(FormItem):
    """组合"""

    class AddItemAction(EventAction):
        """只有开启multiple模式才能使用, multiple模式下，给新增项添加默认值"""

        actionType: Literal["addItem"] = Field(default="addItem", init=False)
        item: Optional[DictStrAny] = None
        componentId: str

    type: Literal["combo"] = Field(default="combo", init=False)
    """指定为 combo 渲染器"""
    formClassName: Optional[str] = None
    """单组表单项的类名"""
    items: Optional[List[FormItem]] = None
    """组合展示的表单项，允许以下额外属性：
    - columnClassName(str): 列的类名，可以用它配置列宽度。默认平均分配
    - unique(bool): 设置当前列值是否唯一，即不允许重复选择。
    """
    noBorder: bool = False
    """单组表单项是否显示边框"""
    scaffold: DictStrAny = {}
    """单组表单项初始值"""
    multiple: bool = False
    """是否多选"""
    multiLine: bool = False
    """默认是横着展示一排，设置以后竖着展示"""
    minLength: Optional[int] = None
    """最少添加的条数"""
    maxLength: Optional[int] = None
    """最多添加的条数"""
    flat: bool = False
    """是否将结果扁平化(去掉 name),只有当 items 的 length 为 1 且 multiple 为 true 的时候才有效。"""
    joinValues: bool = True
    """默认为 true 当扁平化开启的时候，是否用分隔符的形式发送给后端，否则采用 array 的方式。"""
    delimiter: str = ","
    """当扁平化开启并且 joinValues 为 true 时，用什么分隔符。"""
    addable: bool = False
    """是否可新增"""
    addattop: bool = False
    """在顶部添加"""
    removable: bool = False
    """是否可删除"""
    deleteApi: Optional[API] = None
    """如果配置了，则删除前会发送一个 api，请求成功才完成删除"""
    deleteConfirmText: str = "确认要删除？"
    """当配置 deleteApi 才生效！删除时用来做用户确认"""
    draggable: bool = False
    """是否可以拖动排序, 需要注意的是当启用拖动排序的时候，会多一个$id 字段"""
    draggableTip: Optional[str] = None
    """"可通过拖动每行中的【交换】按钮进行顺序调整"  # 可拖拽的提示文字"""
    subFormMode: Literal["normal", "horizontal", "inline"] = "normal"
    """"可选normal、horizontal、inline"""
    subFormHorizontal: Optional[Horizontal] = None
    """当 subFormMode 为 horizontal 时有用，用来控制 label 的展示占比"""
    placeholder: str = ""
    """没有成员时显示。"""
    canAccessSuperData: bool = False
    """指定是否可以自动获取上层的数据并映射到表单项上"""
    conditions: Optional[dict] = None
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
    itemClassName: Optional[str] = None
    """单组 CSS 类"""
    itemsWrapperClassName: Optional[str] = None
    """组合区域 CSS 类"""
    deleteBtn: Union[Button, str] = "自定义删除按钮"
    """只有当removable为 true 时有效; 如果为string则为按钮的文本；如果为Button则根据配置渲染删除按钮。"""
    addBtn: Optional[Button] = None
    """可新增自定义配置渲染新增按钮，在tabsMode: true下不生效。"""
    addButtonClassName: Optional[str] = None
    """新增按钮 CSS 类名"""
    addButtonText: str = "新增"
    """新增按钮文字"""
    onEvent: OnEvent[Literal["add", "delete", "tabsChange"]] = None


class ConditionBuilder(FormItem):
    """组合条件"""

    class ConditionField(AmisNode):
        type: Literal["text"] = Field(default="text", init=False)
        """字段配置中配置成 "text"""
        label: Optional[Union[Literal[False], Template]] = None
        """字段名称。"""
        placeholder: Optional[str] = None
        """占位符"""
        operators: List[str] = [
            "equal",
            "not_equal",
            "is_empty",
            "is_not_empty",
            "like",
            "not_like",
            "starts_with",
            "ends_with",
        ]
        """如果不要那么多，可以配置覆盖。
        默认为 ['equal','not_equal','is_empty','is_not_empty','like','not_like','starts_with','ends_with']
        """
        defaultOp: str = "equal"
        """默认为 "equal"""

    class Text(ConditionField):
        """文本"""

    class Number(ConditionField):
        """数字"""

        type: Literal["number"] = Field(default="number", init=False)
        """数字"""
        minimum: Optional[float] = None
        """最小值"""
        maximum: Optional[float] = None
        """最大值"""
        step: Optional[float] = None
        """步长"""

    class Date(ConditionField):
        """日期"""

        type: Literal["date"] = Field(default="date", init=False)
        """日期"""
        defaultValue: Optional[str] = None
        """默认值"""
        format: str = "YYYY-MM-DD"
        """默认 "YYYY-MM-DD" 值格式"""
        inputFormat: str = "YYYY-MM-DD"
        """默认 "YYYY-MM-DD" 显示的日期格式。"""

    class Datetime(Date):
        """日期时间"""

        type: Literal["datetime"] = Field(default="datetime", init=False)
        """日期时间"""
        timeFormat: str = "HH:mm"
        """默认 "HH:mm" 时间格式，决定输入框有哪些。"""

    class Time(Date):
        """时间"""

        type: Literal["time"] = Field(default="time", init=False)

    class Select(ConditionField):
        """下拉选择"""

        type: Literal["select"] = Field(default="select", init=False)
        """下拉选择"""
        options: Optional[OptionsType] = None
        """选项列表，Array<{label: string, value: any}>"""
        source: Optional[API] = None
        """动态选项，请配置 api。"""
        searchable: Optional[bool] = None
        """是否可以搜索"""
        autoComplete: Optional[API] = None
        """自动提示补全，每次输入新内容后，将调用接口，根据接口返回更新选项。"""

    class Custom(ConditionField):
        """自定义"""

        type: Literal["custom"] = Field(default="custom", init=False)
        """自定义"""
        operators: Union[list, str, dict] = []
        """默认为空，需配置自定义判断条件，支持字符串或 key-value 格式"""
        value: Optional[SchemaNode] = None
        """字段配置右边值需要渲染的组件，支持 amis 输入类组件或自定义输入类组件"""

    type: Literal["condition-builder"] = Field(default="condition-builder", init=False)
    """指定为 condition-builder 渲染器"""
    className: Optional[str] = None
    """外层 dom 类名"""
    fieldClassName: Optional[str] = None
    """输入字段的类名"""
    source: Optional[API] = None
    """通过远程拉取配置项"""
    embed: bool = True
    """内嵌展示"""
    title: Optional[str] = None
    """弹窗配置的顶部标题"""
    fields: Optional[List[Union[Text, Number, Date, Datetime, Time, Select, Custom]]] = None
    """为数组类型，每个成员表示一个可选字段，支持多个层，配置示例"""
    showANDOR: Optional[bool] = None
    """用于 simple 模式下显示切换按钮"""
    showNot: Optional[bool] = None
    """是否显示「非」按钮"""
    draggable: bool = True
    """是否可拖拽"""
    searchable: Optional[bool] = None
    """字段是否可搜索"""
    selectMode: Literal["list", "tree", "chained"] = "list"
    """组合条件左侧选项类型"""
    addBtnVisibleOn: Optional[Expression] = None
    """表达式：控制按钮“添加条件”的显示。参数为depth、breadth，分别代表深度、长度。表达式需要返回boolean类型"""
    addGroupBtnVisibleOn: Optional[Expression] = None
    """表达式：控制按钮“添加条件组”的显示。参数为depth、breadth，分别代表深度、长度。表达式需要返回boolean类型"""
    inputSettings: Optional[Union[Text, Number, Date, Datetime, Time, Select, Custom]] = None
    """	开启公式编辑模式时的输入控件类型"""
    formula: Optional[DictStrAny] = None
    """字段输入控件变成公式编辑器。"""
    showIf: Optional[bool] = None
    """开启后条件中额外还能配置启动条件。"""
    formulaForIf: Optional[DictStrAny] = None
    """给 showIF 表达式用的公式信息"""


class InputDate(FormItem):
    """日期"""

    class Shortcuts(TypedDict):
        label: NotRequired[str]
        date: NotRequired[str]

    type: Literal["input-date"] = Field(default="input-date", init=False)
    """指定为 input-date渲染器"""
    value: Optional[str] = None
    """默认值"""
    valueFormat: str = "X"
    """日期选择器值格式

    https://momentjs.com/docs/#/displaying/format/"""
    displayFormat: str = "YYYY-DD-MM"
    """日期选择器显示格式，即时间戳格式

    https://momentjs.com/docs/#/displaying/format/"""
    closeOnSelect: bool = False
    """点选日期后，是否马上关闭选择框"""
    placeholder: str = "请选择日期"
    """占位文本"""
    shortcuts: Optional[str | List[Shortcuts]] = None
    """日期快捷键"""
    minDate: Optional[str] = None
    """限制最小日期"""
    maxDate: Optional[str] = None
    """限制最大日期"""
    utc: bool = False
    """保存 utc 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    disabledDate: Optional[str] = None
    """用字符函数来控制哪些天不可以被点选"""
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class InputDatetime(InputDate):
    """日期"""

    type: Literal["input-datetime"] = Field(default="input-datetime", init=False)
    """指定为 input-datetime 渲染器"""
    placeholder: str = "请选择日期以及时间"
    """占位文本"""
    minDate: Optional[str] = None
    """限制最小日期时间"""
    maxDate: Optional[str] = None
    """限制最大日期时间"""
    timeConstraints: Optional[Union[dict, bool]] = None
    """请参考： react-datetime"""
    isEndDate: bool = False
    """如果配置为 true，会自动默认为 23:59:59 秒"""
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class InputMonth(FormItem):
    """月份"""

    type: Literal["input-month"] = Field(default="input-month", init=False)
    """指定为 input-month 渲染器"""
    value: Optional[str] = None
    """默认值"""
    valueFormat: str = "X"
    """日期选择器值格式

    https://momentjs.com/docs/#/displaying/format/"""
    displayFormat: str = "YYYY-DD-MM"
    """日期选择器显示格式，即时间戳格式

    https://momentjs.com/docs/#/displaying/format/"""
    placeholder: str = "请选择月份"
    """占位文本"""
    clearable: bool = True
    """是否可清除"""
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class InputDateRange(FormItem):
    """日期范围"""

    class Shortcuts(TypedDict):
        label: NotRequired[str]
        """标签"""
        startDate: NotRequired[str]
        """开始日期"""
        endDate: NotRequired[str]
        """结束日期"""

    type: Literal["input-date-range"] = Field(default="input-date-range", init=False)
    """指定为 input-date-range 渲染器"""
    valueFormat: str = "X"
    """日期选择器值格式

    https://momentjs.com/docs/#/displaying/format/"""
    displayFormat: str = "YYYY-DD-MM"
    """日期选择器显示格式，即时间戳格式

    https://momentjs.com/docs/#/displaying/format/"""
    placeholder: str = "请选择日期范围"
    """占位文本"""
    shortcuts: Optional[str | List[str] | List[Shortcuts]] = None
    """日期范围快捷键"""
    minDate: Optional[str] = None
    """限制最小日期时间，用法同 限制范围"""
    maxDate: Optional[str] = None
    """限制最大日期时间，用法同 限制范围"""
    minDuration: Optional[str] = None
    """限制最小跨度，如： 2days"""
    maxDuration: Optional[str] = None
    """限制最大跨度，如：1year"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    animation: bool = True
    """是否启用游标动画"""
    extraName: Optional[str] = None
    """是否存成两个字段"""
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class InputDatetimeRange(InputDateRange):
    """日期时间范围"""

    type: Literal["input-datetime-range"] = Field(default="input-datetime-range", init=False)
    """指定为 input-datetime-range 渲染器"""
    placeholder: str = "请选择日期时间范围"
    """占位文本"""
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class InputMonthRange(FormItem):
    """月份范围"""

    type: Literal["input-month-range"] = Field(default="input-month-range", init=False)
    """指定为 input-month-range 渲染器"""
    format: str = "X"
    """日期时间选择器值格式"""
    inputFormat: str = "YYYY-MM-DD"
    """日期时间选择器显示格式"""
    placeholder: str = "请选择月份范围"
    """占位文本"""
    minDate: Optional[str] = None
    """限制最小日期时间，用法同 限制范围"""
    maxDate: Optional[str] = None
    """限制最大日期时间，用法同 限制范围"""
    minDuration: Optional[str] = None
    """限制最小跨度，如： 2days"""
    maxDuration: Optional[str] = None
    """限制最大跨度，如：1year"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""
    extraName: Optional[str] = None
    """是否存成两个字段"""
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class InputKV(FormItem):
    """键值对"""

    type: Literal["input-kv"] = Field(default="input-kv", init=False)
    """指定为 input-kv 渲染器"""
    valuetype: Literal["input-text"] = Field(default="input-text", init=False)
    """值类型"""
    keyPlaceholder: Optional[str] = None
    """key 的提示信息"""
    valuePlaceholder: Optional[str] = None
    """value 的提示信息"""
    draggable: bool = True
    """是否可拖拽排序"""
    defaultValue: Any = ""
    """默认值"""
    autoParseJSON: bool = True
    """是否自动转换 json 对象字符串"""
    onEvent: OnEvent[Literal["add", "delete"]] = None


class InputKVS(FormItem):
    """键值对象"""

    class KeyItem(TypedDict):
        label: NotRequired[str]
        """标签"""
        type: NotRequired[str]
        """类型"""
        options: NotRequired[OptionsType]
        """选项"""
        mode: NotRequired[Literal["horizontal"]]
        """水平模式"""

    type: Literal["input-kvs"] = Field(default="input-kvs", init=False)
    """指定为 input-kvs 渲染器"""
    addButtonText: str = "新增字段"
    """新增按钮文本"""
    keyItem: Optional[KeyItem] = None
    """key 的配置"""
    valueItems: List[SchemaNode] = []
    """value 的配置"""


class InputFormula(FormItem):
    """公式编辑器"""

    type: Literal["input-formula"] = Field(default="input-formula", init=False)
    """指定为 input-formula 渲染器"""
    title: str = "公式编辑器"
    """弹框标题"""
    header: Optional[str] = None
    """编辑器 header 标题，如果不设置，默认使用表单项label字段"""
    evalMode: bool = True
    """表达式模式 或者 模板模式，模板模式则需要将表达式写在 ${ 和 } 中间。"""
    variables: Union[dict, list] = []
    """可用变量"""
    variableMode: Literal["tabs", "list", "tree"] = "list"
    """可配置成 tabs 或者 tree 默认为列表，支持分组。"""
    functions: Optional[List[DictStrAny]] = None
    """可以不设置，默认就是 amis-formula 里面定义的函数，如果扩充了新的函数则需要指定"""
    inputMode: Optional[Literal["button", "input-button", "input-group"]] = None
    """控件的展示模式"""
    icon: Optional[str] = None
    """按钮图标，例如fa fa-list"""
    btnLabel: str = "公示编辑"
    """按钮文本，inputMode为button时生效"""
    level: Literal["info", "success", "warning", "danger", "link", "primary", "dark", "light", "default"] = "default"
    """按钮样式"""
    allowInput: Optional[bool] = None
    """输入框是否可输入"""
    btnSize: Optional[Literal["xs", "sm", "md", "lg"]] = None
    """按钮大小"""
    borderMode: Optional[Literal["full", "half", "none"]] = None
    """输入框边框模式"""
    placeholder: str = "暂无数据"
    """输入框占位符"""
    className: Optional[str] = None
    """控件外层 CSS 样式类名"""
    variableClassName: Optional[str] = None
    """变量面板 CSS 样式类名"""
    functionClassName: Optional[str] = None
    """函数面板 CSS 样式类名"""


class DiffEditor(FormItem):
    """对比编辑器"""

    type: Literal["diff-editor"] = Field(default="diff-editor", init=False)
    """指定为 diff-editor 渲染器"""
    language: Optional[str] = None
    """编辑器高亮的语言

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/editor#%E6%94%AF%E6%8C%81%E7%9A%84%E8%AF%AD%E8%A8%80"""
    diffValue: Optional[Tpl] = None
    """左侧值"""
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class Editor(FormItem):
    """代码编辑器"""

    type: Literal["editor"] = Field(default="editor", init=False)
    """指定为 editor 渲染器"""
    language: str = "javascript"
    """编辑器高亮的语言，支持通过 ${xxx} 变量获取"""
    size: Literal["md", "lg", "xl", "xxl"] = "md"
    """编辑器高度，取值可以是 md、lg、xl、xxl"""
    allowFullscreen: bool = False
    """是否显示全屏模式开关"""
    options: Optional[DictStrAny] = None
    """monaco编辑器的其它配置，比如是否显示行号等，参考:

    https://microsoft.github.io/monaco-editor/docs.html#interfaces/editor.IEditorOptions.html"""
    placeholder: Optional[str] = None
    """占位描述，没有值的时候展示"""
    disabled: bool = False
    "只读模式"
    onEvent: OnEvent[Literal["change", "focus", "blur"]] = None


class FieldSet(FormItem):
    """表单项集合"""

    type: Literal["fieldSet"] = Field(default="fieldSet", init=False)
    """指定为 fieldSet 渲染器"""
    className: Optional[str] = None
    """CSS 类名"""
    headingClassName: Optional[str] = None
    """标题 CSS 类名"""
    bodyClassName: Optional[str] = None
    """内容区域 CSS 类名"""
    title: Optional[SchemaNode] = None
    """标题"""
    body: Optional[List[FormItem]] = None
    """表单项集合"""
    mode: Optional[str] = None
    """展示默认，同 Form 中的模式"""
    collapsable: bool = False
    """是否可折叠"""
    collapsed: bool = False
    """默认是否折叠"""
    collapseTitle: SchemaNode = "收起"
    """收起的标题"""
    size: Optional[Literal["xs", "sm", "base", "lg"]] = None
    """大小，支持 xs、sm、base、lg"""


class InputExcel(FormItem):
    """解析 Excel"""

    type: Literal["input-excel"] = Field(default="input-excel", init=False)
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
    onEvent: OnEvent[Literal["change"]] = None


class InputFile(FormItem):
    """文件上传"""

    type: Literal["input-file"] = Field(default="input-file", init=False)
    """指定为 input-file 渲染器"""
    receiver: Optional[API] = None
    """上传文件接口"""
    accept: str = "text/plain"
    """默认只支持纯文本，要支持其他类型，请配置此属性为文件后缀.xxx"""
    asBase64: bool = False
    """将文件以base64的形式，赋值给当前组件"""
    asBlob: bool = False
    """将文件以二进制的形式，赋值给当前组件"""
    maxSize: Optional[int] = None
    """默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B"""
    maxLength: Optional[int] = None
    """默认没有限制，当设置后，一次只允许上传指定数量文件。"""
    multiple: bool = False
    """是否多选。"""
    drag: bool = False
    """是否支持拖拽上传"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    delimiter: Union[str, bool] = ","
    """拼接符"""
    autoUpload: bool = True
    """否选择完就自动开始上传"""
    hideUploadButton: bool = False
    """隐藏上传按钮"""
    stateTextMap: DictStr = {
        "init": "",
        "pending": "等待上传",
        "uploading": "上传中",
        "error": "上传出错",
        "uploaded": "已上传",
        "ready": "",
    }
    """上传状态文案"""
    fileField: str = "file"
    """如果你不想自己存储，则可以忽略此属性。"""
    nameField: str = "name"
    """接口返回哪个字段用来标识文件名"""
    valueField: str = "value"
    """文件的值用那个字段来标识。"""
    urlField: str = "url"
    """文件下载地址的字段名。"""
    btnlabel: Optional[Union[Literal[False], Template, str]] = None
    """上传按钮的文字"""
    downloadUrl: Union[str, bool] = ""
    """
    1.1.6 版本开始支持 post:http://xxx.com/${value} 这种写法
    默认显示文件路径的时候会支持直接下载，可以支持加前缀如：http://xx.dom/filename= ，
    如果不希望这样，可以把当前配置项设置为 false。
    """
    useChunk: Union[bool, Literal["auto"]] = "auto"
    """amis 所在服务器，限制了文件上传大小不得超出 10M，所以 amis 在用户选择大文件的时候，自动会改成分块上传模式。"""
    chunkSize: int = 5 * 1024 * 1024
    """分块大小"""
    startChunkApi: Optional[API] = None
    """startChunkApi"""
    chunkApi: Optional[API] = None
    """chunkApi"""
    finishChunkApi: Optional[API] = None
    """finishChunkApi"""
    concurrency: Optional[int] = None
    """	分块上传时并行个数"""
    documentation: Optional[str] = None
    """文档内容"""
    documentLink: Optional[str] = None
    """文档链接"""
    initAutoFill: bool = True
    """初表单反显时是否执行"""
    onEvent: OnEvent[Literal["change", "remove", "success", "fail"]] = None


class Formula(FormItem):
    """公式"""

    type: Literal["formula"] = Field(default="formula", init=False)
    """指定为 formula 渲染器"""
    name: Optional[str] = None
    """需要应用的表单项name值，公式结果将作用到此处指定的变量中去。"""
    formula: Optional[Expression] = None
    """应用的公式"""
    condition: Optional[Expression] = None
    """公式作用条件"""
    initSet: bool = True
    """初始化时是否设置"""
    autoSet: bool = True
    """观察公式结果，如果计算结果有变化，则自动应用到变量上"""
    id: Optional[str] = None
    """定义个名字，当某个按钮的目标指定为此值后，会触发一次公式应用。这个机制可以在 autoSet 为 false 时用来手动触发"""


class Group(FormItem):
    """表单项组"""

    type: Literal["group"] = Field(default="group", init=False)
    """指定为 group 渲染器"""
    className: Optional[str] = None
    """	CSS 类名"""
    label: Optional[Template] = None
    """group 的标签"""
    body: List[FormItem] = []
    """表单项集合"""
    mode: Optional[Literal["normal", "horizontal", "inline"]] = None
    """展示默认，同 Form 中的模式"""
    gap: Optional[Literal["xs", "sm", "normal"]] = None
    """表单项之间的间距，可选：xs、sm、normal"""
    direction: Literal["vertical", "horizontal"] = "horizontal"
    """可以配置水平展示还是垂直展示。对应的配置项分别是：vertical、horizontal"""


class Hidden(FormItem):
    """隐藏字段"""

    type: Literal["hidden"] = Field(default="hidden", init=False)
    """指定为 hidden 渲染器"""


class InputImage(FormItem):
    """图片上传"""

    class CropInfo(AmisNode):
        aspectRatio: Optional[float] = None
        """裁剪比例。浮点型，默认 1 即 1:1，如果要设置 16:9 请设置 1.7777777777777777 即 16 / 9。。"""
        rotatable: bool = False
        """裁剪时是否可旋转"""
        scalable: bool = False
        """裁剪时是否可缩放"""
        viewMode: int = 1
        """裁剪时的查看模式，0 是无限制"""

    class Limit(AmisNode):
        width: Optional[int] = None
        """限制图片宽度。"""
        height: Optional[int] = None
        """限制图片高度。"""
        minWidth: Optional[int] = None
        """限制图片最小宽度。"""
        minHeight: Optional[int] = None
        """限制图片最小高度。"""
        maxWidth: Optional[int] = None
        """限制图片最大宽度。"""
        maxHeight: Optional[int] = None
        """限制图片最大高度。"""
        aspectRatio: Optional[float] = None
        """
        限制图片宽高比，格式为浮点型数字，默认 1 即 1:1，如果要设置 16:9
        请设置 1.7777777777777777 即 16 / 9。 如果不想限制比率，请设置空字符串。
        """

    type: Literal["input-image"] = Field(default="input-image", init=False)
    """指定为 input-image 渲染器"""
    receiver: Optional[API] = None
    """上传文件接口"""
    accept: str = ".jpeg,.jpg,.png,.gif"
    """支持的图片类型格式，请配置此属性为图片后缀，例如.jpg,.png"""
    maxSize: Optional[int] = None
    """默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B"""
    maxLength: Optional[int] = None
    """默认没有限制，当设置后，一次只允许上传指定数量文件。"""
    multiple: bool = False
    """是否多选。"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    delimiter: Union[str, bool] = ","
    """拼接符"""
    autoUpload: bool = True
    """否选择完就自动开始上传"""
    hideUploadButton: bool = False
    """隐藏上传按钮"""
    fileField: str = "file"
    """如果你不想自己存储，则可以忽略此属性。"""
    crop: Optional[Union[bool, CropInfo]] = None
    """用来设置是否支持裁剪"""
    cropFormat: str = "image/png"
    """裁剪文件格式"""
    cropQuality: int = 1
    """裁剪文件格式的质量，用于 jpeg/webp，取值在 0 和 1 之间"""
    limit: Optional[Limit] = None
    """限制图片大小，超出不让上传。"""
    frameImage: Optional[str] = None
    """默认占位图地址"""
    fixedSize: Optional[bool] = None
    """是否开启固定尺寸,若开启，需同时设置 fixedSizeClassName"""
    fixedSizeClassName: Optional[str] = None
    """
    开启固定尺寸时，根据此值控制展示尺寸。
    例如h-30,即图片框高为 h-30,AMIS 将自动缩放比率设置默认图所占位置的宽度，最终上传图片根据此尺寸对应缩放。
    """
    initAutoFill: bool = False
    """表单反显时是否执行 autoFill"""
    uploadBtnText: Optional[Union[str, SchemaNode]] = None
    """上传按钮文案。支持tpl、schema形式配置"""
    dropCrop: bool = True
    """图片上传后是否进入裁剪模式"""
    initCrop: bool = False
    """图片选择器初始化后是否立即进入裁剪模式"""
    draggable: bool = False
    """开启后支持拖拽排序改变图片值顺序"""
    draggableTip: str = "拖拽排序"
    """拖拽提示文案"""
    onEvent: OnEvent[Literal["change", "remove", "success", "fail"]] = None


class InputGroup(FormItem):
    """输入框组合"""

    class ValidationConfig(TypedDict):
        errorMode: NotRequired[Literal["full", "partial"]]
        """错误提示风格, full整体飘红, partial仅错误元素飘红"""
        delimiter: NotRequired[str]
        """单个子元素多条校验信息的分隔符"""

    type: Literal["input-group"] = Field(default="input-group", init=False)
    """指定为 input-group 渲染器"""
    className: Optional[str] = None
    """CSS 类名"""
    body: List[FormItem] = []
    """表单项集合"""
    validationConfig: Optional[ValidationConfig] = None
    """校验相关配置"""


class ListSelect(FormItem):
    """列表"""

    type: Literal["list-select"] = Field(default="list-select", init=False)
    """指定为 list-select 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
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
    autoFill: Optional[dict] = None
    """自动填充"""
    listClassName: Optional[str] = None
    """支持配置 list div 的 css 类名。比如: flex justify-between"""
    onEvent: OnEvent[Literal["change"]] = None


class LocationPicker(FormItem):
    """地理位置"""

    type: Literal["location-picker"] = Field(default="location-picker", init=False)
    """指定为 location-picker 渲染器"""
    vendor: Literal["baidu", "gaode"] = "baidu"
    """地图厂商，目前只实现了百度地图和高德地图"""
    ak: str
    """百度/高得地图的 ak, 注册地址: http://lbsyun.baidu.com/"""
    clearable: bool = False
    """输入框是否可清空"""
    placeholder: str = "请选择位置"
    """"默认提示"""
    coordinatestype: Literal["bd09"] = Field(default="bd09", init=False)
    """默为百度/高德坐标，可设置为'gcj02', 高德地图不支持坐标转换"""


class UUID(FormItem):
    """随机 ID

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/uuid"""

    type: Literal["uuid"] = Field(default="uuid", init=False)
    """指定为 uuid 渲染器"""
    length: Optional[int] = None
    """生成长度"""


class MatrixCheckboxes(FormItem):
    """矩阵勾选

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/matrix-checkboxes"""

    class Column(TypedDict):
        label: str
        """列标题"""
        col: NotRequired[str]

    class Row(TypedDict):
        label: str
        """列标题"""
        rol: NotRequired[str]

    type: Literal["matrix-checkboxes"] = Field(default="matrix-checkboxes", init=False)
    """指定为 matrix-checkboxes 渲染器"""
    columns: Optional[List[Column]] = None
    """列信息，数组中 label 字段是必须给出的"""
    rows: Optional[List[Row]] = None
    """行信息， 数组中 label 字段是必须给出的"""
    rowLabel: Optional[str] = None
    """行标题说明"""
    source: Optional[API] = None
    """Api 地址，如果选项组不固定，可以通过配置 source 动态拉取。"""
    multiple: bool = True
    """是否多选"""
    singleSelectMode: Literal["cell", "row", "column"] = "column"
    """设置单选模式，multiple为false时有效，可设置为cell, row, column 分别为全部选项中只能单选某个单元格、
    每行只能单选某个单元格，每列只能单选某个单元格"""
    textAlign: str = "center"
    """当开启多选+全选时，默认为'left'"""
    yCheckAll: bool = False
    """列上的全选"""
    xCheckAll: bool = False
    """行上的全选"""
    onEvent: OnEvent[Literal["change"]] = None


class NestedSelect(FormItem):
    """级联选择器"""

    type: Literal["nested-select"] = Field(default="nested-select", init=False)
    """指定为 nested-select 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
    """动态选项组"""
    delimiter: Union[str, bool] = False
    """拼接符"""
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
    maxTagCount: Optional[int] = None
    """标签的最大展示数量，超出数量后以收纳浮层的方式展示，仅在多选模式开启后生效"""
    overflowTagPopover: Optional[DictStrAny] = None  # TODO: TooltipObject
    """收纳浮层的配置属性，详细配置参考Tooltip"""
    onEvent: OnEvent[Literal["change", "blur", "foucs"]] = None


class InputNumber(FormItem):
    """数字输入框"""

    type: Literal["input-number"] = Field(default="input-number", init=False)
    """指定为 input-number 渲染器"""
    min: Optional[Union[int, Template]] = None
    """最小值"""
    max: Optional[Union[int, Template]] = None
    """最大值"""
    step: Optional[Union[float, int]] = None
    """步长"""
    precision: Optional[int] = None
    """精度，即小数点后几位"""
    showSteps: bool = True
    """是否显示上下点击按钮"""
    readOnly: bool = False
    """只读"""
    prefix: Optional[str] = None
    """前缀"""
    suffix: Optional[str] = None
    """后缀"""
    unitOptions: Optional[List[str]] = None
    """单位选项"""
    kilobitSeparator: bool = False
    """千分分隔"""
    keyboard: bool = True
    """键盘事件（方向上下）"""
    big: bool = False
    """是否使用大数"""
    displayMode: Literal["base", "enhance"] = "base"
    """样式类型"""
    borderMode: Literal["full", "half", "none"] = "full"
    """边框模式，全边框，还是半边框，或者没边框"""
    resetValue: Union[int, str] = ""
    """清空输入内容时，组件值将设置为resetValue"""
    clearValueOnEmpty: bool = False
    """内容为空时从数据域中删除该表单项对应的值	"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class Picker(FormItem):
    """列表选择器"""

    class OverflowConfig(AmisNode):
        maxTagCount: int = -1
        """标签的最大展示数量，超出数量后以收纳浮层的方式展示，仅在多选模式开启后生效，默认为-1 不开启"""
        displayPosition: List[Literal["select", "crud"]] = ["select", "crud"]
        """收纳标签生效的位置，未开启内嵌模式默认为选择器, 开启后默认为选择器和CRUD 顶部"""
        overflowTagPopover: Optional[DictStrAny] = None  # TODO TooltipObject
        """选择器内收纳标签的Popover配置，详细配置参考Tooltip"""
        overflowTagPopoverInCRUD: Optional[DictStrAny] = None  # TODO TooltipObject
        """CRUD顶部内收纳标签的Popover配置，详细配置参考Tooltip"""

    type: Literal["picker"] = Field(default="picker", init=False)
    """指定为 picker 渲染器，列表选取，在功能上和 Select 类似，但它能显示更复杂的信息。"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
    """动态选项组"""
    multiple: Optional[bool] = None
    """是否为多选。"""
    delimiter: Union[str, bool] = False
    """拼接符"""
    modalTitle: str = "请选择"
    """设置模态框的标题"""
    modalMode: Literal["dialog", "drawer"] = "dialog"
    """"dialog" # 设置 dialog 或者 drawer，用来配置弹出方式。"""
    pickerSchema: str = """{mode: 'list', listItem: {title: '${label}'}}"""  # TODO 确定类型
    """即用 List 类型的渲染，来展示列表信息。更多配置参考 CRUD"""
    embed: bool = False
    """是否使用内嵌模式"""
    overflowConfig: Optional[OverflowConfig] = None
    """开启最大标签展示数量的相关配置"""
    onEvent: OnEvent[Literal["change", "itemClick"]] = None


class InputQuarter(InputDate):
    """季度"""

    type: Literal["input-quarter"] = Field(default="input-quarter", init=False)
    """指定为 input-quarter 渲染器"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class InputQuarterRange(FormItem):
    """季度范围"""

    type: Literal["input-quarter-range"] = Field(default="input-quarter-range", init=False)
    """"指定为 input-quarter-range 渲染器"""
    valueFormat: str = "X"
    """日期选择器值格式"""
    displayFormat: str = "YYYY-DD"
    """日期选择器显示格式"""
    placeholder: str = "请选择季度范围"
    """占位文本"""
    minDate: Optional[str] = None
    """限制最小日期，用法同 限制范围"""
    maxDate: Optional[str] = None
    """限制最大日期，用法同 限制范围"""
    minDuration: Optional[str] = None
    """限制最小跨度，如： 2quarter"""
    maxDuration: Optional[str] = None
    """限制最大跨度，如：4quarter"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""
    extraName: Optional[str] = None
    """是否存成两个字段"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class Radio(FormItem):
    """ "单选框

    实现组合中的单选功能，此组件只有在 combo 和 input-table 中有意义。

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/radio"""

    type: Literal["radio"] = Field(default="radio", init=False)
    """指定为 radio 渲染器"""
    option: Optional[str] = None
    """选项说明"""
    trueValue: Union[str, int, bool] = True
    """标识真值"""
    falseValue: Union[str, int, bool] = False
    """标识假值"""
    onEvent: OnEvent[Literal["change"]] = None


class Radios(FormItem):
    """单选框"""

    type: Literal["radios"] = Field(default="radios", init=False)
    """指定为 radios 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
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
    onEvent: OnEvent[Literal["change"]] = None


class ChartRadios(FormItem):
    """图表单选框"""

    type: Literal["chart-radios"] = Field(default="chart-radios", init=False)
    """指定为 chart-radios 渲染器"""
    config: Optional[DictStrAny] = None
    """echart图表配置"""
    showTooltipOnHighlight: bool = False
    """高亮的时候是否显示 tooltip"""
    chartValueField: str = "value"
    """图表数值字段名"""


class InputRating(FormItem):
    """评分"""

    type: Literal["input-rating"] = Field(default="input-rating", init=False)
    """指定为 input-rating 渲染器"""
    value: Optional[int] = None
    """当前值"""
    half: bool = False
    """是否使用半星选择"""
    count: int = 5
    """总星数"""
    readOnly: bool = False
    """只读"""
    allowClear: bool = True
    """是否允许再次点击后清除"""
    colors: Union[str, DictStr] = {"2": "#abadb1", "3": "#787b81", "5": "#ffa900"}
    """星星被选中的颜色。 若传入字符串，则只有一种颜色。
    若传入对象，可自定义分段，键名为分段的界限值，键值为对应的类名"""
    inactiveColor: str = "#e7e7e8"
    """未被选中的星星的颜色"""
    texts: Optional[dict] = None
    """星星被选中时的提示文字。可自定义分段，键名为分段的界限值，键值为对应的类名"""
    textPosition: Literal["right", "left"] = "right"
    """文字的位置"""
    char: str = "★"
    """自定义字符"""
    className: Optional[str] = None
    """自定义样式类名"""
    charClassName: Optional[str] = None
    """自定义字符类名"""
    textClassName: Optional[str] = None
    """自定义文字类名"""
    onEvent: OnEvent[Literal["change"]] = None


class InputRange(FormItem):
    """滑块"""

    class Value(TypedDict):
        min: NotRequired[int]
        max: NotRequired[int]

    type: Literal["input-range"] = Field(default="input-range", init=False)
    """指定为 input-rang 渲染器"""
    className: Optional[str] = None
    """css 类名"""
    value: Optional[Union[int, str, Value, Tuple[int, int]]] = None
    """默认值"""
    min: Union[int, str] = 0
    """最小值，支持变量"""
    max: Union[int, str] = 100
    """最大值，支持变量"""
    disabled: bool = False
    """是否禁用"""
    step: Union[int, str] = 1
    """步长，支持变量"""
    showSteps: bool = False
    """是否显示步长"""
    parts: Union[int, List[int]] = 1
    """分割的块数 主持数组传入分块的节点"""
    marks: Optional[DictStrAny] = None  # TODO 确定类型
    """刻度标记- 支持自定义样式- 设置百分比"""
    tooltipVisible: bool = False
    """是否显示滑块标签"""
    tooltipPlacement: Literal["auto", "bottom", "left", "right"] = "auto"
    """滑块标签的位置，默认auto，方向自适应 前置条件：tooltipVisible 不为 false 时有效"""
    tipFormatter: Optional[str] = None
    """控制滑块标签显隐函数 前置条件：tooltipVisible 不为 false 时有效"""
    multiple: bool = False
    """支持选择范围"""
    joinValues: bool = True
    """默认为 true，选择的 value 会通过 delimiter 连接起来，
    否则直接将以{min: 1, max: 100}的形式提交 前置条件：开启multiple时有效"""
    delimiter: str = ","
    """分隔符"""
    unit: Optional[str] = None
    """单位"""
    clearable: bool = False
    """是否可清除 前置条件：开启showInput时有效"""
    showInput: bool = False
    """是否显示输入框"""
    onChange: Optional[str] = None
    """当 组件 的值发生改变时，会触发 onChange 事件，并把改变后的值作为参数传入"""
    onAfterChange: Optional[str] = None
    """与 onmouseup 触发时机一致，把当前值作为参数传入"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class InputRepeat(FormItem):
    """重复频率选择器"""

    type: Literal["input-repeat"] = Field(default="input-repeat", init=False)
    """指定为 input-repeat 渲染器"""
    options: Union[
        str,
        List[Literal["secondly", "minutely", "hourly", "daily", "weekdays", "weekly", "monthly", "yearly"]],
    ] = "hourly,daily,weekly,monthly"
    """可用配置"""
    placeholder: str = "不重复"
    """当不指定值时的说明。"""

    @validator("options")
    def validate_options(cls, v):
        if isinstance(v, list):
            return ",".join(v)
        return v


class InputRichText(FormItem):
    """富文本编辑器"""

    type: Literal["input-rich-text"] = Field(default="input-rich-text", init=False)
    """"指定为 input-rich-text 渲染器"""
    saveAsUbb: Optional[bool] = None
    """是否保存为 ubb 格式"""
    receiver: Optional[API] = None
    """默认的图片保存 API"""
    videoReceiver: Optional[API] = None
    """默认的视频保存 API"""
    fileField: Optional[str] = None
    """上传文件时的字段名"""
    size: Optional[Literal["md", "lg"]] = None
    """框的大小，可设置为 md 或者 lg"""
    options: Optional[DictStrAny] = None
    """需要参考 tinymce 或 froala 的文档"""
    buttons: Optional[List[str]] = None
    """froala 专用，配置显示的按钮，tinymce 可以通过前面的 options 设置 toolbar 字符串"""


class Select(FormItem):
    """下拉框

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/select"""

    class Overlay(TypedDict):
        width: NotRequired[Union[str, int]]
        align: NotRequired[Literal["left", "center", "right"]]

    type: Literal["select"] = Field(default="select", init=False)
    """指定为 select 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[Union[API, DataMapping]] = None
    """动态选项组"""
    autoComplete: Optional[API] = None
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
    filterOption: Optional[str] = None
    """(options: Option[], inputValue: string, option: {keys: string[]}) => Option[]"""
    createBtnLabel: str = "新增选项"
    """新增选项"""
    addControls: Optional[List[FormItem]] = None
    """自定义新增表单项"""
    addApi: Optional[API] = None
    """配置新增选项接口"""
    editable: bool = False
    """编辑选项"""
    editControls: Optional[List[FormItem]] = None
    """自定义编辑表单项"""
    editApi: Optional[API] = None
    """配置编辑选项接口"""
    removable: bool = False
    """删除选项"""
    deleteApi: Optional[API] = None
    """配置删除选项接口"""
    menuTpl: Optional[str] = None
    """支持配置自定义菜单"""
    clearable: Optional[bool] = None
    """单选模式下是否支持清空"""
    hideSelected: bool = False
    """隐藏已选选项"""
    mobileClassName: Optional[str] = None
    """移动端浮层类名"""
    selectMode: Optional[Literal["group", "table", "tree", "chained", "associated"]] = None
    """可选：group、table、tree、chained、associated。分别为：列表形式、表格形式、树形选择形式、级联选择形式，
    关联选择形式（与级联选择的区别在于，级联是无限极，而关联只有一级，关联左边可以是个 tree）。"""
    searchResultMode: Optional[str] = None
    """如果不设置将采用 selectMode 的值，可以单独配置，参考 selectMode，决定搜索结果的展示形式。"""
    columns: Optional[List[DictStrAny]] = None
    """当展示形式为 table 可以用来配置展示哪些列，跟 table 中的 columns 配置相似，只是只有展示功能。"""
    leftOptions: Optional[List[DictStrAny]] = None
    """当展示形式为 associated 时用来配置左边的选项集。"""
    leftMode: Literal["list", "tree"] = "list"
    """当展示形式为 associated 时用来配置左边的选择形式，支持 list 或者 tree。默认为 list。"""
    rightMode: Optional[Literal["list", "tree", "table", "chained"]] = None
    """当展示形式为 associated 时用来配置右边的选择形式，可选：list、table、tree、chained。"""
    maxTagCount: Optional[int] = None
    """标签的最大展示数量，超出数量后以收纳浮层的方式展示，仅在多选模式开启后生效"""
    overflowTagPopover: Optional[DictStrAny] = None  # TODO TooltipObject
    """收纳浮层的配置属性，详细配置参考Tooltip"""
    optionClassName: Optional[str] = None
    """选项 CSS 类名"""
    popOverContainerSelector: Optional[str] = None
    """弹层挂载位置选择器，会通过querySelector获取"""
    overlay: Optional[Overlay] = None
    """弹层宽度与对齐方式 2.8.0 以上版本"""
    showInvalidMatch: bool = False
    """选项值与选项组不匹配时选项值是否飘红"""
    onEvent: OnEvent[Literal["change", "blur", "focus", "add", "edit", "delete"]] = None


class InputSubForm(FormItem):
    """子表单"""

    type: Literal["input-sub-form"] = Field(default="input-sub-form", init=False)
    """指定为 input-sub-form 渲染器"""
    multiple: bool = False
    """是否为多选模式"""
    labelField: Optional[str] = None
    """当值中存在这个字段，则按钮名称将使用此字段的值来展示。"""
    btnLabel: str = "设置"
    """按钮默认名称"""
    minLength: int = 0
    """限制最小个数。"""
    maxLength: int = 0
    """限制最大个数。"""
    draggable: Optional[bool] = None
    """是否可拖拽排序"""
    addable: Optional[bool] = None
    """是否可新增"""
    removable: Optional[bool] = None
    """是否可删除"""
    addButtonClassName: str = ""
    """新增按钮 CSS 类名"""
    itemClassName: str = ""
    """值元素 CSS 类名"""
    itemsClassName: str = ""
    """值包裹元素 CSS 类名"""
    form: Optional[Form] = None
    """子表单配置，同 Form"""
    addButtonText: str = ""
    """自定义新增一项的文本"""
    showErrorMsg: bool = True
    """是否在左下角显示报错信息"""


class Switch(FormItem):
    """开关"""

    class IconSchema(TypedDict):
        type: NotRequired[Literal["icon"]]
        """指定为图标"""
        icon: NotRequired[str]
        """图标"""

    type: Literal["switch"] = Field(default="switch", init=False)
    """指定为 switch 渲染器"""
    option: Optional[str] = None
    """选项说明"""
    onText: Optional[Union[str, IconSchema]] = None
    """开启时的文本"""
    offText: Optional[Union[str, IconSchema]] = None
    """关闭时的文本"""
    trueValue: Union[bool, str, int] = True
    """标识真值"""
    falseValue: Union[bool, str, int] = False
    """标识假值"""
    size: Literal["sm", "md"] = "md"
    """开关大小"""
    onEvent: OnEvent[Literal["change"]] = None


class Static(FormItem):
    """静态展示/标签

    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/static"""

    type: Literal["static"] = Field(default="static", init=False)
    """指定为 static 渲染器"""

    class Json(FormItem):
        type: Literal["static-json"] = Field(default="static-json", init=False)
        """展示Json数据"""
        value: Optional[Union[DictStrAny, str]] = None
        """值"""

    class Date(FormItem):
        type: Literal["static-date"] = Field(default="static-date", init=False)
        """展示日期"""
        value: Optional[str] = None
        """值"""

    class Datetime(FormItem):
        """显示日期"""

        type: Literal["static-datetime"] = Field(default="static-datetime", init=False)
        """展示日期"""
        value: Union[int, str]
        """值"""

    class Mappping(FormItem):
        type: Literal["static-mapping"] = Field(default="static-mapping", init=False)
        """映射"""
        map: Optional[DictStrAny] = None
        """选项组"""
        value: Optional[str] = None
        """值"""

    class Progress(FormItem):
        type: Literal["static-progress"] = Field(default="static-progress", init=False)
        """进度"""
        value: Optional[str] = None
        """值"""

    class Image(FormItem):
        type: Literal["static-image"] = Field(default="static-image", init=False)
        """图片"""
        thumbMode: Optional[str] = None
        """预览图模式"""
        thumbRatio: Optional[str] = None
        """预览比例"""
        title: Optional[str] = None
        """图片标题"""
        imageCaption: Optional[str] = None
        """图片描述信息"""
        enlargeAble: bool = False
        """是否启用放大功能"""
        originalSrc: Optional[str] = None
        """大图地址"""


class InputTable(FormItem):
    """表格"""

    class AddItemAction(EventAction):
        class Args(TypedDict):
            index: NotRequired[int]
            item: Union[DictStrAny, List[DictStrAny]]

        actionType: Literal["addItem"] = Field(default="addItem", init=False)
        componentId: str
        groupType: Optional[str] = None
        args: Args

    class DeleteItemAction(EventAction):
        class Args(TypedDict):
            index: NotRequired[str]
            condition: NotRequired[str]

        actionType: Literal["deleteItem"] = Field(default="deleteItem", init=False)
        componentId: str
        groupType: Optional[str] = None
        args: Args

    class Column(TypedDict):
        quickEdit: NotRequired[Union[bool, DictStrAny]]
        quickEditOnUpdate: NotRequired[Union[bool, DictStrAny]]

    type: Literal["input-table"] = Field(default="input-table", init=False)
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
    addApi: Optional[API] = None
    """新增时提交的 API"""
    footerAddBtn: Optional[SchemaNode] = None
    """底部新增按钮配置"""
    updateApi: Optional[API] = None
    """修改时提交的 API"""
    deleteApi: Optional[API] = None
    """删除时提交的 API"""
    addBtnLabel: Optional[str] = None
    """增加按钮名称"""
    addBtnIcon: str = "plus"
    """增加按钮图标"""
    copyBtnLabel: Optional[str] = None
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
    minLength: Optional[Union[int, str]] = None
    """最小行数, 2.4.1版本后支持变量"""
    maxLength: Optional[Union[int, str]] = None
    """最大行数, 2.4.1版本后支持变量"""
    perPage: int = 10
    """设置一页显示多少条数据"""
    columns: List[Column] = []
    """列信息"""
    onEvent: OnEvent[
        Literal[
            "add",
            "addCofirm",
            "addSuccess",
            "addFail",
            "edit",
            "editConfirm",
            "editSuccess",
            "editFail",
            "delete",
            "deleteSuccess",
            "deleteFail",
            "change",
        ]
    ] = None


class InputTag(FormItem):
    """标签选择器"""

    type: Literal["input-tag"] = Field(default="input-tag", init=False)
    """指定为 input-tag 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    optionsTip: str = "最近您使用的标签"
    """选项提示"""
    source: Optional[API] = None
    """动态选项组"""
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
    clearable: bool = False
    """在有值的时候是否显示一个删除图标在右侧。"""
    resetValue: str = ""
    """删除后设置此配置项给定的值。"""
    max: Optional[int] = None
    """允许添加的标签的最大数量"""
    maxTagLength: Optional[int] = None
    """单个标签的最大文本长度"""
    maxTagCount: Optional[int] = None
    """标签的最大展示数量，超出数量后以收纳浮层的方式展示，仅在多选模式开启后生效"""
    overflowTagPopover: dict = {"placement": "top", "trigger": "hover", "showArrow": False, "offset": [0, -10]}
    """收纳浮层的配置属性，详细配置参考Tooltip"""
    enableBatchAdd: bool = False
    """	是否开启批量添加模式"""
    separator: str = "-"
    """开启批量添加后，输入多个标签的分隔符，支持传入多个符号，默认为"-"事件表"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class InputText(FormItem):
    """输入框"""

    type: Literal["input-text"] = Field(default="input-text", init=False)
    """指定为 input-text 渲染器 """

    class AddOn(AmisNode):
        type: Optional[Literal["text", "button", "submit"]] = None
        """	请选择 text 、button 或者 submit。"""
        label: Optional[Union[str, bool]] = None
        """文字说明"""
        position: Literal["left", "right"] = "right"
        """addOn位置"""

    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
    """动态选项组"""
    autoComplete: Optional[API] = None
    """自动补全"""
    multiple: bool = False
    """是否多选"""
    delimiter: str = ","
    """拼接符"""
    labelField: str = "label"
    """选项标签字段"""
    valueField: str = "value"
    """选项值字段"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    addOn: Optional[Union[SchemaNode, AddOn]] = None
    """输入框附加组件，比如附带一个提示文字，或者附带一个提交按钮。"""
    trimContents: Optional[bool] = None
    """是否去除首尾空白文本。"""
    creatable: Optional[bool] = None
    """是否可以创建，默认为可以，除非设置为 false 即只能选择选项中的值"""
    clearable: Optional[bool] = None
    """是否可清除"""
    resetValue: str = ""
    """清除后设置此配置项给定的值。"""
    prefix: str = ""
    """前缀"""
    suffix: str = ""
    """后缀"""
    showCounter: Optional[bool] = None
    """是否显示计数器"""
    minLength: Optional[int] = None
    """限制最小字数"""
    maxLength: Optional[int] = None
    """限制最大字数"""
    transform: Optional[dict] = None
    """自动转换值，可选 transform: { lowerCase: true, upperCase: true }"""
    borderMode: Literal["full", "half", "none"] = "full"
    """输入框边框模式，全边框，还是半边框，或者没边框"""
    inputControlClassName: Optional[str] = None
    """control 节点的 CSS 类名"""
    nativeInputClassName: Optional[str] = None
    """nativeInputClassName"""
    onEvent: OnEvent[Literal["click", "enter", "change", "blur", "focus"]] = None


class InputUrl(InputText):
    """URL输入框"""

    type: Literal["input-url"] = Field(default="input-url", init=False)
    """指定为 input-url 渲染器"""


class InputEmail(InputText):
    """邮箱输入框"""

    type: Literal["input-email"] = Field(default="input-email", init=False)
    """指定为 input-email 渲染器"""


class InputPassword(InputText):
    """密码输框"""

    type: Literal["input-password"] = Field(default="input-password", init=False)
    """指定为 input-password 渲染器"""
    revealPassword: bool = True
    """是否展示密码显/隐按钮"""


class Textarea(FormItem):
    """多行文本输入框"""

    type: Literal["textarea"] = Field(default="textarea", init=False)
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
    maxLength: Optional[int] = None
    """限制最大字数"""
    clearable: bool = False
    """是否可清除"""
    resetValue: str = ""
    """清除后设置此配置项给定的值。"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class InputTime(FormItem):
    """时间"""

    type: Literal["input-time"] = Field(default="input-time", init=False)
    """指定为 input-time 渲染器"""
    value: Optional[str] = None
    """默认值"""
    valueFormat: str = "X"
    """时间选择器值格式，更多格式类型请参考 moment"""
    displayFormat: str = "HH:mm"
    """时间选择器显示格式，即时间戳格式，更多格式类型请参考 moment"""
    placeholder: str = "请选择时间"
    """占位文本"""
    clearable: bool = True
    """ 是否可清除"""
    timeConstraints: Union[DictStrAny, bool] = True
    """请参考： react-datetime"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class InputTimeRange(FormItem):
    """时间范围"""

    type: Literal["input-time-range"] = Field(default="input-time-range", init=False)
    """指定为 input-time-range 渲染器"""
    valueFormat: str = "HH:mm"
    """时间范围选择器值格式"""
    displayFormat: str = "HH:mm"
    """时间范围选择器显示格式"""
    placeholder: str = "请选择时间范围"
    """占位文本"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""
    extraName: Optional[str] = None
    """是否存成两个字段"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class Transfer(FormItem):
    """穿梭器"""

    class ClearSearchAction(EventAction):
        actionType: Literal["clearSearch"] = Field(default="clearSearch", init=False)
        componentId: str
        left: Optional[bool] = None
        """左侧搜索"""
        right: Optional[bool] = None
        """右侧搜索"""

    type: Literal["transfer"] = Field(default="transfer", init=False)
    """指定为 transfer 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
    """动态选项组"""
    delimiter: Union[str, bool] = ","
    """拼接符"""
    joinValues: bool = True
    """拼接值"""
    extractValue: bool = False
    """提取值"""
    searchApi: Optional[API] = None
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
    """可选：list、table、tree、chained、associated。
    分别为：列表形式、表格形式、树形选择形式、级联选择形式，
    关联选择形式（与级联选择的区别在于，级联是无限极，而关联只有一级，关联左边可以是个 tree）。"""
    searchResultMode: Optional[str] = None
    """如果不设置将采用 selectMode 的值，可以单独配置，参考 selectMode，决定搜索结果的展示形式。"""
    searchable: bool = False
    """当设置为 true 时表示可以通过输入部分内容检索出选项。"""
    searchPlaceholder: Optional[str] = None
    """左侧列表搜索框提示"""
    columns: Optional[List[DictStrAny]] = None  # TODO column dict
    """当展示形式为 table 可以用来配置展示哪些列，跟 table 中的 columns 配置相似，只是只有展示功能。"""
    leftOptions: Optional[List[DictStrAny]] = None  # TODO option dict
    """当展示形式为 associated 时用来配置左边的选项集。"""
    leftMode: Optional[Literal["list", "tree"]] = None
    """当展示形式为 associated 时用来配置左边的选择形式，支持 list 或者 tree。默认为 list。"""
    rightMode: Optional[Literal["list", "table", "tree", "chained"]] = None
    """当展示形式为 associated 时用来配置右边的选择形式，可选：list、table、tree、chained。"""
    resultSearchable: bool = False
    """结果（右则）列表的检索功能，当设置为 true 时，
    可以通过输入检索模糊匹配检索内容（目前树的延时加载不支持结果搜索功能）"""
    resultSearchPlaceholder: Optional[str] = None
    """右侧列表搜索框提示"""
    menuTpl: Optional[SchemaNode] = None
    """用来自定义选项展示"""
    valueTpl: Optional[SchemaNode] = None
    """用来自定义值的展示"""
    multiple: Optional[bool] = None
    """是否多选"""
    itemHeight: int = 32
    """每个选项的高度，用于虚拟渲染"""
    virtualThreshold: int = 100
    """在选项数量超过多少时开启虚拟渲染"""
    onEvent: OnEvent[Literal["change", "selectAll"]] = None


class TransferPicker(Transfer):
    """穿梭选择器"""

    type: Literal["transfer-picker"] = Field(default="transfer-picker", init=False)
    """指定为 transfer-picker 渲染器"""
    borderMode: Optional[Literal["full", "half", "none"]] = None
    """边框模式"""
    pickerSize: Optional[Literal["xs", "sm", "md", "lg", "xl", "full"]] = None
    """弹窗大小"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class TabsTransfer(Transfer):
    """组合穿梭器"""

    type: Literal["tabs-transfer"] = Field(default="tabs-transfer", init=False)
    """指定为 tabs-transfer 渲染器"""
    onEvent: OnEvent[Literal["change", "tab-change"]] = None


class TabsTransferPicker(Transfer):
    """组合穿梭选择器"""

    type: Literal["tabs-transfer-picker"] = Field(default="tabs-transfer-picker", init=False)
    """指定为 tabs-transfer-picker 渲染器"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class InputTree(FormItem):
    """树形选择框"""

    class ExpandAction(EventAction):
        """展开指定层级"""

        actionType: Literal["expand"] = Field(default="expand", init=False)
        componentId: str
        openLevel: Optional[int] = None

    class CollapseAction(EventAction):
        """收起"""

        actionType: Literal["collapse"] = Field(default="collapse", init=False)
        componentId: str

    type: Literal["input-tree"] = Field(default="input-tree", init=False)
    """指定为 input-tree 渲染器"""
    options: Optional[OptionsType] = None
    """选项组"""
    source: Optional[API] = None
    """动态选项组"""
    autoComplete: Optional[API] = None
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
    addControls: Optional[List[FormItem]] = None
    """自定义新增表单项"""
    addApi: Optional[API] = None
    """配置新增选项接口"""
    editable: Optional[bool] = None
    """False  # 编辑选项"""
    editControls: Optional[List[FormItem]] = None
    """自定义编辑表单项"""
    editApi: Optional[API] = None
    """配置编辑选项接口"""
    removable: bool = False
    """删除选项"""
    deleteApi: Optional[API] = None
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
    showOutline: bool = False
    """是否显示树层级展开线"""
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
    minLength: Optional[int] = None
    """最少选中的节点数"""
    maxLength: Optional[int] = None
    """最多选中的节点数"""
    treeContainerClassName: Optional[str] = None
    """tree 最外层容器类名"""
    enableNodePath: bool = False
    """是否开启节点路径模式"""
    pathSeparator: str = "/"
    """节点路径的分隔符，enableNodePath为true时生效"""
    highlightTxt: Optional[str] = None
    """标签中需要高亮的字符，支持变量"""
    itemHeight: int = 32
    """每个选项的高度，用于虚拟渲染"""
    virtualThreshold: int = 100
    """在选项数量超过多少时开启虚拟渲染"""
    menuTpl: Optional[str] = None
    """选项自定义渲染 HTML 片段"""
    enableDefaultIcon: bool = True
    """是否为选项添加默认的前缀 Icon，父节点默认为folder，叶节点默认为file"""
    heightAuto: bool = False
    """默认高度会有个 maxHeight，即超过一定高度就会内部滚动，如果希望自动增长请设置此属性"""
    onEvent: OnEvent[Literal["change", "add", "edit", "delete", "loadFinished"]] = None


class TreeSelect(InputTree):
    """树形选择器"""

    type: Literal["tree-select"] = Field(default="tree-select", init=False)
    """指定为 tree-select 渲染器"""
    hideNodePathLabel: bool = False
    """是否隐藏选择框中已选择节点的路径 label 信息"""
    onlyLeaf: bool = False
    """只允许选择叶子节点"""
    searchable: bool = False
    """是否可检索，仅在 type 为 tree-select 的时候生效"""
    onEvent: OnEvent[Literal["change", "blur", "focus", "add", "edit", "delete", "loadFinished"]] = None


class InputYear(InputDate):
    """年份选择"""

    type: Literal["input-year"] = Field(default="input-year", init=False)
    """指定为 input-year 渲染器"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class InputYearRange(FormItem):
    """年份范围"""

    type: Literal["input-year-range"] = Field(default="input-year-range", init=False)
    """指定为 input-year-range 渲染器"""
    valueFormat: str = "X"
    """日期时间选择器值格式"""
    displayFormat: str = "YYYY"
    """日期时间选择器显示格式"""
    placeholder: str = "请选择年份范围"
    """占位文本"""
    minDate: Optional[str] = None
    """限制最小日期时间，用法同 限制范围"""
    maxDate: Optional[str] = None
    """限制最大日期时间，用法同 限制范围"""
    minDuration: Optional[str] = None
    """限制最小跨度，如： 2days"""
    maxDuration: Optional[str] = None
    """限制最大跨度，如：1year"""
    utc: bool = False
    """保存 UTC 值"""
    clearable: bool = True
    """是否可清除"""
    embed: bool = False
    """是否内联模式"""
    animation: bool = True
    """是否启用游标动画"""
    onEvent: OnEvent[Literal["change", "blur", "focus"]] = None


class JSONSchema(FormItem):
    """JSON生成页面"""

    type: Literal["json-schema"] = Field(default="json-schema", init=False)
    """指定为 json-schema 渲染器"""
    schema_: Union[str, DictStrAny] = Field(alias="schema")
    """指定 json-schema"""


class JSONSchemaEditor(FormItem):
    """JSON页面编辑器"""

    class Placeholder(TypedDict):
        key: NotRequired[str]
        title: NotRequired[str]
        description: NotRequired[str]
        default: NotRequired[str]
        empty: NotRequired[str]

    type: Literal["json-schema-editor"] = Field(default="json-schema-editor", init=False)
    """指定为 json-schema-editor 渲染器"""
    rootTypeMutable: bool = False
    """顶级类型是否可配置"""
    showRootInfo: bool = False
    """是否显示顶级类型信息"""
    disabledTypes: Optional[
        List[Literal["string", "number", "interger", "object", "number", "array", "boolean", "null"]]
    ] = None
    """用来禁用默认数据类型，默认类型有：string、number、interger、object、number、array、boolean、null"""
    definitions: Optional[DictStrAny] = None
    """用来配置预设类型"""
    placeholder: Optional[Placeholder] = None
    """属性输入控件的占位提示文本"""


__all__ = [
    "Form",
    "Column",
    "FormItem",
    "Control",
    "Options",
    "InputArray",
    "ButtonToolbar",
    "ButtonGroupSelect",
    "ChainedSelect",
    "Checkbox",
    "Checkboxes",
    "InputCity",
    "InputColor",
    "Combo",
    "ConditionBuilder",
    "InputDate",
    "InputDatetime",
    "InputMonth",
    "InputDatetimeRange",
    "InputMonthRange",
    "InputKV",
    "InputKVS",
    "InputFormula",
    "DiffEditor",
    "Editor",
    "FieldSet",
    "InputExcel",
    "InputFile",
    "Formula",
    "Group",
    "Hidden",
    "InputImage",
    "InputGroup",
    "ListSelect",
    "LocationPicker",
    "UUID",
    "MatrixCheckboxes",
    "NestedSelect",
    "InputNumber",
    "Picker",
    "InputQuarter",
    "Radio",
    "Radios",
    "ChartRadios",
    "InputRating",
    "InputRange",
    "InputRepeat",
    "InputRichText",
    "Select",
    "InputSubForm",
    "Switch",
    "Static",
    "InputTable",
    "InputTag",
    "InputText",
    "InputUrl",
    "InputEmail",
    "InputPassword",
    "Textarea",
    "InputTime",
    "InputTimeRange",
    "Transfer",
    "TransferPicker",
    "TabsTransfer",
    "TabsTransferPicker",
    "InputTree",
    "TreeSelect",
    "InputYear",
    "InputYearRange",
    "JSONSchema",
    "JSONSchemaEditor",
]
