from src.common.rules import load_rules
from src.agents.protocol_agent import ProtocolAgent

def test_protocol_agent_slice_thickness():
    rules = load_rules('configs/rules.yaml')
    agent = ProtocolAgent(rules)
    row = {'study_uid':'x','series_uid':'s','protocol_name':'CT_ABD_WC','slice_thickness_mm':5.0,'contrast_bolus':'Yes'}
    findings = agent.check(row)
    assert any(f.metric=='slice_thickness_mm' for f in findings)
