#  GDA Copyright (c) 2022.
#  University of Belgrade, Faculty of Mathematics
#  Luka Milosevic
#  lukamilosevic11@gmail.com
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

import pandas as pd

BEFORE = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>GDA</title>
  <meta name="description" content="GDA - gene disease annotation file">
  <meta name="author" content="lukamilosevic11">

  <meta property="og:title" content="GDA">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://github.com/lukamilosevic11/GDA">
  <meta property="og:description" content="GDA - gene disease annotation file">
<!--  <meta property="og:image" content="image.png">-->

<!--  <link rel="icon" href="/favicon.ico">-->
<!--  <link rel="icon" href="/favicon.svg" type="image/svg+xml">-->
<!--  <link rel="apple-touch-icon" href="/apple-touch-icon.png">-->

<!--  <link rel="stylesheet" href="css/styles.css?v=1.0">-->
<link rel="stylesheet" type="text/css" href="Source/DataTables/datatables.min.css"/>
</head>

<body>
    <div class="container">
      <h1>Annotation file</h1>
    </div>
    <div class="container">
    <table id="annotation" class="display table table-striped table-bordered dt-responsive nowrap" style="width:100%">
        <thead>
            <tr>
                <th>Gene Symbol</th>
                <th>Entrez ID</th>
                <th>Uniprot ID</th>
                <th>Ensembl ID</th>
                <th>DOID</th>
                <th>Sources</th>
                <th>Disease Name</th>
            </tr>
        </thead>
        <tbody>
"""

AFTER = """
        </tbody>
    </table>
    </div>
    <script type="text/javascript" src="./Source/DataTables/datatables.min.js"></script>
    <script type="text/javascript" src="./Source/CustomJS/createDataTable.js"></script>
</body>
</html>
"""


class DataTables:
    def __init__(self, filePath):
        self.__annotationData = pd.read_csv(filePath, sep='\t').to_numpy()
        self.fileContents = ""
        self.__ParseData()

    def __ParseData(self):
        tbody = ""
        for row in self.__annotationData:
            tbody += "<tr>"
            for attribute in row:
                tbody += "<td>" + str(attribute) + "</td>"
            tbody += "</tr>"

        self.fileContents = BEFORE + tbody + AFTER

    def CreateDataTableHTML(self, filePath):
        with open(filePath, 'w') as htmlFile:
            htmlFile.write(self.fileContents)
