#!/usr/bin/env python3

from Bio import SeqIO
import sys
import os

def translate_fasta(input_fasta, output_fasta):
    translate_records = []
    for record in SeqIO.parse(input_fasta, "fasta"):
        # translate sequence (standard codon table, stop codon as '*')
        seq_len = len(record.seq)
        if seq_len % 3 != 0:
            print(f"Warning: Sequence {record.id} length is not a multiple of 3, skipping translation.", file=sys.stderr)
            continue
        try:
            protein_seq = record.seq.translate(to_stop=False)
            # create new record with translated sequence
            record.seq = protein_seq
            record.id = record.id + "_translated"
            record.description = "translated from nucleotide sequence"
            translate_records.append(record)
        except Exception as e:
            print(f"Error translating sequence {record.id}: {e}", file=sys.stderr)

    # write translated sequences to output fasta
    SeqIO.write(translate_records, output_fasta, "fasta")
    print(f"Translated sequences written to {output_fasta}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translate_fasta.py <input_fasta> <output_fasta>")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]

    if not os.path.isfile(input_fasta):
        print(f"Error: Input file {input_fasta} does not exist.")
        sys.exit(1)

    translate_fasta(input_fasta, output_fasta)



