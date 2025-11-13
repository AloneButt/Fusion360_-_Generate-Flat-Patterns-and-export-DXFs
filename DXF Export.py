#Author-
#Description- Export selected sheet metal components as DXF with selection UI

import adsk.core, adsk.fusion, adsk.cam, traceback, os

app = adsk.core.Application.get()
ui = app.userInterface

selected_components = []


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs

            # Add image at the top of the dialog
            image_input = inputs.addImageCommandInput('image', '', 'image.png')
            image_input.isFullWidth = True
            image_input.imageHeight = 25  # Height in pixels
            image_input.imageWidth = 50   # Width in pixels

            design = adsk.fusion.Design.cast(app.activeProduct)
            all_comps = design.allComponents

            sheet_metal_comps = [c for c in all_comps if any(b.isSheetMetal for b in c.bRepBodies)]

            if not sheet_metal_comps:
                ui.messageBox('No sheet metal components found.')
                return

            # Group inputs for better organization
            group = inputs.addGroupCommandInput('group', 'Select Components')
            groupChildren = group.children

            for comp in sheet_metal_comps:
                groupChildren.addBoolValueInput(
                    f'{comp.name}_chk',
                    comp.name,
                    True,
                    '',
                    True  # default selected
                )

            # Folder selection input
            folder_input = inputs.addStringValueInput('folder_path', 'Output Folder', r'C:\FusionExports')
            inputs.addBoolValueInput('browse_btn', 'Browse...', False, '', False)

            # Connect to input changed event
            on_input_changed = CommandInputChangedHandler(sheet_metal_comps)
            cmd.inputChanged.add(on_input_changed)
            handlers.append(on_input_changed)

            # Connect to execute event
            on_execute = CommandExecuteHandler(sheet_metal_comps)
            cmd.execute.add(on_execute)
            handlers.append(on_execute)

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self, comps):
        super().__init__()
        self.comps = comps

    def notify(self, args):
        try:
            changed_input = args.input
            inputs = args.inputs

            if changed_input.id == 'browse_btn':
                folderDlg = ui.createFolderDialog()
                folderDlg.title = 'Select Output Folder'
                folderDlg.initialDirectory = r'C:\FusionExports'
                if folderDlg.showDialog() == adsk.core.DialogResults.DialogOK:
                    folder_input = inputs.itemById('folder_path')
                    folder_input.value = folderDlg.folder

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, comps):
        super().__init__()
        self.comps = comps

    def notify(self, args):
        try:
            inputs = args.command.commandInputs
            design = adsk.fusion.Design.cast(app.activeProduct)
            export_mgr = design.exportManager

            output_folder = inputs.itemById('folder_path').value.strip()
            if not os.path.exists(output_folder):
                os.makedirs(output_folder, exist_ok=True)

            # Determine selected components
            selected = []
            for comp in self.comps:
                chk = inputs.itemById(f'{comp.name}_chk')
                if chk and chk.value:
                    selected.append(comp)

            if not selected:
                ui.messageBox('No components selected for export.')
                return

            export_count = 0
            for sm_comp in selected:
                try:
                    if sm_comp.flatPattern is None:
                        sheet_bodies = [b for b in sm_comp.bRepBodies if b.isSheetMetal]
                        if not sheet_bodies:
                            continue
                        body = sheet_bodies[0]
                        flat_faces = [f for f in body.faces if f.geometry.classType() == adsk.core.Plane.classType()]
                        if not flat_faces:
                            continue
                        target_face = max(flat_faces, key=lambda f: f.area)
                        sm_comp.createFlatPattern(target_face)

                    flat_pattern = sm_comp.flatPattern
                    if flat_pattern is None:
                        continue

                    base_name = sm_comp.name.replace('/', '_').replace('\\', '_')
                    filename = os.path.join(output_folder, base_name + '.dxf')
                    count = 1
                    while os.path.exists(filename):
                        filename = os.path.join(output_folder, base_name + f'_{count}.dxf')
                        count += 1

                    dxf_options = export_mgr.createDXFFlatPatternExportOptions(filename, flat_pattern)
                    dxf_options.isCenterLinesExported = False
                    dxf_options.isExtentLinesExported = False
                    dxf_options.isSplineConvertedToPolyline = True

                    export_mgr.execute(dxf_options)
                    export_count += 1
                except:
                    pass

            ui.messageBox(f'Export completed: {export_count} DXFs saved in\n{output_folder}')

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


handlers = []


def run(context):
    try:
        cmd_def = ui.commandDefinitions.itemById('ExportSheetMetalDXF')
        if not cmd_def:
            cmd_def = ui.commandDefinitions.addButtonDefinition(
                'ExportSheetMetalDXF',
                'Export Sheet Metal DXFs',
                'Export selected sheet metal components to DXF.'
            )

        on_command_created = CommandCreatedHandler()
        cmd_def.commandCreated.add(on_command_created)
        handlers.append(on_command_created)

        cmd_def.execute()

        adsk.autoTerminate(False)
    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    global handlers
    handlers = []
