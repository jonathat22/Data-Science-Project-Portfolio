import prot_seq
import pytest


def testReadFile():
    print("Testing readFile()...", end="")
    text = prot_seq.readFile("human_p53.txt")
    assert(len(text) == 19149)
    assert(text[:10] == "GATGGGATTG")
    print("... done!")


def testDnaToRna():
    print("Testing dnaToRna()...", end="")
    # Test a basic sequence
    dna = "ATGGATGGACTCTAA"
    assert(prot_seq.dnaToRna(dna, 0) == ["AUG", "GAU", "GGA", "CUC", "UAA"])
    # Test two mRNA strands in a row, with a random codon in between
    dna = "ATGGATGGACTCTAACTCATGCCCTTTTAG"
    assert(prot_seq.dnaToRna(dna, 0) == ["AUG", "GAU", "GGA", "CUC", "UAA"])
    assert(prot_seq.dnaToRna(dna, 18) == ["AUG", "CCC", "UUU", "UAG"])
    # Test a DNA strand that doesn't end properly
    dna = "CCTATGGACCAT"
    assert(prot_seq.dnaToRna(dna, 3) == ["AUG", "GAC", "CAU"])
    print("... done!")


def testMakeCodonDictionary():
    print("Testing makeCodonDictionary()...", end="")
    d = prot_seq.makeCodonDictionary()
    assert(d["AAA"] == "Lys")
    assert(d["GGA"] == "Gly")
    assert(d["AUG"] == "Met")
    assert(d["UAA"] == "Stop")
    print("... done!")


def testGenerateProtein():
    print("Testing generateProtein()...", end="")
    codonD = prot_seq.makeCodonDictionary()
    rna = ["AUG", "GAU", "GGA", "CUC", "UAA"]
    assert(prot_seq.generateProtein(rna, codonD) == ["Start", "Asp", "Gly", "Leu", "Stop"])
    rna = ["AUG", "CCC", "UUU", "UAG"]
    assert(prot_seq.generateProtein(rna, codonD) == ["Start", "Pro", "Phe", "Stop"])
    rna = ["AUG", "GAC", "CAU"]
    assert(prot_seq.generateProtein(rna, codonD) == [ "Start", "Asp", "His"])
    print("... done!")


