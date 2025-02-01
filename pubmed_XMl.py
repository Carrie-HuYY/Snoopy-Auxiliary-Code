#!/usr/bin/env python3
'''
解析 pubmed 导出的xml文件,并且转换成xlsx格式
'''
import sys
import time
from lxml import etree
import pandas as pd
import numpy as np
import os


def parse_pubmed_xml(file):
    tree = etree.parse(file)
    root = tree.getroot()
    PMID = None
    ArticleTitle = None
    Journal_name = None
    Abstract = None
    First_author = None
    First_author_Affiliation = None
    DOI = None
    Year = None

    for pubmedArticle in root:
        try:
            PMID = pubmedArticle.find("MedlineCitation/PMID").text
            ArticleTitle = pubmedArticle.find(
                "MedlineCitation/Article/ArticleTitle").text
            Journal_name = pubmedArticle.find(
                "MedlineCitation/Article/Journal/Title").text
            Abstract = pubmedArticle.find(
                "MedlineCitation/Article/Abstract/AbstractText").text
            First_author = pubmedArticle.find(
                "MedlineCitation/Article/AuthorList/Author")[0].find("ForeName").text + " " + pubmedArticle.find(
                "MedlineCitation/Article/AuthorList/Author")[0].find("LastName").text
            First_author_Affiliation = pubmedArticle.find(
                "MedlineCitation/Article/AuthorList/Author[1]/AffiliationInfo/Affiliation").text
            DOI = pubmedArticle.find(
                "MedlineCitation/Article/ELocationID").text
            Year = pubmedArticle.find("MedlineCitation/DateRevised/Year").text
        except:
            pass

        line = {"PMID": PMID, "DOI": DOI, "Journal": Journal_name, "Year": Year, "First_author": First_author,
                "First_author_affiliation": First_author_Affiliation, "Title": ArticleTitle, "Abstract": Abstract}
        yield line


def main(folder_path, base_filename, start_num, end_num, out):
    print("start parsing")
    for num in range(start_num, end_num + 1):
        df = pd.DataFrame(columns=["PMID", "DOI", "Journal", "Year",
                                   "First_author", "First_author_affiliation", "Title", "Abstract"])
        start_time = time.time()
        num_str = f"{num:04d}"
        file_path = os.path.join(folder_path, f"{base_filename}{num_str}.xml")
        file_path = os.path.join(file_path, f"{base_filename}{num_str}.xml")
        out_path = os.path.join(out, f"{base_filename}{num_str}.xlsx")
        line = parse_pubmed_xml(file_path)
        print(f"Processing file: {file_path}")
        for line in parse_pubmed_xml(file_path):
            df = pd.concat([df, pd.DataFrame([line])], ignore_index=True)
        df.to_excel(out_path, index=False)
        finish_time = time.time()
        print(f"Finished in {finish_time - start_time} seconds.")
    print(f"Combined data saved to {out}")


if __name__ == "__main__":
    folder_path = "pubmed_extracted/"
    base_filename = "pubmed25n"
    start_num = 1
    end_num = 4
    output_file = "result/"

    main(folder_path, base_filename, start_num, end_num, output_file)

