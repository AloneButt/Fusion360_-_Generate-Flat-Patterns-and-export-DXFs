# Fusion 360 Flat Pattern DXF Exporter

**Are you tired of manually generating flat patterns for multiple components and exporting them as DXFs?**
**This script will solve that problem for you!**

It automates the identification of sheet metal components, generates flat patterns, and exports them as DXF files with the sheet metal rule name in the filename. Perfect for streamlining sheet metal design workflows in assemblies with multiple parts.

## Description

This script provides an interactive dialog to select which sheet metal components to export. It detects sheet metal parts, creates flat patterns if they don't exist, and exports them as DXF files with the sheet metal rule name included in the filename. The exported files follow the naming convention: `[rule name] [component name].dxf` (e.g., `1.5mm Steel Frame.dxf` for a component named "Frame" using the "1.5mm Steel" rule).

## Features

- **Interactive Selection UI**: Choose which sheet metal components to export via checkboxes
- **Automatic Detection**: Scans the entire design (including subassemblies) for sheet metal components
- **Rule Name in Filename**: Automatically prefixes exported DXF files with the sheet metal rule name (e.g., `1.5mm Steel Frame.dxf`)
- **Flat Pattern Generation**: Creates flat patterns on-the-fly if none exist, selecting the largest flat face automatically
- **DXF Export**: Exports each flat pattern as a DXF file using Fusion's ExportManager
- **Folder Selection**: Choose or browse to your desired export destination
- **Error Handling**: Gracefully skips components that can't generate flat patterns and continues processing
- **Completion Feedback**: Displays a message with the number of exported DXFs upon completion
- **Unique Naming**: Appends numbers (e.g., `_1`, `_2`) to avoid overwriting files with duplicate names

## Requirements

- Autodesk Fusion 360 (with API access enabled)
- Python (built-in with Fusion 360's scripting environment)
- No external libraries required beyond Fusion's API (adsk.core, adsk.fusion)

## Installation

1. Open Fusion 360
2. Download the repository .zip and extract it
3. Add it directly via the **Scripts and Add-Ins** dialog

## Usage

1. Open your Fusion 360 design containing sheet metal components
2. In the **Scripts and Add-Ins** panel, select the script and click **Run**
3. A dialog will appear showing all available sheet metal components with checkboxes (all selected by default)
4. Choose which components to export by checking/unchecking the boxes
5. Specify or browse to your desired output folder (default: `C:\FusionExports`)
6. Click **OK** to start the export
7. The script will process all selected sheet metal parts automatically
8. Upon completion, a message box will confirm the number of DXF files exported

**Note:** Ensure your design is in the Design workspace. The script skips non-sheet metal components and handles exceptions without interrupting the process.

## File Naming Convention

Exported DXF files are named with the following format:
```
[rule name] [component name].dxf
```

**Examples:**
- Component named "Frame" using "1.5mm Steel" rule → `1.5mm Steel Frame.dxf`
- Component named "Side Panel" using "2mm Aluminum" rule → `2mm Aluminum Side Panel.dxf`
- Component named "Bracket" using "0.8" rule → `0.8 Bracket.dxf`

If no sheet metal rule is detected, the file will use just the component name.

## How It Works

1. **Component Detection**: Loops through `design.allComponents` to find those with sheet metal bodies (`b.isSheetMetal`)
2. **UI Presentation**: Displays all sheet metal components in a dialog with selection checkboxes
3. **Flat Pattern Creation**: If no flat pattern exists, it identifies the largest flat face and calls `createFlatPattern(target_face)`
4. **Rule Name Extraction**: Retrieves the sheet metal rule name from the component's sheet metal features
5. **Export**: Uses `exportManager.createDXFFlatPatternExportOptions` to save DXFs with rule-name-prefixed, sanitized, unique names
6. **UI Integration**: Leverages Fusion's UI for component selection, folder browsing, and status messages

For detailed code comments, refer to the script file.

## The Author

*Built with ❤️ by Soso Chkhortolia @ARCHMASTER – Happy designing! 🛠️*