def testCommonProteins():
    print("Testing commonProteins()...", end="")
    plist1 = [ [ "Start", "Pro", "Val", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "His", "Stop" ] ]
    plist2 = [ [ "Start", "Cys", "Cys", "Tyr", "Stop" ], ["Start", "Glu", "Asp", "Stop" ],
               [ "Start", "His", "Stop" ], [ "Start", "Stop" ], [ "Start", "Met", "Leu", "Stop" ] ]
    plist3 = [ [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Lys", "Stop" ],
               [ "Start", "Asn", "Asn", "Asn", "Asn", "Stop" ] ]
    assert(prot_seq.commonProteins(plist1, plist2) == [ [ "Start", "His", "Stop" ] ])
    assert(sorted(prot_seq.commonProteins(plist1, plist3)) == [ [ "Start", "Asp", "Glu", "Stop" ],
                                                       [ "Start", "Phe", "Stop" ] ])
    assert(prot_seq.commonProteins(plist2, plist3) == [ ])
    print("... done!")


def testCombineProteins():
    print("Testing combineProteins()...", end="")
    plist1 = [ [ "Start", "Pro", "Val", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "His", "Stop" ] ]
    plist2 = [ [ "Start", "Cys", "Cys", "Tyr", "Stop" ], ["Start", "Glu", "Asp", "Stop" ],
               [ "Start", "His", "Stop" ], [ "Start", "Stop" ], [ "Start", "Met", "Leu", "Stop" ] ]
    plist3 = [ [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Lys", "Stop" ],
               [ "Start", "Asn", "Asn", "Asn", "Asn", "Stop" ] ]
    assert(prot_seq.combineProteins(plist1) == [ "Start", "Pro", "Val", "Stop", "Start",
                                        "Phe", "Stop", "Start", "Asp", "Glu",
                                        "Stop", "Start", "His", "Stop" ])
    assert(prot_seq.combineProteins(plist2) == [ "Start", "Cys", "Cys", "Tyr", "Stop",
                                        "Start", "Glu", "Asp", "Stop", "Start",
                                        "His", "Stop", "Start", "Stop", "Start",
                                        "Met", "Leu", "Stop" ])
    assert(prot_seq.combineProteins(plist3) == [ "Start", "Asp", "Glu", "Stop",  "Start",
                                        "Phe", "Stop", "Start", "Asp", "Glu",
                                        "Stop", "Start", "Lys", "Stop", "Start",
                                        "Asn", "Asn", "Asn", "Asn", "Stop" ])
    print("... done!")


def testAminoAcidDictionary():
    print("Testing aminoAcidDictionary()...", end="")
    aaList1 = [ "Start", "Pro", "Val", "Stop", "Start", "Phe", "Stop", "Start",
                "Asp", "Glu", "Stop", "Start", "His", "Stop" ]
    aaList2 = [ "Start", "Cys", "Cys", "Tyr", "Stop", "Start", "Glu", "Asp",
                "Stop", "Start", "His", "Stop", "Start", "Stop", "Start", "Met",
                "Leu", "Stop" ]
    aaList3 = [ "Start", "Asp", "Glu", "Stop",  "Start", "Phe", "Stop", "Start",
                "Asp", "Glu", "Stop", "Start", "Lys", "Stop", "Start", "Asn",
                "Asn", "Asn", "Asn", "Stop" ]
    assert(prot_seq.aminoAcidDictionary(aaList1) == { "Start" : 4, "Pro" : 1, "Val" : 1,
                "Stop" : 4, "Phe" : 1, "Asp" : 1, "Glu" : 1, "His" : 1 })
    assert(prot_seq.aminoAcidDictionary(aaList2) == { "Start" : 5, "Cys" : 2, "Tyr" : 1,
                "Stop" : 5, "Glu" : 1, "Asp" : 1, "His" : 1, "Met" : 1, "Leu" : 1 })
    assert(prot_seq.aminoAcidDictionary(aaList3) == { "Start" : 5, "Asp" : 2, "Glu" : 2,
                "Stop" : 5, "Phe" : 1, "Lys" : 1, "Asn" : 4 })
    print("... done!")


def testSortAminoAcidsByFreq():
    print("Testing sortAminoAcidsByFreq()...", end="")
    aaList1 = [ "Start", "Pro", "Val", "Stop", "Start", "Phe", "Stop", "Start",
                "Asp", "Glu", "Stop", "Start", "His", "Stop" ]
    aaList2 = [ "Start", "Cys", "Cys", "Tyr", "Stop", "Start", "Glu", "Asp",
                "Stop", "Start", "His", "Stop", "Start", "Stop", "Start", "Met",
                "Leu", "Stop" ]
    aaList3 = [ "Start", "Asp", "Glu", "Stop",  "Start", "Phe", "Stop", "Start",
                "Asp", "Glu", "Stop", "Start", "Lys", "Stop", "Start", "Asn",
                "Asn", "Asn", "Asn", "Stop" ]
    result1 = prot_seq.sortAminoAcidsByFreq(aaList1)
    assert(len(result1) == 6)
    # All the amino acids occur once, so they should all have the same frequency
    for i in range(len(result1)):
        assert(result1[0][0] == result1[i][0])
    result2 = prot_seq.sortAminoAcidsByFreq(aaList2)
    assert(len(result2) == 7)
    # All but one of the amino acids occur once
    for i in range(len(result2)-1):
        assert(result2[0][0] == result2[i][0])
    # And Cys occurs twice
    assert(result2[len(result2)-1][0] == 2*result2[0][0])
    assert(result2[len(result2)-1][1] == "Cys")
    # The last one has simple frequencies, we can check it directly
    result3 = prot_seq.sortAminoAcidsByFreq(aaList3)
    assert((result3[0:2] == [[0.05, 'Lys'], [0.05, 'Phe']]) or \
           (result3[0:2] == [[0.05, 'Phe'], [0.05, 'Lys']]))
    assert((result3[2:4] == [[0.1, 'Asp'], [0.1, 'Glu']]) or \
           (result3[2:4] == [[0.1, 'Glu'], [0.1, 'Asp']]))
    assert(result3[4] == [0.2, 'Asn'])
    print("... done!")


def testFindAminoAcidDifferences():
    print("Testing findAminoAcidDifferences()...", end="")
    plist1 = [ [ "Start", "Pro", "Val", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "His", "Stop" ] ]
    plist2 = [ [ "Start", "Cys", "Cys", "Tyr", "Stop" ], ["Start", "Glu", "Asp", "Stop" ],
               [ "Start", "His", "Stop" ], [ "Start", "Stop" ], [ "Start", "Met", "Leu", "Stop" ] ]
    plist3 = [ [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Lys", "Stop" ],
               [ "Start", "Asn", "Asn", "Asn", "Asn", "Stop" ] ]
    result1 = prot_seq.findAminoAcidDifferences(plist1, plist2)
    assert(result1 == [])
    result2 = prot_seq.findAminoAcidDifferences(plist1, plist3)
    assert(len(result2) == 3)
    assert(sorted([result2[0][0], result2[1][0]]) == ["Asp", "Glu"])
    assert(result2[2][0] == "Phe")
    result3 = prot_seq.findAminoAcidDifferences(plist2, plist3)
    assert(len(result3) == 2)
    assert(sorted([result3[0][0], result3[1][0]]) == ["Asp", "Glu"])
    print("... done!")


def testMakeAminoAcidLabels():
    print("Testing makeAminoAcidLabels()...", end="")
    plist1 = [ [ "Start", "Pro", "Val", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "His", "Stop" ] ]
    plist2 = [ [ "Start", "Cys", "Cys", "Tyr", "Stop" ], ["Start", "Glu", "Asp", "Stop" ],
               [ "Start", "His", "Stop" ], [ "Start", "Stop" ], [ "Start", "Met", "Leu", "Stop" ] ]
    plist3 = [ [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Lys", "Stop" ],
               [ "Start", "Asn", "Asn", "Asn", "Asn", "Stop" ] ]
    geneList = [ plist1, plist2, plist3 ]
    assert(prot_seq.makeAminoAcidLabels(geneList) == [ "Asn", "Asp", "Cys", "Glu", "His",
                "Leu", "Lys", "Met", "Phe", "Pro", "Start", "Stop", "Tyr", "Val" ])
    print("... done!")


def testSetupChartData():
    print("Testing setupChartData()...", end="")
    plist1 = [ [ "Start", "Pro", "Val", "Stop" ], [ "Start", "Phe", "Stop" ],
            [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "His", "Stop" ] ]
    plist2 = [ [ "Start", "Cys", "Cys", "Tyr", "Stop" ], ["Start", "Glu", "Asp", "Stop" ],
            [ "Start", "His", "Stop" ], [ "Start", "Stop" ], [ "Start", "Met", "Leu", "Stop" ] ]
    plist3 = [ [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Lys", "Stop" ],
               [ "Start", "Asn", "Asn", "Asn", "Asn", "Stop" ] ]
    geneList = [ plist1, plist2, plist3 ]
    labels = prot_seq.makeAminoAcidLabels(geneList)
    result = prot_seq.setupChartData(labels, geneList)
    assert(len(result) == 3 and len(result[0]) == 14)
    assert(result[0][0] == 0 and result[1][0] == 0 and result[2][0] == 0.2)
    print("... done!")


def testCreateChart():
    print("Testing createChart()...", end="")
    plist1 = [ [ "Start", "Pro", "Val", "Stop" ], [ "Start", "Phe", "Stop" ],
            [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "His", "Stop" ] ]
    plist2 = [ [ "Start", "Cys", "Cys", "Tyr", "Stop" ], ["Start", "Glu", "Asp", "Stop" ],
            [ "Start", "His", "Stop" ], [ "Start", "Stop" ], [ "Start", "Met", "Leu", "Stop" ] ]
    plist3 = [ [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Lys", "Stop" ],
               [ "Start", "Asn", "Asn", "Asn", "Asn", "Stop" ] ]
    geneList = [ plist1, plist2, plist3 ]
    labels = prot_seq.makeAminoAcidLabels(geneList)
    freqList = prot_seq.setupChartData(labels, geneList)
    freqLabels = ["Ex1", "Ex2", "Ex3"]
    prot_seq.createChart(labels, freqList, freqLabels)
    print("... check your chart!")


def testMakeEdgeList():
    print("Testing makeEdgeList()...", end="")
    plist1 = [ [ "Start", "Pro", "Val", "Stop" ], [ "Start", "Phe", "Stop" ],
            [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "His", "Stop" ] ]
    plist3 = [ [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Phe", "Stop" ],
               [ "Start", "Asp", "Glu", "Stop" ], [ "Start", "Lys", "Stop" ],
               [ "Start", "Asn", "Asn", "Asn", "Asn", "Stop" ] ]
    geneList = [ plist1, plist3 ]
    labels = prot_seq.makeAminoAcidLabels(geneList)
    biggestDiffs = prot_seq.findAminoAcidDifferences(plist1, plist3)
    result = prot_seq.makeEdgeList(labels, biggestDiffs)
    assert(result == ['white', 'black', 'black', 'white', 'white', 'black',
                      'white', 'white', 'white', 'white'])
    print("... done!")
