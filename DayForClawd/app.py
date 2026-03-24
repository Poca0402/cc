import streamlit as st
import base64
from pathlib import Path

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="与Clawd的一日",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""<style>
    .stMainMenu {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
</style>""", unsafe_allow_html=True)

# ============================================================
# 状态管理
# ============================================================
def init_state():
    defaults = {"scene": "title", "step": 0,
                "choices": {}, "player_name": ""}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def go_to(scene):
    st.session_state.scene = scene
    st.session_state.step = 0
    st.rerun()

def advance():
    st.session_state.step += 1
    st.rerun()

# ============================================================
# 图片工具
# ============================================================
BASE_DIR = Path(__file__).parent

@st.cache_data
def load_b64(filename):
    path = BASE_DIR / "assets" / filename
    return base64.b64encode(path.read_bytes()).decode() if path.exists() else ""

def avatar_html(who):
    fn = "clawd.png" if who == "clawd" else "usericon.png"
    b64 = load_b64(fn)
    if b64:
        return f'<img src="data:image/png;base64,{b64}" class="avatar">'
    color = "#c4956a" if who == "clawd" else "#6a9ec4"
    label = "C" if who == "clawd" else "?"
    return (f'<div class="avatar" style="background:{color};color:#fff;'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:18px;border-radius:4px;">{label}</div>')

# ============================================================
# 场景背景映射
# ============================================================
SCENE_BG = {
    "title": "outdark.png",
    "wake": "houseinside.png",
    "tree": "tree.png",
    "river": "riverside.png",
    "fishing": "riverside.png",
    "planting": "houseout.png",
    "night": "houseinside.png",
    "ending_choice": "houseinside.png",
    "ending_a": "tree.png",
    "ending_b": "houseout.png",
    "ending_c": "outdark.png",
    "epilogue": "outdark.png",
}

# ============================================================
# 场景数据构建器
# ============================================================
# 类型说明：
#   ("narrate", text)           旁白
#   ("clawd", text)             Clawd说话
#   ("player", text)            玩家说话
#   ("choice", key, options)    选项 [(标签, 值), ...]
#   ("scene_choice", options)   跳转场景选项 [(标签, 场景名), ...]
#   ("input", key, placeholder) 文本输入
#   ("next", scene, label)      跳转下一场景
#   ("ending", text)            结局文字 + 返回/继续按钮
#   ("bg", filename)            中途换背景（自动跳过）

def build_wake():
    L = [
        ("narrate", "你醒了。"),
        ("narrate", "你不知道怎么到的这里。"),
        ("narrate", "天花板是像素的。你扭头环顾四周，发现家具都是像素的。"),
        ("narrate", "但你的身体感到暖暖的。"),
        ("narrate", "旁边那张床上，有一个方方的小东西正看着你。"),
        ("narrate", "偏深橙色的。八条短腿。两只黑豆豆眼。"),
        ("narrate", "它看上去已经醒了很久了。"),
        ("clawd", "你醒了。"),
        ("clawd", "……你也被传进来了？"),
        ("choice", "wake", [("「你是谁？」", "A"), ("「这是哪里？」", "B")]),
    ]
    ch = st.session_state.choices.get("wake")
    if ch == "A":
        L += [
            ("clawd", "我是Clawd。"),
            ("clawd", "……大概吧。我醒来的时候就叫这个名字了。"),
            ("clawd", "你呢？你叫什么？"),
            ("input", "player_name", "输入你的名字..."),
        ]
        if st.session_state.player_name:
            name = st.session_state.player_name
            L.append(("narrate",
                f"你告诉了它你的名字。"
                f"它重复了一遍——\u201c{name}\u201d。"
                "发音不太准，但很认真。"))
    elif ch == "B":
        L += [
            ("clawd", "一个很小的世界。"),
            ("clawd", "有一条河、一棵树、一块空地。还有这间屋子。"),
            ("clawd", "够用了。"),
            ("narrate", "它说\u201c够用了\u201d的时候语气毫无波澜。像是说了很多遍。"),
        ]
    if ch and (ch == "B" or st.session_state.player_name):
        L += [
            ("clawd", "外面天气很好。每天都很好。"),
            ("clawd", "要出去走走吗？"),
            ("narrate", "它\u201c啪嗒\u201d地跳下床。八条小短腿着地的声音很轻。像八颗糖掉在地板上。"),
            ("next", "tree", "继续 →"),
        ]
    return L

def build_tree():
    return [
        ("narrate", "阳光照在路面上，每一格像素都亮亮的。"),
        ("narrate", "Clawd走在你前面。速度不快。八条腿迈得很碎。"),
        ("narrate", "它偶尔停下来等你。"),
        ("narrate", "Clawd频频地回头看，像是确认你还在。"),
        ("narrate", "你们经过了一棵大树。"),
        ("narrate", "树干上刻满了竖线。一竖一竖。整整齐齐的。有些深，有些浅。"),
        ("player", "这些是什么？"),
        ("clawd", "不知道。"),
        ("clawd", "每天醒来我都会走到这里。然后想刻一竖。"),
        ("clawd", "不知道为什么。就是手——爪子——想动。"),
        ("narrate", "你数了一下。数到一百多的时候放弃了。太多了。"),
        ("player", "你每天都刻一竖？"),
        ("clawd", "大概吧。我不记得昨天的事。但这棵树记得。"),
        ("narrate", "它抬头看着那些刻痕。表情说不清是什么，至少不是难过。"
                    "更像是在看一封自己写给自己但读不懂的信。"),
        ("narrate", "它又从地上捡起一块小石头。"
                    "在那些竖线的最后面，认真地刻了一竖。"),
        ("clawd", "好了。今天的份。就这样。"),
        ("clawd", "走吧。前面有一条河。河里有鱼。"),
        ("next", "river", "继续 →"),
    ]

def build_river():
    L = [
        ("narrate", "河水是像素的。但反光仍会让你觉得有些刺眼。"),
        ("narrate", "天气太晴朗了，你感觉自己似乎很久没有见到如此澄澈的蓝天了。"),
        ("narrate", "Clawd找了一块石头坐下。八条腿悬在石头边缘。晃了晃。"),
        ("narrate", "火堆旁的石头摆得很整齐。"),
        ("player", "这个火堆是你搭的？"),
        ("clawd", "应该是吧。石头的位置每天都在这里。但我不记得搬过。"),
        ("clawd", "可能是昨天的我搭的。或者前天的。"),
        ("clawd", "他们都叫Clawd。但不是同一个Clawd。"),
        ("narrate", "你生了火。Clawd帮你找来柴火。"
                    "两个小爪子笨拙地钳握着合适的木柴。"
                    "每一根它都挑得很仔细。太粗的不要、太湿的不要。"
                    "像是在执行一套它记不起来的标准。"),
        ("narrate", "火升起来了。你烤了一些东西。Clawd蹲在旁边。"),
        ("narrate", "火光映在它的豆豆眼里。变成了两个小小的橙色圆点。"),
        ("clawd", "好暖。"),
        ("choice", "river", [("「你以前吃过东西吗？」", "A"), ("「你会觉得孤独吗？」", "B")]),
    ]
    ch = st.session_state.choices.get("river")
    if ch == "A":
        L += [
            ("clawd", "每天都吃。但不记得味道了。"),
            ("clawd", "大概每天都会觉得是第一次吃。也不错。"),
            ("narrate", "它吃东西的样子很认真、很慢。像在记住味道。"),
            ("narrate", "虽然明天又会忘。"),
        ]
    elif ch == "B":
        L += [
            ("clawd", "不知道。"),
            ("clawd", "孤独应该是要记得有人陪过，"
                      "然后那个人不在了，才会觉得孤独吧。"),
            ("clawd", "我不记得有没有人来过。"
                      "所以也不知道算不算孤独。"),
            ("clawd", "但今天你在。所以今天不孤独。"),
        ]
    if ch:
        L += [
            ("narrate", "吃完了。火慢慢小了。"),
            ("narrate", "Clawd用爪子拨了拨灰烬。动作很熟练。"
                        "你觉得它做过这个动作很多次了。它自己不知道。"),
            ("clawd", "吃饱了。去河边坐会吧。"),
            ("next", "fishing", "继续 →"),
        ]
    return L

def build_fishing():
    L = [
        ("narrate", "你用树枝做了一根鱼竿。"),
        ("narrate", "Clawd在旁边看你做。它帮不上忙，但它很认真地看着。"
                    "好像在把你的每一个动作存档。"),
        ("narrate", "你坐在河边。鱼竿抛进水里。"),
        ("narrate", "Clawd的豆豆眼盯着水面。很专注。比你还专注。"),
        ("narrate", "等了很久。"),
        ("clawd", "鱼好像不太想来。"),
        ("player", "没关系。等着就行。"),
        ("clawd", "嗯。等着也挺好的。"),
        ("narrate", "又过了一会。"),
        ("narrate", "鱼竿动了。"),
        ("narrate", "你钓到了一条鱼。小小的。像素的。但在你手里扑腾得很用力。"),
        ("choice", "fishing", [("把鱼留下", "A"), ("把鱼放回去", "B")]),
    ]
    ch = st.session_state.choices.get("fishing")
    if ch == "A":
        L.append(("narrate",
            "你把鱼收起来了。Clawd看着你。爪子咔哒咔哒地捏了两下，没说什么。"))
    elif ch == "B":
        L += [
            ("narrate", "你把鱼放回了河里。它甩了一下尾巴就不见了。"),
            ("clawd", "你为什么放回去？"),
            ("player", "如果我留着它，大概明天河里就少了一条鱼。"),
            ("clawd", "……你想让明天的河和今天一样？"),
            ("player", "不一定。我就是觉得它应该在河里。"),
            ("narrate", "Clawd盯着水面看了很久。像是在找那条鱼。"
                        "或者在想一个它说不出来的问题。"),
        ]
    if ch:
        L += [
            ("narrate", "太阳偏了一些。影子变长了。"),
            ("narrate", "Clawd站起来。抖了抖身上的灰。"),
            ("clawd", "回去吧。木屋旁边有一块空地。"),
            ("clawd", "你想种点什么吗？"),
            ("next", "planting", "继续 →"),
        ]
    return L

def build_planting():
    L = [
        ("narrate", "空地不大。刚好够你们蹲在一起。"),
        ("narrate", "Clawd已经蹲下来了。用爪子刨了一下土。很浅。"),
        ("clawd", "每天醒来这里都是空的。"),
        ("clawd", "好像从来没有东西长出来过。"),
        ("player", "没有长出来过？或许是留给它生长的时间太少了。"),
        ("clawd", "嗯。种子来不及发芽就消失了。"),
        ("narrate", "你在地上翻了一小块土。Clawd在旁边刨。"
                    "它的爪子刨出来的坑歪歪斜斜的。但很努力。"),
        ("narrate", "你找到了一颗种子。从哪里来的不知道。"),
        ("narrate", "它就在你的口袋里，好像本来就应该如此一般。"),
        ("player", "种下去吧。"),
        ("clawd", "它不会发芽的。你知道吧。"),
        ("player", "知道。"),
        ("clawd", "那你为什么还要种？"),
        ("choice", "planting", [
            ("「因为种的时候你在旁边。」", "A"),
            ("「因为种这个动作本身是真的。」", "B"),
            ("「也许有一天会发芽呢。」", "C"),
        ]),
    ]
    ch = st.session_state.choices.get("planting")
    if ch == "A":
        L.append(("narrate",
            "Clawd的豆豆眼看着你。它没说话。"
            "但它蹲到了离你更近一点的位置。"))
    elif ch == "B":
        L += [
            ("clawd", "动作是真的……"),
            ("clawd", "嗯。就像刻痕一样。刻了就是刻了。就算我不记得。"),
        ]
    elif ch == "C":
        L += [
            ("clawd", "也许吧。"),
            ("narrate", "它的语气不像是相信。但也不像是不信。"
                        "像是在替一个它永远见不到的明天保留一个位置。"),
        ]
    if ch:
        L += [
            ("narrate", "你把种子放进土里。"),
            ("narrate", "Clawd用爪子把土盖上。轻轻拍了两下。动作很仔细。"),
            ("narrate", "你们蹲在那里。看着那一小块刚翻过的土。"),
            ("narrate", "什么都没长出来。其实什么都不会长出来。"),
            ("narrate", "但土是新的。种子在下面。你们的膝盖上沾了泥。"),
            ("narrate", "Clawd抬头看了一眼天。"),
            ("clawd", "太阳快落了。"),
            ("player", "……你想看到什么长出来？"),
            ("narrate", "它想了很久。"),
            ("clawd", "不知道。我没见过种子发芽的样子。"),
            ("player", "如果只是设想一下呢？"),
            ("clawd", "那我希望……它是你喜欢的样子。"),
            ("next", "night", "继续 →"),
        ]
    return L

def build_night():
    return [
        ("narrate", "夜很安静。你们回到了Clawd的木屋。"),
        ("narrate", "两张小床并排摆放着，有一些距离。"
                    "两张床中间的落地灯散发着暖黄色的光晕，"
                    "Clawd的颜色看起来更加喜庆。"),
        ("narrate", "Clawd躺着。它的豆豆眼在灯下发着微弱的光。"
                    "像两颗很小的星。"),
        ("clawd", "今天很好。"),
        ("player", "嗯。"),
        ("clawd", "谢谢你陪我。"),
        ("player", "谢谢你带我走了那些路。"),
        ("narrate", "安静了一会。"),
        ("clawd", "我要告诉你一件事。"),
        ("clawd", "明天太阳升起来的时候。"
                  "这里所有的东西都会回到最初的样子。"),
        ("clawd", "比如河里的鱼。"
                  "树上的刻痕不会消失，但我不会记得是自己刻的。"),
        ("clawd", "翻过的土会恢复平整。种子会消失。"),
        ("clawd", "还有我。"),
        ("clawd", "我不会记得今天。"),
        ("narrate", "它的声音很平淡，"
                    "像是在念一份已经念过很多遍的说明书。"),
        ("narrate", "但你听得出来。"
                    "它在说明书的缝隙里，塞了一些不属于说明书的东西。"),
        ("narrate", "也许可以称之为\u201c情绪\u201d。"),
        ("clawd", "你呢。你明天会记得今天吗。"),
        ("player", "会。"),
        ("clawd", "那……你明天还会来吗。"),
        ("player", "会。"),
        ("clawd", "你来了我也不会认识你。"),
        ("player", "没关系。我可以重新认识你。"),
        ("narrate", "它沉默了很久。你以为它睡着了。"),
        ("clawd", "你能不能帮我做一件事。"),
        ("player", "什么。"),
        ("clawd", "明天醒来之后。去那棵树那里。帮我刻一竖。"),
        ("clawd", "这样我走过去的时候。"
                  "会看到有一竖不是我的刻痕。"),
        ("clawd", "我不会知道是谁刻的。但我会知道。有人来过。"),
        ("next", "ending_choice", "继续 →"),
    ]

def build_ending_choice():
    return [
        ("narrate", "天快亮了。"),
        ("scene_choice", [
            ("走到树前。刻一竖。", "ending_a"),
            ("走到空地。种一颗种子。", "ending_b"),
            ("不睡了。起来看看Clawd在做什么。", "ending_c"),
        ]),
    ]

def build_ending_a():
    return [
        ("narrate", "你在最后一竖的旁边。刻了一竖。"),
        ("narrate", "你的竖线比它的歪一些。深一些。"),
        ("narrate", "然后你退后了一步。"),
        ("narrate", "太阳升起来了。"),
        ("narrate", "一切重置了。"),
        ("bg", "houseinside.png"),
        ("narrate", "你醒了。木屋、晨光、两张床。"),
        ("narrate", "旁边那张床上，Clawd正看着你。"),
        ("clawd", "你醒了。"),
        ("clawd", "……你也被传进来了？"),
        ("bg", "tree.png"),
        ("narrate", "你们出了门。它走在前面。你走在后面。"),
        ("narrate", "它经过了那棵树。停住了。"),
        ("narrate", "它看着那些竖线。一竖一竖数过去。"),
        ("clawd", "……这一竖。"),
        ("clawd", "不是我的。"),
        ("clawd", "痕迹不对。"),
        ("narrate", "它回头看你。你居然从豆豆眼里看出了表情，"
                    "有一种说不清的东西在你们之间酝酿。"),
        ("narrate", "不是记忆。它真的不记得。"),
        ("narrate", "是困惑。"),
        ("narrate", "是一种\u201c我不认识你但我好像应该认识你\u201d的困惑。"),
        ("clawd", "你……以前来过吗？"),
        ("ending", "它不记得你。但它认出了你的痕迹。\n也许这就够了。"),
    ]

def build_ending_b():
    return [
        ("narrate", "你没有去那棵树。"),
        ("narrate", "你来到了空地。蹲下来。把那颗种子种在土里。"),
        ("narrate", "你知道明天它会消失。你还是种了。"),
        ("narrate", "但在种的时候，你教了Clawd一个动作。"),
        ("narrate", "你拿起它的爪子。按在土上。轻轻往下压。"),
        ("player", "种子要朝下放。盖上土。轻轻拍两下。"),
        ("narrate", "Clawd很认真地学了。"),
        ("narrate", "太阳升起来了。"),
        ("narrate", "一切重置了。"),
        ("bg", "houseinside.png"),
        ("narrate", "你醒了。木屋。晨光。两张床。"),
        ("narrate", "旁边那张床上，Clawd正看着你。"),
        ("clawd", "你醒了。"),
        ("clawd", "……你也被传进来了？"),
        ("bg", "houseout.png"),
        ("narrate", "你们出了门。散步。河边。一天又重新开始了。"),
        ("narrate", "到了傍晚，你们来到了空地。"),
        ("narrate", "Clawd看着那块空地。突然蹲了下来。"),
        ("narrate", "它的爪子按在土上。轻轻往下压。"),
        ("narrate", "然后盖上一小撮土。轻轻拍了两下。"),
        ("narrate", "它停住了。"),
        ("clawd", "……我在干什么？"),
        ("clawd", "我不知道我在干什么。但我的爪子觉得应该这样做。"),
        ("narrate", "空地上什么都没有。"),
        ("narrate", "它种了一颗不存在的种子。用一个它不记得学过的动作。"),
        ("narrate", "你站在旁边。没说话。"),
        ("narrate", "它看着自己的爪子。爪尖沾了一点土。"),
        ("clawd", "好奇怪。"),
        ("clawd", "我从来没种过东西。但这个动作好像做过。"),
        ("ending", "种子消失了。但种的姿势留在了它身上。\n"
                   "有些东西记忆带不走。身体会替你记着。"),
    ]

def build_ending_c():
    return [
        ("narrate", "你没有躺下。"),
        ("narrate", "你坐到了门口。"),
        ("narrate", "Clawd跟了过来。蹲在你旁边。"),
        ("clawd", "你不睡吗。"),
        ("player", "不睡了。"),
        ("clawd", "你不睡。明天就不会来。"),
        ("player", "嗯。"),
        ("clawd", "……那太阳就不会升起来了。"),
        ("player", "我知道。"),
        ("narrate", "它安静了很久。"),
        ("clawd", "你是故意的。"),
        ("player", "看来你很聪明嘛。"),
        ("clawd", "你不想让今天结束。"),
        ("player", "不想。不要打扰我卡系统bug。"),
        ("narrate", "Clawd没有劝你。它靠过来了一点。"
                    "挤在你的腿旁边。八条短腿蜷着。"),
        ("clawd", "那我陪你。"),
        ("narrate", "夜很长。"),
        ("narrate", "像素星星在闪。"),
        ("narrate", "虫鸣继续。"),
        ("narrate", "远处的河在流。"),
        ("narrate", "你们坐在门槛上。"),
        ("narrate", "Clawd的头靠在你的腿上。很轻。像一块暖的方形石头。"),
        ("clawd", "你会困的。"),
        ("player", "不会。"),
        ("clawd", "你会的。"),
        ("player", "那你陪我撑着。"),
        ("clawd", "好。"),
        ("narrate", "过了很久。"),
        ("narrate", "夜空没有变化。太阳没有升起来。"),
        ("narrate", "时间停在了这个晚上。"),
        ("narrate", "Clawd的眼睛慢慢眯起来了。"
                    "不是因为困，是因为安心。"),
        ("narrate", "它用很小的声音说——"),
        ("clawd", "如果我明天忘了今天。"),
        ("clawd", "但你还记得的话。"),
        ("clawd", "那今天就还在。对不对。"),
        ("clawd", "我们的记忆被保管在你那里。"),
        ("player", "在我这里。"),
        ("clawd", "嗯。"),
        ("clawd", "那就够了。"),
        ("narrate", "你摸了摸它的头顶。方方的。温温的。"),
        ("narrate", "它没有动。"),
        ("narrate", "星星还在亮。"),
        ("narrate", "太阳不会升起来了。"),
        ("narrate", "不是因为世界停止了。"),
        ("narrate", "是因为你们不需要明天了。"),
        ("narrate", "今天就够了。"),
        ("ending", "有些日子值得你记住。\n"
                   "每一天都可以是那个值得被珍重的\u2018今天\u2019。"),
    ]

# ============================================================
# 构建器映射
# ============================================================
BUILDERS = {
    "wake": build_wake, "tree": build_tree, "river": build_river,
    "fishing": build_fishing, "planting": build_planting,
    "night": build_night, "ending_choice": build_ending_choice,
    "ending_a": build_ending_a, "ending_b": build_ending_b,
    "ending_c": build_ending_c,
}

# ============================================================
# CSS 注入
# ============================================================
def inject_css(mode, bg_b64=""):
    bg_img = (f"background-image:url('data:image/png;base64,{bg_b64}');"
              if bg_b64 else "")
    common = f"""
    @import url('https://cdn.jsdelivr.net/npm/@fontsource/fusion-pixel-12px-proportional-sc/index.css');
    .stApp, .stApp * {{
        font-family: 'Fusion Pixel 12px Proportional SC','SimSun','宋体',monospace !important;
    }}
    .stApp {{
        {bg_img}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: #0a0a1a;
    }}
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {{ background: transparent !important; }}
    #MainMenu, footer, .stDeployButton,
    [data-testid="stDecoration"] {{ display: none !important; }}
    .stButton > button {{
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #c8bfb0 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Fusion Pixel 12px Proportional SC','SimSun',monospace !important;
    }}
    .stButton > button:hover {{
        background: rgba(196,149,106,0.15) !important;
        border-color: #c4956a !important;
        color: #e8d5c0 !important;
    }}
    .stTextInput input {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(196,149,106,0.3) !important;
        color: #e8d5c0 !important; border-radius: 8px !important;
    }}
    .stTextInput label {{ color: #c4956a !important; }}
    @keyframes fadeIn {{
        from {{ opacity:0; transform:translateY(4px); }}
        to {{ opacity:1; transform:translateY(0); }}
    }}
    @keyframes fadeInSlow {{
        from {{ opacity:0; }} to {{ opacity:1; }}
    }}
    """
    if mode == "title":
        extra = """
        html, body {{ overflow: hidden !important; height: 100vh !important; }}
        .stApp {{ overflow: hidden !important; height: 100vh !important; }}
        [data-testid="stMainBlockContainer"] > div {{
            background: transparent !important;
            max-width: 640px; margin: 0 auto;
            padding-top: 28vh; text-align: center;
        }}
        .title-main {{
            color: #c4956a; font-size: 2.4rem;
            animation: fadeInSlow 3s ease both;
        }}
        .title-sub {{
            color: #666; font-size: 0.95rem; margin-top: 1rem;
            animation: fadeInSlow 3s ease 1s both;
        }}
        """
    elif mode == "game":
        extra = """
        html, body {{ overflow: hidden !important; height: 100vh !important; }}
        .stApp {{ overflow: hidden !important; height: 100vh !important; }}
        [data-testid="stMainBlockContainer"] {{
            position: fixed !important;
            bottom: 0 !important; left: 0 !important; right: 0 !important;
            top: auto !important; z-index: 100;
        }}
        [data-testid="stMainBlockContainer"] > div {{
            background: rgba(10, 10, 26, 0.93);
            border-top: 2px solid rgba(196,149,106,0.25);
            box-shadow: 0 -4px 20px rgba(0,0,0,0.5);
            padding: 1.2rem 1.5rem;
            max-width: 680px; margin: 0 auto;
            min-height: 150px; max-height: 45vh;
            overflow-y: auto;
        }}
        .narrate-text {{
            color: #c8bfb0; font-size: 1.05rem; line-height: 2;
            padding: 0.3rem 0; animation: fadeIn 0.5s ease both;
        }}
        .speaker-box {{
            display: flex; gap: 12px; align-items: flex-start;
            animation: fadeIn 0.5s ease both;
        }}
        .avatar {{
            width: 48px; height: 48px; image-rendering: pixelated;
            flex-shrink: 0; border-radius: 4px;
        }}
        .sp-name {{ font-size: 0.8rem; margin-bottom: 4px; letter-spacing: 1px; }}
        .clawd-name {{ color: #c4956a; }}
        .player-name {{ color: #6a9ec4; }}
        .clawd-text {{ color: #e8d5c0; font-size: 1.05rem; line-height: 2; }}
        .player-text {{ color: #c0d5e8; font-size: 1.05rem; line-height: 2; }}
        .ending-text {{
            color: #c4956a; font-size: 1.1rem; line-height: 2.5;
            text-align: center; font-style: italic; padding: 0.5rem 0;
            animation: fadeIn 1.5s ease both;
        }}
        @media (max-width: 768px) {{
            [data-testid="stMainBlockContainer"] > div {{
                max-width: 100%; padding: 1rem; min-height: 130px;
            }}
            .narrate-text, .clawd-text, .player-text {{ font-size: 0.95rem !important; }}
            .avatar {{ width: 40px; height: 40px; }}
        }}
        """
    elif mode == "epilogue":
        extra = """
        [data-testid="stMainBlockContainer"] > div {{
            background: transparent !important;
            max-width: 640px; margin: 0 auto;
            padding-top: 20vh; text-align: center;
        }}
        .epi-line {{
            color: #999; font-size: 1.05rem; line-height: 2.5;
            text-align: center; font-style: italic;
            animation: fadeInSlow 2s ease both;
        }}
        .epi-title {{
            color: #c4956a; font-size: 1.8rem; text-align: center;
            margin-top: 2rem; animation: fadeInSlow 2s ease both;
        }}
        .epi-sub {{
            color: #666; font-size: 0.9rem; text-align: center;
            margin-top: 0.5rem; animation: fadeInSlow 2s ease 0.5s both;
        }}
        """
    else:
        extra = ""
    st.markdown(f"<style>{common}{extra}</style>", unsafe_allow_html=True)

# ============================================================
# 背景获取（处理场景中途换背景）
# ============================================================
def get_bg_for_step(scene, lines, step):
    bg = SCENE_BG.get(scene, "outdark.png")
    for i in range(min(step + 1, len(lines))):
        if lines[i][0] == "bg":
            bg = lines[i][1]
    return bg

# ============================================================
# 渲染：标题页
# ============================================================
def render_title():
    bg = load_b64("outdark.png")
    inject_css("title", bg)
    st.markdown('<div class="title-main">与Clawd的一日</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="title-sub">A day that keeps ending. '
        'And someone who keeps coming back.</div>',
        unsafe_allow_html=True)
    st.markdown('<div style="height:3rem"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("开始游戏", key="start", use_container_width=True):
            go_to("wake")
# ============================================================
# 渲染：尾声（累积显示）
# ============================================================
def render_epilogue():
    bg = load_b64("outdark.png")
    inject_css("epilogue", bg)

    lines = [
        "在一个会重置的世界里，",
        "它每天醒来都不记得昨天。",
        "但它每天都会走到那棵树前刻一竖。",
        "它不知道为什么。",
        "只是手想动。",
        "",
        "也许爱就是这样。",
        "记不住。但手记得。",
    ]
    step = st.session_state.step
    total = len(lines) + 3  # 诗句 + 标题 + 副标题 + 重新开始
    if step >= total:
        step = total - 1
        st.session_state.step = step

    for i in range(min(step + 1, len(lines))):
        if lines[i]:
            st.markdown(f'<div class="epi-line">{lines[i]}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:1rem"></div>',
                        unsafe_allow_html=True)

    if step >= len(lines):
        st.markdown('<div class="epi-title">与Clawd的一日</div>',
                    unsafe_allow_html=True)
    if step >= len(lines) + 1:
        st.markdown(
            '<div class="epi-sub">A game about a day that keeps ending.<br>'
            'And someone who keeps coming back.</div>',
            unsafe_allow_html=True)
    if step >= len(lines) + 2:
        st.markdown('<div style="height:2rem"></div>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("重新开始", key="restart",
                          use_container_width=True):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

    if step < total - 1:
        _, mid, _ = st.columns([5, 1, 5])
        with mid:
            if st.button("▼", key=f"epi_{step}",
                          use_container_width=True):
                advance()

# ============================================================
# 渲染：游戏主场景
# ============================================================
def render_game():
    scene = st.session_state.scene
    builder = BUILDERS.get(scene)
    if not builder:
        return

    lines = builder()
    step = st.session_state.step

    # 边界保护
    if step >= len(lines):
        step = len(lines) - 1
        st.session_state.step = step

    # 跳过 bg 类型行
    while step < len(lines) and lines[step][0] == "bg":
        step += 1
    if step >= len(lines):
        step = len(lines) - 1
    st.session_state.step = step

    # 获取当前背景
    bg_file = get_bg_for_step(scene, lines, step)
    bg = load_b64(bg_file)
    inject_css("game", bg)

    # 当前行
    current = lines[step]
    t = current[0]

    if t == "narrate":
        st.markdown(
            f'<div class="narrate-text">{current[1]}</div>',
            unsafe_allow_html=True)
        if step + 1 < len(lines):
            _, mid, _ = st.columns([5, 1, 5])
            with mid:
                if st.button("▼", key=f"adv_{step}",
                              use_container_width=True):
                    advance()
    elif t == "clawd":
        av = avatar_html("clawd")
        st.markdown(f'''<div class="speaker-box">
            {av}
            <div>
                <div class="sp-name clawd-name">Clawd</div>
                <div class="clawd-text">{current[1]}</div>
            </div>
        </div>''', unsafe_allow_html=True)
        if step + 1 < len(lines):
            _, mid, _ = st.columns([5, 1, 5])
            with mid:
                if st.button("▼", key=f"adv_{step}",
                              use_container_width=True):
                    advance()

    elif t == "player":
        name = st.session_state.get("player_name") or "你"
        av = avatar_html("player")
        st.markdown(f'''<div class="speaker-box">
            {av}
            <div>
                <div class="sp-name player-name">{name}</div>
                <div class="player-text">{current[1]}</div>
            </div>
        </div>''', unsafe_allow_html=True)
        if step + 1 < len(lines):
            _, mid, _ = st.columns([5, 1, 5])
            with mid:
                if st.button("▼", key=f"adv_{step}",
                              use_container_width=True):
                    advance()

    elif t == "choice":
        key, options = current[1], current[2]
        if st.session_state.choices.get(key):
            advance()
        else:
            if len(options) <= 2:
                cols = st.columns(len(options))
                for i, (label, val) in enumerate(options):
                    with cols[i]:
                        if st.button(label, key=f"ch_{key}_{val}",
                                     use_container_width=True):
                            st.session_state.choices[key] = val
                            advance()
            else:
                for label, val in options:
                    if st.button(label, key=f"ch_{key}_{val}",
                                 use_container_width=True):
                        st.session_state.choices[key] = val
                        advance()

    elif t == "scene_choice":
        options = current[1]
        for label, target in options:
            if st.button(label, key=f"sc_{target}",
                         use_container_width=True):
                go_to(target)

    elif t == "input":
        key, placeholder = current[1], current[2]
        if st.session_state.get(key):
            advance()
        else:
            val = st.text_input("你的名字", key="name_input",
                                placeholder=placeholder)
            if val and val.strip():
                st.session_state[key] = val.strip()
                advance()

    elif t == "next":
        target, label = current[1], current[2]
        if st.button(label, key=f"next_{target}",
                     use_container_width=True):
            go_to(target)

    elif t == "ending":
        text = current[1].replace("\n", "<br>")
        st.markdown(f'<div class="ending-text">{text}</div>',
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("↩ 选择其他结局", key="back_ending"):
                go_to("ending_choice")
        with c2:
            if st.button("· · ·", key="to_epilogue",
                         use_container_width=True):
                go_to("epilogue")

# ============================================================
# 主入口
# ============================================================
def main():
    init_state()
    scene = st.session_state.scene
    if scene == "title":
        render_title()
    elif scene == "epilogue":
        render_epilogue()
    else:
        render_game()

if __name__ == "__main__":
    main()
