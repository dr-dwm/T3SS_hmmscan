#!/usr/bin/env python3
from Bio import SearchIO
import sys
import os   

def parse_hmmer_tbl(tbl_file, output_file=None, evalue_threshold=1e-5):
    """parse hmmscan --tblout output and summarise top hits per query sequence """

    if not os.path.exists(tbl_file):
        print(f"Error: File {tbl_file} does not exist.")
        sys.exit(1)

    print(f"Parsing HMMER tblout file: {tbl_file}")
    results_summary = []

    #parse the HMMER tblout file
    for qresults in SearchIO.parse(tbl_file, "hmmer3-tab"):
        if not qresults.hits:
            continue  #skip queries with no hits

        #sort hits by E-value (lowest = best)
        hits_sorted = sorted(qresults.hits, key=lambda h: h.evalue)

        best_hit = hits_sorted[0]
        if best_hit.evalue <= evalue_threshold:
            result = {
                "query_id": qresults.id,
                "best_hit_id": best_hit.id,
                "evalue": best_hit.evalue,
                "bit_score": best_hit.bitscore
            }
            results_summary.append(result)

    #output results to file
    if output_file:
        with open(output_file, "w") as out:
            out.write("query_id\tbest_hit_id\tevalue\tbit_score\n")
            for r in results_summary:
                out.write(f"{r['query_id']}\t{r['best_hit_id']}\t{r['evalue']}\t{r['bit_score']:.2f}\n")
        print(f"Results written to {output_file}")
    else:
        for r in results_summary:
            print(f"{r['query_id']}\t{r['best_hit_id']}\t{r['evalue']}\t{r['bit_score']:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_hmmer_results.py <hmmer_tblout [output_file]")
        sys.exit(1)

    tbl_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None

    parse_hmmer_tbl(tbl_file, output_file)

    