export const ManuscriptItemTypeEnum = {
  Button: { key: 'quick_reply', text: 'Quick Reply' },
  Text: { key: 'text', text: 'Text' },
  Quiz_Result: { key: 'quiz_result', text: 'Quiz: Show result'},
  Quiz_PromisesChecked: { key: 'quiz_q_promises_checked', text: 'Quiz: Show checked promises questions'},
  Quiz_PartySelect: { key: 'quiz_q_party_select', text: 'Quiz: Show which party promised questions'},
  Quiz_PartyBool: { key: 'quiz_q_party_bool', text: 'Quiz: Show did party X promise Y questions'},
  VG_Result: { key: 'vg_result', text: 'Voter guide: Show result'},
  VG_Categories: { key: 'vg_categories', text: 'Voter guide: Show category select'},
  VG_Questions: { key: 'vg_questions', text: 'Voter guide: Show questions'},
};

export const ManuscriptTypeEnum = {
  ElectoralGuide: { key: 'voter_guide', text: 'Electoral Guide' },
  Info: { key: 'generic', text: 'Info' },
  Quiz: { key: 'quiz', text: 'Quiz' }
};
