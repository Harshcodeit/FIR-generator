from app.utils.loaders import load_pdf
from app.rag.chunking import split_legal_document

def verify_pipeline():
    print("⏳ Loading and chunking BNS.pdf...")
    
    # 1. Run your loader and chunker
    raw_docs = load_pdf("BNS.pdf")
    processed_chunks = split_legal_document(raw_docs, chunk_size=800, chunk_overlap=150)
    
    print(f"✅ Finished! Total chunks generated: {len(processed_chunks)}\n")
    print("🔍 Searching for Section 303 chunks...")
    print("=" * 60)
    
    found_any = False
    count = 0
    
    # 2. Scan chunks for the theft provision
    for idx, chunk in enumerate(processed_chunks):
        content = chunk.page_content
        
        # Look for chunks starting with or containing "303" and "Theft"
        if "303" in content and ("Theft" in content or "theft" in content):
            found_any = True
            count += 1
            print(f"📦 CHUNK MATCH #{count} (Index: {idx} | Page: {chunk.metadata.get('page_label', chunk.metadata.get('page', 'Unknown'))})")
            print("-" * 60)
            print(content)
            print("=" * 60)
            
            # Stop printing after 3 matches to keep your terminal readable
            if count >= 3:
                break
                
    if not found_any:
        print("❌ Could not find Section 303! Check if the section text format matches '\\n\\s*\\d+\\s*\\.\\s*'")

if __name__ == "__main__":
    verify_pipeline()
