import os
import re
import fitz  # PyMuPDF
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=device)

# Reference phrases
env_ref = ["environment","climate change","carbon emissions","pollution","waste","green energy",
           "renewable resources","sustainability","biodiversity","eco-friendly","net zero",
           "solar energy","wind energy","water conservation"]

esg_ref = ["environment","social responsibility","governance","sustainability","carbon emissions",
           "green energy","renewable resources","waste management","climate change","pollution control",
           "biodiversity","eco-friendly","net zero","solar energy","wind energy","water conservation",
           "community development","employee welfare","diversity","ethics"]

action_ref = ["implemented","adopted","reduced emissions","recycled","renewable energy",
              "sustainability project","steps taken to reduce carbon emissions",
              "initiatives to help the environment","measures to prevent greenwashing"]

claim_ref = ["plans to achieve","committed to","targets","pledges","goal","aims to",
             "intent to reduce","objective to be","aims for sustainability","pledged to achieve",
             "will reduce carbon","expect to reach net zero","plans to be carbon neutral by",
             "commitment to net zero by","goal to be eco friendly by","target year for sustainability",
             "striving to be net zero","intends to adopt renewable energy","aiming for eco-friendly operations"]

# Extract text
def extract_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def semantic_matches(sentences, reference, threshold=0.55, batch_size=64):
    ref_emb = model.encode(reference, convert_to_tensor=True)
    matches = []
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i+batch_size]
        sent_emb = model.encode(batch, convert_to_tensor=True)
        sim_matrix = util.cos_sim(sent_emb, ref_emb)
        for j, sim_scores in enumerate(sim_matrix):
            if sim_scores.max().item() >= threshold:
                matches.append(batch[j].strip())
    return matches if matches else ["NA"]

# Pipeline for PDFs
def run_pipeline(pdf_folder):
    data = []
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    for pdf in pdf_files:
        company_name = os.path.splitext(pdf)[0]
        pdf_path = os.path.join(pdf_folder, pdf)

        text = extract_text(pdf_path)
        sentences = split_sentences(text)
        total_sentences = len(sentences) if sentences else 1  # avoid division by zero

        env_sentences = semantic_matches(sentences, env_ref)
        esg_sentences = semantic_matches(sentences, esg_ref)
        action_sentences = semantic_matches(sentences, action_ref)
        claim_sentences = semantic_matches(sentences, claim_ref, threshold=0.54)

        env_count = len([s for s in env_sentences if s != "NA"])
        esg_count = len([s for s in esg_sentences if s != "NA"])
        action_count = len([s for s in action_sentences if s != "NA"])
        claim_count = len([s for s in claim_sentences if s != "NA"])

        env_score = (env_count / total_sentences) * 100
        claim_score = (claim_count / total_sentences) * 100
        action_score = (action_count / total_sentences) * 100
        relative_focus = (esg_count / total_sentences) * 100

        net_action = action_score - claim_score
        net_direction = "Positive" if net_action > 0 else "Negative"

        data.append({
            "Company": company_name,
            "Relative Focus Score": round(relative_focus, 2),
            "Environment Score": round(env_score, 2),
            "Claims Score": round(claim_score, 2),
            "Actions Score": round(action_score, 2),
            "Net Action": round(net_action, 2),
            "Direction": net_direction
        })

    return pd.DataFrame(data)
