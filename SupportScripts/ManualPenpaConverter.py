import json
import re

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — edit these before running
# ═════════════════════════════════════════════════════════════════════════════

FNameWithoutExtension = "five_of_diamonds"
INPUT_FILE  = f"{FNameWithoutExtension}.json"
REPORT_FILE = f"{FNameWithoutExtension}_report.txt"

METADATA = {
    "url"             : "https://sudokupad.app/k3ancvxjzb",
    "PuzzleTestStatus": "Unverified",
}

# ═════════════════════════════════════════════════════════════════════════════


# ─────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────

def ParseRC(RCCoordinate):
    match = re.match(r'R(\d+)C(\d+)', RCCoordinate)
    if match:
        return [int(match.group(1)) - 1, int(match.group(2)) - 1]
    return None


def SectionHeader(Title):
    Line = "=" * 60
    return f"\n{Line}\n{Title}\n{Line}\n"


# ─────────────────────────────────────────────
# LOAD INPUT
# ─────────────────────────────────────────────

with open(INPUT_FILE, 'r') as IP_File:
    data = json.load(IP_File)

InputJSONKeys = list(data.keys())

ReportLines = []


# ─────────────────────────────────────────────
# PUZZLE INFO
# ─────────────────────────────────────────────

ReportLines.append(SectionHeader("PUZZLE INFO"))

Title  = data.get("title",  METADATA.get("title",  "N/A"))
Author = data.get("author", METADATA.get("author", "N/A"))
URL    = METADATA.get("url", "N/A")
Status = METADATA.get("PuzzleTestStatus", "Unverified")

ReportLines.append(f"Title  : {Title}")
ReportLines.append(f"Author : {Author}")
ReportLines.append(f"URL    : {URL}")
ReportLines.append(f"Status : {Status}")

if "ruleset" in InputJSONKeys:
    ReportLines.append(f"Rules  : {data['ruleset'].strip()}")


# ─────────────────────────────────────────────
# GRID / MATRIX
# ─────────────────────────────────────────────

if "grid" in InputJSONKeys:

    ReportLines.append(SectionHeader("GRID / MATRIX"))

    Grid = data["grid"]
    Size = len(Grid)

    # Detect if any cell has a given marker
    HasGivens = any(
        "given" in cell
        for row in Grid
        for cell in row
        if isinstance(cell, dict)
    )

    if not HasGivens:
        # Check if any cell has a value at all
        HasValues = any(
            "value" in cell
            for row in Grid
            for cell in row
            if isinstance(cell, dict)
        )

        if HasValues:
            ReportLines.append("NOTE: Grid contains values but no 'given' markers.")
            ReportLines.append("      These are likely solution values, not givens.")
            ReportLines.append("      Matrix will be all zeros — verify manually.\n")
        else:
            ReportLines.append("NOTE: Grid is empty — no givens. Matrix is all zeros.\n")

        Matrix = [[0] * Size for _ in range(Size)]

    else:
        Matrix = [[0] * Size for _ in range(Size)]
        for i, row in enumerate(Grid):
            for j, cell in enumerate(row):
                if isinstance(cell, dict) and cell.get("given", False) and "value" in cell:
                    Matrix[i][j] = int(cell["value"])

    ReportLines.append("Matrix = [")
    for row in Matrix:
        ReportLines.append(f"    {row},")
    ReportLines.append("]")


# ─────────────────────────────────────────────
# DIFFERENCE PAIRS
# ─────────────────────────────────────────────

