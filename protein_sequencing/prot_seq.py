#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
15-110 Protein Sequencing Project
Name: Jonathan Taylor
AndrewID: jonathat
"""


from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

project = "ProteinSeq"

def readFile(filename):
    d = open(filename, 'r')
    text = d.read()
    text = text.replace('\n', '')
    return text


def dnaToRna(dna, startIndex):
    """
    dnaToRna - converts DNA sequence into RNA sequence

    Arguments:
        dna: string of DNA sequence that was loaded in Step 0 above

        startIndex: start codon of DNA sequence

    Returns:
        rna: string of RNA sequence
    """

    rna = []
    aug = False
    while startIndex + 2 < len(dna):
        dna = dna.replace("T", "U")
        codon = dna[startIndex:startIndex+3]
        if codon == "AUG" or aug == True:
            aug = True
            if codon == "UAG" or codon == "UAA" or codon == "UGA":
                rna.append(codon)
                return rna
            else:
                rna.append(codon)
                dna = dna[3:]
        else:
            startIndex += 1
    return rna


def makeCodonDictionary():
    """
    makeCodonDictionary - takes the "codon_table.json" file
    (which maps amino acids to a list of codons) and maps
    each codon to its amino acid

    Returns:
        codonD: dictionary in which each codon is paired
        with an amino acid
    """

    codonD = {}
    import json
    c = open("codon_table.json", "r")
    aminoD = json.load(c)
    for key in aminoD:
        value = aminoD[key]
        for codon in value:
            codon = codon.replace("T", "U")
            codonD[codon] = key
    return codonD


def generateProtein(codons, codonD):
    """
    generateProtein - turns RNA sequence into
    protein sequence

    Arguments:
        codons: RNA sequence generated by dnaToRna

        codonD: dictionary generated by makeCodonDictionary

    Returns:
        protein: list of amino acid strings
    """

    protein = []
    for i in range(len(codons)):
        codon = codons[i]
        if codon == "AUG":
            if i == 0:
                protein.append("Start")
            else:
                protein.append(codonD[codon])
        else:
            a_acid = codonD[codon]
            protein.append(a_acid)
    return protein


def synthesizeProteins(filename):
    """
    synthesizeProteins - ties all previous functions together
    and creates a list of proteins from the original DNA sequence

    Argument:
        filename: filename containing DNA sequences

    Returns:
        protein_lst: list of all proteins synthesized from DNA
    """

    dna = readFile(filename)
    codonDict = makeCodonDictionary()
    protein_lst = []
    unused_bases = 0
    i = 0
    while i < len(dna):
        triplet = dna[i:i+3]
        if triplet == "ATG":
            rna_seq = dnaToRna(dna, i)
            protein = generateProtein(rna_seq, codonDict)
            protein_lst.append(protein)
            i += 3 * len(rna_seq)
        else:
            i += 1
            unused_bases += 1

    table = PrettyTable(["Length of DNA in " + filename, "# Proteins", "# Unused Bases"])
    table.add_row([len(dna), len(protein_lst), unused_bases])
    print(table)

    return protein_lst


def commonProteins(proteinList1, proteinList2):
    """
    commonProteins - shows proteins that occur in both genes

    Arguments:
        proteinList1 and 2: two lists of proteins generated
        by synthesizeProteins function

    Returns:
        common_proteins: list of proteins that occur in
        both genes
    """

    common_proteins = []
    for i in range(len(proteinList1)):
        protein = proteinList1[i]
        if protein in proteinList2 and protein not in common_proteins:
            common_proteins.append(protein)
    return common_proteins


def combineProteins(proteinList):
    """
    combineProteins - generates list of all the amino acids that
    occur across all proteins, in order

    Argument:
        proteinList: list of proteins generated by synthesizeProteins

    Returns:
        combined_proteins: list of amino acids occuring in all proteins
    """

    combined_proteins = []
    for i in range(len(proteinList)):
        for aa in range(len(proteinList[i])):
            combined_proteins.append(proteinList[i][aa])
    return combined_proteins


def aminoAcidDictionary(aaList):
    """
    aminoAcidDictionary - counts of each amino acid

    Argument:
        aaList: list of amino acids generated by combineProteins

    Returns:
        aa_dict: dictionary that maps each amino acid to a count of
        how often it occurs
    """

    aa_dict = {}
    for i in range(len(aaList)):
        key = aaList[i]
        if key not in aa_dict:
            aa_dict[key] = aaList.count(key)
    return aa_dict


def sortAminoAcidsByFreq(aaList):
    """
    sortAminoAcidsByFreq - sorts list of amino acids by
    frequency

    Argument:
        aaList: amino acid list generated by combineProteins

    Returns:
        freq_list: list of amino acids sorted from most frequent
        to least frequent
    """

    freq_list = []
    aa_dict = aminoAcidDictionary(aaList)
    for keys in aa_dict.keys():
        frequency = []
        occurance = aa_dict[keys]
        prob = occurance / len(aaList)
        frequency.append(prob)
        if keys != "Start" and keys != "Stop":
            frequency.append(keys)
            freq_list.append(frequency)
    freq_list.sort()
    return freq_list


def findAminoAcidDifferences(proteinList1, proteinList2):
    """
    findAminoAcidDifferences - finds differences
    between genes

    Arguments:
        proteinList1 and 2: two protein lists
        (one for each gene) generated by
        synthesizeProteins

    Returns:
        comb_freq_list: list of amino acids that
        occur at different indexes between the two
        protein lists and their frequencies
    """

    comb_freq_list = []
    comb_prot1 = combineProteins(proteinList1)
    comb_prot2 = combineProteins(proteinList2)
    freq_list1 = sortAminoAcidsByFreq(comb_prot1)
    freq_list2 = sortAminoAcidsByFreq(comb_prot2)
    for i in range(len(freq_list1)):
        for j in range(len(freq_list2)):
            aa_list = []
            aa1 = freq_list1[i][1]
            aa2 = freq_list2[j][1]
            if aa1 == aa2:
                frequency1 = freq_list1[i][0]
                frequency2 = freq_list2[j][0]
                difference = abs(frequency1 - frequency2)
                threshold = 0.005
                aa_list.append(aa1)
                aa_list.append(frequency1)
                aa_list.append(frequency2)
                if i != j and difference >= threshold:
                    comb_freq_list.append(aa_list)
    return comb_freq_list


def displayTextResults(commonalities, differences):
    """
    displayTextResults - generates and displays
    text report of similarities and differences between genes

    Arguments:
        commonalities: list of common proteins between genes

        differences: list of the most different amino acids between genes
    """


    print("The following proteins occurred in both DNA sequences:")
    for i in range(len(commonalities)):
        if len(commonalities[i]) > 2:
            for j in range(1, len(commonalities[i])-1):
                print(commonalities[i][j], end=" ")
        print("")

    table = PrettyTable(["Amino_Acid", "Frequency in Human (%)", "Frequency in Elephant (%)"])

    print("The following amino acids occurred at very different rates in the two DNA sequences:")
    for x in range(len(differences)):
        for y in range(len(differences[x])):
            aa = differences[x][0]
            freq1 = (differences[x][1] * 100)
            freq2 = (differences[x][2] * 100)
        table.add_row([aa, str(freq1), str(freq2)])
    print(table)


def makeAminoAcidLabels(geneList):
    """
    makeAminoAcidLabels - reformats data for plotting

    Argument:
        geneList: list of genes

    Returns:
        xLabels: sorted list of all the amino acids found
    """

    total_aa = []
    sorted_aa_lst = []
    comb_prot = []
    for i in range(len(geneList)):
        comb_prot.append(combineProteins(geneList[i]))
    for j in range(len(comb_prot)):
        for k in range(len(comb_prot[j])):
            total_aa.append(comb_prot[j][k])
    comb_aa_dict = aminoAcidDictionary(total_aa)
    xLabels = list(comb_aa_dict.keys())
    xLabels.sort() #sorted aa_list
    return xLabels


def setupChartData(labels, geneList):
    """
    seupChartData - generates a list of lists
    for plotting with matplotlib

    Arguments:
        labels: labels list generated by
        makeAminoAcidLabels

        geneList: list of genes

    Returns:
        freqList: list of frequency lists
    """

    freqList = []
    for i in range(len(geneList)):
        c = combineProteins(geneList[i])
        dict_aa = aminoAcidDictionary(c)
        freq_lst = []
        for j in range(len(labels)):
            if labels[j] in dict_aa:
                occurance = dict_aa[labels[j]]
                prob = occurance / len(c)
                freq_lst.append(prob)
            else:
                freq_lst.append(0)
        freqList.append(freq_lst)
    return freqList


def createChart(xLabels, freqList, freqLabels, edgeList=None):
    """
    createChart - generates bar chart of results

    Arguments:
    xLabels: labels list generated by makeAminAcidLabels

    freqList: list of frequency lists generated by setupChartData

    freqLabels: list of strings, where each string is the name of
    the gene represented by the corresponding list in freqLists

    edgeList
    """

    x = np.arange(len(xLabels))
    width = 0.6 / len(freqList)
    fig, ax = plt.subplots(figsize=(10, 8))
    for i in range(len(freqList)):
        offset = -0.3 + width/2
        ax.bar(x + offset + i*width, freqList[i], width, edgecolor=edgeList)

    ax.set_ylabel("Frequencies")
    ax.set_title("Protein Sequencing")
    ax.set_xticks(x)
    ax.set_xticklabels(xLabels)
    ax.legend(["Human p53", "Elephant p53"])

    fig.tight_layout()
    plt.show()


def makeEdgeList(labels, biggestDiffs):
    """
    makeEdgeList - adds black edges around the amino acids with
    significantly different frequencies between the two genes

    Arguments:
        labels: labels list generated by makeAminoAcidLabels

        biggestDiffs: list of most different amino acids
        generated by findAminoAcidDifferences

    Returns:
        edge_lst: list, the same length as the labels list, where each
        element of the list is "black" if the corresponding amino acid
        is in the biggestDiffs list, and "white" otherwise.
    """

    lst = []
    edge_lst = []
    for j in range(len(biggestDiffs)):
        lst.append(biggestDiffs[j][0])
    for i in range(len(labels)):
        if labels[i] in lst:
            edge_lst.append("black")
        else:
            edge_lst.append("white")
    return edge_lst


def runFullProgram():
    """
    Pulls all functions defined in this program together to process,
    analyze and display similarities and differences between the
    human and elephant p53 genes
    """

    humanProteins = synthesizeProteins("human_p53.txt")
    elephantProteins = synthesizeProteins("elephant_p53.txt")
    commonalities = commonProteins(humanProteins, elephantProteins)
    differences = findAminoAcidDifferences(humanProteins, elephantProteins)
    displayTextResults(commonalities, differences)
    Labels = makeAminoAcidLabels([humanProteins, elephantProteins])
    freqList = setupChartData(Labels, [humanProteins, elephantProteins])
    freqLabels = ["human", "elephant"]
    edge_List = makeEdgeList(Labels, differences)
    Chart = createChart(Labels, freqList, freqLabels, edge_List)
    return

runFullProgram()
