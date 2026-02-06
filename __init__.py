import os
class ExposeOutputFile:
    """
    Takes a path string (like '3D/Hy3D_00001.glb' or '/opt/ComfyUI/output/3D/Hy3D_00001.glb')
    and exposes it as a ComfyUI UI output so comfyui-api can return/upload it.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "", "multiline": False})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "expose"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def expose(self, path: str):
        p = (path or "").replace("\\", "/").strip()

        # Make it robust to different path styles
        # Strip anything up to and including output/ or outputs/
        for marker in ["/output/", "output/", "/outputs/", "outputs/"]:
            if marker in p:
                p = p.split(marker, 1)[1]

        p = p.lstrip("/")  # now should be relative like "3D/Hy3D_00001.glb"
        filename = os.path.basename(p)
        subfolder = os.path.dirname(p)

        results = [{
            "filename": filename,
            "subfolder": subfolder,
            "type": "output"
        }]

        return {"ui": {"images": results}}

NODE_CLASS_MAPPINGS = {
    "ExposeOutputFile": ExposeOutputFile
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExposeOutputFile": "Expose Output File (for API)"
}