#/bin/bash
#Script for whole genome sequencing
#Building No.2
################
#GLOBAL SETTING#
################

java="/data/hgl/AQ/Tools/java-8/bin/java"
TOOLS_PATH="/data/hgl/AQ/Tools"
REF_PATH="/data/hgl/AQ/H_refgenome"
dbSNP="/data/hgl/AQ/H_refgenome/common_all_20180418.vcf"
humanref="/data/GAL/00Pub/hg19.ref/bwa07/ref.fa"
trimmomatic="$TOOLS_PATH/Trimmomatic-0.38/"
adapter="$TOOLS_PATH/Trimmomatic-0.38/adapters/TruSeq3-PE.fa"
bwa="$TOOLS_PATH/bwa-0.7.12/bwa"
gatk="$TOOLS_PATH/gatk-4.1.0.0/gatk-package-4.1.0.0-local.jar"
picard="$TOOLS_PATH/PICARD-2.18.7/picard.jar"
annovar_convert="$TOOLS_PATH/annovar/convert2annovar.pl"
annovar="$TOOLS_PATH/annovar/annotate_variation.pl"
humandb="$REF_PATH/humandb"
G_REF="/data/hgl/AQ/H_refgenome/hg19/ref.fa" 

#########################
#SAMPLE DATA PREPARATION#
#########################

echo -e "\e[31m ======================= \e[0m"
echo -e "\e[31m SAMPLE DATA PREPARATION \e[0m"
echo -e "\e[31m ======================= \e[0m"

#Get sample name and sample information

sample_id=$1

$java -jar $trimmomatic"trimmomatic-0.38.jar" PE \
-threads 10 -phred33 -trimlog ${sample_id}.log \
-summary ${sample_id}.log \
 ${sample_id}_1.fastq.gz ${sample_id}_2.fastq.gz \
${sample_id}_1.paired.fastq ${sample_id}_1.unpaired.fastq.gz \
${sample_id}_2.paired.fastq ${sample_id}_2.unpaired.fastq.gz \
ILLUMINACLIP:$adapter:2:30:10 \
LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
read1=${sample_id}_1.paired.fastq
read2=${sample_id}_2.paired.fastq

##################
#MAPPING WITH BWA#
##################

echo "==============="
echo "MAPING WITH BWA"
echo "==============="

$bwa mem -t 10 $humanref $read1 $read2 > ${sample_id}.sam

##################
#SORT WITH PICARD#
##################

echo "================"
echo "SORT WITH PICARD"
echo "================"

$java -Xmx32G -jar $picard SortSam \
I=${sample_id}.sam \
O=${sample_id}.sort.bam \
SORT_ORDER=coordinate \
CREATE_INDEX=true
VALIDATION_STRINGENCY=SILENT

#####################
#FIXMATE WITH PICARD#
#####################

echo "==================="
echo "FIXMATE WITH PICARD"
echo "==================="

$java -Xmx32G -jar $picard FixMateInformation \
I=${sample_id}.sort.bam \
O=${sample_id}.sort.fixmate.bam \
SORT_ORDER=coordinate \
CREATE_INDEX=true \
VALIDATION_STRINGENCY=SILENT

########
#FILTER#
########

#Add group by Picard

echo "====================="
echo "ADD GROUP WITH PICARD"
echo "====================="

$java -Xmx32G -jar $picard AddOrReplaceReadGroups \
I=${sample_id}.sort.fixmate.bam \
O=${sample_id}.sort.fixmate.group.bam \
SORT_ORDER=coordinate \
RGID=4 \
RGLB=lib1 \
RGPL=illumina \
RGPU=unit1 \
RGSM=20 \
CREATE_INDEX=true

#filter by GATK

echo "=============="
echo "FILTER BY GATK"
echo "=============="

$java -Xmx32G -jar $gatk PrintReads \
-I ${sample_id}.sort.fixmate.group.bam \
-O ${sample_id}.sort.fixmate.group.filter.bam \
--read-filter MappedReadFilter \
--read-filter PairedReadFilter \
--read-filter ProperlyPairedReadFilter
#note keep mapped read, reads with pair, pass PE resolution

###################
#REMOVE DUPLICATES#
###################

echo "==========================="
echo "REMOVE DUPLICATES BY Picard"
echo "==========================="

$java -Xmx32G -jar $picard MarkDuplicates \
I=${sample_id}.sort.fixmate.group.filter.bam \
O=${sample_id}.sort.fixmate.group.filter.markdup.bam \
M=${sample_id}_marked_dup_metric.txt \
CREATE_INDEX=true \
VALIDATION_STRINGENCY=SILENT 
#Note: markdup = marked duplicates


############################
#FILTER LOW QUALITY MAPPING#
############################

echo "=================================="
echo "FILTER LOW QUALTIY MAPPING BY GATK"
echo "=================================="

$java -Xmx32G -jar $gatk \
PrintReads \
-I ${sample_id}.sort.fixmate.group.filter.markdup.bam \
-O ${sample_id}.sort.fixmate.group.filter.markdup.FLQM.bam \
--read-filter MappingQualityReadFilter \
--minimum-mapping-quality 10 
#Note: FLQM = Filter low quality mapping

