## miniproject.py
## 
## Main steps
##    0. Import libraries and parse command line options
##    1. Retrieve Illumina reads for the resequencing of the K-12 project
##    2. Use SPAdes to assemble the reads
##    3. Filter the assembled reads to only include contigs longer than 1000bp
##    4. Calculate the length of the assembly
##    5. Use Prokka to annotate the assembly
##    6. Write Prokka summary results to logfile
##    7. Find discrepencies in coding sequences and tRNAs between the Prokka assembly and RefSeq NC_000913
##    8. Use Tophat and Cufflinks to map reads of the K-12 derivative BW38028 and quantify their expression using the annotated genome NC_000913
##    9. Parse Cufflink output and create transcriptome_data.fpkm, which includes the seqname, start, end, strand, and FPKM for each record in the Cufflinks output file


#====  0. Import libraries and parse command line options ========

import os, argparse, multiprocessing, glob, string, pandas
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

# retrieve files using SRA-toolkit
os.system("prefetch SRX5005282 -O results")

# unpack the .sra file
os.system("fastq-dump -I --outdir results results/SRR8185310/SRR8185310.sra")


#==== 2. Use SPAdes to assemble the reads ========

# make a folder for the SPAdes results
if not os.path.isdir("results/SPAdes"):
    os.mkdir("results/SPAdes")

# write spades command to logfile
with open("results/miniproject.log","a") as handle:
    handle.write("spades.py -k 55,77,99,127 -t " + str(args['threads']) + " -s results/SRR8185310.fastq -o results/SPAdes\n")

# os.system("spades.py -k 55,77,99,127 -t " + str(args['threads']) + " -s results/SRR8185310.fastq -o results/SPAdes")

#==== 3. Filter the assembled reads to only include contigs longer than 1000bp ========

contigs = []
assembly_len = 0

with open("results/SPAdes/contigs.fasta") as handle:
    for read in SeqIO.parse(handle,"fasta"):
        if len(read.seq) > 1000:
            contigs.append(read)
            assembly_len += len(read.seq)

with open("results/miniproject.log","a") as handle:
    handle.write("There are " + str(len(contigs)) + " contigs > 1000 in the assembly.\n")

with open("results/1000bpcontigs.fasta", "w") as handle:
    SeqIO.write(contigs, handle, "fasta")

#==== 4. Calculate the length of the assembly ========

with open("results/miniproject.log","a") as handle:
    handle.write("There are " + str(assembly_len) + " bp in the assembly.\n")

#==== 5. Use Prokka to annotate the assembly ========

# clear any previous results (hope you didn't need them!) from prokka folder or make a folder for the prokka results if one doesn't exist
if os.path.isdir("results/prokka"):
    for f in os.listdir("results/prokka"):
        os.remove(os.path.join("results/prokka", f))
else:
    os.mkdir("results/prokka")

with open("results/miniproject.log","a") as handle:
    handle.write("prokka --cpus " + str(args['threads']) + " --force --genus Escherichia --usegenus --outdir results/prokka results/1000bpcontigs.fasta\n")

# os.system("prokka --cpus " + str(args['threads']) + " --force --genus Escherichia --usegenus --outdir results/prokka results/1000bpcontigs.fasta")

#==== 6. Write Prokka summary results to logfile ========

os.system("cat results/prokka/*.txt >> results/miniproject.log")

#==== 7. Find discrepencies in coding sequences and tRNAs between the Prokka assembly and RefSeq NC_000913 ========

results = dict()

# bit of a hack using glob.glob() to get around the date suffix, but since I cleared the prokka results directory there will only be one .txt file.
for filename in glob.glob("results/prokka/*.txt"):
    with open(filename, "r") as handle:
        lines = handle.readlines()
        for line in lines:
            key, value = string.strip(line).split(": ")
            results[key] = value

NC_000913_CDS = 4140
NC_000913_tRNA = 89

with open("results/miniproject.log","a") as handle:
    handle.write("Prokka found ")

    if NC_000913_CDS - int(results["CDS"]) > 0:
        handle.write(str(NC_000913_CDS - int(results["CDS"])) + " less CDS and ")
    else:
        handle.write(str(abs(NC_000913_CDS - int(results["CDS"]))) + " additional CDS and ")

    if NC_000913_tRNA - int(results["tRNA"]) > 0:
        handle.write(str(NC_000913_tRNA - int(results["tRNA"])) + " less tRNA than the RefSeq\n")
    else:
        handle.write(str(abs(NC_000913_tRNA - int(results["tRNA"]))) + " more tRNA than the RefSeq\n")

#==== 8. Use Tophat and Cufflinks to map reads of the K-12 derivative BW38028 and quantify their expression using the annotated genome NC_000913 ========

# retrieve K-12 derivative BW38028
os.system("prefetch SRR1411276 -O results")

# # unpack the BW38028 .sra file to a fasta file
os.system("fastq-dump -I --outdir results results/SRR1411276/SRR1411276.sra")
## earlier I included the --fasta option, ensure it still works with fastq

# check if bowtie2 results folder exists and make it if it doesn't
if not os.path.isdir("results/bowtie2"):
    os.mkdir("results/bowtie2")

# build bowtie2 index files
os.system("bowtie2-build NC_000913.fasta results/bowtie2/NC_000913 --threads " + str(args['threads']))

# check if tophat results folder exists and make it if it doesn't
if not os.path.isdir("results/tophat"):
    os.mkdir("results/tophat")

# map reads using tophat, do not do novel splice site discovery
os.system("tophat --no-novel-juncs --num-threads " + str(args['threads']) + " --output-dir results/tophat results/bowtie2/NC_000913 results/SRR1411276.fastq")

# check if cufflinks results folder exists and make it if it doesn't
if not os.path.isdir("results/cufflinks"):
    os.mkdir("results/cufflinks")

# cufflinks 
os.system("cufflinks --num-threads " + str(args['threads']) + " -o results/cufflinks results/tophat/accepted_hits.bam")

#==== 9. Parse Cufflink output and create transcriptome_data.fpkm, which includes the seqname, start, end, strand, and FPKM for each record in the Cufflinks output file ========

with open("results/cufflinks/genes.fpkm_tracking") as handle:
    dataframe = pandas.read_csv(handle,delimiter="\t")

out = pandas.DataFrame()

out["seqname"] = dataframe["tracking_id"]

x = dataframe["locus"].str.split("-",expand=True)
out["start"] = x[0].str.split(":",expand=True)[1]
out["end"] = x[1]

out["FPKM"] = dataframe["FPKM"]

with open("results/transcriptome_data.fpkm","w") as handle:
    out.to_csv(handle,index=False)