## miniproject.py
## 
## Main steps
##    0. Import libraries and parse command line options
##    1. Retrieve Illumina reads for the resequencing of the K-12 project
##    2. Use SPAdes to assemble the reads
##    3. Filter the assembled reads to only include contigs longer than 1000bp
##    4. Calculate the length of the assembly
##    5. Use Prokka to annotate the assembly
##    6. Write Prokka results to logfile
##    7. Find discrepencies in coding sequences and tRNAs between the Prokka assembly and RefSeq NC_000913
##    8. Use Tophat and Cufflinks to map reads of the K-12 derivative BW38028 and quantify their expression using the annotated genome NC_000913
##    9. Parse Cufflink output and create transcriptome_data.fpkm, which includes the  the seqname, start, end, strand, and FPKM for each record in the Cufflinks output file.


#====  0. Import libraries and parse command line options ========

import os, argparse, multiprocessing
from Bio import SeqIO

ap = argparse.ArgumentParser()
ap.add_argument('-t','--threads', type = int, default = multiprocessing.cpu_count()/2, help = 'Number of CPUs to use in computation. Defaults to half the number of available CPUs', metavar = '')

args = vars(ap.parse_args())

# check if results folder exists and make it if it doesn't
if not os.path.isdir("results"):
    os.mkdir("results")

with open("results/miniproject.log","w") as handle:
    handle.write("running miniproject with " + str(args['threads']) + " threads\n")

# #==== 1. Retrieve Illumina reads for the resequencing of the K-12 project ========

# # retrieve files using SRA-toolkit
# os.system("prefetch SRX5005282 -O results")

# # unpack the .sra file
# os.system("fastq-dump -I --outdir results results/SRR8185310/SRR8185310.sra")


#==== 2. Use SPAdes to assemble the reads ========

# make a folder for the SPAdes results
if not os.path.isdir("results/SPAdes"):
    os.mkdir("results/SPAdes")

# write spades command to logfile
with open("results/miniproject.log","a") as handle:
    handle.write("spades.py -k 55,77,99,127 -t " + str(args['threads']) + " -s results/SRR8185310.fastq -o results/SPAdes\n")

# os.system("spades.py -k 55,77,99,127 -t " + str(args['threads']) + " -s results/SRR8185310.fastq -o results/SPAdes")

#==== 3. Filter the assembled reads to only include contigs longer than 1000bp ========

long = []
assembly_len = 0

with open("results/SPAdes/contigs.fasta") as handle:
    for read in SeqIO.parse(handle,"fasta"):
        if len(read.seq) > 1000:
            long.append(read)
            assembly_len += len(read.seq)

with open("results/miniproject.log","a") as handle:
    handle.write("There are " + str(len(long)) + " contigs > 1000 in the assembly.\n")

#==== 4. Calculate the length of the assembly ========

with open("results/miniproject.log","a") as handle:
    handle.write("There are " + str(assembly_len) + " bp in the assembly.\n")

#==== 5. Use Prokka to annotate the assembly ========
