#!/usr/bin/env python3
import subprocess
import shutil
import sys
import os

def check_hmmer():
    """Check if HMMER is installed."""
    if shutil.which("hmmbuild") is None:
        print("HMMER is not installed. Please install it or use Docker container.")
        sys.exit(1)
    print("HMMER is installed.")

def run_hmmscan(protein_fasta, hmm_db, output_file):
    """Run hmmscan on the given protein FASTA file against the HMM database."""
    cmd = [
        "hmmscan",
        "--tblout", output_file, #tablular output file 
        hmm_db,                  # hmm database   
        protein_fasta            # protein fasta file
    ]

    print(f"running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"hmmscan completed successfully. Results written to {output_file}")
    except subprocess.CalledProcessError:
        print("Error running hmmscan.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_hmmscan.py <protein_fasta> <hmm_db> <output_file>")
        sys.exit(1)

    protein_fasta = sys.argv[1]
    hmm_db = sys.argv[2]
    output_file = sys.argv[3]

    if not os.path.exists(protein_fasta):
        print(f"Protein FASTA file {protein_fasta} does not exist.")
        sys.exit(1)
    if not os.path.exists(hmm_db):
        print(f"HMM database file {hmm_db} does not exist.")
        sys.exit(1)

    check_hmmer()
    run_hmmscan(protein_fasta, hmm_db, output_file)
    