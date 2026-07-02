from app.services.extraction import extract_information
from app.services.questioning import fill_missing_information
from app.services.analysis import get_relevant_data
from app.services.fir_service import generate_fir
from app.services.pdf_service import generate_pdf
from app.utils.helpers import get_missing_fields

from rich import print


story = """My name is Harshit Singh. I am 24 years old, an Indian national, and I work as a Software Engineer. I live at 14 Akash Deep Enclave, Kolkata, West Bengal. My phone number is 

On 30 June 2026 at around 4:00 PM, I parked my black Royal Enfield Classic 350 motorcycle near Akash Deep Enclave, close to City Centre Mall in Kolkata, West Bengal. When I returned after about an hour, the motorcycle was missing. The estimated value of the motorcycle is around ₹1,80,000.

I do not know the identity of the accused, but a nearby shopkeeper mentioned seeing a man wearing a black hoodie and blue jeans loitering around the parking area before the theft.

I could not report the matter immediately because I was searching for the motorcycle in nearby areas and also checking with local security guards. Therefore, I am filing this complaint today."""


report = extract_information(story)

print("Incomplete report","="*100)
print(report)

while get_missing_fields(report):
    report = fill_missing_information(report)

print("complete report","="*100)
print(report)


legal_analysis = get_relevant_data(report)
print("Legal analysis", "="*100)
print(legal_analysis)

fir = generate_fir({
    'report' : report,
    'legal_context' : legal_analysis
})
print("fir","="*100)
print(fir)

fir_path = generate_pdf(report,legal_analysis,fir,'fir.pdf')
print("fir_path","="*100)
print(fir_path)

