from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import aiohttp
import json

@register("astrbot_plugin_ragecoop", "--sora--", "GTAV RageCoop服务器查询插件", "1.0")
class RageCoopPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_urls = [
            "https://masterserver.ragecoop.com/",
            "https://masterserver.s-o-r-a.top/"
        ]
        
        # 完整的国家/地区代码映射
        self.country_mapping = {
            "AF": "阿富汗(Afghanistan)",
            "AX": "奥兰群岛(Aland Islands)",
            "AL": "阿尔巴尼亚(Albania)",
            "DZ": "阿尔及利亚(Algeria)",
            "AS": "美属萨摩亚(American Samoa)",
            "AD": "安道尔(Andorra)",
            "AO": "安哥拉(Angola)",
            "AI": "安圭拉(Anguilla)",
            "AQ": "南极洲(Antarctica)",
            "AG": "安提瓜和巴布达(Antigua and Barbuda)",
            "AR": "阿根廷(Argentina)",
            "AM": "亚美尼亚(Armenia)",
            "AW": "阿鲁巴(Aruba)",
            "AU": "澳大利亚(Australia)",
            "AT": "奥地利(Austria)",
            "AZ": "阿塞拜疆(Azerbaijan)",
            "BS": "巴哈马(Bahamas)",
            "BH": "巴林(Bahrain)",
            "BD": "孟加拉国(Bangladesh)",
            "BB": "巴巴多斯(Barbados)",
            "BY": "白俄罗斯(Belarus)",
            "BE": "比利时(Belgium)",
            "BZ": "伯利兹(Belize)",
            "BJ": "贝宁(Benin)",
            "BM": "百慕大(Bermuda)",
            "BT": "不丹(Bhutan)",
            "BO": "玻利维亚(Bolivia)",
            "BA": "波黑(Bosnia and Herzegovina)",
            "BW": "博茨瓦纳(Botswana)",
            "BV": "布维岛(Bouvet Island)",
            "BR": "巴西(Brazil)",
            "IO": "英属印度洋领地(British Indian Ocean Territory)",
            "BN": "文莱(Brunei Darussalam)",
            "BG": "保加利亚(Bulgaria)",
            "BF": "布基纳法索(Burkina Faso)",
            "BI": "布隆迪(Burundi)",
            "KH": "柬埔寨(Cambodia)",
            "CM": "喀麦隆(Cameroon)",
            "CA": "加拿大(Canada)",
            "CV": "佛得角(Cape Verde)",
            "KY": "开曼群岛(Cayman Islands)",
            "CF": "中非(Central African Republic)",
            "TD": "乍得(Chad)",
            "CL": "智利(Chile)",
            "CN": "中国(China)",
            "CX": "圣诞岛(Christmas Island)",
            "CC": "科科斯（基林）群岛(Cocos (Keeling) Islands)",
            "CO": "哥伦比亚(Colombia)",
            "KM": "科摩罗(Comoros)",
            "CG": "刚果（布）(Congo)",
            "CD": "刚果（金）(Congo (the Democratic Republic of the))",
            "CK": "库克群岛(Cook Islands)",
            "CR": "哥斯达黎加(Costa Rica)",
            "CI": "科特迪瓦(Côte d'Ivoire)",
            "HR": "克罗地亚(Croatia)",
            "CU": "古巴(Cuba)",
            "CY": "塞浦路斯(Cyprus)",
            "CZ": "捷克(Czech Republic)",
            "DK": "丹麦(Denmark)",
            "DJ": "吉布提(Djibouti)",
            "DM": "多米尼克(Dominica)",
            "DO": "多米尼加(Dominican Republic)",
            "EC": "厄瓜多尔(Ecuador)",
            "EG": "埃及(Egypt)",
            "SV": "萨尔瓦多(El Salvador)",
            "GQ": "赤道几内亚(Equatorial Guinea)",
            "ER": "厄立特里亚(Eritrea)",
            "EE": "爱沙尼亚(Estonia)",
            "ET": "埃塞俄比亚(Ethiopia)",
            "FK": "福克兰群岛（马尔维纳斯）(Falkland Islands [Malvinas])",
            "FO": "法罗群岛(Faroe Islands)",
            "FJ": "斐济(Fiji)",
            "FI": "芬兰(Finland)",
            "FR": "法国(France)",
            "GF": "法属圭亚那(French Guiana)",
            "PF": "法属波利尼西亚(French Polynesia)",
            "TF": "法属南部领地(French Southern Territories)",
            "GA": "加蓬(Gabon)",
            "GM": "冈比亚(Gambia)",
            "GE": "格鲁吉亚(Georgia)",
            "DE": "德国(Germany)",
            "GH": "加纳(Ghana)",
            "GI": "直布罗陀(Gibraltar)",
            "GR": "希腊(Greece)",
            "GL": "格陵兰(Greenland)",
            "GD": "格林纳达(Grenada)",
            "GP": "瓜德罗普(Guadeloupe)",
            "GU": "关岛(Guam)",
            "GT": "危地马拉(Guatemala)",
            "GG": "格恩西岛(Guernsey)",
            "GN": "几内亚(Guinea)",
            "GW": "几内亚比绍(Guinea-Bissau)",
            "GY": "圭亚那(Guyana)",
            "HT": "海地(Haiti)",
            "HM": "赫德岛和麦克唐纳岛(Heard Island and McDonald Islands)",
            "VA": "梵蒂冈(Holy See [Vatican City State])",
            "HN": "洪都拉斯(Honduras)",
            "HK": "香港(Hong Kong)",
            "HU": "匈牙利(Hungary)",
            "IS": "冰岛(Iceland)",
            "IN": "印度(India)",
            "ID": "印度尼西亚(Indonesia)",
            "IR": "伊朗(Iran (the Islamic Republic of))",
            "IQ": "伊拉克(Iraq)",
            "IE": "爱尔兰(Ireland)",
            "IM": "英国属地曼岛(Isle of Man)",
            "IL": "以色列(Israel)",
            "IT": "意大利(Italy)",
            "JM": "牙买加(Jamaica)",
            "JP": "日本(Japan)",
            "JE": "泽西岛(Jersey)",
            "JO": "约旦(Jordan)",
            "KZ": "哈萨克斯坦(Kazakhstan)",
            "KE": "肯尼亚(Kenya)",
            "KI": "基里巴斯(Kiribati)",
            "KP": "朝鲜(Korea (the Democratic People's Republic of))",
            "KR": "韩国(Korea (the Republic of))",
            "KW": "科威特(Kuwait)",
            "KG": "吉尔吉斯斯坦(Kyrgyzstan)",
            "LA": "老挝(Lao People's Democratic Republic)",
            "LV": "拉脱维亚(Latvia)",
            "LB": "黎巴嫩(Lebanon)",
            "LS": "莱索托(Lesotho)",
            "LR": "利比里亚(Liberia)",
            "LY": "利比亚(Libyan Arab Jamahiriya)",
            "LI": "列支敦士登(Liechtenstein)",
            "LT": "立陶宛(Lithuania)",
            "LU": "卢森堡(Luxembourg)",
            "MO": "澳门(Macao)",
            "MK": "前南马其顿(Macedonia (the former Yugoslav Republic of))",
            "MG": "马达加斯加(Madagascar)",
            "MW": "马拉维(Malawi)",
            "MY": "马来西亚(Malaysia)",
            "MV": "马尔代夫(Maldives)",
            "ML": "马里(Mali)",
            "MT": "马耳他(Malta)",
            "MH": "马绍尔群岛(Marshall Islands)",
            "MQ": "马提尼克(Martinique)",
            "MR": "毛利塔尼亚(Mauritania)",
            "MU": "毛里求斯(Mauritius)",
            "YT": "马约特(Mayotte)",
            "MX": "墨西哥(Mexico)",
            "FM": "密克罗尼西亚联邦(Micronesia (the Federated States of))",
            "MD": "摩尔多瓦(Moldova (the Republic of))",
            "MC": "摩纳哥(Monaco)",
            "MN": "蒙古(Mongolia)",
            "ME": "黑山(Montenegro)",
            "MS": "蒙特塞拉特(Montserrat)",
            "MA": "摩洛哥(Morocco)",
            "MZ": "莫桑比克(Mozambique)",
            "MM": "缅甸(Myanmar)",
            "NA": "纳米比亚(Namibia)",
            "NR": "瑙鲁(Nauru)",
            "NP": "尼泊尔(Nepal)",
            "NL": "荷兰(Netherlands)",
            "AN": "荷属安的列斯(Netherlands Antilles)",
            "NC": "新喀里多尼亚(New Caledonia)",
            "NZ": "新西兰(New Zealand)",
            "NI": "尼加拉瓜(Nicaragua)",
            "NE": "尼日尔(Niger)",
            "NG": "尼日利亚(Nigeria)",
            "NU": "纽埃(Niue)",
            "NF": "诺福克岛(Norfolk Island)",
            "MP": "北马里亚纳群岛(Northern Mariana Islands)",
            "NO": "挪威(Norway)",
            "OM": "阿曼(Oman)",
            "PK": "巴基斯坦(Pakistan)",
            "PW": "帕劳(Palau)",
            "PS": "巴勒斯坦领土(Palestinian Territory (the Occupied))",
            "PA": "巴拿马(Panama)",
            "PG": "巴布亚新几内亚(Papua New Guinea)",
            "PY": "巴拉圭(Paraguay)",
            "PE": "秘鲁(Peru)",
            "PH": "菲律宾(Philippines)",
            "PN": "皮特凯恩群岛(Pitcairn)",
            "PL": "波兰(Poland)",
            "PT": "葡萄牙(Portugal)",
            "PR": "波多黎各(Puerto Rico)",
            "QA": "卡塔尔(Qatar)",
            "RE": "留尼汪(Réunion)",
            "RO": "罗马尼亚(Romania)",
            "RU": "俄罗斯(Russian Federation)",
            "RW": "卢旺达(Rwanda)",
            "BL": "圣巴泰勒米岛(Saint Barthélemy)",
            "SH": "圣赫勒拿(Saint Helena, Ascension and Tristan da Cunha)",
            "KN": "圣基茨和尼维斯(Saint Kitts and Nevis)",
            "LC": "圣卢西亚(Saint Lucia)",
            "MF": "圣马丁(Saint Martin (French part))",
            "PM": "圣皮埃尔和密克隆(Saint Pierre and Miquelon)",
            "VC": "圣文森特和格林纳丁斯(Saint Vincent and the Grenadines)",
            "WS": "萨摩亚(Samoa)",
            "SM": "圣马力诺(San Marino)",
            "ST": "圣多美和普林西比(Sao Tome and Principe)",
            "SA": "沙特阿拉伯(Saudi Arabia)",
            "SN": "塞内加尔(Senegal)",
            "RS": "塞尔维亚(Serbia)",
            "SC": "塞舌尔(Seychelles)",
            "SL": "塞拉利昂(Sierra Leone)",
            "SG": "新加坡(Singapore)",
            "SK": "斯洛伐克(Slovakia)",
            "SI": "斯洛文尼亚(Slovenia)",
            "SB": "所罗门群岛(Solomon Islands)",
            "SO": "索马里(Somalia)",
            "ZA": "南非(South Africa)",
            "GS": "南乔治亚岛和南桑德威奇群岛(South Georgia and the South Sandwich Islands)",
            "ES": "西班牙(Spain)",
            "LK": "斯里兰卡(Sri Lanka)",
            "SD": "苏丹(Sudan)",
            "SR": "苏里南(Suriname)",
            "SJ": "斯瓦尔巴群岛和扬马延岛(Svalbard and Jan Mayen)",
            "SZ": "斯威士兰(Swaziland)",
            "SE": "瑞典(Sweden)",
            "CH": "瑞士(Switzerland)",
            "SY": "叙利亚(Syrian Arab Republic)",
            "TW": "中国台湾(Taiwan (Province of China))",
            "TJ": "塔吉克斯坦(Tajikistan)",
            "TZ": "坦桑尼亚(Tanzania, United Republic of)",
            "TH": "泰国(Thailand)",
            "TL": "东帝汶(Timor-Leste)",
            "TG": "多哥(Togo)",
            "TK": "托克劳(Tokelau)",
            "TO": "汤加(Tonga)",
            "TT": "特立尼达和多巴哥(Trinidad and Tobago)",
            "TN": "突尼斯(Tunisia)",
            "TR": "土耳其(Turkey)",
            "TM": "土库曼斯坦(Turkmenistan)",
            "TC": "特克斯和凯科斯群岛(Turks and Caicos Islands)",
            "TV": "图瓦卢(Tuvalu)",
            "UG": "乌干达(Uganda)",
            "UA": "乌克兰(Ukraine)",
            "AE": "阿拉伯联合酋长国(United Arab Emirates)",
            "GB": "英国(United Kingdom)",
            "US": "美国(United States)",
            "UM": "美国本土外小岛屿(United States Minor Outlying Islands)",
            "UY": "乌拉圭(Uruguay)",
            "UZ": "乌兹别克斯坦(Uzbekistan)",
            "VU": "瓦努阿图(Vanuatu)",
            "VE": "委内瑞拉(Venezuela (Bolivarian Republic of))",
            "VN": "越南(Viet Nam)",
            "VG": "英属维尔京群岛(Virgin Islands (British))",
            "VI": "美属维尔京群岛(Virgin Islands (U.S.))",
            "WF": "瓦利斯和富图纳群岛(Wallis and Futuna)",
            "EH": "西撒哈拉(Western Sahara)",
            "YE": "也门(Yemen)",
            "ZM": "赞比亚(Zambia)",
            "ZW": "津巴布韦(Zimbabwe)"
        }

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    async def fetch_server_data(self):
        """获取RageCoop服务器列表数据"""
        for api_url in self.api_urls:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data
            except Exception as e:
                logger.error(f"从 {api_url} 获取服务器数据失败: {e}")
                continue
        return []

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        """监听所有消息，当消息为'ip'时触发查询"""
        # 检查消息是否为纯文本"ip"
        if event.message_str.strip().lower() == "ip":
            try:
                servers = await self.fetch_server_data()
                if not servers:
                    yield event.plain_result("获取服务器列表失败，请稍后再试。")
                    return
                    
                # 构建消息内容
                message_lines = ["RageCoop服务器列表"]
                
                for server in servers:
                    name = server.get("name", "Unknown Server")
                    address = server.get("address", "")
                    port = server.get("port", "")
                    players = server.get("players", 0)
                    max_players = server.get("maxPlayers", 0)
                    country = server.get("country", "Unknown")
                    
                    # 获取国家显示名称
                    country_display = self.country_mapping.get(country, f"{country}({country})")
                    
                    line = f"【{name}】 {address}:{port} 在线玩家: {players}/{max_players}人 国家/区域：{country_display}"
                    message_lines.append(line)
                
                message_lines.append("本插件由--sora--提供技术支持")
                
                # 发送消息
                yield event.plain_result("\n".join(message_lines))
                
            except Exception as e:
                logger.error(f"查询RageCoop服务器时出错: {e}")
                yield event.plain_result("查询服务器列表时发生错误，请稍后再试。")
        # 当用户发送"ragecoop"时，显示相关链接
        elif event.message_str.strip().lower() == "ragecoop":
            response_text = """ragecoop客户端安装教程：https://s-o-r-a.top/archives/ragecoop\n推荐使用GTAV工具箱一键安装：https://mod.3dmgame.com/mod/200236\nragecoop各种弹窗问题汇总：https://tieba.baidu.com/p/7996543677\n官网服务器列表：https://ragecoop.com/servers\n国内官网服务器列表：https://ragecoop.s-o-r-a.top/\nragecoop官方群：765532209"""
            yield event.plain_result(response_text)
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""