if "difference" in InputJSONKeys:

    '''
    Expecting the difference to be like this:
    "difference": [
        {"cells": ["R7C4", "R8C4"]},
        {"cells": ["R8C4", "R9C4"]},
        ...
    ]
    By default, the differences are equal to 1.
    If a "value" key is present on an entry, that value is used instead.
    '''

    ReportLines.append(SectionHeader("DIFFERENCE PAIRS"))

    DifferencePairs = []
    DifferencePairsDifferences = []

    if type(data["difference"]) is list:
        for entry in data["difference"]:
            CellList = []
            for RCCoordinate in entry["cells"]:
                pair = ParseRC(RCCoordinate)
                if pair:
                    CellList.append(pair)
            DifferencePairs.append(CellList)
            DiffValue = int(entry["value"]) if "value" in entry else 1
            DifferencePairsDifferences.append(DiffValue)

    ReportLines.append(f"Total pairs: {len(DifferencePairs)}\n")
    ReportLines.append("DifferencePairsCondition = True")
    ReportLines.append("DifferencePairs = [")
    for Pair in DifferencePairs:
        ReportLines.append(f"    {Pair},")
    ReportLines.append("]")
    ReportLines.append(f"DifferencePairsDifferences = {DifferencePairsDifferences}")


# ─────────────────────────────────────────────
# RATIO PAIRS
# ─────────────────────────────────────────────

if "ratio" in InputJSONKeys:

    '''
    Expecting the ratio to be like this:
    "ratio": [
        {"cells": ["R7C4", "R8C4"]},
        {"cells": ["R8C4", "R9C4"]},
        ...
    ]
    By default, the ratio is 1:2.
    If a "value" key is present as "n/d", that is used instead.
    '''

    ReportLines.append(SectionHeader("RATIO PAIRS"))

    RatioPairs = []
    RatioPairsNumerators = []
    RatioPairsDenominators = []

    if type(data["ratio"]) is list:
        for entry in data["ratio"]:
            CellList = []
            for RCCoordinate in entry["cells"]:
                pair = ParseRC(RCCoordinate)
                if pair:
                    CellList.append(pair)
            RatioPairs.append(CellList)

            Value = str(entry.get("value", "1/2"))
            if "/" in Value:
                Parts = Value.split("/")
                try:
                    RatioPairsNumerators.append(int(Parts[0]))
                    RatioPairsDenominators.append(int(Parts[1]))
                except (ValueError, IndexError):
                    RatioPairsNumerators.append(1)
                    RatioPairsDenominators.append(2)
            else:
                RatioPairsNumerators.append(1)
                RatioPairsDenominators.append(2)

    ReportLines.append(f"Total pairs: {len(RatioPairs)}\n")
    ReportLines.append("RatioPairsCondition = True")
    ReportLines.append("RatioPairs = [")
    for Pair in RatioPairs:
        ReportLines.append(f"    {Pair},")
    ReportLines.append("]")
    ReportLines.append(f"RatioPairsNumerators   = {RatioPairsNumerators}")
    ReportLines.append(f"RatioPairsDenominators = {RatioPairsDenominators}")


# ─────────────────────────────────────────────
# KILLER CAGES
# ─────────────────────────────────────────────

if "killercage" in InputJSONKeys:

    '''
    Expecting killer cages to be like this:
    "killercage": [
        {"cells": ["R1C1", "R1C2"], "value": "14"},
        ...
    ]
    '''

    ReportLines.append(SectionHeader("KILLER CAGES"))

    Size = data.get("size", 9)
    KillerCageMap = [[0] * Size for _ in range(Size)]
    KillerCageSums = []

    for CageID, CageEntry in enumerate(data["killercage"], start=1):
        try:
            KillerCageSums.append(int(CageEntry.get("value", 0)))
        except (ValueError, TypeError):
            KillerCageSums.append(0)

        for RCCoordinate in CageEntry.get("cells", []):
            pair = ParseRC(RCCoordinate)
            if pair:
                KillerCageMap[pair[0]][pair[1]] = CageID

    ReportLines.append(f"Total cages: {len(KillerCageSums)}\n")
    ReportLines.append("KillerCage = True")
    ReportLines.append("KillerCageMap = [")
    for row in KillerCageMap:
        ReportLines.append(f"    {row},")
    ReportLines.append("]")
    ReportLines.append(f"KillerCageSums = {KillerCageSums}")


# ─────────────────────────────────────────────
# WHISPERS (dedicated key)
# ─────────────────────────────────────────────

