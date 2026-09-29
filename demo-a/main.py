import os
import requests


CONFIDENCE_THRESHOLD = 0.75


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

    response = session.post(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

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
            "您希望解决什么具体问题，或者自动化什么工作流程？"
        )

    analysis = {
        "customer_input": question,
        "industry": industry,
        "industry_confidence": industry_confidence,
        "requirement_type": requirement_type,
        "requirement_confidence": requirement_confidence,
        "business_goal": "待分析",
        "pain_points": [],
        "constraints": [],
        "unknowns": unknowns,
        "followup_questions": followup_questions,
        "initial_solution": "待分析",
        "risks": []
    }

    return analysis


question = input("请输入客户需求：")
result = create_analysis_template(question)

print("客户原始需求：", result["customer_input"])
print("行业：", result["industry"])
print("行业置信度：", result["industry_confidence"])
print("需求类型：", result["requirement_type"])
print("需求类型置信度：", result["requirement_confidence"])
print("待确认信息：", result["unknowns"])
print("建议追问：", result["followup_questions"])