# ComfyUI-ExposeOutputFile

A minimal ComfyUI custom node that exposes saved files as UI outputs, allowing comfyui-api to capture and upload them.

## Purpose

ComfyUI's API wrapper only uploads outputs that are returned via the standard `{"ui": {"images": [...]}}` format. Some nodes (like `Hy3DExportMesh`) save files directly to disk without producing this output format.

This node bridges that gap by taking a file path and exposing it as a proper ComfyUI output.

## Usage

1. Connect the file path output (e.g., `glb_path` from `Hy3DExportMesh`) to this node's `path` input
2. The file will now appear in the API response's `images` and `filenames` arrays
3. If S3 upload is configured, the file will be uploaded to your bucket

## Installation

### Via ComfyUI Manager
Search for "ExposeOutputFile" in ComfyUI Manager

### Manual Installation
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MedAmineTebessi/ComfyUI-ExposeOutputFile
```

### Via Salad Manifest
Add to your `MANIFEST_JSON`:
```json
{
  "custom_nodes": [
    "https://github.com/MedAmineTebessi/ComfyUI-ExposeOutputFile"
  ]
}
```

## Workflow Example

```
[Hy3DExportMesh] --glb_path--> [ExposeOutputFile]
```

The `ExposeOutputFile` node acts as an OUTPUT_NODE, making the GLB file visible to the API.
