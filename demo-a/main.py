import os
import requests


CONFIDENCE_THRESHOLD = 0.75
MAX_FOLLOWUP_ROUNDS = 3


def analyze_with_jev(question):
    api_key = os.getenv("TYPESAFE_API_KEY")

    if not api_key:
        print("没有读取到 TYPESAFE_API_KEY")
        raise SystemExit

    url = "https://api.typesafe.ai/v1/systemone"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "state": question,
        "model": "jev-latest",
        "questions": {
            "industry": {
                "type": "choice",
                "instructions": "这项客户需求属于哪个行业？",
                "criteria": {
                    "金融业": "银行、证券、保险、基金、信托等金融机构",
                    "医疗健康": "医院、医生、患者、药企等医疗场景",
                    "制造业": "工厂、生产、设备、产线等制造场景",
                    "教育行业": "学校、教师、学生、培训等教育场景",
                    "专业服务": "咨询、律所、会计师事务所、审计等场景",
                    "其他": "缺少行业信息，或者无法归入以上行业"
                }
            },
            "requirement_type": {
                "type": "choice",
                "instructions": "这项客户需求主要属于哪种需求类型？",
                "criteria": {
                    "知识问答": "根据资料、制度或文档回答问题",
                    "流程自动化": "自动执行审批、处理或业务流程",
                    "数据分析": "分析数据、指标或生成报表",
                    "其他": "需求不明确，或者无法归入以上需求类型"
                }
            }
        }
    }
    session = requests.Session()
    session.trust_env = False

    try:
        response = session.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("Jev 响应超时，请稍后重新运行。")
        raise SystemExit

    except requests.exceptions.ConnectionError:
        print("无法连接 Jev，请检查网络或代理。")
        raise SystemExit

    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code

        if status_code == 401:
            print("Jev API Key 无效或没有正确载入。")
        elif status_code == 422:
            print("发送给 Jev 的请求格式有误。")
        elif status_code == 429:
            print("Jev 请求过于频繁，请稍后重试。")
        elif status_code == 529:
            print("Jev 服务当前繁忙，请稍后重试。")
        else:
            print("Jev API 请求失败，状态码：", status_code)

        raise SystemExit

    except requests.exceptions.RequestException as error:
        print("调用 Jev 时发生未知网络错误：", error)
        raise SystemExit

    data = response.json()
    return data["answers"]

def create_analysis_template(question):
    answers = analyze_with_jev(question)

    industry_answer = answers["industry"]
    requirement_answer = answers["requirement_type"]

    industry = industry_answer["choice"]
    industry_confidence = industry_answer["confidence"]

    requirement_type = requirement_answer["choice"]
    requirement_confidence = requirement_answer["confidence"]

    unknowns = []
    followup_questions = []

    if industry == "其他" or industry_confidence < CONFIDENCE_THRESHOLD:
        unknowns.append("客户所属行业")
        followup_questions.append("请问贵公司属于什么行业？")

    if (
        requirement_type == "其他"
        or requirement_confidence < CONFIDENCE_THRESHOLD
    ):
        unknowns.append("具体需求类型")
        followup_questions.append(
            "您希望解决什么具体问题，或者改进什么工作流程？"
        )

    analysis = {
        "customer_input": question,
        "industry": industry,
        "industry_confidence": industry_confidence,
        "requirement_type": requirement_type,
        "requirement_confidence": requirement_confidence,
        "business_goal": "待确认",
        "current_process": "待确认",
        "pain_points": "待确认",
        "target_users": "待确认",
        "data_sources": "待确认",
        "constraints": "待确认",
        "expected_outcome": "待确认",
        "unknowns": unknowns,
        "followup_questions": followup_questions,
        "initial_solution": "待分析",
        "risks": []
    }

    return analysis

def collect_requirement_details():
    detail_questions = {
        "business_goal": "您希望最终实现什么业务目标？",
        "current_process": "目前这项工作是如何完成的？",
        "pain_points": "当前最主要的问题或痛点是什么？",
        "target_users": "这个系统主要由哪些人使用？",
        "data_sources": "需要使用哪些数据、资料或系统？",
        "constraints": "项目有哪些时间、预算、安全或系统限制？",
        "expected_outcome": "您希望最终看到什么结果或指标改善？"
    }

    details = {}

    for field_name, prompt in detail_questions.items():
        answer = input(prompt + "：").strip()

        if answer:
            details[field_name] = answer
        else:
            details[field_name] = "待确认"

    return details


question = input("请输入客户需求：")
result = create_analysis_template(question)

followup_round = 0

while (
    result["followup_questions"]
    and followup_round < MAX_FOLLOWUP_ROUNDS
):
    followup_round += 1

    print("正在进行第", followup_round, "轮需求确认")

    for followup_question in result["followup_questions"]:
        answer = input(followup_question + "：")

        question += "\n补充问题：" + followup_question
        question += "\n客户回答：" + answer

    result = create_analysis_template(question)

print("客户原始需求：", result["customer_input"])
print("行业：", result["industry"])
print("行业置信度：", result["industry_confidence"])
print("需求类型：", result["requirement_type"])
print("需求类型置信度：", result["requirement_confidence"])

if result["followup_questions"]:
    print("待确认信息：", result["unknowns"])
    print("建议追问：", result["followup_questions"])
    print("已经达到最大追问轮数，需要人工继续确认。")

else:
    print("需求分类确认完成，现在收集详细业务信息。")

    details = collect_requirement_details()
    result.update(details)

    print("\n完整需求分析")
    print("业务目标：", result["business_goal"])
    print("当前流程：", result["current_process"])
    print("核心痛点：", result["pain_points"])
    print("目标用户：", result["target_users"])
    print("数据来源：", result["data_sources"])
    print("限制条件：", result["constraints"])
    print("期望结果：", result["expected_outcome"])