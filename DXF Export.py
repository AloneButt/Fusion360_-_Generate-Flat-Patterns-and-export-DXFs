#Author-
#Description-

import adsk.core, adsk.fusion, traceback
import os

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        
        # Ensure the active product is a design
        if product.productType != 'DesignProductType':
            ui.messageBox('This script must be run in a design workspace.')
            return
        
        design = adsk.fusion.Design.cast(product)
        
        # Prompt for output folder using folder dialog
        folderDlg = ui.createFolderDialog()
        folderDlg.title = 'Select Output Folder'
        folderDlg.initialDirectory = r'C:\FusionExports'
        if folderDlg.showDialog() != adsk.core.DialogResults.DialogOK:
            return
        output_folder = folderDlg.folder
        
        # Create the output folder if it doesn't exist (though selected, but in case)
        os.makedirs(output_folder, exist_ok=True)
        
        # Get all unique components in the design
        all_comps = design.allComponents
        
        # Collect sheet metal components
        sheet_metal_comps = []
        for comp in all_comps:
            if any(b.isSheetMetal for b in comp.bRepBodies):
                sheet_metal_comps.append(comp)
        
        # Counter for exported DXFs
        export_count = 0
        
        # Export manager
        export_mgr = design.exportManager
        
        # Process each sheet metal component
        for sm_comp in sheet_metal_comps:
            try:
                # Check if flat pattern exists, create if not
                if sm_comp.flatPattern is None:
                    # Find sheet metal body (assume first)
                    sheet_bodies = [b for b in sm_comp.bRepBodies if b.isSheetMetal]
                    if not sheet_bodies:
                        continue
                    body = sheet_bodies[0]
                    
                    # Get flat faces
                    flat_faces = [f for f in body.faces if f.geometry.classType() == adsk.core.Plane.classType()]
                    if not flat_faces:
                        continue
                    
                    # Select largest flat face
                    target_face = max(flat_faces, key=lambda f: f.area)
                    
                    # Create flat pattern
                    sm_comp.createFlatPattern(target_face)
                
                flat_pattern = sm_comp.flatPattern
                if flat_pattern is None:
                    continue  # Skip if still no flat pattern
                
                # Generate unique filename based on component name
                base_name = sm_comp.name.replace('/', '_').replace('\\', '_')  # Sanitize name
                filename = os.path.join(output_folder, base_name + '.dxf')
                count = 1
                while os.path.exists(filename):
                    filename = os.path.join(output_folder, base_name + f'_{count}.dxf')
                    count += 1
                
                # Create DXF export options for flat pattern
                dxf_options = export_mgr.createDXFFlatPatternExportOptions(filename, flat_pattern)
                
                # Execute export
                export_mgr.execute(dxf_options)
                export_count += 1
                
            except:
                # Handle exceptions gracefully, continue to next
                pass
        
        # Display completion message
        ui.messageBox(f'Export completed: {export_count} DXFs saved')
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    pass