##################
#CALLING VARIANTS#
##################

echo "=========================================="
echo "CALLING VARIANT BY HAPLOTYPECALLER IN GATK"
echo "=========================================="
$java -Xmx32G -jar $gatk HaplotypeCaller -R $G_REF -I ${sample_id}.sort.fixmate.group.filter.markdup.FLQM.bam \
-O ${sample_id}.raw.vcf


#################################################
#SEPARATE RAW VCF INTO SNPS AND INDELS VCF FILES#
#################################################

echo "========================================================"
echo "SEPERATE RAW DATA INTO SNPS AND INDELS FILES BY VCFTOOLS"
echo "========================================================"

vcftools --vcf ${sample_id}.raw.vcf --out ${sample_id}.indels.raw \
--keep-only-indels --recode --recode-INFO-all

vcftools --vcf ${sample_id}.raw.vcf --out ${sample_id}.SNPs.raw \
--remove-indels --recode --recode-INFO-all

#index snps and indels raw files

$java -Xmx32G -jar $gatk IndexFeatureFile --feature-file ${sample_id}.SNPs.raw.recode.vcf
$java -Xmx32G -jar $gatk IndexFeatureFile --feature-file ${sample_id}.indels.raw.recode.vcf 

####################
#VARIANT FILTRATION#
####################

echo "=========================="
echo "VARIANT FILTRATION BY GATK"
echo "=========================="

#variant filtration indels file

$java -Xmx32G -jar $gatk VariantFiltration \
--output  ${sample_id}.indels.vcf \
--variant ${sample_id}.indels.raw.recode.vcf \
-R $G_REF \
--filter-expression "QD < 2.0" \
--filter-name "QDFilter"
--filter-expression "ReadPosRankSum < -20.0" \
--filter-name "ReadPosFilter" \
--filter-expression "FS > 200.0" \
--filter-name "FSFilter" \
--filter-expression "MQ0 >= 4 && ((MQ0 / (1.0*DP)) > 0.1)" \
--filter-name "HARD_TO_VALIDATE" \
--filter-expression "QUAL < 30.0 || DP < 6 || DP > 5000 || HRun > 5" \
--filter-name "QualFilter"

mline2=`grep -n "#CHROM" ${sample_id}.indels.vcf | cut -d':' -f 1`
head -n $mline2 ${sample_id}.indels.vcf > ${sample_id}.headindels.vcf
cat ${sample_id}.indels.vcf | grep PASS \
  | cat ${sample_id}.headindels.vcf -> ${sample_id}.indels.PASS.vcf

#index indels pass files

$java -Xmx32G -jar $gatk IndexFeatureFile --feature-file ${sample_id}.indels.PASS.vcf

#variant filtration snps file

$java -Xmx32G -jar $gatk VariantFiltration \
-R $G_REF \
--output ${sample_id}.SNPs.vcf \
--variant ${sample_id}.SNPs.raw.recode.vcf \
--mask ${sample_id}.indels.PASS.vcf \
--mask-name InDel \
--cluster-size 3 \
--cluster-window-size 10 \
--filter-expression "QD < 2.0" \
--filter-name "QDFilter" \
--filter-expression "MQ < 40.0" \
--filter-name "MQFilter" \
--filter-expression "FS > 60.0" \
--filter-name "FSFilter" \
--filter-expression "HaplotypeScore > 13.0" \
--filter-name "HaplotypeScoreFilter" \
--filter-expression "MQRankSum < -12.5" \
--filter-name "MQRankSumFilter" \
--filter-expression "ReadPosRankSum < -8.0" \
--filter-name "ReadPosRankSumFilter"
--filter-expression "QUAL < 30.0 || DP < 6 || DP > 5000 ||HRun > 5" \
--filter-name "StandardFilters" \
--filterExpression "MQ0 >= 4 && ((MQ0 / (1.0 * DP)) > 0.1)" \
--filter-name "HARD_TO_VALIDATE"

mline=`grep -n "#CHROM" ${sample_id}.SNPs.vcf | cut -d':' -f 1`
head -n $mline ${sample_id}.SNPs.vcf > ${sample_id}.headSNPs.vcf
cat ${sample_id}.SNPs.vcf | grep PASS \
  | cat ${sample_id}.headSNPs.vcf -> ${sample_id}.SNPs.PASS.vcf

############
#ANNOTATION#
############

#Convert VCF to annovar readable format

echo "=============================="
echo "PREPARE INPUT FILE FOR ANNOVAR"
echo "=============================="

$annovar_convert -format vcf4 --includeinfo \
 ${sample_id}.SNPs.PASS.vcf -outfile ${sample_id}.SNPs.PASS.avinput

$annovar_convert -format vcf4 --includeinfo \
 ${sample_id}.indels.PASS.vcf -outfile ${sample_id}.indels.PASS.avinput

#Annotate variants by ANNOVAR

echo "=================="
echo "VARIANT ANNOTATION"
echo "=================="

$annovar -buildver hg19 \
${sample_id}.SNPs.PASS.avinput \
$humandb \
--outfile ${sample_id}.SNPs 

$annovar -buildver hg19 \
${sample_id}.indels.PASS.avinput \
$humandb \
--outfile ${sample_id}.indels


