from langchain_core.messages import AIMessage
from app.schemas.user_report import UserReportSchema


# examples for testing

report = """My name is Harshit Singh and my father name is rk singh. I am 24 years old, an Indian national, and I work as a Software Engineer. I live at 14 Akash Deep Enclave, Kolkata, West Bengal. My phone number is 9876543210.

On 30 June 2026 at around 4:00 PM, I parked my black Royal Enfield Classic 350 motorcycle near Akash Deep Enclave, close to City Centre Mall in Kolkata, West Bengal. When I returned after about an hour, the motorcycle was missing. The estimated value of the motorcycle is around ₹1,80,000.

I do not know the identity of the accused, but a nearby shopkeeper mentioned seeing a man wearing a black hoodie and blue jeans loitering around the parking area before the theft.

I could not report the matter immediately because I was searching for the motorcycle in nearby areas and also checking with local security guards. Therefore, I am filing this complaint today."""

report = UserReportSchema(
    offence_description='Theft of a black Royal Enfield Classic 350 motorcycle',
    offence_date='30 June 2026',
    offence_time='around 4:00 PM',
    location_name='near Akash Deep Enclave',
    landmark='close to City Centre Mall',
    city='Kolkata',
    state='West Bengal',
    reporter_full_name='Harshit Singh',
    father_or_husband_name='rk singh',
    dob='2nd may 205',
    nationality='Indian',
    occupation='Software Engineer',
    address='14 Akash Deep Enclave, Kolkata, West Bengal',
    phone_number='81717212028',
    delay_reason='searching for the motorcycle in nearby areas and also checking with local security guards',
    accused_description='a man wearing a black hoodie and blue jeans loitering around the parking area',
    property_type='black Royal Enfield Classic 350 motorcycle',
    estimated_value='₹1,80,000'
)

legal_analysis = AIMessage(
    content="""Applicable BNS Sections:\n- BNS Section 303: Theft\n  Reason: The accused dishonestly took a movable property (motorcycle) out of the owner's possession without consent.\n\nProcedurally Relevant 
BNSS Sections:\n- BNSS Section 116: Identifying unlawfully acquired property\n  Reason: This section allows the court to direct police to take steps for tracing and identifying the stolen motorcycle.\n\nRejected
Sections:\n- BNS Section 307: Theft after preparation for causing death, hurt or restraint\n  Reason: There is no evidence of the accused making preparations to cause death, hurt, or restraint.\n- BNS Section 
306: Theft by clerk or servant\n  Reason: The facts do not establish an employer-employee relationship between the reporter and the accused.\n- BNS Section 52: Abettor liability\n  Reason: There is no mention of
abetment or a secondary act committed by an abettor.\n- BNS Section 190: Unlawful assembly\n  Reason: The report describes a single individual, not an unlawful assembly.\n- BNSS Section 286: Record in summary 
trials\n  Reason: This section pertains to the format of records during summary trials rather than the investigation of this theft.\n\nReasoning:\nThe incident involves the clear theft of a motorcycle, which 
satisfies the ingredients of BNS Section 303. There is no evidence of violence, preparation for violence, or an employer-servant relationship required for other BNS sections. BNSS Section 116 is relevant as it 
provides the procedure for tracing stolen property.""",
    additional_kwargs={},
    response_metadata={
        'model': 'gemma4:26b',
        'created_at': '2026-07-02T14:25:52.6224632Z',
        'done': True,
        'done_reason': 'stop',
        'total_duration': 87178681300,
        'load_duration': 402558400,
        'prompt_eval_count': 3697,
        'prompt_eval_duration': 13689274000,
        'eval_count': 1362,
        'eval_duration': 72821695000,
        'logprobs': None,
        'model_name': 'gemma4:26b',
        'model_provider': 'ollama'
    },
    id='lc_run--019f2337-7763-7f61-8b4a-9791f6197c1a-0',
    tool_calls=[],
    invalid_tool_calls=[],
    usage_metadata={'input_tokens': 3697, 'output_tokens': 1362, 'total_tokens': 5059}
)

fir = AIMessage(
    content='''FORM – IF1 - (Integrated Form) \n \nFIRST INFORMATION REPORT \n(Under Section 154 Cr.P.C) \n \n1. Dist. Kolkata   P.S.               Year 2026  F.I.R. No.              Date           \n \n2. (i) 
*Act BNS *Sections 303                                               \n (ii) *Act BNSS *Sections 116                                              \n (iii)  *Act                                                   
*Sections                                                                  \n (iv)  * Other Acts & Sections                                                                                                        
\n3.  \n(a) \n \n* Occurrence of Offence: * Day               *Date 30 June 2026 *Time around 4:00 PM  \n  \n(b) \n \nInformation received at P.S.  Date                                Time                       
\n  \n(c) \n \nGeneral Diary Reference: Entry No(s)                             Time                                         \n  \n4. Type of information :     *Written  \n \n5. Place of occurrence:  (a) 
Direction and Distance from P.S.               Beat No.             \n \n (b) * Address near Akash Deep Enclave, close to City Centre Mall, Kolkata, West Bengal\n………………………………………………………………………………………………….. \n (c) In
case outside limit of this Police Station, then the name of P.S.                                         \nDistrict Kolkata                                        \n \n6. Complainant / information :  \n \n (a) 
Name Harshit Singh \n \n (b) Father’s / Husband’s Name rk singh\n \n (c)\nDate / Year of Birth  2nd may 205 (d) Nationality Indian    \n (e) Passport No:                                Date of Issue:            
Place of Issue                \n (f) Occupation: Software Engineer  \n \n \n(g) Address: 14 Akash Deep Enclave, Kolkata, West Bengal \n7. Details of known / suspected / unknown / accused with full particulars 
\n(Attach separate sheet if necessary):  \na man wearing a black hoodie and blue jeans loitering around the parking area\n…………………………………………………………………………………….. \n……………………………… ………………………………………………………………………….. 
\n…………………………………………………………………………………….. \n8. Reasons for delay in reporting by the  complainant / Informant searching for the motorcycle in nearby areas and also checking with local security 
guards\n…………………………………………………………………………………………………………  \n…………………………………………………………………………………………………………. \n9. Particulars of properties stolen / involved (Attach separate sheet if ne cessary): black Royal Enfield Classic 
350 motorcycle, estimated value ₹1,80,000''',
    additional_kwargs={},
    response_metadata={
        'model': 'gemma4:26b',
        'created_at': '2026-07-02T14:27:31.4197344Z',
        'done': True,
        'done_reason': 'stop',
        'total_duration': 98791776400,
        'load_duration': 428352800,
        'prompt_eval_count': 1271,
        'prompt_eval_duration': 5098396000,
        'eval_count': 1740,
        'eval_duration': 93119149000,
        'logprobs': None,
        'model_name': 'gemma4:26b',
        'model_provider': 'ollama'
    },
    id='lc_run--019f2338-cbf3-71f3-bb30-325fcd9db2bd-0',
    tool_calls=[],
    invalid_tool_calls=[],
    usage_metadata={'input_tokens': 1271, 'output_tokens': 1740, 'total_tokens': 3011}
)