if "whispers" in InputJSONKeys:

    '''
    Expecting whispers to be like this:
    "whispers": [
        {"lines": [["R2C1", "R1C2", "R2C3", "R3C2"]], "value": "4"},
        ...
    ]
    value = minimum difference (4 = Dutch, 5 = German)
    '''

    ReportLines.append(SectionHeader("WHISPERS (dedicated key)"))

    WhisperGroups = {}

    for entry in data["whispers"]:
        DiffVal = int(entry.get("value", 5))
        WhisperGroups.setdefault(DiffVal, [])
        for Segment in entry.get("lines", []):
            LineCells = []
            for RCCoordinate in Segment:
                pair = ParseRC(RCCoordinate)
                if pair:
                    LineCells.append(pair)
            if LineCells:
                WhisperGroups[DiffVal].append(LineCells)

    for DiffVal, Lines in sorted(WhisperGroups.items()):
        Label = "German Whispers" if DiffVal >= 5 else "Dutch Whispers" if DiffVal == 4 else f"Line Difference >= {DiffVal}"
        ReportLines.append(f"Difference value {DiffVal} — {Label} — {len(Lines)} segment(s):")
        for Line in Lines:
            ReportLines.append(f"    {Line},")
        ReportLines.append("")


# ─────────────────────────────────────────────
# RENBAN (dedicated key)
# ─────────────────────────────────────────────

if "renban" in InputJSONKeys:

    ReportLines.append(SectionHeader("RENBAN LINES (dedicated key)"))

    RenbanLines = []
    for entry in data["renban"]:
        for Segment in entry.get("lines", []):
            LineCells = []
            for RCCoordinate in Segment:
                pair = ParseRC(RCCoordinate)
                if pair:
                    LineCells.append(pair)
            if LineCells:
                RenbanLines.append(LineCells)

    ReportLines.append(f"Total segments: {len(RenbanLines)}\n")
    ReportLines.append("RenbanCondition = True")
    ReportLines.append("RenbanLines = [")
    for Line in RenbanLines:
        ReportLines.append(f"    {Line},")
    ReportLines.append("]")


# ─────────────────────────────────────────────
# THERMOMETER (dedicated key)
# ─────────────────────────────────────────────

if "thermometer" in InputJSONKeys:

    ReportLines.append(SectionHeader("THERMOMETERS (dedicated key)"))

    Thermometers = []
    for entry in data["thermometer"]:
        for Segment in entry.get("lines", []):
            LineCells = []
            for RCCoordinate in Segment:
                pair = ParseRC(RCCoordinate)
                if pair:
                    LineCells.append(pair)
            if LineCells:
                Thermometers.append(LineCells)

    ReportLines.append(f"Total thermometers: {len(Thermometers)}\n")
    ReportLines.append("ThermometerConstraint = True")
    ReportLines.append("Thermometers = [")
    for Line in Thermometers:
        ReportLines.append(f"    {Line},")
    ReportLines.append("]")


# ─────────────────────────────────────────────
# ARROW (dedicated key)
# ─────────────────────────────────────────────

if "arrow" in InputJSONKeys:

    ReportLines.append(SectionHeader("ARROWS (dedicated key)"))

    ArrowCircles = []
    ArrowBodies  = []

    for entry in data["arrow"]:
        CircleCells = entry.get("cells", [])
        if not CircleCells:
            continue

        Circle = ParseRC(CircleCells[0])
        if not Circle:
            continue

        for Segment in entry.get("lines", []):
            LineCells = []
            for RCCoordinate in Segment:
                pair = ParseRC(RCCoordinate)
                if pair:
                    LineCells.append(pair)
            if LineCells:
                ArrowCircles.append(Circle)
                ArrowBodies.append(LineCells)

    ReportLines.append(f"Total arrows: {len(ArrowCircles)}\n")
    ReportLines.append("ArrowSumSudoku = True")
    ReportLines.append("ArrowSumSudokuCircles = [")
    for Circle in ArrowCircles:
        ReportLines.append(f"    {Circle},")
    ReportLines.append("]")
    ReportLines.append("ArrowSumSudokuBodies = [")
    for Body in ArrowBodies:
        ReportLines.append(f"    {Body},")
    ReportLines.append("]")


