#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from Bio import SeqIO, SearchIO

# ============= UTILITY FUNCTIONS =============

def check_dependancies():
    """Check that HMMER and Biopython dependancies are avaliable."""
    print ("checking dependancies...")
    if shutil.which("hmmscan") is None:
        sys.exit("Error: hmmscan not found. Please install HMMER or use the container.")
    print("HMMER found.")

# ============= Step 1: Translate FASTA =============

def translate_fasta(input_fasta, output_fasta):
    """Translate nucleotide sequence into amino acids."""
    from Bio.Seq import Seq

    translated_records = []
    for record in SeqIO.parse(input_fasta, "fasta"):
        protein_seq = record.seq.translate(to_stop=False)
        translated_record = record[:]
        translated_record.seq = protein_seq
        translated_records.append(translated_record)

    SeqIO.write(translated_records, output_fasta, "fasta")
    print(f"Translated sequences written to {output_fasta}")

# ============= Step 2 : HMMER Search =============

def run_hmmscan(protein_fasta, hmm_db, tblout_file):
    """Run hmmscan and save tabular output."""
    cmd = [
        "hmmscan",
        "--tblout", tblout_file,
        hmm_db,
        protein_fasta
    ]
    print(f"Running hmmscan: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"HMMER results written to {tblout_file}")

# ============= Step 3: Parse HMMER Results =============

def parse_hmmer_results(tbl_file, summary_file, evalue_threshold=1e-5):
    """Parse hmmscan results and extract top hits per query."""
    results_summary = []

    for qresults in SearchIO.parse(tbl_file, "hmmer3-tab"):
        if not qresults.hits:
            continue

        hits_sorted = sorted(qresults.hits, key=lambda h: h.evalue)
        best_hit = hits_sorted[0]

        if best_hit.evalue <= evalue_threshold:
            results_summary.append({
                "query_id": qresults.id,
                "best_hit_id": best_hit.id,
                "evalue": best_hit.evalue,
                "bit_score": best_hit.bitscore
            })

        with open(summary_file, "w") as out:
            out.write("query_id\tbest_hit_id\tevalue\tbit_score\n")
            for r in results_summary:
                out.write(f"{r['query_id']}\t{r['best_hit_id']}\t{r['evalue']}\t{r['bit_score']:.2f}\n")

        print(f"summary written to {summary_file}")

# ============= MAIN SCRIPT =============

def main():
    if len(sys.argv) != 4:
        print ("Usage: python t3ss_hmmscan_pipeline.py <nucleotide_fasta> <hmm_db> <output_prefix>")

    input_fasta = sys.argv[1]
    hmm_db = sys.argv[2]
    prefix = sys.argv[3]

    if not os.path.exists(input_fasta):
        sys.exit(f"Error: Input FASTA file {input_fasta} does not exist.")
    if not os.path.exists(hmm_db):
        sys.exit(f"Error: HMM database file {hmm_db} does not exist.")

    check_dependancies()

    #file paths
    translated_fasta = f"{prefix}_translated.faa"
    tblout_file = f"{prefix}_hmmscan.tbl"
    summary_file = f"{prefix}_summary.tsv"

    # run the pipeline
    print ("\n=== Step 1: Translate FASTA ===")
    translate_fasta(input_fasta, translated_fasta)

    print ("\n=== Step 2: HMMER search ===")
    run_hmmscan(translated_fasta, hmm_db, tblout_file)

    print ("\n=== Step 3: Parse HMMER results ===")
    parse_hmmer_results(tblout_file, summary_file)

    print ("\nPipeline complete.")
    print (f"Results summary: {summary_file}")

if __name__ == "__main__":
    main()
    


               

