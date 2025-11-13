# Fusion 360 flat pattern DXF Exporter 🚀



**Are you tired of manually generating flat patterns for multimple components and exporting them as DXFs?**
**This script will solve that problem for you!**



It automates the identification of sheet metal components, generates flat patterns, and exports them as DXF files. Perfect for streamlining sheet metal design workflows in assemblies with multiple parts.

## Description 📝

This script iterates through all components in the active Fusion 360 design, detects sheet metal parts, creates flat patterns if they don't exist, and exports them as DXF files to a user-selected folder. It handles nested components, skips non-sheet metal parts, and ensures unique file names to avoid overwrites. Designed to run silently with minimal user interaction beyond selecting the output folder.
Features ✨

🔍 Automatic Detection: Scans the entire design (including subassemblies) for sheet metal components.
🛠️ Flat Pattern Generation: Creates flat patterns on-the-fly if none exist, selecting the largest flat face automatically.
📤 DXF Export: Exports each flat pattern as a DXF file using Fusion's ExportManager.
📁 Folder Selection: Uses a folder dialog for choosing the export destination.
⚠️ Error Handling: Gracefully skips components that can't generate flat patterns and continues processing.
📊 Completion Feedback: Displays a message with the number of exported DXFs upon completion.
🔄 Unique Naming: Appends numbers (e.g., _1, _2) to avoid overwriting files with duplicate names.

## Requirements ⚙️

Autodesk Fusion 360 (with API access enabled).
Python (built-in with Fusion 360's scripting environment).
No external libraries required beyond Fusion's API (adsk.core, adsk.fusion).

## Installation 🛠️

Open Fusion 360.
Download the repository .zip, extract it and add it directly via the Scripts and Add-Ins dialog.

## Usage 📖

Open your Fusion 360 design containing sheet metal components.
In the Scripts and Add-Ins panel, select the script and click Run.
A window will appear with the selection of your active sheet metal components and a button for the output path.
The script will process all sheet metal parts that you checked automatically.
Upon completion, a message box will confirm the number of DXF files exported.

Note: **Ensure your design is in the Design workspace. The script skips non-sheet metal components and handles exceptions without interrupting the process.**

## How It Works 🔍

Iteration: Loops through design.allComponents to find those with sheet metal bodies (b.isSheetMetal).
Flat Pattern Creation: If no flat pattern exists, it identifies the largest flat face and calls createFlatPattern(target_face).
Export: Uses exportManager.createDXFFlatPatternExportOptions to save DXFs with sanitized, unique names.
UI Integration: Leverages Fusion's UI for folder selection and messages.

For detailed code comments, refer to the script file.



## 📜 The author 

*Built with ❤️ by Soso Chkhortolia @ARCHMASTER – Happy designing! 🛠️*