# ─────────────────────────────────────────────
# XV / ADDITION PAIRS (dedicated key)
# ─────────────────────────────────────────────

if "xv" in InputJSONKeys:

    '''
    Expecting XV to be like this:
    "xv": [
        {"cells": ["R1C1", "R1C2"], "value": "X"},
        {"cells": ["R2C2", "R2C3"], "value": "V"},
        ...
    ]
    X = sum 10, V = sum 5
    '''

    ReportLines.append(SectionHeader("XV / ADDITION PAIRS (dedicated key)"))

    AdditionPairs = []
    AdditionPairsSums = []

    for entry in data["xv"]:
        CellList = []
        for RCCoordinate in entry.get("cells", []):
            pair = ParseRC(RCCoordinate)
            if pair:
                CellList.append(pair)
        if len(CellList) == 2:
            AdditionPairs.append(CellList)
            AdditionPairsSums.append(10 if str(entry.get("value", "X")).upper() == "X" else 5)

    ReportLines.append(f"Total pairs: {len(AdditionPairs)}\n")
    ReportLines.append("AdditionPairsCondition = True")
    ReportLines.append("AdditionPairs = [")
    for Pair in AdditionPairs:
        ReportLines.append(f"    {Pair},")
    ReportLines.append("]")
    ReportLines.append(f"AdditionPairsSums = {AdditionPairsSums}")


# ─────────────────────────────────────────────
# LINES (colour-grouped, manual classification)
# ─────────────────────────────────────────────

if "line" in InputJSONKeys:

    ReportLines.append(SectionHeader("LINES (colour-grouped — classify manually)"))

    LineConstraints = set()
    LineColours     = set()
    LineWidths      = set()

    for LineDict in data["line"]:
        if "fromConstraint" in LineDict.keys():
            LineConstraints.add(LineDict["fromConstraint"])
        if "outlineC" in LineDict.keys():
            LineColours.add(LineDict["outlineC"])
        if "width" in LineDict.keys():
            LineWidths.add(LineDict["width"])

    ReportLines.append(f"Colours found  : {sorted(LineColours)}")
    ReportLines.append(f"Widths found   : {sorted(LineWidths)}")
    ReportLines.append(f"Constraints    : {sorted(LineConstraints) if LineConstraints else 'None — colour-only'}\n")

    # Group lines by colour
    LineGroups = {}
    for Colour in sorted(LineColours):
        LineGroups[Colour] = []
        for LineDict in data["line"]:
            if LineDict.get("outlineC") != Colour:
                continue
            for Segment in LineDict["lines"]:
                LineCells = []
                for RCCoordinate in Segment:
                    pair = ParseRC(RCCoordinate)
                    if pair:
                        LineCells.append(pair)
                if LineCells:
                    LineGroups[Colour].append(LineCells)

    for Colour, Lines in LineGroups.items():
        ReportLines.append(f"Colour {Colour} — {len(Lines)} segment(s):")
        for Line in Lines:
            ReportLines.append(f"    {Line},")
        ReportLines.append("")


# ─────────────────────────────────────────────
# UNHANDLED KEYS NOTICE
# ─────────────────────────────────────────────

HandledKeys = {
    "size", "title", "author", "ruleset", "solution", "grid",
    "difference", "ratio", "killercage", "whispers", "renban",
    "thermometer", "arrow", "xv", "line"
}

UnhandledKeys = [k for k in InputJSONKeys if k not in HandledKeys]

if UnhandledKeys:
    ReportLines.append(SectionHeader("UNHANDLED KEYS — MANUAL TRANSCRIPTION NEEDED"))
    for key in UnhandledKeys:
        ReportLines.append(f"  {key}")


# ─────────────────────────────────────────────
# WRITE REPORT
# ─────────────────────────────────────────────

with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write("\n".join(ReportLines))

print(f"Report written to: {REPORT_FILE}")